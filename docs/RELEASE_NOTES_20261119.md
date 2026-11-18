# Dr. Krunal Kumbhare: portfolio refinement (19 Nov 2026)

## Visual and content changes

- Bilingual hero eyebrow corrected to **डॉ. क्रुणाल कुंभरे**. Repeated hero badge removed; desktop portrait sits beside the headline and appears during the first mobile viewport.
- Serif headline tighter (`letter-spacing: -0.028em`), highlighted phrase more legible, visual hierarchy quieter.
- CSS entrance/reveal animations, restrained card and button hover interactions, scroll-triggered sections, keyboard-visible focus, `prefers-reduced-motion` support. No JavaScript animation library or remote tracking.
- Six Areas of Care cards rewritten around presenting conditions and linked as whole-card targets to dedicated `/care/{slug}/` pages. The pages are static, informative, and avoid guaranteed outcomes.
- Robotic operating-room exposure shown under completed FNB training at FMRI rather than offered as a standalone surgical service.
- Contact page now includes a direct WhatsApp link, phone, email, and an optional callback-request handoff (Name, Phone Number, Brief Concern). Form validates locally and opens a prefilled WhatsApp message; the patient must press Send. There is no database or message delivery guarantee.

## Facts awaiting medical-owner confirmation

The following JSON fields are blank until documentary confirmation:

| Field | Needed | Result until verified |
|---|---|---|
| `mmc_registration_number` | Exact Maharashtra Medical Council registration | Displays only “Maharashtra Medical Council registered” |
| `clinic_name` | Hospital or clinic name | Generic Nagpur location |
| `clinic_locality` | Precise Nagpur locality | Generic Nagpur location |
| `clinic_address` | Full street address | Contact-page appointment address message |
| `clinic_map_embed_url` | Google Maps embed URL for confirmed address | No potentially misleading map |
| `opd_days` | Actual recurring clinic days | Only confirmed evening hours, 7–10 PM |
| Production domain | Domain name plus owner DNS access | Railway preview URL remains in use, SEO `noindex` |

Never substitute example values such as Mon–Sat or `drkrunalkumbhare.com` without confirming ownership and accuracy. Once confirmed, update `content/doctor.json`, regenerate and validate the website, and separately approve the domain connection and public indexing.

## Verification

- Static generator: `python3 build.py` → 9 HTML pages.
- Python unit/integration tests: `python3 -m unittest discover -s tests -v` → 12/12 pass.
- `node --check assets/site.js` → pass.
- CSS parser: 338 parsed rules, 0 errors.
- Offline Chromium screenshot/interaction check: 24/24 pass across desktop 1440×900 and mobile 390×844, all 9 pages, decoded images, nav Escape, callback URL validation and enabled animations. Screenshot pixels inspected in ChatGPT.
- Public-build fixture: 9 sitemap URLs and canonical/robots logic validated; `noindex` restored immediately.
- **Not verified:** Mac/REA/Playwright on the new branch or a newly deployed Railway revision. The screenshots are offline Playwright `page.set_content` renders; there is no claim of a live-branch browser audit or custom-domain connectivity.
