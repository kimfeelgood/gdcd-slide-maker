# PPTX intake — what the extractor gives you

Run once per deck:

```bash
python3 scripts/extract_pptx.py <input.pptx> <workdir>
```

It prints a per-slide summary and writes `<workdir>/manifest.json` plus every
image to `<workdir>/media/`. You design from the manifest; you do not re-parse the
.pptx yourself.

## How markers are detected

For every shape (descending into groups) the extractor checks three places for a
marker: the **shape name**, its **alt text (descr)**, and its **text**. So an
author can tag an element by any of:

- typing `박스1` / `노출1` as text in the shape, or
- renaming the shape to `박스1` (Selection Pane), or
- setting the image's alt text to `노출1`.

Patterns (number is captured, leading zeros ok):

- box button → `박스N`, `버튼N`, or `box N`  (the user often writes 버튼/button)
- reveal asset → `노출N`, `노출 N`, `reveal N`, `show N`

**One shape per marker for clean auto-detection.** The extractor reads the first
marker it finds per shape. If an author packs several markers into a single shape
(e.g. one textbox containing `버튼1 … 버튼2 … 버튼3 …`, common in rough drafts),
only the first is detected and the whole shape is treated as one element. When you
see that, split the text by the `버튼N`/`박스N` markers yourself and design one flip
box per marker (front = that step's title, back = the text that followed it). For
reliable auto-detection going forward, put each 박스/노출 on its own shape.

A 노출 element's **type** is inferred: a picture → `image` (exported to media); a
text/shape containing a URL → `url` (or `video` if the URL ends in a video
extension); a bare `<video>`-style file → `video`; a text-only 노출 → `text`.

**Label-on-image pattern (handled automatically).** A very common authoring habit
is to place a small `노출N` *label* textbox **on top of** the real image instead of
renaming the image. The extractor detects this: an empty-text `노출N` marker is
bound to the image it overlaps (or is nearest to), so that reveal comes out as
`type:"image"` pointing at the right file. Identical duplicated pictures (authors
often stack two copies) are de-duplicated to a single media file. You will
normally just see one clean `image` reveal per number — no action needed.

## manifest.json schema

```jsonc
{
  "source": "/abs/path/input.pptx",
  "slide_size_in": [13.33, 7.5],
  "slide_count": 3,
  "slides": [
    {
      "index": 1,
      "fp": "a1b2c3d4e5f6",
      "texts":  [ {"name":"Title 1","text":"AI 에이전트란","pos":[l,t,w,h]} ],
      "images": [ {"name":"Pic 2","file":"media/s1_img2.png","pos":[...]} ],
      "boxes":  [ {"n":1,"label":"작동 원리","face_image":null,"pos":[...]} ],
      "reveals":[ {"n":1,"type":"image","file":"media/s1_reveal1.png","pos":[...]},
                  {"n":2,"type":"url","url":"https://youtu.be/abc","label":"데모 영상","pos":[...]} ]
    }
  ]
}
```

- `texts` / `images` are **unmarked** content — your raw material for the bento
  layout (titles, body, supporting pictures).
- `boxes` are the interactive buttons. `label` is the shape's text with the
  marker stripped (may be null → name it from the paired reveal or a default like
  "자세히 보기"). `face_image` is set only if the button itself was a picture.
- `reveals` are the toggle targets, paired to boxes by `n`.

## Turning a manifest slide into a designed slide

1. Read `texts` — promote the most important line to the slide's headline (an
   action-style, teaching-friendly sentence), the rest into supporting tiles.
2. Place `images` into tiles sized to their role (a diagram gets a big tile, an
   icon a small one). Reference them as `media/...` (copy the workdir `media/`
   next to the output html, or base64-embed).
3. For each `boxes[i]`, emit a `<button class="boxbtn" data-reveal="N">` tile, and
   for the matching `reveals` entry emit a `<template class="reveal"
   data-reveal="N" data-type="...">` with the right inner markup (see
   `interactions.md`). Keep the numbers identical.
4. If a box has no matching reveal (or vice-versa), still render the box (it just
   won't open) and note the mismatch in one line for the user.

## YouTube / Vimeo / page URLs

Convert watch URLs to embeddable form when you build the `url` reveal:

- `youtu.be/ID` or `youtube.com/watch?v=ID` → `https://www.youtube.com/embed/ID`
- `vimeo.com/ID` → `https://player.vimeo.com/video/ID`
- other pages → embed in an iframe; if the site blocks framing (X-Frame-Options),
  fall back to a neumorphic "link card" tile that opens the URL in a new tab, and
  mention it.
