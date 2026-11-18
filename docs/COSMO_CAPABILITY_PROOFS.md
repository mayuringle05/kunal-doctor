# COSMO-FABRIC Capability Proofs — Dr. Krunal Kumbhare Site

**Date:** 2026-11-18 (IST)  
**Task:** implement original 3-page static surgeon portfolio inspired by the supplied [Dr. Amara reference](https://dr-amara-wbs.framer.website/) and grounded in a 3-page CV and intro nameplate image.

## Revision: three user-supplied photographs (18 Nov 2026)

- **User request:** use three supplied images where the context fits, preserving the existing static site design.
- **Sources:** `Friendly Doctor in Clinic Corridor(2).png` for Home hero; `Approachable Doctor with Notebook(1).png` for Home professional profile and About hero; `Warm Clinic Consultation(1).png` for Home consultation guidance and Contact page. No generated or third-party photo substitutions.
- **Implementation:** added six responsive, locally served WebP files; replaced hero monogram placeholder and abstract professional-profile illustration; integrated appointment photo alongside the first-visit steps; added semantic alt text, native dimensions, lazy loading for nonhero photos and `fetchpriority=high` for hero.
- **Unit tests:** fresh `python3 -m unittest discover -s tests -v` 9/9 PASS, 0 failed. Regression test initially failed for missing images before implementation. Local HTTP smoke returned **14/14 HTTP 200** including all 6 WebP assets with the correct MIME type; CSS parser found **272 rules, 0 errors**; `node --check assets/site.js` exited 0.
- **Offline render:** Chromium launched from ChatGPT environment. Real localhost navigation is administratively blocked (`net::ERR_BLOCKED_BY_ADMINISTRATOR`). Instead, loaded generated pages with CSS, JS and WebP assets inlined via `page.set_content`, verified image decoding, zero horizontal overflow, and one H1 per page. **10 desktop/mobile section screenshots** were captured across Home/About/Contact; mobile nav opened and closed with Escape. Screenshots inspected visually. These prove static layout rendering only, not deployed browsing or Mac verification.
- **Outstanding:** Mac/Dagu and Cloudflare browser proof, full reference-site parity, and confirmation of the exact clinic address, OPD days and public photo-use permission. No deploy, push or merge.

## Revision: Humanizer + No AI Slop and FNB completion (18 Nov 2026)

- **Inputs:** Owner clarified that Dr. Kumbhare completed his FNB fellowship and all qualifications listed on the nameplate are complete. Exact FNB completion date not provided. Original résumé listed fellowship as ongoing; that is retained only as a historical source note in the private profile.
- **Humanizer and No AI Slop:** Read the owner's canonical GitHub forks and the no-ai-slop `eval.md`. Reviewed all visible copy in generated Home, About and Contact pages. Removed generic claims about precision, thoughtful care, broad expertise, commitment to care and scripted conversation-led slogans. Replaced them with specialty names, documented training, fellowship completion, surgical roles and concrete OPD instructions.
- **Credential change:** Home and About display `FNB (Minimal Access Surgery)` and `FIAGES`; education and professional timeline use **completed**, without inventing the award date. Robotic/bariatric work remains described as training/exposure, not independently credentialed privileges.
- **Safety and layout:** No new testimonials, clinical outcome statistics, affiliations, patient information storage, remote services or new UI dependencies. Draft SEO remains `noindex,nofollow`.
- **Latest validation:** `python3 -m unittest discover -s tests -v` passed **8/8**; `tinycss2` found **0 CSS syntax errors**; local HTTP checks returned **8/8 HTTP 200**; visible-copy checks across three pages found **no stale FNB status or targeted generic phrases**. The generated website remains `noindex,nofollow`. Mac/REA pixel proof and deployed Cloudflare tunnel verification were not performed in ChatGPT's workspace.

## Completed in ChatGPT authoring environment

- **Source extraction:** `.docx` read through `python-docx`; 47 paragraphs, no embedded doctor portrait. User-supplied intro card transcribed. Source-labelled profile in `content/DOCTOR_PROFILE.md` records all roles, education, affiliations, areas of care and OPD time, and marks discrepancies.
- **Reference inspection:** Public REA `analyze_public_ui` called 2026-11-18; desktop **1440×900** and mobile layout snapshots returned, including navigation layout and dark indigo (`rgb(27,24,118)`) Newsreader serif heading styling. The remote REA tool returned screenshot locations on the owner's Mac but did **not** transfer screenshot pixels into ChatGPT's container. Therefore no reference-to-build visual parity claim is made.
- **Static build:** `python3 build.py` → **PASS**, output 3 HTML pages + assets; default `noindex,nofollow`, `robots.txt Disallow: /`.
- **Unit / integration:** `python3 -m unittest discover -s tests -v` → **8 tests, 8 passed, 0 failed**. Tests check intro/CV capture, no invented reviews or premature FNB completion claims in the **original** version, contacts, link targets, static WhatsApp enquiry logic, HTML escaping, and draft SEO safeguards.
- **CSS parser:** `tinycss2` parsed **241 CSS rules, 0 parse errors**.
- **Public build smoke (isolated local):** `SITE_PUBLIC=1 SITE_URL=https://example.org python3 build.py` → **PASS** for indexable meta tag, canonical URLs, generated 3-URL sitemap and robots Allow. Immediately restored default *noindex* draft via `python3 build.py`. `example.org` was a local fixture; no production deployment.
- **Local HTTP server:** Python `ThreadingHTTPServer` served Home, `/index.html`, About, Contact, CSS, JS, favicon and robots file: **8/8 HTTP 200 with nonempty body**.

## Blocked / unverified

- **Chromium visual proof:** `playwright` launched `/usr/bin/chromium`, but navigation to `http://127.0.0.1:<port>/` failed with **`net::ERR_BLOCKED_BY_ADMINISTRATOR`**. Confirmed that `file://` and `data:` navigation also fail in this container. No real viewport screenshots or mobile interaction run succeeded. Browser smoke harness provided at `tests/browser_smoke.py` for an authorized runner.
- **REA parity screenshots:** screenshot file paths emitted by the REA tool are remote Mac-local paths, not viewable in this container; no original screenshot pixels were inspected in ChatGPT.
- **Mac / Dagu / Playwright verification:** Not executed. User's Mac is restricted to verification; this chat has no authenticated Dagu task authorization or a connected Mac execution route. Do not claim DONE by Mac proof.
- **GitHub push:** No destination doctor-portfolio repository was supplied or found in a GitHub search; the connector has no create-repository tool. Work is exported as a project ZIP and ChatGPT-authored patch instead of being pushed to an unrelated repository.
- **Deploy / merge:** Neither requested for a specific target nor performed. No new Railway/Cloudflare resources, spend, paid APIs, hosted CI or production changes.

## Medical/publication verification requirements

1. FNB completion confirmed by owner; obtain the precise completion date if the doctor wants it published.
2. FIAGES appears on the supplied intro card and the owner says all listed qualifications are completed. Confirm official credential styling for production publication.
3. Confirm Dr. Kumbhare’s permission to publish the three provided photos.
4. Confirm OPD days, real clinic/hospital and address.
5. Verify Maharashtra Medical Council registration number (if public display required).
6. Authorize using CV phone for patient enquiries.
7. Verify robotic/bariatric independent practice claims (website deliberately says *exposure*).

**Result:** Site and profile documentation updated with user-supplied photos and unit/offline-render checks completed in ChatGPT. **Full reference-site parity and Mac verification remain blocked.**


## Railway hosted preview and browser checks (18 Nov 2026)

- **Repository:** mayuringle05/kunal-doctor
- **Feature branch:** `feat/railway-doctor-deploy-20261118`
- **Verified code SHA:** `4975d55a28a73ba3d91373a1e884bbab6e206464`
- **Railway project:** `13bae324-a378-4b82-a451-999713689e91`
- **Service:** `7f24c15e-43ad-45e6-817b-d9a28a81c80b`
- **Environment:** `e6d8a157-0082-4595-8b38-5643bffa4728` (production environment of the isolated doctor-only project)
- **Successful deployment:** `bbb03d5a-6675-4985-9dac-db578668e096`, status `SUCCESS`
- **Public preview:** https://kunal-doctor-web-production.up.railway.app/
- **Configuration:** Dockerfile, Python static server on `PORT`, Railway healthcheck `/`, app sleeping enabled, 0.25 vCPU and 0.25 GB memory limits.
- **Initial failure:** `a3f91906-fbf0-426a-b75b-40bfad6c88bc` pulled the empty `main` commit `ea54d853` and failed Railpack detection. Corrected the GitHub source selection and pinned `4975d55`; second deployment succeeded.
- **Railway build:** `RUN python3 build.py` printed `Built 3 pages into /app/dist (PUBLIC=False, SITE_URL=unset)`; container started successfully.
- **Railway live HTTP logs:** `/`, `/about/`, `/contact/`, `/assets/site.css`, `/assets/site.js`, `/assets/favicon.svg`, and all six responsive WebP assets returned HTTP 200 (37 observed requests; no 4xx/5xx among them).
- **REA live UI audit:** independently opened Home, About and Contact on desktop (1440px) and mobile (390px), confirming the actual page titles, H1 headings and site navigation. Live screenshots saved in the owner's REA audit folder `/Users/mayuringale/rea-public-ui-audits/kunal-doctor-web-production-up-railway-app/` under audit IDs `2026-11-18T18-20-22-315Z`, `2026-11-18T18-21-06-968Z`, and `2026-11-18T18-21-27-581Z`. Browser output proved page structure and server reachability; **pixel contents of these live Mac screenshots were not directly retrieved into ChatGPT**.
- **ChatGPT unit tests:** `python3 -m unittest discover -s tests -v` ran 9 tests: all passed.
- **ChatGPT offline Playwright:** 9/9 assertions passed across desktop/mobile Home, About, Contact, lazy-image decoding, horizontal-overflow check, mobile menu open/Escape, and form validation/WhatsApp URL generation. Offline rendered screenshots were actually opened and visually reviewed in ChatGPT. Local origin `page.goto` was blocked by the container administrator; these checks used `page.set_content` and inlined local assets.
- **Publication:** deliberately `noindex,nofollow` because OPD days, exact clinic location and final credential/photo permissions still require owner/doctor review. A WhatsApp enquiry URL is not a confirmed appointment.
- **Scope:** no changes to AVENIME/COSMO EDU, no GitHub hosted CI, and no payment API. Railway is usage-metered; sleeping and resource limits reduce usage but do not guarantee zero charges.
