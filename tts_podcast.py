"""
tts_podcast.py — 文字轉語音 + Podcast RSS Feed

流程：
  1. 讀取整合報告文字（docs/latest_synthesis.txt）
  2. 呼叫 OpenAI TTS API 生成 MP3
  3. 產生 RSS Feed XML 供 Overcast / Apple Podcasts 訂閱
  4. 將 MP3 與 RSS 上傳至 GitHub Pages (docs/audio/)
"""

import os
import re
import json
import datetime
import subprocess
import tempfile
from pathlib import Path
from openai import OpenAI
from feedgen.feed import FeedGenerator

# ── 環境變數 ─────────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# ── 路徑常數 ─────────────────────────────────────────────────────────────────
DOCS_DIR       = Path("docs")
AUDIO_DIR      = DOCS_DIR / "audio"
RSS_PATH       = DOCS_DIR / "podcast.xml"
SYNTHESIS_PATH = DOCS_DIR / "latest_synthesis.txt"
EPISODES_META  = AUDIO_DIR / "episodes.json"

# ── Podcast 設定 ─────────────────────────────────────────────────────────────
BASE_URL       = "https://research.investmquest.com"
PODCAST_TITLE  = "InvestMQuest 財報分析播客"
PODCAST_AUTHOR = "InvestMQuest Research"
PODCAST_DESC   = "每日財報自動化分析，涵蓋 10-Q / 10-K 深度解讀與產業趨勢整合報告。"
PODCAST_LANG   = "zh-tw"
PODCAST_EMAIL  = "research@investmquest.com"

# OpenAI TTS：每次最多 4096 字元
TTS_CHUNK_SIZE = 4000
TTS_MODEL      = "tts-1"        # 或 "tts-1-hd" 提升音質（費用 2x）
TTS_VOICE      = "nova"         # alloy / echo / fable / onyx / nova / shimmer


# ── 客戶端 ───────────────────────────────────────────────────────────────────
openai_client = OpenAI(api_key=OPENAI_API_KEY)


# ── TTS 工具函式 ─────────────────────────────────────────────────────────────

def _preprocess_text(text: str) -> str:
    """
    清理 Markdown 符號，讓 TTS 唸起來更自然。
    移除 # ## ### **粗體** *斜體* ── 分隔線 等標記。
    """
    text = re.sub(r"#{1,6}\s*", "", text)           # 標題符號
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)  # 粗斜體
    text = re.sub(r"_{1,2}([^_]+)_{1,2}", r"\1", text)    # 底線
    text = re.sub(r"[-─━]{3,}", "。", text)          # 分隔線 → 句號
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)  # Markdown 連結
    text = re.sub(r"`{1,3}[^`]*`{1,3}", "", text)   # 程式碼區塊
    text = re.sub(r"\n{3,}", "\n\n", text)           # 多餘空行
    return text.strip()


def _split_text_chunks(text: str, chunk_size: int = TTS_CHUNK_SIZE) -> list[str]:
    """
    依句號 / 換行切分文字，確保每塊不超過 chunk_size 字元。
    """
    # 以「。！？\n」為潛在切割點
    sentences = re.split(r"([。！？\n])", text)
    chunks    = []
    current   = ""

    i = 0
    while i < len(sentences):
        part = sentences[i]
        sep  = sentences[i + 1] if i + 1 < len(sentences) else ""
        segment = part + sep

        if len(current) + len(segment) <= chunk_size:
            current += segment
        else:
            if current:
                chunks.append(current.strip())
            current = segment

        i += 2

    if current.strip():
        chunks.append(current.strip())

    return chunks


