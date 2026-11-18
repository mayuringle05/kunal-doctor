#!/usr/bin/env python3
"""Dependency-free static site generator from content/doctor.json.

Drafts are noindex by default. Only verified publication should set SITE_PUBLIC=1.
"""
from __future__ import annotations
import html
import json
import os
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'content/doctor.json').read_text(encoding='utf-8'))
DIST = ROOT / 'dist'
PUBLIC = os.environ.get('SITE_PUBLIC') == '1'
SITE_URL = os.environ.get('SITE_URL', '').strip().rstrip('/')


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def icon(name: str, size=20) -> str:
    shapes = {
        'arrow': '<path d="M4 12h15m-6-6 6 6-6 6"/>',
        'arrow-up': '<path d="M6 18 18 6M8 6h10v10"/>',
        'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l4 2"/>',
        'phone': '<path d="M22 16.5v3a2.5 2.5 0 0 1-2.7 2.5A19.5 19.5 0 0 1 2 4.7 2.5 2.5 0 0 1 4.5 2h3a2 2 0 0 1 2 1.7l.6 3a2 2 0 0 1-.6 1.8L8 10a16 16 0 0 0 6 6l1.5-1.5a2 2 0 0 1 1.8-.6l3 .6a2 2 0 0 1 1.7 2Z"/>',
        'mail': '<rect x="2" y="4" width="20" height="16" rx="3"/><path d="m3 6 9 7 9-7"/>',
        'pin': '<path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
        'check': '<path d="m4 12 5 5L20 6"/>',
        'scope': '<path d="M7 2v6a5 5 0 0 0 10 0V2M5 2h4m6 0h4M12 13v3a5 5 0 0 0 10 0v-2"/><circle cx="22" cy="12" r="1.5"/>',
        'stomach': '<path d="M15 2v5c0 1 1 2 2 2 3 0 5 3 5 6s-2 7-8 7c-7 0-11-3-11-8 0-3 1-4 4-4 2 0 3 1 3 3h3V2"/>',
        'layers': '<path d="m12 2 9 5-9 5-9-5 9-5Zm-9 10 9 5 9-5M3 17l9 5 9-5"/>',
        'target': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
        'spark': '<path d="m12 2 1.5 7.5L21 11l-7.5 1.5L12 20l-1.5-7.5L3 11l7.5-1.5L12 2ZM19 17l.5 2.5L22 20l-2.5.5L19 23l-.5-2.5L16 20l2.5-.5L19 17Z"/>',
        'robot': '<rect x="4" y="7" width="16" height="13" rx="3"/><path d="M12 7V3m-3 0h6M8 13h1m6 0h1m-7 4h6"/>',
        'shield': '<path d="m12 2 9 4v6c0 6-4 9-9 11-5-2-9-5-9-11V6l9-4Z"/><path d="m8 12 3 3 5-6"/>',
        'menu': '<path d="M3 6h18M3 12h18M3 18h18"/>',
        'close': '<path d="M5 5 19 19M19 5 5 19"/>',
        'heart': '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l8.9 8.7 8.8-8.7a5.5 5.5 0 0 0 0-7.8Z"/>',
        'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 2v6m10-6v6M3 10h18"/>',
        'book': '<path d="M12 7a7 7 0 0 0-9-1v14a7 7 0 0 1 9 1 7 7 0 0 1 9-1V6a7 7 0 0 0-9 1Zm0 0v14"/>',
    }
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{shapes.get(name, shapes["arrow"])}</svg>'


def button(text, href, light=False, external=False, extra=''):
    cls = 'button button--light' if light else 'button button--primary'
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a class="{cls} {extra}" href="{e(href)}"{attrs}>{e(text)} <span class="button__icon">{icon("arrow-up", 17)}</span></a>'


def logo(prefix):
    name_tokens = DATA['name'].rsplit(' ', 1)
    primary = name_tokens[0]
    last = name_tokens[1] if len(name_tokens) == 2 else ''
    return f'<a class="wordmark" href="{prefix}index.html" aria-label="{e(DATA["name"])} home"><span class="wordmark__symbol" aria-hidden="true">{e(DATA["initials"][0])}<span>+</span></span><span class="wordmark__text">{e(primary)} <strong>{e(last)}</strong><small>{e(DATA["brand_subtitle"])}</small></span></a>'


