# ID refresh queue（2026-09-05 持有人拍板，全部裁決級 refresh、做完各自 commit＋push）
狀態：todo / running / done(commit) / failed(原因)
1. AdvancedPackaging_20260419 — done(c2e8ea047)
2. AIAcceleratorDemand_20260419 — done(34ddc9b90)
3. CUDARocmMoat_20260501 — done(463b7a016)
4. MemorySupercycle_20260430 — done(23c08d9a5)
5. AINetworking_20260419 — failed(WebSearch 額度耗盡 200/200；三輪採集仍無市場撮合價與任何機構 AI 網路絕對 TAM，必交物 D4／D6／D9 無法達成，不硬撐、未寫檔未 commit)
6. AIDataCenter_20260419 — done(1d96e51ac)
7. AIDCPowerElectronics_20260421 — todo
8. LiquidCooling_20260419 — todo
9. LeadingEdgeNode_20260419 — todo
10. WaferFabEquipment_20260430 — todo
11. HybridBondingSoIC_20260420 — todo
12. FoundryGeography_20260427 — todo
13. AIStorage_20260427 — todo
14. AIEDAIP_20260427 — todo
15. CopperSupercycle_20260428 — todo
16. NuclearRenaissance_20260430 — todo
17. CommercialAerospace_20260427 — todo
18. HeavyMachineryMining_20260427 — todo
19. AerospaceMetals_20260427 — todo
20. DataCenterREITDuopoly_20260629 — todo
21. HyperscalerCloudBigThree_20260505 — todo
22. TokenEconomics_20260427 — todo
23. AICybersecurityDoubleEdge_20260423 — todo

## AINetworking 重跑備註（2026-09-05）
WebSearch 額度耗盡導致失敗，非流程錯誤。**可直接從 writer Phase 2 續跑**，Phase 1 與三輪採集成果全部保留：
`writer_phase1_AINetworking.md`（thesis sketch／id-meta 草稿／五格燈號猜想／kill 草稿／問題清單）、
`evidence_AINetworking.md`＋`evidence2_`＋`evidence3_`（T1 分部營收序列、hyperscaler capex、標準組織時程皆已到位）、
`dd_meta_AINetworking.md`、`returns_AINetworking.md`、`prior_brief_AINetworking.md`。
重跑前必須先確認 WebSearch 可用；仍缺：800G/1.6T ASP 逐期序列（撮合價）、機構 AI 網路絕對 TAM、EML lead time、每 GPU 網路含量、Axis E 大半。
已查實可直接用的兩項發現：APH 為 2:1 分割（8-K 2026-08-06）故站內 −57% 報酬為資料假象；NVDA 自 Q1 FY27 起停止單獨揭露 Networking 行（最後三季 $7,252M→$8,187M→$11,000M），K4 需重新設計。
