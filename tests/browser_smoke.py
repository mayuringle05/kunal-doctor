"""Bounded local Chromium smoke test. No outside requests or paid services."""
from __future__ import annotations
import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from shutil import which
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'proofs' / 'browser'
OUTPUT.mkdir(parents=True,exist_ok=True)
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

server = ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(ROOT/'dist')))
thread = threading.Thread(target=server.serve_forever,daemon=True);thread.start()
origin = f'http://127.0.0.1:{server.server_address[1]}'
results = {'base_url':origin,'checks':[],'failures':[],'screenshots':[]}
try:
  with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path=(which('chromium') or which('google-chrome')),headless=True,args=['--no-sandbox','--disable-dev-shm-usage']) if (which('chromium') or which('google-chrome')) else pw.chromium.launch(headless=True)
    for label,width,height in [('desktop',1440,900),('mobile',390,844)]:
      ctx=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,reduced_motion='reduce')
      ctx.route('https://**/*',lambda route:route.abort())
      page=ctx.new_page()
      console_errors=[]
      page.on('pageerror',lambda error:console_errors.append(str(error)))
      for path in ['/','/about/','/contact/'] + [f'/care/{x}/' for x in ['laparoscopic','gi','hernia','sils','proctology','general']]:
        response=page.goto(origin+path,wait_until='load',timeout=15000)
        page.wait_for_timeout(250)
        name = 'home' if path=='/' else path.strip('/')
        screenshot=OUTPUT/f'{label}-{name}.png'
        page.screenshot(path=str(screenshot),full_page=True,animations='disabled')
        results['screenshots'].append(str(screenshot))
        metrics=page.evaluate('''() => ({scrollWidth:document.documentElement.scrollWidth,innerWidth:window.innerWidth,height:document.documentElement.scrollHeight, h1:document.querySelectorAll('h1').length, font: getComputedStyle(document.querySelector('h1')).fontFamily})''')
        ok=(response.status==200 and metrics['scrollWidth']<=width and metrics['h1']==1)
        results['checks'].append({'viewport':label,'page':path,'http':response.status,'metrics':metrics,'pass':ok})
        if not ok:results['failures'].append({'viewport':label,'page':path,'metrics':metrics})
      if label=='mobile':
        page.goto(origin+'/',wait_until='load');page.locator('.menu-toggle').click()
        menu_open=page.locator('#mobile-nav').is_visible() and page.locator('.menu-toggle').get_attribute('aria-expanded')=='true'
        page.keyboard.press('Escape')
        menu_closed=not page.locator('#mobile-nav').is_visible()
        results['checks'].append({'test':'mobile nav open/esc','pass':menu_open and menu_closed})
        if not menu_open or not menu_closed:results['failures'].append('Mobile menu state')
      page.goto(origin+'/contact/',wait_until='load')
      page.locator('#appointment-form button').click()
      invalid='Please enter your name' in page.locator('#form-status').inner_text()
      page.locator('#patient-name').fill('Test Person')
      page.locator('#patient-phone').fill('9988776655')
      page.locator('#patient-concern').fill('Hernia consultation')
      page.evaluate("window.open = (url) => { window.__appointmentUrl = url; return { closed:false }; }")
      page.locator('#appointment-form button').click()
      url=page.evaluate('window.__appointmentUrl')
      valid=bool(url and 'wa.me/918793529690' in url and 'Test%20Person' in url and 'Hernia%20consultation' in url)
      results['checks'].append({'test':'form validation + WhatsApp URL', 'viewport':label,'pass':invalid and valid})
      if not invalid or not valid:results['failures'].append({'test':'form', 'viewport':label,'url':url,'invalid':invalid})
      if console_errors:results['failures'].append({'test':'console', 'viewport':label,'errors':console_errors})
      ctx.close()
    browser.close()
finally:
  server.shutdown();server.server_close()
(OUTPUT/'smoke-results.json').write_text(json.dumps(results,indent=2))
for r in results['checks']:
  print(('PASS' if r.get('pass') else 'FAIL'),r.get('viewport', ''),r.get('page',r.get('test','')),r.get('http',''),r.get('metrics',{}).get('scrollWidth',''))
print('Failures:',len(results['failures']))
if results['failures']:
  print(json.dumps(results['failures'],indent=2));raise SystemExit(1)
