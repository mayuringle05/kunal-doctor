# Areas of Care photographic card refinement (19 Nov 2026)

## Scope

The six existing care cards retain their text, destinations and ordering. Their medical pictograms have been replaced by photographs of Dr. Krunal Kumbhare supplied by the owner. Each image is sourced locally from the six WebP sizes already in `assets/photos/` (three distinct doctor photos, with two responsive variants each), with deliberately different crops in the two card rows. No stock or synthetic operating-room images were introduced, and the photos do not claim to show the procedures described on the cards.

Visual changes: edge-to-edge photo at top, translucent numbered marker, ivory card body with small uppercase specialty, larger editorial heading, thin rule, restrained hover zoom, explicit “Explore this care” link and an accessible full-card target. The JavaScript, six condition detail pages, contact flow and public noindex setting are unchanged.

## Verification performed in ChatGPT environment

- `python3 build.py`: generated nine pages, default preview `noindex`.
- `python3 -m unittest discover -s tests -v`: 13/13 passing, including a new source/markup/photo/no-icon regression test.
- `node --check assets/site.js`: passes (no JS changes).
- Offline Chromium with local assets inlined via data URIs: desktop 1440px, tablet 820px and mobile 390px. Six card images decode and paint in each viewport; unique links, no horizontal overflow or JavaScript errors. Reduced-motion mode and pointer hover transition checked. All four visual checks passed.
- Screenshots visually inspected in ChatGPT at desktop and mobile sizes. These are local/offline renders, not live Railway or Mac screenshots.

## Release boundary

No main merge, Railway environment change, paid image CDN or external asset request is required to review the branch. The existing three doctor photographs remain the only card image sources. Run the authorized Mac/REA or isolated preview inspection before a production merge. Continue to keep public indexing disabled until MMC reg