def text_to_mp3(text: str, output_path: Path) -> Path:
    """
    呼叫 OpenAI TTS API 將文字轉成 MP3 檔案。
    若文字超過 4000 字元，自動分段後合併。
    回傳最終 MP3 路徑。
    """
    clean_text = _preprocess_text(text)
    chunks     = _split_text_chunks(clean_text)

    print(f"  TTS：共 {len(chunks)} 段，總字元數 {len(clean_text)}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if len(chunks) == 1:
        # 單段直接寫入
        response = openai_client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=chunks[0],
        )
        response.stream_to_file(str(output_path))
        print(f"  TTS 完成：{output_path}")
        return output_path

    # 多段：先寫臨時檔，再用 ffmpeg 合併
    tmp_files = []
    for idx, chunk in enumerate(chunks):
        print(f"  TTS 段落 {idx+1}/{len(chunks)}...", end=" ", flush=True)
        response = openai_client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=chunk,
        )
        tmp = tempfile.NamedTemporaryFile(
            suffix=".mp3", delete=False, dir=AUDIO_DIR
        )
        response.stream_to_file(tmp.name)
        tmp_files.append(tmp.name)
        print("✓")

    # 嘗試用 ffmpeg 合併
    try:
        concat_list = output_path.parent / "concat_list.txt"
        with open(concat_list, "w") as f:
            for tmp in tmp_files:
                f.write(f"file '{Path(tmp).name}'\n")

        subprocess.run(
            [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_list),
                "-c", "copy",
                str(output_path),
            ],
            cwd=str(AUDIO_DIR),
            check=True,
            capture_output=True,
        )
        concat_list.unlink(missing_ok=True)
        print(f"  合併完成：{output_path}")

    except (subprocess.CalledProcessError, FileNotFoundError):
        # ffmpeg 不可用：直接串接二進位（非最佳但可用）
        print("  ffmpeg 不可用，直接串接 MP3 二進位...")
        with open(output_path, "wb") as out:
            for tmp in tmp_files:
                with open(tmp, "rb") as inp:
                    out.write(inp.read())

    finally:
        for tmp in tmp_files:
            try:
                Path(tmp).unlink()
            except OSError:
                pass

    return output_path


# ── RSS Feed ─────────────────────────────────────────────────────────────────

def _load_episodes_meta() -> list[dict]:
    """載入既有 episodes 元數據（JSON）。"""
    if EPISODES_META.exists():
        with open(EPISODES_META, encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_episodes_meta(episodes: list[dict]) -> None:
    EPISODES_META.parent.mkdir(parents=True, exist_ok=True)
    with open(EPISODES_META, "w", encoding="utf-8") as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)


def generate_rss_feed(episodes: list[dict]) -> None:
    """
    從 episodes 列表產生 RSS Feed XML。
    每個 episode 格式：
      {
        "title":       str,
        "description": str,
        "filename":    str,   # docs/audio/ 下的檔名
        "pub_date":    str,   # ISO 8601
        "file_size":  int,   # bytes
        "duration":    str,   # "HH:MM:SS"
      }
    """
    fg = FeedGenerator()
    fg.load_extension("podcast")

    fg.id(f"{BASE_URL}/podcast.xml")
    fg.title(PODCAST_TITLE)
    fg.author({"name": PODCAST_AUTHOR, "email": PODCAST_EMAIL})
    fg.link(href=f"{BASE_URL}/podcast.xml", rel="self")
    fg.link(href=BASE_URL, rel="alternate")
    fg.description(PODCAST_DESC)
    fg.language(PODCAST_LANG)
    fg.image(
        url=f"{BASE_URL}/assets/podcast_cover.png",
        title=PODCAST_TITLE,
        link=BASE_URL,
    )

    fg.podcast.itunes_category("Business", "Investing")
    fg.podcast.itunes_author(PODCAST_AUTHOR)
    fg.podcast.itunes_summary(PODCAST_DESC)
    fg.podcast.itunes_explicit("no")
    fg.podcast.itunes_image(f"{BASE_URL}/assets/podcast_cover.png")

    for ep in reversed(episodes):     # 最新在前
        fe = fg.add_entry()
        audio_url = f"{BASE_URL}/audio/{ep['filename']}"

        fe.id(audio_url)
        fe.title(ep["title"])
        fe.description(ep["description"])
        fe.published(ep["pub_date"])
        fe.enclosure(
            url=audio_url,
            length=str(ep.get("file_size", 0)),
            type="audio/mpeg",
        )
        fe.podcast.itunes_duration(ep.get("duration", "00:10:00"))
        fe.podcast.itunes_summary(ep["description"][:300])

    RSS_PATH.parent.mkdir(parents=True, exist_ok=True)
    fg.rss_str(pretty=True)
    fg.rss_file(str(RSS_PATH))
    print(f"  RSS Feed 已更新：{RSS_PATH}")


