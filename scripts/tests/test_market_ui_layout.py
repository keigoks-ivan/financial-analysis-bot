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
    assert "審查狀態未知" in html
    assert '"快照 " + snapshot' in html
    assert 'id="questionBoardTrace"' in html
    assert "支持條件" in html
    assert "未確認時" in html
    assert "獨立性註記" in html
    assert "board.sources" in html
    assert 'safeSourceUrl(source.url, "")' in html
    assert "查看問題板資料來源" in html
    assert '<a href="#sec-evidence">頁內證據層</a>' in html


# 2026-09-14：追溯資訊保留在原生展開區，主時間框架表維持閱讀焦點。
def test_market_page_collapses_technical_trace_details():
    html = PAGE.read_text(encoding="utf-8")
    assert '<details class="compact-details" id="horizonClaims" hidden>' in html
    assert "查看帳簿命題" in html
    assert "claimDetails.hidden = !claimRows.length" in html
    assert "<th>帳簿命題</th>" not in html
    assert 'id="judgmentNumbers"' not in html
    assert "查看與帳簿表格的分歧" in html
    assert "研究參考 · 方法與限制" in html
    assert '<h2 style="margin-bottom:.3rem">三個時間框架<span class="en">' not in html


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


# 2026-09-14：窄卡片的鍵值欄允許長中文標籤換行，數值與日期仍保有獨立欄寬。
def test_metric_cards_keep_values_readable_without_overflow():
    html = PAGE.read_text(encoding="utf-8")
    assert ".metric-kv{grid-template-columns:minmax(0,1fr) minmax(5.5rem,auto)" in html
    assert ".metric-kv b{min-width:0;white-space:normal" in html
    assert ".metric-kv>span{min-width:0;text-align:right;overflow-wrap:anywhere}" in html
    assert ".transmission-kv>span{white-space:nowrap}" in html
    assert ".transmission-kv .quote-meta{white-space:normal}" in html
    assert html.count('class="kv metric-kv') == 3


# 2026-09-14：320px 視窗下類比與情境卡不得以固定最小寬度撐出頁面。
def test_narrative_card_grids_shrink_to_the_content_width():
    html = PAGE.read_text(encoding="utf-8")
    responsive_columns = "grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr))"
    assert html.count(responsive_columns) == 2


# 2026-09-14：頁內導覽需替固定導覽列保留空間，跳轉後仍看得到段落標題。
def test_in_page_navigation_keeps_section_headings_visible():
    html = PAGE.read_text(encoding="utf-8")
    assert "#page-body>section,#sec-evidence{scroll-margin-top:110px}" in html
