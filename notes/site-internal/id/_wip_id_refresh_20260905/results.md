# ID v4 裁決級 refresh 結果表

| 主題 | commit | 可見字／KB／表 | T1 | critic 首輪→re-gate | 燈號 前版→本版 | token 拆分 |
|---|---|---|---|---|---|---|
| AdvancedPackaging | c2e8ea047 | 13,395／75.6KB／11 表 | 62.5%（floor 60，未覆蓋） | 🔴0 🟡0 🟢3 → 無 re-gate | shortage·II·mid·（無）·×2.3 → shortage·II·mid·high·×1.9 | 合計 43.1M／279 輪：writer 11.6M(55) ＋採集 2.6M(23) ＋完整性 0.5M(6) ＋critic 2.6M(25) ＋patch 18.2M(110) ＋發布 7.7M(60) |
| AIAcceleratorDemand | 34ddc9b90 | 13,758／73.3KB／11 表 | 63.2%（floor 60，未覆蓋） | 🔴0 🟡2 🟢1 → 無 re-gate | shortage·II·mid·（無）·×3.1 → shortage·II·mid·mid·×2.8 | 合計 29.5M／224 輪：writer 6.0M(32) ＋採集 10.2M(65) ＋完整性 0.6M(7) ＋critic 4.4M(37) ＋patch 3.4M(35) ＋發布 5.0M(48) |
| AINetworking | **failed（未產檔）** | — | 已採集部分約 75–80% T1，但覆蓋率不足 | 未進 critic | 前版 shortage·II·mid·（空）·×3.4 → 未定 | 合計約 8.0M：writer P1 3.3M ＋採集一輪 1.9M ＋採集二輪 1.2M ＋採集三輪 1.3M（無 critic／patch／發布） |
| AIDataCenter | 1d96e51ac | 13,655／74.6KB／11 表 | 82.4%（floor 60，未覆蓋） | 🔴0 🟡4 → 無 re-gate | shortage·II·high·（無）·×3.1 → shortage·II·mid·mid·×2.2 | 合計 42.4M／321 輪：writer 5.6M(32) ＋採集 13.2M(97) ＋完整性 0.5M(6) ＋critic 5.5M(49) ＋patch 9.4M(72) ＋發布 8.1M(65) |
| MemorySupercycle | 23c08d9a5 | 13,989／78.7KB／12 表 | 56.7%（floor 45 覆蓋，結構性理由：逐季合約價無 T1 對應物） | 🔴2 🟡2 🟢3 → re-gate 🔴0 🟡0 🟢3 | shortage·II·mid·（無）·×2.3 → split·II 末段·mid·high·×1.1（金額口徑；位元 ×2.6） | 合計 44.1M／341 輪：writer 8.0M(37，opus) ＋採集 5.2M(47) ＋補件採集 4.2M(36) ＋完整性 0.8M(9) ＋critic 6.6M(49) ＋re-gate 0.9M(10) ＋patch 10.2M(87) ＋發布 8.3M(66)。※ WebSearch 額度 200/200 全罄，採集與覆核全走 WebFetch 直取已知 URL（TrendForce presscenter 逐頁／SEC EDGAR／IR PDF＋pdftotext／Federal Register JSON API） |
| CUDARocmMoat | 463b7a016 | 13,701／77.8KB／11 表 | 81.8%（floor 60，未覆蓋） | 🔴0 🟡1 🟢1 → 無 re-gate | balanced·II·high·（無）·×1.0 → split·II·mid·high·×6.0 | 合計 42.9M／303 輪：writer 7.5M(41，Phase1+2；大 Write 未落帳，實際輸出約 27.5K vs 面值 19.1K) ＋採集 14.2M(94) ＋完整性 0.7M(8) ＋critic 3.7M(31) ＋patch 4.3M(43) ＋發布 12.6M(86) |