def header(prefix, active):
    nav = ''.join(f'<a href="{prefix}{path}" class="nav__link{" is-active" if name == active else ""}"{" aria-current=\"page\"" if name == active else ""}>{name}</a>' for name, path in [('Home','index.html'),('About','about/index.html'),('Contact','contact/index.html')])
    return f'''<header class="site-header" id="top"><div class="shell nav-wrap">{logo(prefix)}<nav class="desktop-nav" aria-label="Main navigation">{nav}</nav><a class="header-cta" href="{prefix}contact/index.html">Request an appointment <span>{icon('arrow-up',17)}</span></a><button class="menu-toggle" aria-label="Open menu" aria-controls="mobile-nav" aria-expanded="false" type="button">{icon('menu',25)}</button></div><nav class="mobile-nav" id="mobile-nav" aria-label="Mobile navigation" hidden>{nav}<a class="mobile-nav__cta" href="{prefix}contact/index.html">Request an appointment {icon('arrow-up',16)}</a></nav></header>'''


def footer(prefix):
    return f'''<footer class="site-footer"><div class="shell"><div class="footer-top"><div class="footer-brand">{logo(prefix)}<p>General, GI and laparoscopic surgery in Nagpur. FNB in Minimal Access Surgery completed at FMRI, Gurugram.</p><span class="footer-registration">{icon('shield',16)} {e(DATA['registration'])}</span></div><div class="footer-col"><h3>Explore</h3><a href="{prefix}index.html">Home</a><a href="{prefix}about/index.html">About the doctor</a><a href="{prefix}index.html#specialties">Areas of care</a><a href="{prefix}contact/index.html">Appointments</a></div><div class="footer-col"><h3>Get in touch</h3><a href="tel:{e(DATA['phone_e164'])}">{e(DATA['phone_display'])}</a><a href="mailto:{e(DATA['email'])}">{e(DATA['email'])}</a><p>{e(DATA['city'])}, {e(DATA['state'])}, {e(DATA['country'])}</p></div></div><div class="footer-bottom"><p>© 2026 {e(DATA['name'])}. All rights reserved.</p><p>For medical emergencies, seek immediate emergency medical care. Website content is informational, not individual medical advice.</p></div></div></footer>'''