# ── GitHub Pages 上傳 ─────────────────────────────────────────────────────────

def commit_and_push(files: list[Path], commit_msg: str) -> None:
    """
    將指定檔案 git add → commit → push 至 GitHub Pages。
    假設已在 repo 根目錄，且已設定遠端。
    """
    try:
        # git add
        for f in files:
            subprocess.run(
                ["git", "add", str(f)],
                check=True, capture_output=True
            )

        # git status 確認有變更
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            check=True, capture_output=True, text=True
        )
        if not status.stdout.strip():
            print("  git：無新增變更，跳過 commit")
            return

        # git commit
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            check=True, capture_output=True
        )

        # git push
        subprocess.run(
            ["git", "push"],
            check=True, capture_output=True
        )
        print(f"  git push 完成（{len(files)} 個檔案）")

    except subprocess.CalledProcessError as exc:
        print(f"  [WARNING] git 操作失敗: {exc.stderr.decode(errors='replace')}")
    except FileNotFoundError:
        print("  [WARNING] git 指令不存在，跳過上傳")


# ── 主函式 ───────────────────────────────────────────────────────────────────

def generate_podcast_episode(
    synthesis_text: str | None = None,
    date_str: str | None = None,
) -> None:
    """
    主流程：
      1. 讀取整合報告
      2. 生成 MP3
      3. 更新 episodes 元數據
      4. 重建 RSS Feed
      5. Push 至 GitHub Pages
    """
    if date_str is None:
        date_str = datetime.date.today().isoformat()

    # 讀取文字
    if synthesis_text is None:
        if not SYNTHESIS_PATH.exists():
            print(f"[TTS] 找不到 {SYNTHESIS_PATH}，跳過 Podcast 生成")
            return
        with open(SYNTHESIS_PATH, encoding="utf-8") as f:
            synthesis_text = f.read().strip()

    if not synthesis_text:
        print("[TTS] 整合報告為空，跳過")
        return

    print(f"\n[TTS] 開始生成 Podcast 語音 ({date_str})...")

    # 輸出路徑
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    mp3_filename = f"synthesis_{date_str}.mp3"
    mp3_path     = AUDIO_DIR / mp3_filename

    # 生成 MP3
    text_to_mp3(synthesis_text, mp3_path)
    file_size = mp3_path.stat().st_size if mp3_path.exists() else 0

    # 更新 episodes 元數據
    episodes = _load_episodes_meta()
    pub_dt   = datetime.datetime.fromisoformat(date_str).replace(
        tzinfo=datetime.timezone.utc
    )

    new_episode = {
        "title":       f"財報整合報告 {date_str}",
        "description": synthesis_text[:300].replace("\n", " "),
        "filename":    mp3_filename,
        "pub_date":    pub_dt.isoformat(),
        "file_size":   file_size,
        "duration":    "00:10:00",    # 估算值；可用 ffprobe 實際測量
    }

    # 去重（同日期只保留最新一筆）
    episodes = [e for e in episodes if e.get("pub_date", "")[:10] != date_str]
    episodes.append(new_episode)
    episodes.sort(key=lambda e: e["pub_date"])

    _save_episodes_meta(episodes)

    # 重建 RSS
    generate_rss_feed(episodes)

    # Push 至 GitHub Pages
    changed_files = [mp3_path, RSS_PATH, EPISODES_META]
    commit_and_push(
        changed_files,
        f"podcast: add synthesis episode {date_str}"
    )

    print(f"[TTS] Podcast 更新完成！")
    print(f"  音頻檔案：{BASE_URL}/audio/{mp3_filename}")
    print(f"  RSS Feed ：{BASE_URL}/podcast.xml")


if __name__ == "__main__":
    generate_podcast_episode()
