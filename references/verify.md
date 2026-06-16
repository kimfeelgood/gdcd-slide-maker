# Verifying the deck + build gotchas

Lessons that make the difference between "looks done" and "actually works." Read
this before declaring a build finished.

## Render with a real browser (not LibreOffice / Quick Look)

The zzanmul look depends on soft neumorphic shadows, 3D flips, and acrylic blur —
LibreOffice and `qlmanage` do not render these. Use headless Chrome to screenshot:

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=1340,754 --virtual-time-budget=1500 \
  --screenshot=/tmp/s.png "<deck>/index.html"
```

`--virtual-time-budget` lets fonts/images settle before the shot. 1340×754 ≈ a
16:9-ish slide; raise the budget (~2000ms) when a slide loads a remote image or a
YouTube iframe.

## Screenshot a SPECIFIC slide (and an opened reveal)

The deck shows slide 1 by default. To verify any other slide — or a flipped-open
reveal — inject a tiny `load` script into a throwaway copy, then shoot that copy:

```python
# show slide index 2 (0-based), and flip its box open + load the video
h = open('index.html', encoding='utf-8').read()
inj = ('<script>addEventListener("load",()=>setTimeout(()=>{'
       'const s=document.querySelectorAll(".slide");'
       's.forEach(x=>x.classList.remove("active"));s[2].classList.add("active");'
       'const f=s[2].querySelector(".flipbox");'
       'if(f){f.classList.add("flipped");const i=f.querySelector("iframe");'
       'if(i&&!i.src&&i.dataset.src)i.src=i.dataset.src;}'
       '},200));</script>')
open('_probe.html','w',encoding='utf-8').write(h.replace('</body>', inj+'\n</body>'))
```

Then screenshot `_probe.html` and delete it. Check: the slide fills the width, the
hero/tiles aren't squished, a flip box flips to its 노출 asset, video lazy-loads,
nothing overflows the viewport.

## Gotcha 1 — every utility class a slide uses must exist in the deck CSS

A deck's `<style>` often defines only the `.col-*` spans (and list/helper classes)
that its current slides happen to use. If you BUILD a slide using `.col-6` or a
`ul` bullet style the deck never declared, the element silently loses its span and
**collapses to one narrow column** (the tell-tale symptom: a tile squished to the
left, text wrapping every word, content overflowing downward).

Fix: before finishing, make sure every class your new markup references is defined.
Add any missing ones to the shared `<style>` **additively** (a class no existing
slide uses → KEEP slides are unaffected). Common ones to check: `.col-6`, list
styles, any new tile variant. Then re-render and confirm existing slides look
identical.

## Gotcha 2 — image-only / full-bleed source slides: redesign, don't paste

A sparse `.pptx` slide is sometimes just **one full-bleed image** with no text and
no 박스/노출 markers (e.g. a comparison chart the author pasted). Do **not** embed
that foreign-styled screenshot as the slide. Read what it says and **rebuild it as
native zzanmul tiles** (bento layout, POSCO-blue, the deck's type) so it matches
the rest of the deck. The image is the content brief, not the output. (Only embed
an image verbatim when it's a genuine asset to display — a photo, a real chart the
learner must read pixel-for-pixel — typically via a 노출 reveal.)

## Gotcha 3 — keep each slide within one viewport

Slides are absolutely positioned and vertically centered; content taller than
~100vh overflows with the top scrolled off and the bottom clipped. If a slide runs
tall, it usually means too much copy or a layout bug (see Gotcha 1). Trim copy,
use a wider span, or split into two tiles — don't ship a slide whose hero or last
tile is cut off.

## Gotcha 4 — don't renumber a KEEP slide's label

When you insert a slide between numbered ones (e.g. "· 2강" and "· 3강"), giving
the new one "· 3강" would clash, and renumbering the existing ones edits finished
slides. Default: give the inserted slide a non-conflicting thematic eyebrow (no
number, or a topic tag) and leave the KEEP slides' labels alone. Renumber only if
the user explicitly asks.