def layout(title, description, body, prefix, active, path):
    canonical = f'<link rel="canonical" href="{e(SITE_URL + path)}">' if SITE_URL else ''
    robots = 'index,follow' if PUBLIC else 'noindex,nofollow'
    person = {'@context':'https://schema.org','@type':'Physician','name':DATA['name'],'description':DATA['tagline'],'telephone':DATA['phone_e164'],'email':DATA['email'],'address':{'@type':'PostalAddress','addressLocality':DATA['city'],'addressRegion':DATA['state'],'addressCountry':'IN'}}
    if SITE_URL: person['url'] = SITE_URL + '/'
    ld = json.dumps(person,ensure_ascii=False).replace('<','\\u003c')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="theme-color" content="#1b1876"><meta name="robots" content="{robots}"><meta name="description" content="{e(description)}"><meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:locale" content="en_IN"><title>{e(title)}</title>{canonical}<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}assets/site.css"><script type="application/ld+json">{ld}</script><script defer src="{prefix}assets/site.js"></script></head><body>{header(prefix,active)}<main id="main">{body}</main>{footer(prefix)}</body></html>'''


def doctor_photo(slug: str, alt: str, prefix: str = '', class_name: str = '', eager: bool = False) -> str:
    # Optimized, user-supplied portraits. Local assets; no external hosting or tracking.
    base = f'{prefix}assets/photos/{slug}'
    performance = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{e(class_name)}" src="{base}-960.webp" '
            f'srcset="{base}-480.webp 480w, {base}-960.webp 960w" '
            f'sizes="(max-width:800px) 100vw, 46vw" '
            f'width="1122" height="1402" alt="{e(alt)}" '
            f'decoding="async" {performance}>')


def card(area):
    return f'''<article class="care-card" id="care-{e(area['id'])}"><div class="care-card__upper"><div class="care-icon">{icon(area['icon'],28)}</div><span class="care-card__number">{e(area['index'])} / 06</span></div><div><span class="eyebrow care-card__eyebrow">{e(area['eyebrow'])}</span><h3>{e(area['title'])}</h3><p>{e(area['description'])}</p></div><a class="care-card__link" href="contact/index.html" aria-label="Enquire about {e(area['title'])}">{icon('arrow-up',18)}</a></article>'''


def home():
    phone = f'tel:{DATA["phone_e164"]}'
    wa = 'https://wa.me/' + DATA['phone_e164'].lstrip('+') + '?text=' + quote('Hello Dr. Kumbhare, I would like to enquire about an OPD appointment.')
    cards = ''.join(card(a) for a in DATA['care_areas'])
    education = ''.join(f'<div class="education-row"><div><span class="eyebrow">{e(item["year"])}</span><h3>{e(item["degree"])}</h3><p>{e(item["institution"])}</p></div><span class="education-row__mark">{icon("arrow-up",18)}</span></div>' for item in DATA['education'])
    return f'''<section class="hero"><div class="shell hero-grid"><div class="hero-content"><div class="pill"><span class="status-dot"></span> {e(DATA['tagline'].upper())} <span class="pill__sep">·</span> {e(DATA['city'].upper())}</div><div class="hero-name">{e(DATA['name'])} <span>·</span> <span lang="mr">{e(DATA['name_marathi'])}</span></div><h1>General surgery and <em>minimal access</em> care in Nagpur.</h1><p class="hero-lead">{e(DATA['hero_description'])}</p><div class="hero-actions">{button('Request an appointment','contact/index.html') }<a class="text-link" href="about/index.html">Meet {e(DATA['short_name'])} {icon('arrow',18)}</a></div><div class="hero-facts"><div><span class="facts__label">Qualifications</span><strong>{e(DATA["qualifications"])}</strong></div><div><span class="facts__label">Fellowship & credential</span><strong>{e(DATA["fellowship"])}</strong></div></div></div><div class="hero-art hero-art--photo">{doctor_photo('portrait-corridor','Dr. Krunal Kumbhare wearing a white coat in a clinic.',class_name='hero-art__photo',eager=True)}<div class="hero-art__corner hero-art__corner--photo">SURGERY <span>•</span> {e(DATA['city'].upper())}</div><div class="hero-profile"><div class="hero-profile__icon">{icon('shield',24)}</div><div><strong>{e(DATA['name'])}</strong><span>{e(DATA['tagline'])}</span></div><span class="hero-profile__arrow">{icon('arrow-up',18)}</span></div></div></div><div class="shell hero-mini-strip"><div class="mini-strip-item">{icon('shield',20)} Maharashtra Medical Council registered</div><span class="strip-divider"></span><div class="mini-strip-item">{icon('clock',20)} Evening OPD: {e(DATA['opd_time'])}</div><span class="strip-divider"></span><div class="mini-strip-item">{icon('pin',20)} {e(DATA['city'])}, {e(DATA['state'])}</div></div></section>
