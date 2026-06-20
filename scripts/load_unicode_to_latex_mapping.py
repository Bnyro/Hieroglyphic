#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import yaml
import os


scripts_folder = os.path.dirname(os.path.abspath(__file__))
unicode_to_latex = os.path.join(scripts_folder, "../unicode_to_latex.yaml")

resp = requests.get("https://www.w3.org/Math/characters/unicode.xml")
if not resp.ok:
    resp.raise_for_status()

parsed_xml = BeautifulSoup(resp.text, features=["xml"])


symbols = {}
for character_el in parsed_xml.select("character"):
    unicode_symbol = character_el.attrs.get("id")
    latex_cmd = character_el.select_one("latex")
    if not unicode_symbol or not latex_cmd:
        continue

    symbols[unicode_symbol[:6]] = latex_cmd.text.strip()

with open(unicode_to_latex, 'w') as outfile:
    yaml.dump(symbols, outfile, default_flow_style=False, encoding="utf-8")
