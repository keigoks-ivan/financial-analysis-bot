# Source Tier 黑/白名單（v1.9 起生效）

由 `industry-analyst` skill 維護。`scripts/validate_source_blacklist.py` 自動執行。

---

## 🚫 黑名單（CI 阻斷 — 不可作為 cite）

引用以下域名 → CI fail，必須移除或替換為合格 source。

### SEO 內容農場 / 自動生成站
- `heygotrade.com`
- `aicerts.ai`
- `wonderfulpcb.com`
- `intelmarketresearch.com`
- `extrapolate.com`
- `marketgrowthreports.com`
- `kingsresearch.com`
- `verifiedmarketreports.com`
- `archivemarketresearch.com`
- `360iresearch.com`
- `globalgrowthinsights.com`
- `businessresearchinsights.com`
- `credenceresearch.com`
- `valuates.com`
- `easelinkelec.com`
- `ugpcb.com`
- `nwengineeringllc.com`
- `rocket-pcb.com`
- `pcbdirectory.com`
- `creating-nanotech.com`
- `unibetter-ic.com`
- `siliconanalysts.com`
- `tspasemiconductor.substack.com` *(未署名，與其他 SEO 站關聯)*
- `tradingkey.com`
- `fspinvest.co.za`
- `bingx.com`
- `aichief.com`
- `dataconomy.com`
- `aijourn.com`
- `ai2.work`
- `arturmarkus.com`
- `webpronews.com`

### PR 自動發布站（多家共用模板）
- `markets.financialcontent.com` *(子站包含 tokenring / predictstreet / marketminute / finterra / pilot)*
- `business.thepilotnews.com`
- `financialcontent.com`
- `prnewswire.com` *(原文 PR 可用，二次轉載站不可)*

### 維基 / 社群（不可作 fact source）
- `wikipedia.org` *(可作 historical lead，不可 cite for current data)*
- `reddit.com`
- `twitter.com` / `x.com` *(除非署名 named analyst — Dylan Patel / Ming-Chi Kuo / Dan Nystedt 等)*
- `facebook.com`
- `pttweb.cc` *(PTT Stock 板)*

---

## ✅ 白名單

### Tier 1（Primary · 最高優先）
- 公司 IR：`investor.*` / `*.com/ir/` / `nvidianews.nvidia.com` / `investors.broadcom.com` / `ir.amd.com` / `ats.net/en/press/` / `ibiden.com` / `shinko.co.jp` / `apple.com/newsroom/` / etc
- SEC EDGAR：`sec.gov`
- 公開資訊觀測站：`mops.twse.com.tw`
- HKEX：`hkex.com.hk`
- 公司技術 keynote：`developer.nvidia.com/blog/` / `cloud.google.com/blog/` / `engineering.fb.com` / `microsoft.com/en-us/research/`
- 法說會逐字稿：`fool.com/earnings/call-transcripts/` / `seekingalpha.com/article/.../transcript`
- 公司技術白皮書：`*.com/technology/` / `*.com/whitepaper/`
- 公開的 R&D / 產品文件
- Anthropic / OpenAI 官方公告：`anthropic.com/news` / `openai.com/blog` / `openai.com/index`

### Tier 2（Authoritative Third-party）
- 產業協會：`semi.org` / `sia-online.org` / `jedec.org` / `oif-forum.com` / `opencompute.org`
- 研究機構：`yolegroup.com` / `ic-insights.com` / `idc.com` / `gartner.com` / `mordorintelligence.com` *(品質中等可用)*
- 學術：`ieee.org` / `ieeexplore.ieee.org` / `nature.com` / `acm.org`
- 政府：`commerce.gov` / `chips.gov` / `nist.gov` / `bea.gov` / `bls.gov` / `eu.europa.eu`
- 工研院 / 資策會：`itri.org.tw` / `iek.iii.org.tw`
- TrendForce：`trendforce.com` *(半導體預測需與英文 T1 交叉驗證)*

### Tier 3-A（券商產業 primer / sector report）
- `morganstanley.com` / `goldmansachs.com` / `jpmorgan.com`
- `barclays.com` / `jefferies.com` / `tdcowen.com` / `daiwa-cm.com`
- `ubs.com` / `bofa.com` / `ml.com` / `citigroup.com`
- 引用必須含 `p.XX` 或 slide 編號

### Tier 3-B（主流財經媒體）
- `bloomberg.com` / `reuters.com` / `wsj.com` / `ft.com`
- `nikkei.com` / `cnbc.com` / `forbes.com` / `fortune.com` / `barrons.com`
- 中文：`ctee.com.tw` (工商) / `udn.com` (聯合) / `wantgoo.com` / `cnyes.com` (鉅亨網) / `commercialtimes.com.tw`

### Tier 3-C（Named-analyst / 專業媒體）
- `semianalysis.com` *(Dylan Patel — 升 T3-A 等級)*
- `stratechery.com` *(Ben Thompson — 升 T3-A 等級)*
- `anandtech.com` *(已停刊但歷史內容可引)*
- `tomshardware.com`
- `theinformation.com`
- `digitimes.com` *(電子時報 — 半導體領域 T3-A 級，但單來源需交叉驗證)*
- `eetimes.com`
- `semiwiki.com`
- `theregister.com`
- `nextplatform.com`
- `datacenterdynamics.com` *(DCD)*
- `globaltechresearch.substack.com` *(若署名分析師則 T3-A)*

### 中文 T3-zh
- 大叔美股筆記 *(Substack — 升 T3-A 等級若署名)*
- 半導體行業觀察 *(微信公眾號)*
- 鉅亨網 / 經濟日報 / 工商時報 / 財訊 / 商周 / 天下

### 灰色（warning，需作者標註理由）
- `medium.com/@*` — 因人而異，看作者
- `*.substack.com` — 同上
- `ad-hoc-news.de` — 翻譯轉載多
- `iconnect007.com` — PCB 業界但無查證流程
- `evertiq.com` — 同上
- `marketscreener.com` — 二手轉載
- `pitchbook.com` — 私募數據可信但需 paywall
- 其他不在白/黑名單的域名

---

## 引用規範

每個 claim 後必須附 source-tag，格式：

```html
<span class="source-tag">[T1: <a href="https://nvidianews.nvidia.com/.../keynote">NVIDIA GTC 2026 Keynote slide 47</a>]</span>
```

**Tier 標籤強制要求**：
- 不可只寫 `[source]` 或 `[ref]`
- 不可省略 Tier 標籤
- T3 必須細分為 T3-A / T3-B / T3-C
- 遇黑名單域名 → CI fail
- 遇灰色域名 → CI warning + 必須加註理由（例如 `[T3-grey: ad-hoc-news 為德文翻譯轉載 — 對 EU defense 議題仍有價值]`）

---

## 維護

- 發現新內容農場 / SEO 站 → append 到黑名單
- 發現新權威來源 → append 對應 Tier
- 名單變更須 commit 訊息註明 (e.g. `update source tier lists: blacklist heygotrade`)
