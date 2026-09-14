"""市況頁資訊層級與資料標示契約。"""

from pathlib import Path


PAGE = Path(__file__).parents[2] / "docs" / "market" / "index.html"


def test_market_page_keeps_compact_and_full_text_layers():
    html = PAGE.read_text(encoding="utf-8")
    assert "function concisePoints" in html
    assert "查看完整原文" in html
    assert "若／如果條件句維持到句末" in html
    assert "slice(0, 4)" in html
    assert "主要力量" in html


def test_market_page_labels_probability_and_quote_provenance():
    html = PAGE.read_text(encoding="utf-8")
    assert "研究判斷 · 尚無校準樣本" in html
    assert "pctile_window || \"未知\"" in html
    assert "Number(q.num) / (1 + Number(q.chg30_pct) / 100)" in html
    assert "Number(q.chg30_pct) <= -100" in html
    assert 'frequency === "monthly" ? 45' in html
    assert "未來日期" in html
    assert "最近判讀核准" in html
    assert "最近資料成功更新" in html
    assert "quoteDateMeta(q, currentAsOf)" in html


def test_market_page_reserves_global_slot_and_orders_sections():
    html = PAGE.read_text(encoding="utf-8")
    assert '<section id="sec-global">' in html
    order = [
        '"sec-judgment", "sec-questions", "sec-global", "sec-scenarios", "sec-falsifiers", "sec-history", "sec-source-history"',
        '"sec-history", "sec-source-history", "sec-analogs", "sec-judgment-score"',
    ]
    assert all(fragment in html for fragment in order)


def test_market_page_renders_question_board_with_point_in_time_evidence():
    html = PAGE.read_text(encoding="utf-8")
    assert '<section id="sec-questions" hidden>' in html
    assert 'function renderQuestionBoard(board, state)' in html
    assert 'board.schema === "market-question-board-v1"' in html
    assert "bundle.question_board" in html
    assert "board.evidence_snapshot && board.evidence_snapshot.quotes" in html
    assert "判讀當時：" in html
    assert "quoteHasChanged(thenQuote, currentQuote)" in html
    assert "目前：" in html
    assert "目前來源缺失" in html
    assert "thenQuote && thenQuote.label" in html
    assert 'String(thenQuote.unit || "")' in html
    assert "查看支持、反對與未知" in html
    assert "期限：" in html
    assert "需要重審" in html
    assert "本期待驗證問題" in html
    assert "本區更新不代表既有機率判讀已重新核准" in html
    assert "審查狀態未知" in html
    assert "snapshot.slice(0, 8)" in html
    assert "支持條件" in html
    assert "未確認時" in html
    assert "獨立性註記" in html
    assert "board.sources" in html
    assert 'safeSourceUrl(source.url, "")' in html
    assert "查看問題板資料來源" in html
    assert '<a href="#sec-evidence">頁內證據層</a>' in html


def test_market_page_renders_history_context_without_empty_region_cards():
    html = PAGE.read_text(encoding="utf-8")
    assert 'context.schema !== "market-history-context-v1"' in html
    assert "region.observations && region.observations.length" in html
    assert "item.coverage && item.coverage.long_history" in html
    assert "historyWindowSelect" in html
    assert "change.actual_start" in html
    assert "context.replay && context.replay.note" in html
    assert "bundle.history_context" in html
    assert 'mom: "月對月", qoq: "季對季", yoy: "年對年"' in html
    assert 'item.changes[w.id].status === "ok"' in html


def test_fuses_distinguish_absolute_and_relative_distance():
    html = PAGE.read_text(encoding="utf-8")
    assert "r.distance_abs != null" in html
    assert "%（相對距離）" in html
    assert 'r.as_of || "日期未知"' in html


def test_long_copy_and_live_tables_are_collapsed_with_precise_metadata():
    html = PAGE.read_text(encoding="utf-8")
    assert '<script src="text-summaries.js"></script>' in html
    assert "window.MARKET_TEXT_SUMMARIES[original]" in html
    assert 'h.resolve_by || h.end_date' in html
    assert "目前數據與日期" in html
    assert "近 30 筆觀測" in html
    assert "近期變化" in html
