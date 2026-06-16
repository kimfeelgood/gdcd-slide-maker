# Data viz — turn sparse numbers into zzanmul charts, tables, timelines

Sparse `.pptx` slides often carry bare numbers. Don't leave them as plain text —
promote them into a chart, table, or timeline. These are self-contained (no chart
library), neumorphic, and use the deck's tokens. **Paste the CSS you need into the
deck's `<style>` (additive), then the markup into a `.tile`.** Keep original
figures verbatim.

## When to use which

- **Bar chart** — comparing a handful of magnitudes (usage, share, score).
- **Donut** — one part-of-whole percentage (a share, a pass rate).
- **Trend (SVG line)** — change over time.
- **Table** — multi-attribute comparison (A vs B vs C across rows).
- **Timeline** — events along time.
- **Code block** — technical lectures.

## Bar chart (CSS)

```css
.zchart{display:flex;flex-direction:column;gap:14px;width:100%;}
.zbar{display:grid;grid-template-columns:96px 1fr auto;align-items:center;gap:14px;}
.zbar .zbl{font-size:14px;font-weight:700;color:var(--primary);}
.zbar .ztrack{height:18px;border-radius:20px;background:var(--base);overflow:hidden;
  box-shadow:inset 3px 3px 6px var(--shadow),inset -3px -3px 6px var(--light);}
.zbar .zfill{display:block;height:100%;border-radius:20px;background:linear-gradient(90deg,var(--accent),var(--primary));}
.zbar .zfill.alt{background:var(--muted);}      /* de-emphasised series */
.zbar .zval{font-size:13px;font-weight:700;color:var(--ink);font-variant-numeric:tabular-nums;}
```
```html
<div class="zchart">
  <div class="zbar"><span class="zbl">딥시크</span><span class="ztrack"><span class="zfill" style="width:100%"></span></span><span class="zval">1조 1,400억</span></div>
  <div class="zbar"><span class="zbl">클로드</span><span class="ztrack"><span class="zfill alt" style="width:91%"></span></span><span class="zval">1조 400억</span></div>
  <div class="zbar"><span class="zbl">제미나이</span><span class="ztrack"><span class="zfill alt" style="width:82%"></span></span><span class="zval">9,390억</span></div>
</div>
```
Width % = value ÷ max × 100. Highlight the focus series with `.zfill` (blue), the
rest with `.zfill.alt` (gray) — same emphasis rule as the rest of zzanmul.

## Donut (one percentage)

```css
.zdonut{position:relative;--p:50;--size:170px;width:var(--size);height:var(--size);border-radius:50%;
  background:conic-gradient(var(--accent) calc(var(--p)*1%), var(--shadow) 0);
  display:grid;place-items:center;box-shadow:6px 6px 14px var(--shadow),-6px -6px 14px var(--light);}
.zdonut::after{content:"";position:absolute;inset:20%;border-radius:50%;background:var(--base);
  box-shadow:inset 3px 3px 7px var(--shadow),inset -3px -3px 7px var(--light);}
.zd-center{position:relative;z-index:1;text-align:center;}
.zd-center b{display:block;font-size:30px;font-weight:800;color:var(--primary);}
.zd-center span{font-size:12px;color:var(--muted);}
```
```html
<div class="zdonut" style="--p:79"><div class="zd-center"><b>79%</b><span>오답률</span></div></div>
```

## Trend line (SVG)

```css
.ztrend{width:100%;height:130px;}
.ztrend .zt-line{fill:none;stroke:var(--accent);stroke-width:3;stroke-linecap:round;stroke-linejoin:round;}
.ztrend .zt-dot{fill:var(--primary);}
```
```html
<svg class="ztrend" viewBox="0 0 320 130" preserveAspectRatio="none">
  <polyline class="zt-line" points="0,110 64,96 128,100 192,58 256,40 320,12"/>
  <circle class="zt-dot" cx="320" cy="12" r="5"/>
</svg>
```
Map each value v to y = H − (v−min)/(max−min)×H; x spaced evenly across the width.

## Comparison table

```css
.ztable{width:100%;border-collapse:separate;border-spacing:0;font-size:14px;}
.ztable th{text-align:left;padding:12px 16px;color:var(--muted);font-weight:700;border-bottom:2px solid var(--primary);}
.ztable td{padding:12px 16px;border-bottom:1px solid #DCE2EA;color:var(--ink);}
.ztable td.hi{color:var(--accent);font-weight:700;}        /* the winning cell */
.ztable tr:last-child td{border-bottom:0;}
```
```html
<div class="tile col-12"><table class="ztable">
  <thead><tr><th>항목</th><th>점진적 도입</th><th>전면 재설계</th></tr></thead>
  <tbody>
    <tr><td>속도</td><td>보통</td><td class="hi">빠름</td></tr>
    <tr><td>리스크</td><td class="hi">낮음</td><td>높음</td></tr>
  </tbody>
</table></div>
```

## Timeline (horizontal)

```css
.ztl{display:flex;align-items:flex-start;width:100%;}
.ztl-item{flex:1;text-align:center;position:relative;padding-top:30px;}
.ztl-item::before{content:"";position:absolute;top:9px;left:0;right:0;height:3px;background:var(--shadow);}
.ztl-item:first-child::before{left:50%;}.ztl-item:last-child::before{right:50%;}
.ztl-dot{position:absolute;top:2px;left:50%;transform:translateX(-50%);width:16px;height:16px;border-radius:50%;
  background:var(--accent);box-shadow:0 0 0 4px var(--base),3px 3px 7px var(--shadow);}
.ztl-yr{font-size:15px;font-weight:800;color:var(--primary);}
.ztl-tx{font-size:13px;color:var(--muted);margin-top:4px;line-height:1.4;}
```
```html
<div class="ztl">
  <div class="ztl-item"><div class="ztl-dot"></div><div class="ztl-yr">2011</div><div class="ztl-tx">구글 브레인</div></div>
  <div class="ztl-item"><div class="ztl-dot"></div><div class="ztl-yr">2026</div><div class="ztl-tx">GPT-5.2</div></div>
</div>
```

## Code block

```css
.zcode{background:#0E2236;color:#E6EEF6;border-radius:16px;padding:20px 22px;overflow:auto;
  font-family:'SFMono-Regular',Consolas,'D2Coding',monospace;font-size:14px;line-height:1.6;
  box-shadow:inset 4px 4px 10px rgba(0,0,0,.3);}
.zcode .k{color:#7FD2F5;}.zcode .s{color:#9FE0A0;}.zcode .c{color:#6E7681;}
```
```html
<pre class="zcode"><code><span class="c"># 에이전트 호출</span>
<span class="k">def</span> run(task):
    <span class="k">return</span> agent.invoke(task)</code></pre>
```

Every chart sits inside a `.tile` (so it gets the neumorphic frame) and a slide
keeps one hero. Add a `출처:` caption under data you pulled from a source.
