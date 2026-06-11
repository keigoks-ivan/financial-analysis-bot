# 利潤池 Value Chain inline SVG 樣板 v2.0

v1.x 的 value chain box 只標毛利率，v2.0 改為**利潤池語境**：水平 3-box（上游 / 中游 / 下游）+ 箭頭保留，但 box 內標示改為「**利潤池占比 %（T-2 → 現在）+ 遷移方向箭頭**」，不只毛利率。

落點：§3（供給側 + 利潤池），搭配利潤池遷移表（模組 §3-1）一起呈現 — 表給數字、SVG 給一眼可見的遷移方向。

## 規則

- **box 內標示**（由上而下）：環節名稱 → 利潤池占比 `T-2 → 現在`（% point 遷移）→ 代表廠商。
- **遷移方向**：box 右上角加 ↑（吃進更多池子）/ ↓（被擠出）/ → （持平）視覺 marker；用顏色強化（↑ 綠 #16A34A、↓ 紅 #DC2626、→ 灰 #6B7280）。
- **利潤池 % 必 source**（QC-18）：無 source → 改定性「主導 / 均勢 / 次要」取代數字。
- box 間箭頭代表 value 流向（上游 → 中游 → 下游）。

## 樣板

```html
<svg class="vc-svg" viewBox="0 0 900 240" xmlns="http://www.w3.org/2000/svg">
  <!-- 上游 -->
  <rect x="20"  y="40" width="240" height="160" rx="8" fill="#EDE9FE" stroke="#7C3AED" stroke-width="2"/>
  <text x="140" y="70"  text-anchor="middle" font-size="14" font-weight="700" fill="#4C1D95">上游</text>
  <text x="140" y="92"  text-anchor="middle" font-size="11.5" fill="#5B21B6">{子類別}</text>
  <text x="140" y="120" text-anchor="middle" font-size="13" font-weight="600" fill="#1E1B4B">利潤池 {AA}% → {BB}%</text>
  <text x="245" y="62"  text-anchor="end" font-size="16" font-weight="700" fill="#16A34A">↑</text>  <!-- 遷移方向：↑綠 / ↓紅#DC2626 / →灰#6B7280 -->
  <text x="140" y="160" text-anchor="middle" font-size="11" fill="#1E1B4B">代表 {公司}</text>
  <text x="140" y="182" text-anchor="middle" font-size="10" fill="#6B7280">{遷移一句：吃進 / 被擠出 / 持平}</text>

  <!-- 中游 -->
  <rect x="330" y="40" width="240" height="160" rx="8" fill="#DDD6FE" stroke="#7C3AED" stroke-width="2"/>
  <text x="450" y="70"  text-anchor="middle" font-size="14" font-weight="700" fill="#4C1D95">中游</text>
  <text x="450" y="92"  text-anchor="middle" font-size="11.5" fill="#5B21B6">{子類別}</text>
  <text x="450" y="120" text-anchor="middle" font-size="13" font-weight="600" fill="#1E1B4B">利潤池 {AA}% → {BB}%</text>
  <text x="555" y="62"  text-anchor="end" font-size="16" font-weight="700" fill="#6B7280">→</text>
  <text x="450" y="160" text-anchor="middle" font-size="11" fill="#1E1B4B">代表 {公司}</text>
  <text x="450" y="182" text-anchor="middle" font-size="10" fill="#6B7280">{遷移一句}</text>

  <!-- 下游 -->
  <rect x="640" y="40" width="240" height="160" rx="8" fill="#C4B5FD" stroke="#7C3AED" stroke-width="2"/>
  <text x="760" y="70"  text-anchor="middle" font-size="14" font-weight="700" fill="#4C1D95">下游</text>
  <text x="760" y="92"  text-anchor="middle" font-size="11.5" fill="#5B21B6">{子類別}</text>
  <text x="760" y="120" text-anchor="middle" font-size="13" font-weight="600" fill="#1E1B4B">利潤池 {AA}% → {BB}%</text>
  <text x="865" y="62"  text-anchor="end" font-size="16" font-weight="700" fill="#DC2626">↓</text>
  <text x="760" y="160" text-anchor="middle" font-size="11" fill="#1E1B4B">代表 {公司}</text>
  <text x="760" y="182" text-anchor="middle" font-size="10" fill="#6B7280">{遷移一句}</text>

  <!-- value 流向箭頭 -->
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7C3AED"/>
    </marker>
  </defs>
  <line x1="260" y1="120" x2="330" y2="120" stroke="#7C3AED" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="570" y1="120" x2="640" y2="120" stroke="#7C3AED" stroke-width="2" marker-end="url(#arrow)"/>
</svg>
```

## 退化規則（無 % source 時）

利潤池占比無可靠 source → 把 `利潤池 {AA}% → {BB}%` 改為定性 `利潤池：主導 / 均勢 / 次要`，遷移方向 marker 保留（方向比精準 % 重要）。例：

```html
<text x="140" y="120" text-anchor="middle" font-size="13" font-weight="600" fill="#1E1B4B">利潤池：主導</text>
```

## 與利潤池表的分工

| 元素 | 負責 |
|:---|:---|
| 利潤池遷移表（模組 §3-1） | 給精確 % + T-2/現在/遷移方向/搶被搶（可審計、進 Gate） |
| 本 SVG | 給一眼可見的「誰吃進、誰被擠出」視覺，輔助敘事，**非強制阻斷**（QC-4 註：v1.x value chain SVG 在 v2.0 改利潤池語境，建議保留但非強制） |
