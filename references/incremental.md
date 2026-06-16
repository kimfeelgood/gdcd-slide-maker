# Incremental updates — keep finished slides, build only what's new

The author grows the source `.pptx` over time and inserts slides anywhere (front,
middle, end). The rule: **never re-make a slide that's already done** — build only
the genuinely new ones and place them at their pptx position.

## How identity survives reordering

Every built `<section>` is stamped with `data-fp="<fingerprint>"`. The fingerprint
(from `extract_pptx.py`) is a hash of the slide's **content** — its text, image
bytes, and 박스/노출 markers — and deliberately **excludes position**. So:

- Insert a slide in the middle → all other slides keep the same fp → all KEEP;
  only the inserted one is new → BUILD.
- Reorder slides → every fp unchanged → all KEEP, just re-sequenced.
- Edit a slide's words/image → its fp changes → it shows as BUILD (treated as new
  content). If the user wanted that slide left alone, confirm before rebuilding.

## Step by step

1. Re-extract the updated pptx to a fresh workdir (gets new `manifest.json`).
2. Run the planner against the existing deck:
   ```bash
   python3 scripts/diff_build.py <workdir>/manifest.json <existing>/index.html
   ```
   Read the printed plan and the `<PLAN_JSON>` block: an ordered list where each
   entry is `KEEP` (fp present in the old deck) or `BUILD` (new fp), plus
   `removed` fps (in the old deck, absent from the pptx).
3. Load the existing `index.html`. Extract every
   `<section class="slide" data-fp="X"> … </section>` into a map keyed by `X`.
   (A simple regex or an HTML parser both work; capture the whole section node.)
4. Assemble the new deck body by walking the plan **in order**:
   - **KEEP** → output the existing section for that fp **verbatim**. Do not
     re-word, re-layout, restyle, or "improve" it. It is finished.
   - **BUILD** → design a new section in zzanmul from the manifest slide, wire its
     flip box(es), and stamp `data-fp` with the manifest fp.
5. Copy any new images from `<workdir>/media/` into the deck's `media/` (the
   extractor de-dupes, so existing files are unaffected).
6. Save `index.html`. The runtime rebuilds nav dots and page numbers from the
   sections automatically, so inserting/removing sections renumbers everything.
7. Tell the user exactly what changed: e.g. "3페이지를 2번 위치에 추가했고 나머지
   4장은 그대로 두었습니다."

## Pinned (URL/web) slides

Slides ingested from a web URL aren't in the .pptx, so they carry
`data-fp="url-…"` + `data-source="<url>"`. `diff_build.py` lists them under
**PINNED**, never KEEP/BUILD/REMOVED. When you rebuild after a .pptx change: lay
out the pptx-ordered sections (KEEP/BUILD) first, then **re-append the pinned URL
sections verbatim** in their existing relative position. Never drop them just
because they're absent from the manifest.

## Removed slides

If a fp is in the old deck but gone from the pptx (`removed`), the pptx is the
source of truth for which slides exist, so drop it from the deck — but say so in
the summary. If the user clearly wants it kept, keep it; when unsure, ask in one
line.

## Additive CSS is fine; restyling is not

A BUILD slide may need a helper class the existing deck never defined (e.g. an
older deck only declared the `.col-*` spans its slides happened to use, so a new
two-up slide needs `.col-6`, or a bulleted slide needs a `ul` rule). Adding such
rules to the shared `<style>` block is allowed **as long as they are purely
additive** — a class no existing slide uses, so KEEP slides render identically.
Verify by eye that slides 1..N look unchanged. Never modify or repurpose a rule an
existing slide already relies on.

## Things to never do on an update

- Never restyle, re-word, or re-lay-out a KEEP slide. "별도 요청이 없다면 바꾸지
  말 것."
- Never drop the `data-fp` stamp — without it the next update can't tell done from
  new.
- Never renumber by hand in a way that fights the engine; let the sections' order
  drive the page numbers.