<section class="approach-section"><div class="shell approach-shell"><div class="section-label"><span class="label-line"></span> MY APPROACH</div><h2>The right procedure <em>depends on the diagnosis.</em></h2><p>A surgical assessment starts with the condition, medical history and examination. The choice of an open or minimally invasive procedure depends on those findings.</p><div class="approach-bottom"><span class="mini-signature">{e(DATA['name'])} <small>MS (General Surgery) · FNB (Minimal Access Surgery)</small></span><div class="approach-badge">{icon('heart',22)} FNB fellowship completed at FMRI</div></div></div></section>
<section class="section section--light" id="specialties"><div class="shell"><div class="section-heading"><div><div class="section-label"><span class="label-line"></span> AREAS OF CARE</div><h2>Areas of <em>surgical practice.</em></h2></div><p>Dr. Kumbhare’s work and training cover GI, hernia, laparoscopic and single-incision procedures, along with laser proctology and robotic operating-room techniques.</p></div><div class="care-grid">{cards}</div><p class="section-fineprint">Robotic surgery information describes documented training and operating-room exposure. Ask the clinic which procedures are currently offered.</p></div></section>
<section class="stats-band"><div class="shell stats-grid"><div class="stat"><strong>5<span>+</span></strong><p>Years of experience in elective, emergency and trauma surgery</p></div><div class="stat"><strong>02</strong><p>Senior residency posts in Pune and Nagpur</p></div><div class="stat"><strong>7–10 <small>PM</small></strong><p>Evening OPD hours. Confirm days before visiting</p></div></div></section>
<section class="section about-preview"><div class="shell about-preview-grid"><figure class="about-preview__graphic about-preview__graphic--photo">{doctor_photo('doctor-notebook','Dr. Krunal Kumbhare writing in a notebook at a clinic.',class_name='about-preview__photo')}<figcaption class="about-preview__caption"><span>{e(DATA['name'])}</span><strong>General &amp; laparoscopic surgery</strong></figcaption></figure><div class="about-preview__copy"><div class="section-label"><span class="label-line"></span> MEET YOUR SURGEON</div><h2>Surgical roles in <em>Nagpur, Pune and Gurugram.</em></h2><p>{e(DATA['about_short'])}</p><p>{e(DATA['about_long'])}</p><div class="training-card"><span class="training-card__icon">{icon('book',22)}</span><div><strong>Completed FNB fellowship</strong><span>Fortis Memorial Research Institute, Gurugram</span></div></div>{button('More about ' + DATA['short_name'],'about/index.html')}</div></div></section>
<section class="section section--light"><div class="shell"><div class="section-heading section-heading--tight"><div><div class="section-label"><span class="label-line"></span> MEDICAL EDUCATION</div><h2>Medical education <em>and fellowship.</em></h2></div><a class="text-link" href="about/index.html#experience">View full experience {icon('arrow',18)}</a></div><div class="education-list">{education}</div></div></section>
<section class="section journey-section"><div class="shell"><div class="section-heading"><div><div class="section-label"><span class="label-line"></span> YOUR FIRST VISIT</div><h2>Planning your <em>first consultation.</em></h2></div><p>The evening OPD hours are 7:00 PM to 10:00 PM. Confirm the consulting day and clinic address before leaving home.</p></div><div class="journey-layout"><figure class="journey-photo">{doctor_photo('doctor-consultation','Dr. Krunal Kumbhare speaking with a patient during a clinic consultation.',class_name='journey-photo__image')}<figcaption>Consultation with Dr. Kumbhare</figcaption></figure><div class="journey-grid"><div class="journey-card"><span>01 / GET IN TOUCH</span>{icon('phone',28)}<h3>Call or message the clinic</h3><p>Use the contact number below to ask for an OPD slot.</p></div><div class="journey-card"><span>02 / CONFIRM</span>{icon('calendar',28)}<h3>Confirm the clinic details</h3><p>Ask for the OPD day, location and available appointment time.</p></div><div class="journey-card"><span>03 / CONSULT</span>{icon('heart',28)}<h3>Bring your medical records</h3><p>Bring relevant prescriptions, scans and test results to your consultation.</p></div></div></div></div></section>
<section class="contact-banner"><div class="shell banner-grid"><div><div class="section-label section-label--white"><span class="label-line"></span> GET IN TOUCH</div><h2>Arrange a <em>surgical consultation.</em></h2><p>Call or send a WhatsApp enquiry using the listed number. The clinic must confirm the appointment.</p><div class="banner-actions">{button('Request an appointment','contact/index.html',True)}<a href="{e(phone)}" class="banner-phone">{icon('phone',19)} {e(DATA['phone_display'])}</a></div></div><div class="banner-card"><span>EVENING OPD</span><strong>{e(DATA['opd_time'])}</strong><p>Please confirm OPD days and clinic address by phone.</p><a href="{e(wa)}" target="_blank" rel="noopener noreferrer">Enquire on WhatsApp {icon('arrow-up',17)}</a></div></div></section>'''


def experience_item(item, idx):
    points = ''.join(f'<li>{e(p)}</li>' for p in item['highlights'])
    return f'''<article class="timeline-item"><span class="timeline-index">0{idx}</span><div class="timeline-content"><span class="eyebrow">{e(item['dates'])}</span><h3>{e(item['role'])}</h3><p class="timeline-place">{e(item['institution'])}</p><ul>{points}</ul></div></article>'''


def about():
    education = ''.join(f'<article class="detail-education"><span>{e(item["year"])}</span><div><h3>{e(item["degree"])}</h3><p>{e(item["institution"])}</p></div></article>' for item in DATA['education'])
    roles = ''.join(experience_item(item,i) for i,item in enumerate(DATA['experience'],1))
    affiliations = ''.join(f'<li>{icon("check",17)} {e(item)}</li>' for item in DATA['certifications_affiliations'])
    return f'''<section class="inner-hero"><div class="shell inner-hero-grid"><div><div class="pill"><span class="status-dot"></span> ABOUT {e(DATA['short_name'].upper())}</div><h1>General surgery, <em>followed by a completed FNB fellowship.</em></h1><p>{e(DATA['about_short'])}</p></div><figure class="inner-hero-photo">{doctor_photo('doctor-notebook','Dr. Krunal Kumbhare writing in a notebook at a clinic.',prefix='../',class_name='inner-hero-photo__image')}<figcaption>{e(DATA['name'])} <span>{e(DATA['qualifications'])} · {e(DATA['fellowship'])}</span></figcaption></figure></div></section>
