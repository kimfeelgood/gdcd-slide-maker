# Interactions — transitions & 박스→노출 reveals

The template (`assets/template.html`) already contains both engines. You only set
markup + data attributes; the JS handles animation, matching, and toggling. This
file explains the knobs and the reveal markup per asset type.

## Dynamic page transitions

Set the mode on the deck root; it animates every page change automatically.

```html
<div class="deck" id="deck" data-transition="depth"> ... </div>
```

| mode | feel | good for |
|------|------|----------|
| `depth` (default) | incoming rises from depth, outgoing recedes/scales back | most teaching decks |
| `slide` | horizontal push (direction-aware) | linear step-by-step flow |
| `flip` | 3D card turn | chapter breaks, "reveal a new topic" |
| `zoom` | zoom through | emphasis, before/after |
| `cover` | new slide slides up over the old | layered build-ups |

Direction is automatic (forward vs back) from nav. Motion is gated behind
`prefers-reduced-motion` — don't remove that. You can vary the feel by changing
the single `data-transition` value; per-slide variation is possible but keep it
purposeful, not random.

Navigation is wired for: ← → ↑ ↓, PageUp/Down, Space, on-screen arrows, nav dots,
and touch swipe. Opening a reveal does not change slides; changing slides closes
any open reveal.

## The reveal pattern (박스N ↔ 노출N)

A **box button** and its **reveal template** share the same number `N`:

```html
<!-- the neumorphic button the learner clicks (박스1) -->
<button class="boxbtn col-4" data-reveal="1">
  <span class="bxicon">＋</span>
  <span><span class="bxlabel">작동 원리</span><span class="bxsub">눌러서 보기</span></span>
</button>

<!-- the content shown when box 1 is clicked (노출1). Inert until opened. -->
<template class="reveal" data-reveal="1" data-type="image">
  <img src="media/s2_reveal1.png" alt="작동 원리">
  <div class="reveal-cap">에이전트의 인지–행동 루프</div>
</template>
```

The engine: first click on 박스N clones 노출N into a centered overlay card that
**scales up from the button's position** over an acrylic-blurred backdrop; the
button presses in (inset + accent icon) to show it is "on". Clicking 박스N again,
or the backdrop, the × button, or Esc, animates it back out (a true toggle).
Numbers are unique per deck, so 박스3 always opens 노출3.

### Reveal markup by `data-type`

```html
<!-- image -->
<template class="reveal" data-reveal="1" data-type="image">
  <img src="media/s2_reveal1.png" alt="...">
  <div class="reveal-cap">캡션(선택)</div>
</template>

<!-- local video file -->
<template class="reveal" data-reveal="2" data-type="video">
  <video controls playsinline src="media/clip.mp4"></video>
</template>

<!-- YouTube / Vimeo / embeddable URL (use the /embed form) -->
<template class="reveal" data-reveal="3" data-type="url">
  <div class="iframe-wrap"><iframe src="https://www.youtube.com/embed/ID" allowfullscreen></iframe></div>
</template>

<!-- text-only reveal (e.g. an answer, a definition) -->
<template class="reveal" data-reveal="4" data-type="text">
  <div class="reveal-text">정답: ...</div>
</template>
```

Putting media inside `<template>` keeps videos/iframes from loading or autoplaying
until the learner opens them, and clearing the overlay on close stops playback.

## Alternative: in-place reveal (replace the tile)

If the user prefers the image to appear **inside the slide** (swapping the box
tile) rather than as an overlay, use a flip-tile instead of the overlay engine:

```html
<div class="flipbox col-4" tabindex="0">
  <div class="flip-inner">
    <div class="flip-face front boxbtn"><span class="bxicon">＋</span><span class="bxlabel">박스1 라벨</span></div>
    <div class="flip-face back"><img src="media/s2_reveal1.png" alt=""></div>
  </div>
</div>
```

```css
.flipbox{perspective:1000px;cursor:pointer;}
.flip-inner{position:relative;transition:transform .55s var(--ease);transform-style:preserve-3d;min-height:160px;}
.flipbox.flipped .flip-inner{transform:rotateY(180deg);}
.flip-face{position:absolute;inset:0;backface-visibility:hidden;border-radius:var(--r-tile);
  box-shadow:8px 8px 18px var(--shadow),-8px -8px 18px var(--light);overflow:hidden;}
.flip-face.back{transform:rotateY(180deg);}
```

For a **video/URL** reveal in a flip tile, put a 9:16 (or 16:9) wrapper on the
back face and lazy-load via `data-src` so the player only loads when flipped, and
stop playback when it flips back:

```html
<div class="flip-face back">
  <button class="reflip">↩</button>
  <div class="video-wrap"><iframe data-src="https://www.youtube.com/embed/VIDEO_ID?rel=0"
       allow="encrypted-media; picture-in-picture; web-share" allowfullscreen></iframe></div>
</div>
```
```css
.flip-face.back .video-wrap{height:90%;aspect-ratio:9/16;border-radius:14px;overflow:hidden;}  /* 16/9 for landscape */
.flip-face.back .video-wrap iframe{width:100%;height:100%;border:0;}
```
```js
function setFlip(f,on){
  f.classList.toggle('flipped',on);
  const ifr=f.querySelector('iframe');
  if(ifr){ if(on){ if(!ifr.src&&ifr.dataset.src) ifr.src=ifr.dataset.src; } else if(ifr.src){ ifr.src=''; } }
}
document.querySelectorAll('.flipbox').forEach(f=>
  f.addEventListener('click',()=>setFlip(f,!f.classList.contains('flipped'))));
// also call setFlip(f,false) on every flipped tile when the slide changes
```

Same toggle behavior, but the reveal happens within the bento cell. Pick the
overlay engine for big images, the flip-tile for in-context reveals and short
vertical videos (YouTube Shorts embed cleanly at 9:16).

**Front-face copy:** keep it minimal — the `＋` (image) or `▶` (video) icon plus a
short label and sub already signal "tap me." Do **not** add a "탭하면 뒤집힙니다 /
tap to flip" hint line; it's redundant and the user dislikes it.
