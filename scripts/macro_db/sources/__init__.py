"""fetcher REGISTRY：名稱 -> 模組路徑（延遲載入）。

美國 fetcher 由 builder A 維護；台灣 fetcher（tw_ 開頭）由 builder B 在下方 TW 區塊加行。
每個模組需有 fetch(specs: list[dict]) -> dict。
"""
import importlib

REGISTRY = {
    # --- US ---
    "fred": "macro_db.sources.fred",
    "umich": "macro_db.sources.umich",
    "zillow": "macro_db.sources.zillow",
    "cleveland": "macro_db.sources.cleveland",
    "nyfed": "macro_db.sources.nyfed",
    "nyfed_markets": "macro_db.sources.nyfed_markets",
    "fedboard": "macro_db.sources.fedboard",
    "census_trade": "macro_db.sources.census_trade",
    "fiscaldata": "macro_db.sources.fiscaldata",
    # --- TW（B 只在此區塊加 tw_ 開頭的行）---
    "tw_dgbas": "macro_db.sources.tw_dgbas",
    "tw_cbc": "macro_db.sources.tw_cbc",
    "tw_ndc": "macro_db.sources.tw_ndc",
    "tw_mof": "macro_db.sources.tw_mof",
    "tw_moea": "macro_db.sources.tw_moea",
    "tw_energy": "macro_db.sources.tw_energy",
    "tw_moi": "macro_db.sources.tw_moi",
    "tw_jcic": "macro_db.sources.tw_jcic",
    "tw_twse": "macro_db.sources.tw_twse",
    "tw_tpex": "macro_db.sources.tw_tpex",
    # --- JP（第二波：只在此區塊加 jp_ 開頭的行）---
    "jp_boj": "macro_db.sources.jp_boj",
    "jp_esri": "macro_db.sources.jp_esri",
    "jp_stat": "macro_db.sources.jp_stat",
    "jp_estat_file": "macro_db.sources.jp_estat_file",
    "jp_mof": "macro_db.sources.jp_mof",
    "jp_customs": "macro_db.sources.jp_customs",
    "jp_misc": "macro_db.sources.jp_misc",
    # --- CN（第二波：只在此區塊加 cn_ 開頭的行）---
    "cn_nbs": "macro_db.sources.cn_nbs",
    "cn_pbc": "macro_db.sources.cn_pbc",
    "cn_chinamoney": "macro_db.sources.cn_chinamoney",
    "cn_chinabond": "macro_db.sources.cn_chinabond",
    "cn_csindex": "macro_db.sources.cn_csindex",
    # --- EU（第二波：只在此區塊加 eu_ 開頭的行）---
    "eu_eurostat": "macro_db.sources.eu_eurostat",
    "eu_ecb": "macro_db.sources.eu_ecb",
    "eu_smard": "macro_db.sources.eu_smard",
    # --- AN（第二波：只在此區塊加 an_ 開頭的行）---
    "an_singstat": "macro_db.sources.an_singstat",
    "an_opendosm": "macro_db.sources.an_opendosm",
    # --- AN-VN（越南 builder 只在這行與下一行之間加 an_vn_ 開頭的行）---
    # --- AN-VN 結束 ---
    # --- AN-MY（馬來西亞 builder 只在這行與下一行之間加 an_my_ 開頭的行）---
    # --- AN-MY 結束 ---
    # --- AN-TH（泰國 builder 只在這行與下一行之間加 an_th_ 開頭的行）---
    "an_th_bot": "macro_db.sources.an_th_bot",
    "an_th_tpso": "macro_db.sources.an_th_tpso",
    "an_th_oie": "macro_db.sources.an_th_oie",
    # --- AN-TH 結束 ---
    # --- AN-ID（印尼 builder 只在這行與下一行之間加 an_id_ 開頭的行）---
    # --- AN-ID 結束 ---
    # --- AN-SG（新加坡 builder 只在這行與下一行之間加 an_sg_ 開頭的行）---
    # --- AN-SG 結束 ---
    # --- 跨國共用（IMF／BIS／OECD 等國際機構 API，第二波）---
    "intl_imf": "macro_db.sources.intl_imf",
    "intl_bis": "macro_db.sources.intl_bis",
    "intl_worldbank": "macro_db.sources.intl_worldbank",
}


def get_fetcher(name):
    return importlib.import_module(REGISTRY[name]).fetch
