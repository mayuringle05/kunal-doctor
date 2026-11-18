import json
import os
import re
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
DATA = json.loads((ROOT / 'content/doctor.json').read_text(encoding='utf-8'))

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1=0; self.title=0; self.ids=set(); self.links=[]; self.images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='h1':self.h1+=1
        if tag=='title':self.title+=1
        if 'id' in a:self.ids.add(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='img':self.images.append(a)

class DoctorSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env=os.environ.copy();env.pop('SITE_PUBLIC',None);env.pop('SITE_URL',None)
        subprocess.run([sys.executable,'build.py'], cwd=ROOT,env=env,check=True,capture_output=True,text=True)

    def test_source_all_resume_and_card_sections_captured(self):
        md=(ROOT/'content/DOCTOR_PROFILE.md').read_text()
        for phrase in ['डॉ. कुणाल कुंभरे','FIAGES','FNB completion confirmed','Maharashtra Medical Council','July 2024','October 2023','December 2021','Single Incision Laparoscopic Cholecystectomy','ACSCON 2021','Johnson & Johnson','FALS','7.00 PM to 10.00 PM','Hernia Surgery','Robotic Surgery']:
            self.assertIn(phrase,md)

    def test_user_generated_content_is_escaped(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('doctor_build', ROOT / 'build.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.e('<script>"&'), '&lt;script&gt;&quot;&amp;')

    def test_data_contact_matches_resume(self):
        self.assertEqual(DATA['phone_e164'],'+918793529690')
        self.assertEqual(DATA['email'],'krunalkumbhre010@gmail.com')
        self.assertEqual(DATA['name_marathi'],'डॉ. कुणाल कुंभरे')
        self.assertEqual(len(DATA['experience']),3)
        self.assertEqual(len(DATA['education']),3)

    def test_three_complete_indexable_structure_pages(self):
        for rel in ['index.html','about/index.html','contact/index.html']:
            page=(DIST/rel).read_text(encoding='utf-8')
            parser=Tags();parser.feed(page)
            with self.subTest(rel=rel):
                self.assertEqual(parser.h1,1)
                self.assertEqual(parser.title,1)
                self.assertIn('content="noindex,nofollow"',page)
                self.assertIn(DATA['name'],page)
                self.assertTrue(any('contact/index.html' in href for href in parser.links))
                self.assertIn('application/ld+json',page)

    def test_completed_fellowship_and_plain_language(self):
        home=(DIST/'index.html').read_text(encoding='utf-8')
        about=(DIST/'about/index.html').read_text(encoding='utf-8')
        for bad in ['18 yrs','610 reviews','42 papers','Johns Hopkins','Dr. Amara','5.0 rated',
                    'FNB Fellow ·', 'ongoing in résumé', 'Present (as stated in résumé)',
                    'Modern surgical care, built on', 'Thoughtful care.',
                    'a commitment to care.', 'We\'re here to hear from you.',
                    'The supplied résumé']:
            with self.subTest(bad=bad):
                self.assertNotIn(bad, home+about)
        self.assertIn('training and operating-room exposure',home)
        self.assertIn('Completed FNB Fellowship', about)
        self.assertIn('FIAGES', home)
        self.assertIn('FIAGES', about)
        self.assertIn('FNB (Minimal Access Surgery)', home)
        self.assertIsNone(re.search(r'\bFNB Fellow\b(?!ship)', home + about))
        self.assertIn('completed', DATA['experience'][0]['dates'].lower())
        self.assertIn('Completed FNB Fellowship', DATA['education'][0]['degree'])

    def test_contact_is_nonpersistent_whatsapp_handoff(self):
        form=(DIST/'contact/index.html').read_text(encoding='utf-8')
        js=(DIST/'assets/site.js').read_text(encoding='utf-8')
        self.assertIn('id="appointment-form"',form)
        self.assertIn('does not store the form',form)
        self.assertIn('data-whatsapp-number="918793529690"',form)
        self.assertIn("'https://wa.me/' + whatsappNumber",js)
        self.assertIn('encodeURIComponent(message)',js)
        self.assertNotIn('fetch(',js)
        self.assertNotIn('localStorage',js)

    def test_preview_robots_disallow(self):
        self.assertEqual((DIST/'robots.txt').read_text(),'User-agent: *\nDisallow: /\n')
        self.assertFalse((DIST/'sitemap.xml').exists())

    def test_supplied_doctor_photos_match_page_context(self):
        home=(DIST/'index.html').read_text(encoding='utf-8')
        about=(DIST/'about/index.html').read_text(encoding='utf-8')
        contact=(DIST/'contact/index.html').read_text(encoding='utf-8')
        for location, filename, alt in [
            (home, 'portrait-corridor', 'Dr. Krunal Kumbhare'),
            (home, 'doctor-notebook', 'notebook'),
            (home, 'doctor-consultation', 'patient'),
            (about, 'doctor-notebook', 'notebook'),
            (contact, 'doctor-consultation', 'patient'),
        ]:
            with self.subTest(image=filename):
                self.assertIn(filename+'-960.webp', location)
                self.assertIn(alt, location)
        self.assertNotIn('Professional portrait placeholder',home)
        self.assertNotIn('Doctor\'s approved photograph required',home)
        for rel in ['index.html','about/index.html','contact/index.html']:
            page_path=DIST/rel
            parser=Tags();parser.feed(page_path.read_text(encoding='utf-8'))
            for a in parser.images:
                with self.subTest(page=rel,src=a.get('src','')):
                    self.assertTrue(a.get('alt'))
                    self.assertTrue(a.get('width') and a.get('height'))
                    image_path=(page_path.parent/a['src']).resolve()
                    self.assertTrue(image_path.is_file(),image_path)
                    self.assertTrue(image_path.read_bytes()[:4]==b'RIFF')
                    self.assertLess(image_path.stat().st_size,300_000)

    def test_internal_links_exist(self):
        for rel in ['index.html','about/index.html','contact/index.html']:
            page_path=DIST/rel
            parser=Tags();parser.feed(page_path.read_text())
            for url in parser.links:
                if not url or url.startswith(('#','tel:','mailto:','https://','http://')):continue
                path_no_hash=url.split('#',1)[0]
                if not path_no_hash:continue
                resolved=(page_path.parent/path_no_hash).resolve()
                with self.subTest(page=rel,link=url):
                    self.assertTrue(resolved.is_file() or (resolved.is_dir() and (resolved/'index.html').exists()),f'Broken link {url} in {rel}')

if __name__=='__main__':unittest.main()
