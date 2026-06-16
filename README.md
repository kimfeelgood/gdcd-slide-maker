# gdcd-slide-maker

A [Claude](https://claude.com/claude-code) **Skill** that turns a minimally-filled
PowerPoint (`.pptx`) into a finished, **interactive educational slide deck** — a
self-contained HTML deck in the *zzanmul* design system (POSCO-blue neumorphic
tiles, Microsoft Fluent depth, bento-grid layout) with dynamic page transitions
and click-to-reveal interactions.

You drop rough text, images, and two simple markers into the `.pptx`; the skill
designs the slides, wires the interactions, and keeps already-finished slides
untouched when you add more.

## What it does

- **Designs from sparse input** — a few words + images per slide become a polished
  bento layout (one hero tile + supporting tiles), in a friendly teaching tone.
- **Box → reveal interactions** — tag a shape `박스N` (or `버튼N`/`box N`) to make a
  neumorphic button; tag an image/video/URL `노출N` to reveal when it's clicked.
  The reveal flips in place (default) and toggles closed on a second click.
- **Media** — images, local videos, and **YouTube/Vimeo/web URLs** (lazy-loaded,
  stop on close).
- **Learn from a URL** — fetch and summarize a web article into 1 (max 2) slides.
- **Incremental & positional updates** — every slide is stamped with a content
  fingerprint, so when you add slides to the `.pptx` (inserted anywhere, out of
  order) only the *new* slides are built, at the right position; finished slides
  stay byte-for-byte the same.
- **Lecture spine** — cover, table of contents, chapter dividers, an automatic
  progress bar with chapter ticks, and a **presenter mode** (press `P`: timer,
  clock, and a live preview of the next slide).
- **Data viz** — promote bare numbers into bar / donut / trend charts, comparison
  tables, timelines, and code blocks (self-contained, neumorphic, no libraries).

## The marker convention (the heart of the skill)

Tag shapes in your `.pptx`; matching is **by number**.

| Marker | Meaning |
|--------|---------|
| `박스N` · `버튼N` · `box N` | becomes an interactive neumorphic **button** |
| `노출N` · `reveal N` · `show N` | the **image / video / URL** revealed when box N is clicked |

The marker text itself is stripped from the output. Put each marker on its own
shape for clean auto-detection. (A `노출N` label placed on top of an image binds to
that image automatically.)

## Install

This is a Claude Code / Claude skill. Install by placing the folder under your
skills directory:

```bash
git clone https://github.com/<you>/gdcd-slide-maker.git ~/.claude/skills/gdcd-slide-maker
```

Then in Claude, ask: *"이 ppt로 강의 슬라이드 만들어줘"* / *"gdcd-slide-maker로 만들어줘"*
and attach a `.pptx`. The skill triggers on educational-slide requests and the
marker convention.

**Requirements:** Python 3 with [`python-pptx`](https://pypi.org/project/python-pptx/)
(`pip install python-pptx`). Output is rendered/verified with headless Chrome.
Fonts (Noto Sans KR / Segoe UI Variable) load from the web with a system fallback.

## How it works

```
gdcd-slide-maker/
├── SKILL.md                  # skill definition: workflow, marker convention, defaults
├── assets/
│   └── template.html         # the engine: flip transitions, in-place reveals,
│                             #   progress bar, presenter mode, zzanmul tokens
├── scripts/
│   ├── extract_pptx.py       # .pptx → manifest.json (text, images, markers, fingerprint)
│   └── diff_build.py         # incremental build planner (KEEP / BUILD / PINNED)
└── references/
    ├── interactions.md       # transitions + in-place flip reveals (image/video/URL)
    ├── incremental.md        # keep-finished-slides update workflow
    ├── structure.md          # cover / TOC / chapters / progress / presenter mode
    ├── dataviz.md            # charts / tables / timelines / code blocks
    ├── pptx-intake.md        # manifest schema + marker detection
    └── verify.md             # render/verify with headless Chrome + build gotchas
```

Typical flow: `extract_pptx.py` parses the deck → the skill designs each slide from
the manifest into `assets/template.html` → output is `index.html` + a `media/`
folder. On re-runs, `diff_build.py` diffs the new `.pptx` against the existing deck
so only new slides are rebuilt.

## License

MIT — see [LICENSE](LICENSE).
