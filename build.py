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
  