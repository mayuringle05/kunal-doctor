# Dr. Krunal Kumbhare — Static Doctor Portfolio

A **self-contained, dependency-free, nine-page static website** based on the supplied résumé and introductory nameplate. The visual direction is inspired by [Dr. Amara](https://dr-amara-wbs.framer.website/): indigo + pale-blue palette, editorial serif typography, rounded navigation and appointment CTAs. The site uses original HTML/CSS/JS and its own graphic treatment; it does **not** copy Framer's original source code, images, testimonials or third-party assets.

## Included

- `content/DOCTOR_PROFILE.md` — comprehensive, source-labelled extraction of the résumé and intro card; includes contradictions, missing information and public-launch verification checklist.
- `content/doctor.json` — structured doctor facts, experience, specialties and contact details driving generated pages. Generic editorial headings and layout text remain in `build.py`.
- `assets/photos/*.webp` — three user-supplied photographs, optimized to two responsive WebP widths each. The corridor portrait is used in the hero, the notebook image alongside the professional profile, and the consultation image beside the appointment guidance.
- `content/original-intro-card.jpeg` — original image, kept privately as a research/reference source, **not** included in the public `dist/` output.
- `build.py` — zero-dependency static generator, escaping user content and producing nine separate accessible HTML pages.
- `assets/site.css` — responsive design without frameworks or remote font requests.
- `assets/site.js` — mobile nav, reduced-motion-safe scroll animation, and three-field callback request via WhatsApp (no database, tracking or storage).
- `dist/` — ready-to-host static files, **draft noindex** by default.
- `tests/test_site.py` — source integrity, pages, links, privacy and cautious medical claims.
- `docs/COSMO_CAPABILITY_PROOFS.md` — local verification receipts and remaining proof blockers.

## Run locally

```bash
python3 build.py
python3 -m http.server 4173 --directory dist
# Visit http://localhost:4173
```

To test:

```bash
python3 -m unittest discover -s tests -v
```

## Change doctor details

Edit `content/doctor.json`, then rerun `python3 build.py`. This generates Home, About and Contact. The template is reusable, but additional doctor-specific editorial prose in `build.py` should also be reviewed when adapting it for another clinician. The doctor’s FNB fellowship is recorded as completed based on the owner’s 18 November 2026 update. Its exact completion date is unknown, so the website does not invent one. Record future corrections and confirmations in `content/DOCTOR_PROFILE.md`. `build.py` HTML-escapes JSON-derived text.

## Publishing control

`dist/` defaults to **`noindex,nofollow` and `Disallow: /`** because OPD days/address and final public credential styling still need confirmation. The owner has confirmed completion of his FNB fellowship, and the site now displays the FNB and FIAGES credentials. No domain, deployment, production change, Railway preview, Cloudflare service or payment was activated as part of this build.

Only once **all claims are confirmed** and an actual production domain is specified, rebuild with:

```bash
SITE_PUBLIC=1 SITE_URL=https://your-verified-domain.example python3 build.py
```

The public build generates appropriate canonical URLs, a sitemap and a permissive robots file. Do not use a sample domain for live publishing.

## Appointments and sensitive information

The Contact form collects only name, contact number and appointment category in-browser and opens an editable **WhatsApp message** using the phone number in the résumé. It does not submit to any private server, analytics provider, or database. The user's browser and WhatsApp handle the message; opening WhatsApp is **not** a booking confirmation. Do not solicit medical histories through this static form.

## Parity gaps and image policy

The user subsequently supplied three images of Dr. Kumbhare. Those photographs now replace the artificial monogram placeholder and appear in relevant consultation/background sections. Real person photos or quotes from the reference website have not been reused. This is visual/structural emulation, **not** a pixel-exact replica. A later authorized pass should insert a licensed photo of the actual doctor and inspect live browser screenshots against the reference.

## COSMO-FABRIC engineering boundaries

All code authored in ChatGPT's working container. No Mac source editing, deploy or merge. Without a destination repository and an approved verification target, the deliverable is an exported project ZIP (and optional patch), **not** a proof of Mac/Railway completion. Reference contract: `mayuringle05/cosmo-ai-os-fabric` issue #657.

## Added photos, draft proof (18 Nov 2026)

- Hero: corridor portrait, immediate visible load with priority.
- Homepage professional background and About: doctor writing in a notebook.
- First consultation section and Contact: doctor speaking with a patient.
- Images have two WebP widths (`480w`, `960w`) and are served locally using `srcset`. Six files total approximately 215 KB. The original PNG uploads are not embedded in the public static export.
- 9 unit/integration tests passed. Offline Chromium `set_content` screenshots captured all three images on desktop (1440×900) and mobile (390×844), including a mobile menu interaction. This offline render inlines the site assets because HTTP and file navigation are blocked by the container administrator; it **does not** establish real origin/navigation behavior or Mac/Cloudflare proof.

## Railway deployment (isolated static site)

The repository includes a minimal `Dockerfile` for Railway. It builds the generated
HTML with Python and serves the `dist/` directory on Railway's injected `PORT`
(default local port: `8080`). No database, external API or paid dependency is
needed for the application code itself.

- **Service source:** this GitHub repository and the approved feature branch
- **Builder:** Dockerfile
- **Health endpoint:** `/` (static homepage)
- **Public paths:** `/`, `/about/`, `/contact/`, six `/care/<slug>/` routes and `/assets/...`
- **Publication:** default `noindex,nofollow` until verified clinic details
- **Costs:** Railway meters runtime resources. Check the existing plan's credit
  and budget before enabling a service; this repo does not enforce a zero-cost cap.

A deployment is not proof of the appointment flow. Verify the public pages, image
assets, mobile menu and WhatsApp redirect with real HTTP/browser receipts.


## Current deployed preview (18 Nov 2026)

Site: https://kunal-doctor-web-production.up.railway.app/

Railway is connected to the doctor-only project on the deployment feature branch. Successful deployment of `4975d55` has been verified with 200 responses for all three pages and all six photos. Desktop/mobile public-URL inspection and offline Playwright interactions are recorded in `docs/COSMO_CAPABILITY_PROOFS.md`. The site is intentionally `noindex` until the remaining medical profile/clinic facts are approved. Railway usage is metered.


## Refined doctor portfolio feature branch (19 Nov 2026)

The optional release update is in `feat/elegant-motion-care-pages-20261119` and is **not currently deployed on `main`**. It adds six patient-oriented care detail pages, the corrected Marathi hero name, gentle reduced-motion-safe animations, a cleaner hero and a three-field WhatsApp callback handoff. Read `docs/RELEASE_NOTES_20261119.md` for the precise fields awaiting confirmation. The live Railway site continues to serve the previous `main` deployment until the change receives live browser verification and release approval.