<section class="section"><div class="shell about-story-grid"><div class="section-label"><span class="label-line"></span> PROFESSIONAL PROFILE</div><div><h2>Surgical work in <em>Nagpur, Pune and Gurugram.</em></h2><p>{e(DATA['about_long'])}</p><p>During his senior residency appointments, he managed elective and emergency patients, worked in the ICU and operating theatre, and supervised junior doctors.</p><div class="story-note">{icon('shield',22)} <span>Registered with the Maharashtra Medical Council.</span></div></div></div></section>
<section class="section section--light" id="experience"><div class="shell"><div class="section-heading"><div><div class="section-label"><span class="label-line"></span> CAREER JOURNEY</div><h2>Professional <em>experience.</em></h2></div><p>Fellowship completed at Fortis Memorial Research Institute, Gurugram. Previous senior residency roles were in Pune and Nagpur.</p></div><div class="timeline">{roles}</div></div></section>
<section class="section"><div class="shell detail-split"><div><div class="section-label"><span class="label-line"></span> ACADEMIC BACKGROUND</div><h2>Education & <em>qualifications.</em></h2><div class="detail-education-list">{education}</div></div><aside class="accreditation-card"><div class="accreditation-icon">{icon('book',31)}</div><span>RESEARCH & PRESENTATION</span><h3>Single Incision Laparoscopic Cholecystectomy</h3><p>Presented at a surgical academic forum and received a certificate of recognition.</p><div class="accreditation-rule"></div><h4>Training, events & affiliations</h4><ul>{affiliations}</ul></aside></div></section>
<section class="contact-banner"><div class="shell banner-grid"><div><div class="section-label section-label--white"><span class="label-line"></span> APPOINTMENTS</div><h2>To book an <em>OPD consultation.</em></h2><p>Call the listed number or send a WhatsApp message to enquire about availability.</p>{button('Get in touch','../contact/index.html',True)}</div><div class="banner-card"><span>CONTACT</span><strong class="banner-contact-name">{e(DATA['phone_display'])}</strong><p>Evening OPD: {e(DATA['opd_time'])}. Please confirm the OPD day and address before visiting.</p><a href="mailto:{e(DATA['email'])}">Send an email {icon('arrow-up',17)}</a></div></div></section>'''


def contact():
    return f'''<section class="inner-hero inner-hero--contact"><div class="shell"><div class="pill"><span class="status-dot"></span> CONTACT & APPOINTMENTS</div><h1>Book an <em>OPD consultation.</em></h1><p>Call or send a WhatsApp message to ask about an appointment with {e(DATA['short_name'])}. The clinic will confirm availability.</p></div></section>
