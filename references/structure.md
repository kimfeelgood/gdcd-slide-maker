# Structure & delivery — cover, TOC, chapters, progress, presenter mode

A lecture deck needs a spine: a cover, an agenda, chapter breaks, a progress
indicator, and a presenter view. The template's engine already wires the progress
bar, chapter ticks, and presenter mode — you just add the slide types below.
Stamp every slide with `data-fp` as usual.

## Cover (first slide)

```html
<section class="slide cover" data-fp="{{FP}}">
  <div class="bento"><div class="headwrap" style="text-align:left">
    <div class="cover-eyebrow">짠물 강의 · AI 리터러시</div>
    <div class="cover-title">AI를 일에 쓰는 법,<br><span class="hl">한 시간이면 충분합니다</span></div>
    <div class="cover-sub">챗봇을 넘어 에이전트까지: 실무에 바로 쓰는 AI 활용 6단계.</div>
    <div class="cover-meta"><b>강정구</b> · 2026 · 전 6강</div>
  </div></div>
</section>
```

## TOC / agenda

One row per chapter; the big number anchors it. Keep it to 4–7 rows.

```html
<section class="slide" data-fp="{{FP}}">
  <div class="bento"><div class="headwrap"><div class="eyebrow">강의 구성</div>
    <h2>오늘 다룰 <span class="cy">여섯 가지</span></h2></div>
    <div class="toc" style="grid-column:span 12">
      <div class="toc-row"><span class="tn">01</span><span class="tt">AI 챗봇 시장의 반전</span><span class="td">제타 1위</span></div>
      <div class="toc-row"><span class="tn">02</span><span class="tt">토큰 경제의 폭증</span><span class="td">4~10배</span></div>
      <div class="toc-row"><span class="tn">03</span><span class="tt">도입 전략, 두 갈래</span><span class="td">유지 vs 재설계</span></div>
    </div>
  </div>
</section>
```

## Chapter divider

A clean section break. Put it before each chapter's content slides; the engine
drops a tick on the progress bar at every `.chapter` (and `.cover`) slide.

```html
<section class="slide chapter" data-fp="{{FP}}">
  <div class="bento"><div class="headwrap">
    <div class="chapter-no">02</div>
    <div class="chapter-title">토큰 경제의 폭증</div>
    <div class="chapter-sub">왜 사용량이 1년 만에 4~10배로 뛰었는가, 그리고 딥시크의 약진.</div>
  </div></div>
</section>
```

## Progress bar + chapter ticks (automatic)

Already in the template: a 5px bar at the bottom fills as you advance, with a
white tick at each chapter/cover slide. Nothing to wire — just use `.cover` /
`.chapter` classes and the ticks place themselves.

## Presenter mode (automatic, press P)

Built into the engine. While presenting:

- **P** — toggle the presenter overlay: a running **timer**, the wall **clock**,
  the current slide title + page, and a live **scaled preview of the next slide**.
- **F** — fullscreen. **R** — reset the timer. **← / →** — navigate (works with
  the overlay open). **Esc** — close the overlay.

The next-slide preview is a real scaled clone, so charts/images show too. No extra
markup is needed; it reads titles from each slide's `.cover-title` / `.chapter-title`
/ `h1` / `h2`, so give every slide a heading.

## Recommended deck spine

`cover → TOC → (chapter → content… )×N → closing`. Keep one hero per content slide,
a chapter divider before each section, and headings on everything so presenter
mode and the TOC read cleanly. Page numbers and ticks renumber themselves when you
insert/remove slides (incremental builds stay safe).
