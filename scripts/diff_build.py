#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Incremental build planner for gdcd-slide-maker.

Compares the freshly-extracted manifest against an already-built index.html and
prints, in the NEW pptx order, which slides to KEEP verbatim (already designed,
unchanged) and which to BUILD (newly added or edited). Slides that exist in the
old deck but are gone from the pptx are reported as REMOVED.

Matching is by the position-independent content fingerprint (`fp`) the extractor
writes, so reordering or inserting a slide anywhere only marks the genuinely new
slide as BUILD — every completed slide is preserved.

Usage:
    python3 diff_build.py <workdir>/manifest.json [<existing_index.html>]

Output: a human-readable plan plus a machine-readable JSON block between
<PLAN_JSON> ... </PLAN_JSON> the skill can parse.
"""
import sys, os, re, json


def existing_sections(html_path):
    """Return [{fp, external}] for each built section. `external` is True for
    slides not sourced from the pptx (URL/web ingests), which carry data-source or
    a 'url-' fp — those are pinned and must never be reported as REMOVED."""
    if not html_path or not os.path.exists(html_path):
        return []
    html = open(html_path, encoding='utf-8').read()
    out = []
    for tag in re.findall(r'<section\b[^>]*>', html):
        m = re.search(r'data-fp="([^"]+)"', tag)
        if not m:
            continue
        fp = m.group(1)
        external = ('data-source=' in tag) or fp.startswith('url-')
        out.append({'fp': fp, 'external': external})
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    manifest = json.load(open(sys.argv[1], encoding='utf-8'))
    old = existing_sections(sys.argv[2] if len(sys.argv) > 2 else None)
    old_set = {s['fp'] for s in old}
    pinned = [s['fp'] for s in old if s['external']]

    plan = []
    cur_fps = []
    for s in manifest['slides']:
        fp = s['fp']
        cur_fps.append(fp)
        plan.append({
            'pos': s['index'], 'fp': fp,
            'action': 'KEEP' if fp in old_set else 'BUILD',
            'summary': (s['texts'][0]['text'].split(chr(10))[0][:42] if s['texts'] else ''),
            'boxes': [b['n'] for b in s['boxes']],
            'reveals': [{'n': r['n'], 'type': r.get('type')} for r in s['reveals']],
        })
    # only pptx-sourced slides can be REMOVED; URL/web slides are pinned, kept.
    removed = [s['fp'] for s in old
               if not s['external'] and s['fp'] not in set(cur_fps)]

    print(f'existing deck slides: {len(old)}   pptx slides now: {len(cur_fps)}')
    if not old:
        print('(no existing deck found — first build, everything is BUILD)')
    for p in plan:
        tag = '＋ BUILD' if p['action'] == 'BUILD' else '· keep '
        rv = ''.join(f" 노출{r['n']}({r['type']})" for r in p['reveals'])
        bx = ''.join(f" 박스{n}" for n in p['boxes'])
        print(f"  {p['pos']:>2} [{p['fp']}] {tag}  {p['summary']}{bx}{rv}")
    if pinned:
        print(f'  PINNED (URL/web slides, keep in place, not from pptx): {pinned}')
    if removed:
        print(f'  REMOVED (in old deck, gone from pptx): {removed}')
    n_build = sum(1 for p in plan if p['action'] == 'BUILD')
    print(f'=> build {n_build} new slide(s); keep {len(plan) - n_build} pptx slide(s) '
          f'+ {len(pinned)} pinned URL slide(s) as-is.')

    print('<PLAN_JSON>')
    print(json.dumps({'order': plan, 'removed': removed, 'pinned': pinned},
                     ensure_ascii=False))
    print('</PLAN_JSON>')


if __name__ == '__main__':
    main()
