---
name: gdcd-slide-maker
description: >-
  Builds and INCREMENTALLY UPDATES interactive educational slide decks from a
  minimally-filled PowerPoint (.pptx), rendered in the user's zzanmul house style
  (POSCO-blue neumorphic tiles, Fluent depth, bento layout) with flip page
  transitions and in-place flip reveals. Use this skill WHENEVER the user wants to
  make or extend 교육용 슬라이드 / 강의 자료 / gdcd-slide-maker 슬라이드 from a sparse .pptx, or
  uses the marker convention 박스N (neumorphic box buttons) revealing 노출N
  (images / videos / URLs). Its defining feature: when the user adds slides to the
  .pptx — even inserted at the front or middle, out of order — it rebuilds ONLY
  the newly added slides and places them at the correct position, leaving every
  already-finished slide untouched unless explicitly asked to change them.
  It can also ingest a web URL — fetch and summarize an article into 1 (max 2)
  zzanmul slides and insert them, pinned so later .pptx updates keep them. Trigger
  on "gdcd-slide-maker로 만들어줘 / 강의 슬라이드 만들어줘 / 새 페이지 추가됐어 반영해줘 / 이
  사이트 내용 요약해서 슬라이드로 추가해줘" with a .pptx or URL. Output is a
  self-contained interactive HTML deck.
---

# gdcd-slide-maker

gdcd-slide-maker turns a near-empty teaching `.pptx` into a finished, interactive deck in
the **zzanmul** design system (POSCO-blue neumorphic tiles + Fluent depth + bento
grid), and — crucially — **keeps already-finished
slides intact** when the source `.pptx` grows. The author keeps adding slides over
time (often inserted in the middle or front, not appended); this skill builds only
what is new and drops it into the right position.

It does three things: **extract** the rough content + markers, **design** new
slides in zzanmul, and **preserve** everything already built.

## Defaults (the user's confirmed preferences)

- Visual system: **zzanmul** (base tone `#EAEEF4`, POSCO blue `#004F91`, Fluent
  accent `#0078D4`, cyan highlights, Noto Sans KR, neumorphic tiles, bento grid).
- Page transition: **flip**. Reveal: **in-place flip tile** (the box tile flips
  where it sits — not an overlay).
- Box front shows just the `＋` (image) / `▶` (video) icon + label + sub. **No
  "탭하면 뒤집힙니다 / tap to flip" hint line.**
- Video/URL reveals embed as a **lazy-loaded iframe** that **stops on close**.
- Output: `index.html` + `media/` (relative refs) in an output folder named after
  the deck.

These are defaults, not locks — honor explicit requests to change any of them.

## The marker convention (박스N ↔ 노출N)

Matched by number. The author tags shapes in the .pptx:

- **박스N** (or `box N`) → an interactive neumorphic **flip box** (front face).
- **노출N** (or `노출 N` / `reveal N` / `show N`) → the asset shown when box N
  flips: an **image**, a **video file**, or a **URL** (YouTube/Vimeo/web). A very
  common pattern is a small `노출N` label placed **on top of** the target image —
  the extractor binds it to that image automatically. The marker text is metadata:
  strip it from any visible label.

## Workflow — first build

1. **Extract.**
   ```bash
   python3 scripts/extract_pptx.py <input.pptx> <workdir>
   ```
   Writes `<workdir>/manifest.json` (per-slide text, images, boxes, reveals, and a
   content **fingerprint `fp`**) and images to `<workdir>/media/`. See
   `references/pptx-intake.md`.
2. **Design.** Copy `assets/template.html`; for each slide compose a bento layout
   (one hero tile, supporting tiles, one flip box per 박스N). Teaching tone: clear,
   friendly, progressive. **Stamp each `<section class="slide" data-fp="…">`** with
   that slide's `fp` from the manifest — this is what makes future updates safe.
   Wire flip boxes per `references/interactions.md`. A source slide that is just one
   full-bleed image with no text/markers is a content brief, **not** an asset to
   paste — read it and rebuild it as native zzanmul tiles (see `references/verify.md`,
   Gotcha 2). Make sure every utility class you use (`.col-6`, list styles, …) is
   actually defined in the deck CSS (Gotcha 1).
3. **Output + verify** `index.html` + `media/` into `<deck>_slides/`. **Always
   render with headless Chrome and screenshot — not LibreOffice/Quick Look, which
   don't show neumorphic shadows, flips, or blur.** To check a specific slide or an
   opened reveal, inject a `load` script that forces that section `.active`
   (and `.flipped` + loads the iframe). The exact command and probe snippet are in
   `references/verify.md`. Confirm: flip transitions animate, each 박스N flips to its
   노출N and back, video lazy-loads and stops on close, no slide overflows the
   viewport, reduced-motion respected.

## Workflow — incremental update (the headline feature)

When the user gives an updated `.pptx` (new slides added anywhere) and an
already-built deck exists:

