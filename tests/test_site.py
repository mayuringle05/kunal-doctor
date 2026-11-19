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
        self.assertEqual(DATA['name_marathi'],'डॉ.