<section class="section contact-section"><div class="shell contact-grid"><div class="contact-info"><div class="section-label"><span class="label-line"></span> DIRECT CONTACT</div><h2>Contact <em>the clinic.</em></h2><p>Evening OPD: {e(DATA['opd_time'])}. Please confirm the day and clinic address before travelling.</p><a class="contact-line" href="tel:{e(DATA['phone_e164'])}"><span>{icon('phone',23)}</span><div><small>CALL FOR APPOINTMENTS</small><strong>{e(DATA['phone_display'])}</strong></div>{icon('arrow-up',19)}</a><a class="contact-line" href="mailto:{e(DATA['email'])}"><span>{icon('mail',23)}</span><div><small>EMAIL</small><strong>{e(DATA['email'])}</strong></div>{icon('arrow-up',19)}</a><div class="contact-line contact-line--static"><span>{icon('clock',23)}</span><div><small>EVENING OPD</small><strong>{e(DATA['opd_time'])}</strong><em>Days to be confirmed by phone</em></div></div><div class="contact-line contact-line--static"><span>{icon('pin',23)}</span><div><small>LOCATION</small><strong>{e(DATA['city'])}, {e(DATA['state'])}</strong><em>Full address not yet supplied</em></div></div><figure class="contact-photo">{doctor_photo('doctor-consultation','Dr. Krunal Kumbhare speaking with a patient during a clinic consultation.',prefix='../',class_name='contact-photo__image')}<figcaption>Consultation enquiries by phone or WhatsApp</figcaption></figure></div><div class="form-panel"><div class="form-panel__heading"><span class="eyebrow">FOR PATIENTS</span><h2>Request an appointment</h2><p>Enter your contact details to prepare an appointment request in WhatsApp. This site does not store the form or confirm a booking.</p></div><form id="appointment-form" data-whatsapp-number="{e(DATA['phone_e164'].lstrip('+'))}" data-doctor-name="{e(DATA['short_name'])}" novalidate><div class="field"><label for="patient-name">Your name <span aria-hidden="true">*</span></label><input id="patient-name" name="patientName" type="text" autocomplete="name" placeholder="Enter your full name" maxlength="100" required></div><div class="field"><label for="patient-phone">Mobile number <span aria-hidden="true">*</span></label><input id="patient-phone" name="patientPhone" type="tel" autocomplete="tel" inputmode="tel" placeholder="Your contact number" maxlength="20" required></div><div class="field"><label for="visit-type">Appointment category</label><select id="visit-type" name="visitType"><option value="General surgery consultation">General surgery consultation</option><option value="GI surgery enquiry">GI surgery enquiry</option><option value="Hernia surgery enquiry">Hernia surgery enquiry</option><option value="Laparoscopic surgery enquiry">Laparoscopic surgery enquiry</option><option value="Other consultation">Other consultation</option></select></div><p class="form-notice">Do not include private medical records, diagnosis details or emergency requests in this form. WhatsApp is a third-party messaging service.</p><button type="submit" class="button button--primary form-submit">Continue on WhatsApp <span class="button__icon">{icon('arrow-up',17)}</span></button><div id="form-status" class="form-status" role="status" aria-live="polite"></div></form></div></div></section>
<section class="small-disclaimer"><div class="shell">{icon('shield',19)} This site is informational. For a medical emergency, go to the nearest emergency department or call your local emergency number. This website does not provide emergency advice or online diagnosis.</div></section>'''


def build():
    for page, body, title, desc, prefix, path in [
        ('index.html',home(),f"{DATA['name']} | Consultant Laparoscopic Surgeon, Nagpur",'Dr. Krunal Kumbhare, consultant laparoscopic surgeon in Nagpur. Completed FNB in Minimal Access Surgery at FMRI, Gurugram. GI, hernia and laparoscopic surgery.','', '/'),
        ('about/index.html',about(),f"About {DATA['name']} | Qualifications & Experience",'Dr. Krunal Kumbhare: MBBS, MS (General Surgery), completed FNB (Minimal Access Surgery) and FIAGES. Surgical experience in Nagpur, Pune and Gurugram.','../','/about/'),
        ('contact/index.html',contact(),f"Appointments & Contact | {DATA['name']}",'Contact Dr. Krunal Kumbhare for a surgical consultation enquiry in Nagpur. Evening OPD listed from 7 PM to 10 PM; confirm day and location.','../','/contact/'),
    ]:
        destination = DIST / page
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(layout(title,desc,body,prefix, 'Home' if page=='index.html' else 'About' if page.startswith('about/') else 'Contact',path),encoding='utf-8')
    from shutil import copytree
    copytree(ROOT / 'assets',DIST / 'assets',dirs_exist_ok=True)
    (DIST/'robots.txt').write_text('User-agent: *\n' + ('Allow: /\n' if PUBLIC else 'Disallow: /\n'),encoding='utf-8')
    if SITE_URL and PUBLIC:
        import datetime
        today = datetime.date.today().isoformat()
        urls=''.join(f'<url><loc>{e(SITE_URL+path)}</loc><lastmod>{today}</lastmod></url>' for path in ['/','/about/','/contact/'])
        (DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls+'</urlset>',encoding='utf-8')
    else:
        (DIST/'sitemap.xml').unlink(missing_ok=True)
    print(f'Built 3 pages into {DIST} (PUBLIC={PUBLIC}, SITE_URL={SITE_URL or "unset"})')

if __name__ == '__main__': build()