1. **Re-extract** the new `.pptx` to a fresh workdir.
2. **Plan the diff:**
   ```bash
   python3 scripts/diff_build.py <workdir>/manifest.json <existing>/index.html
   ```
   It prints, in the new pptx order, each slide as **KEEP** (fp already in the
   built deck → leave it exactly as is) or **BUILD** (new/changed fp → design it),
   plus any **REMOVED** (gone from the pptx). A `<PLAN_JSON>…</PLAN_JSON>` block
   gives the machine-readable order. See `references/incremental.md`.
3. **Reuse + insert:** parse the existing `index.html`, collect each
   `<section data-fp="X">…</section>` into a map by fp. Build the new deck body by
   walking the plan in order: for **KEEP**, paste the existing section **verbatim**
   (do not re-design, re-word, or restyle it); for **BUILD**, design a new section
   and stamp its `data-fp`. This naturally puts an inserted slide in its correct
   position while every finished slide stays byte-for-byte the same.
4. **Renumber & finish:** copy any new media into `media/`, update page numbers /
   nav (the engine rebuilds dots automatically from the sections), and save.
   Report which slides were added vs kept.

Because the fingerprint is **content-based, not position-based**, reordering or
inserting a slide marks only the genuinely new slide as BUILD. A slide the user
lightly edited will change fp and be rebuilt — if they want an edited slide left
alone, that's the one case to confirm. Never restyle a KEEP slide on your own.

## Workflow — add content from a web URL

When the user gives a URL and asks to summarize it into slide(s):

1. **Fetch + summarize** with WebFetch: pull the title, a one-line thesis, 6–10
   concrete facts/numbers, the named people/companies/products, and the takeaway.
   **Keep original figures and proper nouns verbatim — never invent numbers.**
2. **Decide length:** default **1 slide**; use **up to 2 (the max)** only when the
   content has two clean angles (e.g. a claim on one page, its evidence on the
   next) that won't fit one page well. Do not exceed 2 per URL unless asked.
3. **Design** in zzanmul like any slide: a hero carrying the key claim or number,
   supporting tiles (figures as `.statline`, named entities as `.chips`), and a
   source caption `출처: <매체> (연도)`. One hero per slide.
4. **Insert** at the position the user asks for (e.g. "5페이지에 추가" → after slide
   4; default is to append at the end).
5. **Fingerprint as external (pinned).** These slides are NOT in the .pptx, so
   stamp each with `data-fp="url-<hash>"` (a 2nd page uses the same hash + `-2`)
   **and** `data-source="<the url>"`. This pins them: `diff_build.py` lists them
   under **PINNED**, never REMOVED, so future .pptx updates keep them. On a later
   pptx rebuild, after laying out the pptx-ordered sections, re-append the pinned
   URL sections in their existing relative position.

## Lecture spine & data viz

A teaching deck is more than content slides. Give it a spine and make numbers
visual:

- **Spine (see `references/structure.md`):** open with a **cover**, add a **TOC**,
  and put a **chapter divider** before each section. The engine then auto-draws a
  bottom **progress bar with chapter ticks** and provides a **presenter mode**
  (press **P**: timer, clock, current title, live preview of the next slide; **F**
  fullscreen, **R** reset). Use `.slide.cover` / `.slide.chapter` classes and give
  every slide a heading so presenter mode and the TOC read cleanly. A good default
  spine: `cover → TOC → (chapter → content…)×N`.
- **Data viz (see `references/dataviz.md`):** sparse slides often carry bare
  numbers — promote them into a **bar chart, donut, trend line, table, or
  timeline** (self-contained, neumorphic, no library). Keep figures verbatim and
  add a `출처:` caption for sourced data. Don't leave comparable numbers as plain
  text when a chart reads faster.

Both are optional per slide but expected for a polished lecture; offer them when
the input has chapters or numbers, even if the user didn't ask explicitly.

## Visual system (zzanmul: POSCO blue + Fluent + neumorphism + bento)

`assets/template.html` bundles every token, so the deck is self-contained. Keep
base tone `#EAEEF4` (never white — neumorphism needs the mid-light base), paired
neumorphic shadows (light highlight top-left / dark shadow bottom-right, light
source fixed top-left), POSCO blue `#004F91` for brand/hero, Fluent blue `#0078D4`
for interactive (box buttons), cyan `#00A8E5` for tiny highlights, Noto Sans KR +
Segoe UI Variable type, an 8px spacing grid, one hero tile per slide, and generous
whitespace.

## References

- `references/structure.md` — cover, TOC, chapter dividers, progress bar, and
  presenter mode (the lecture spine).
- `references/dataviz.md` — bar/donut/trend charts, comparison tables, timelines,
  code blocks (turn numbers into visuals).
- `references/verify.md` — how to render/screenshot with headless Chrome, probe a
  specific slide, and the build gotchas learned in practice (missing utility
  classes, image-only slides, viewport overflow, KEEP-label renumbering).
- `references/incremental.md` — the keep-completed-slides update process in detail.
- `references/interactions.md` — flip transitions + in-place flip reveals (image /
  video / URL), lazy-load and stop-on-close.
- `references/pptx-intake.md` — manifest schema, marker detection, URL embedding.

If something is ambiguous on one slide (an unrecognized marker, an un-embeddable
URL, an edited-vs-new slide), make the reasonable call, note it in one line, and
keep going — never let one slide block the build, and never touch a KEEP slide.
