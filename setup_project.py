#!/usr/bin/env python3
import os
import urllib.request
import json
import ssl
import time
import random

DEPT_WIKI_FILES = {
    "01": "Blason département fr Ain.svg", "02": "Blason département fr Aisne.svg",
    "03": "Blason département fr Allier.svg", "04": "Blason département fr Alpes-de-Haute-Provence.svg",
    "05": "Blason département fr Hautes-Alpes.svg", "06": "Blason département fr Alpes-Maritimes.svg",
    "07": "Blason département fr Ardèche.svg", "08": "Blason département fr Ardennes.svg",
    "09": "Blason département fr Ariège.svg", "10": "Blason département fr Aube.svg",
    "11": "Blason département fr Aude.svg", "12": "Blason département fr Aveyron.svg",
    "13": "Blason département fr Bouches-du-Rhône.svg", "14": "Blason département fr Calvados.svg",
    "15": "Blason département fr Cantal.svg", "16": "Blason département fr Charente.svg",
    "17": "Blason département fr Charente-Maritime.svg", "18": "Blason département fr Cher.svg",
    "19": "Blason département fr Corrèze.svg", "2A": "Blason département fr Corse-du-Sud.svg",
    "2B": "Blason département fr Haute-Corse.svg", "21": "Blason département fr Côte-d'Or.svg",
    "22": "Blason département fr Côtes-d'Armor.svg", "23": "Blason département fr Creuse.svg",
    "24": "Blason département fr Dordogne.svg", "25": "Blason département fr Doubs.svg",
    "26": "Blason département fr Drôme.svg", "27": "Blason département fr Eure.svg",
    "28": "Blason département fr Eure-et-Loir.svg", "29": "Blason département fr Finistère.svg",
    "30": "Blason département fr Gard.svg", "31": "Blason département fr Haute-Garonne.svg",
    "32": "Blason département fr Gers.svg", "33": "Blason département fr Gironde.svg",
    "34": "Blason département fr Hérault.svg", "35": "Blason département fr Ille-et-Vilaine.svg",
    "36": "Blason département fr Indre.svg", "37": "Blason département fr Indre-et-Loire.svg",
    "38": "Blason département fr Isère.svg", "39": "Blason département fr Jura.svg",
    "40": "Blason département fr Landes.svg", "41": "Blason département fr Loir-et-Cher.svg",
    "42": "Blason département fr Loire.svg", "43": "Blason département fr Haute-Loire.svg",
    "44": "Blason département fr Loire-Atlantique.svg", "45": "Blason département fr Loiret.svg",
    "46": "Blason département fr Lot.svg", "47": "Blason département fr Lot-et-Garonne.svg",
    "48": "Blason département fr Lozère.svg", "49": "Blason département fr Maine-et-Loire.svg",
    "50": "Blason département fr Manche.svg", "51": "Blason département fr Marne.svg",
    "52": "Blason département fr Haute-Marne.svg", "53": "Blason département fr Mayenne.svg",
    "54": "Blason département fr Meurthe-et-Moselle.svg", "55": "Blason département fr Meuse.svg",
    "56": "Blason département fr Morbihan.svg", "57": "Blason département fr Moselle.svg",
    "58": "Blason département fr Nièvre.svg", "59": "Blason département fr Nord.svg",
    "60": "Blason département fr Oise.svg", "61": "Blason département fr Orne.svg",
    "62": "Blason département fr Pas-de-Calais.svg", "63": "Blason département fr Puy-de-Dôme.svg",
    "64": "Blason département fr Pyrénées-Atlantiques.svg", "65": "Blason département fr Hautes-Pyrénées.svg",
    "66": "Blason département fr Pyrénées-Orientales.svg", "67": "Blason département fr Bas-Rhin.svg",
    "68": "Blason département fr Haut-Rhin.svg", "69": "Blason département fr Rhône.svg",
    "70": "Blason département fr Haute-Saône.svg", "71": "Blason département fr Saône-et-Loire.svg",
    "72": "Blason département fr Sarthe.svg", "73": "Blason département fr Savoie.svg",
    "74": "Blason département fr Haute-Savoie.svg", "75": "Blason ville fr Paris.svg",
    "76": "Blason département fr Seine-Maritime.svg", "77": "Blason département fr Seine-et-Marne.svg",
    "78": "Blason département fr Yvelines.svg", "79": "Blason département fr Deux-Sèvres.svg",
    "80": "Blason département fr Somme.svg", "81": "Blason département fr Tarn.svg",
    "82": "Blason département fr Tarn-et-Garonne.svg", "83": "Blason département fr Var.svg",
    "84": "Blason département fr Vaucluse.svg", "85": "Blason département fr Vendée.svg",
    "86": "Blason département fr Vienne.svg", "87": "Blason département fr Haute-Vienne.svg",
    "88": "Blason département fr Vosges.svg", "89": "Blason département fr Yonne.svg",
    "90": "Blason département fr Territoire de Belfort.svg", "91": "Blason département fr Essonne.svg",
    "92": "Blason département fr Hauts-de-Seine.svg", "93": "Blason département fr Seine-Saint-Denis.svg",
    "94": "Blason département fr Val-de-Marne.svg", "95": "Blason département fr Val-d'Oise.svg",
    "971": "Blason région fr Guadeloupe.svg", "972": "Blason département fr Martinique.svg",
    "973": "Blason département fr Guyane.svg", "974": "Blason région fr La Réunion.svg",
    "976": "Blason département fr Mayotte.svg"
}

def setup_project():
    print("[+] Creating project folder structure...")
    os.makedirs("sticker_factory/symbols", exist_ok=True)
    os.makedirs("sticker_factory/output", exist_ok=True)

    script_path = os.path.join("sticker_factory", "license_plates_sticker.py")
    script_content = '''#!/usr/bin/env python3
import sys
import os
import urllib.request
import urllib.error
import json
import ssl
import time
import random
import xml.etree.ElementTree as ET

SHEET_SIZES = {
    "A4": (210.0, 297.0),
    "A3": (297.0, 420.0),
    "SRA3": (320.0, 450.0),
}

STICKER_WIDTH = 45.0
STICKER_HEIGHT = 98.0
BLEED = 2.0
TOTAL_W = STICKER_WIDTH + (2 * BLEED)
TOTAL_H = STICKER_HEIGHT + (2 * BLEED)
CORNER_RADIUS = 3.0

REFLEX_BLUE = "#0038A8"
CUT_COLOR = "#FF007F"

DEPT_WIKI_FILES = {
    "01": "Blason département fr Ain.svg", "02": "Blason département fr Aisne.svg",
    "03": "Blason département fr Allier.svg", "04": "Blason département fr Alpes-de-Haute-Provence.svg",
    "05": "Blason département fr Hautes-Alpes.svg", "06": "Blason département fr Alpes-Maritimes.svg",
    "07": "Blason département fr Ardèche.svg", "08": "Blason département fr Ardennes.svg",
    "09": "Blason département fr Ariège.svg", "10": "Blason département fr Aube.svg",
    "11": "Blason département fr Aude.svg", "12": "Blason département fr Aveyron.svg",
    "13": "Blason département fr Bouches-du-Rhône.svg", "14": "Blason département fr Calvados.svg",
    "15": "Blason département fr Cantal.svg", "16": "Blason département fr Charente.svg",
    "17": "Blason département fr Charente-Maritime.svg", "18": "Blason département fr Cher.svg",
    "19": "Blason département fr Corrèze.svg", "2A": "Blason département fr Corse-du-Sud.svg",
    "2B": "Blason département fr Haute-Corse.svg", "21": "Blason département fr Côte-d'Or.svg",
    "22": "Blason département fr Côtes-d'Armor.svg", "23": "Blason département fr Creuse.svg",
    "24": "Blason département fr Dordogne.svg", "25": "Blason département fr Doubs.svg",
    "26": "Blason département fr Drôme.svg", "27": "Blason département fr Eure.svg",
    "28": "Blason département fr Eure-et-Loir.svg", "29": "Blason département fr Finistère.svg",
    "30": "Blason département fr Gard.svg", "31": "Blason département fr Haute-Garonne.svg",
    "32": "Blason département fr Gers.svg", "33": "Blason département fr Gironde.svg",
    "34": "Blason département fr Hérault.svg", "35": "Blason département fr Ille-et-Vilaine.svg",
    "36": "Blason département fr Indre.svg", "37": "Blason département fr Indre-et-Loire.svg",
    "38": "Blason département fr Isère.svg", "39": "Blason département fr Jura.svg",
    "40": "Blason département fr Landes.svg", "41": "Blason département fr Loir-et-Cher.svg",
    "42": "Blason département fr Loire.svg", "43": "Blason département fr Haute-Loire.svg",
    "44": "Blason département fr Loire-Atlantique.svg", "45": "Blason département fr Loiret.svg",
    "46": "Blason département fr Lot.svg", "47": "Blason département fr Lot-et-Garonne.svg",
    "48": "Blason département fr Lozère.svg", "49": "Blason département fr Maine-et-Loire.svg",
    "50": "Blason département fr Manche.svg", "51": "Blason département fr Marne.svg",
    "52": "Blason département fr Haute-Marne.svg", "53": "Blason département fr Mayenne.svg",
    "54": "Blason département fr Meurthe-et-Moselle.svg", "55": "Blason département fr Meuse.svg",
    "56": "Blason département fr Morbihan.svg", "57": "Blason département fr Moselle.svg",
    "58": "Blason département fr Nièvre.svg", "59": "Blason département fr Nord.svg",
    "60": "Blason département fr Oise.svg", "61": "Blason département fr Orne.svg",
    "62": "Blason département fr Pas-de-Calais.svg", "63": "Blason département fr Puy-de-Dôme.svg",
    "64": "Blason département fr Pyrénées-Atlantiques.svg", "65": "Blason département fr Hautes-Pyrénées.svg",
    "66": "Blason département fr Pyrénées-Orientales.svg", "67": "Blason département fr Bas-Rhin.svg",
    "68": "Blason département fr Haut-Rhin.svg", "69": "Blason département fr Rhône.svg",
    "70": "Blason département fr Haute-Saône.svg", "71": "Blason département fr Saône-et-Loire.svg",
    "72": "Blason département fr Sarthe.svg", "73": "Blason département fr Savoie.svg",
    "74": "Blason département fr Haute-Savoie.svg", "75": "Blason ville fr Paris.svg",
    "76": "Blason département fr Seine-Maritime.svg", "77": "Blason département fr Seine-et-Marne.svg",
    "78": "Blason département fr Yvelines.svg", "79": "Blason département fr Deux-Sèvres.svg",
    "80": "Blason département fr Somme.svg", "81": "Blason département fr Tarn.svg",
    "82": "Blason département fr Tarn-et-Garonne.svg", "83": "Blason département fr Var.svg",
    "84": "Blason département fr Vaucluse.svg", "85": "Blason département fr Vendée.svg",
    "86": "Blason département fr Vienne.svg", "87": "Blason département fr Haute-Vienne.svg",
    "88": "Blason département fr Vosges.svg", "89": "Blason département fr Yonne.svg",
    "90": "Blason département fr Territoire de Belfort.svg", "91": "Blason département fr Essonne.svg",
    "92": "Blason département fr Hauts-de-Seine.svg", "93": "Blason département fr Seine-Saint-Denis.svg",
    "94": "Blason département fr Val-de-Marne.svg", "95": "Blason département fr Val-d'Oise.svg",
    "971": "Blason région fr Guadeloupe.svg", "972": "Blason département fr Martinique.svg",
    "973": "Blason département fr Guyane.svg", "974": "Blason région fr La Réunion.svg",
    "976": "Blason département fr Mayotte.svg"
}

def print_help():
    print("French License Plate Sticker Imposition Generator")
    print("================================================")
    print("Usage:")
    print("  python license_plates_sticker.py <dept_code> [sheet_format]")
    print("  python license_plates_sticker.py ALL [sheet_format]")
    print("")
    print("Arguments:")
    print("  <dept_code>     Department number (e.g., 38, 75, 2A, 974) or 'ALL'")
    print("  [sheet_format]  Paper size format: A4, A3, or SRA3 (default: A3)")
    print("")
    print("Examples:")
    print("  python license_plates_sticker.py 38 A3")
    print("  python license_plates_sticker.py 75 SRA3")
    print("  python license_plates_sticker.py ALL A3")

def fetch_symbol_if_needed(dept_code):
    sym_path = os.path.join("symbols", f"{dept_code}.svg")
    if os.path.exists(sym_path) and os.path.getsize(sym_path) > 100:
        return sym_path
    
    if dept_code not in DEPT_WIKI_FILES:
        return ""

    print(f"[+] Fetching symbol for {dept_code} from Wikimedia Commons...")
    filename = DEPT_WIKI_FILES[dept_code]
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles=File:{urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&format=json"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(api_url, headers={'User-Agent': 'LicensePlateStickerBot/1.0'})
    
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_info in pages.items():
                if int(page_id) > 0 and "imageinfo" in page_info:
                    img_url = page_info["imageinfo"][0]["url"]
                    img_req = urllib.request.Request(img_url, headers={'User-Agent': 'LicensePlateStickerBot/1.0'})
                    with urllib.request.urlopen(img_req, context=ctx) as img_resp:
                        content = img_resp.read()
                        with open(sym_path, "wb") as f:
                            f.write(content)
                        print(f"[✓] Downloaded symbol for {dept_code}")
                        sleep_time = random.uniform(1.0, 3.0)
                        time.sleep(sleep_time)
                        return sym_path
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"[X] HTTP Error 429: Too Many Requests on department {dept_code}. Wikimedia is rate-limiting. Aborting script completely.")
            sys.exit(1)
        else:
            print(f"[!] HTTP Error {e.code} for {dept_code}: {e.reason}")
    except Exception as e:
        print(f"[!] Could not download symbol for {dept_code}: {e}")
    return ""

def generate_single_sticker_svg(dept_code, symbol_path):
    french_flag = \"\"\"
      <g id="french-flag">
        <rect x="0" y="0" width="8.33" height="16.66" fill="#002395" />
        <rect x="8.33" y="0" width="8.33" height="16.66" fill="#FFFFFF" />
        <rect x="16.66" y="0" width="8.33" height="16.66" fill="#ED2939" />
        <rect x="0" y="0" width="25" height="16.66" fill="none" stroke="#FFFFFF" stroke-width="0.3" opacity="0.4"/>
      </g>
    \"\"\"

    symbol_markup = ""
    if symbol_path and os.path.exists(symbol_path) and os.path.getsize(symbol_path) > 100:
        try:
            tree = ET.parse(symbol_path)
            root = tree.getroot()
            symbol_inner = "".join([ET.tostring(child, encoding='unicode') for child in root])
            symbol_markup = f\"\"\"
            <g id="dept-symbol" transform="translate(12, 66)">
                <svg width="25" height="25" viewBox="{root.attrib.get('viewBox', '0 0 100 100')}">
                    {symbol_inner}
                </svg>
            </g>
            \"\"\"
        except Exception:
            symbol_markup = ""

    if not symbol_markup:
        symbol_markup = f\"\"\"
        <g id="dept-symbol" transform="translate(12, 66)">
            <rect x="0" y="0" width="25" height="25" fill="none" stroke="#FFFFFF" stroke-width="0.5" stroke-dasharray="1,1" opacity="0.5"/>
            <text x="12.5" y="13.5" font-family="Arial, sans-serif" font-size="3.5" fill="#FFFFFF" text-anchor="middle">DEPT {dept_code}</text>
        </g>
        \"\"\"

    svg = f\"\"\"<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{TOTAL_W}mm" height="{TOTAL_H}mm" viewBox="0 0 {TOTAL_W} {TOTAL_H}">
  <defs>
    {french_flag}
    <clipPath id="sticker-cut">
      <rect x="{BLEED}" y="{BLEED}" width="{STICKER_WIDTH}" height="{STICKER_HEIGHT}" rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}" />
    </clipPath>
  </defs>

  <rect x="0" y="0" width="{TOTAL_W}" height="{TOTAL_H}" fill="{REFLEX_BLUE}" />

  <g clip-path="url(#sticker-cut)">
    <g transform="translate(12, 6)">
      <use href="#french-flag" />
    </g>

    <text x="24.5" y="47" 
          font-family="Arial, Helvetica, sans-serif" 
          font-weight="900" 
          font-size="22" 
          fill="#FFFFFF" 
          text-anchor="middle" 
          dominant-baseline="central" 
          letter-spacing="-0.5">{dept_code}</text>

    {symbol_markup}
  </g>

  <rect x="{BLEED}" y="{BLEED}" width="{STICKER_WIDTH}" height="{STICKER_HEIGHT}" rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}" 
        fill="none" stroke="{CUT_COLOR}" stroke-width="0.25" id="CutContour" />
</svg>\"\"\"
    return svg

def generate_imposition_sheet(dept_code, single_svg_str, sheet_type="A3"):
    sheet_w, sheet_h = SHEET_SIZES.get(sheet_type.upper(), SHEET_SIZES["A3"])
    margin_x, margin_y = 15.0, 15.0
    gap_x, gap_y = 2.0, 2.0
    
    usable_w = sheet_w - (2 * margin_x)
    usable_h = sheet_h - (2 * margin_y)
    
    cols = int((usable_w + gap_x) // (TOTAL_W + gap_x))
    rows = int((usable_h + gap_y) // (TOTAL_H + gap_y))
    total_stickers = cols * rows
    
    start_x = (sheet_w - (cols * TOTAL_W + (cols - 1) * gap_x)) / 2
    start_y = (sheet_h - (rows * TOTAL_H + (rows - 1) * gap_y)) / 2

    single_tree = ET.fromstring(single_svg_str)
    inner_content = "".join([ET.tostring(child, encoding='unicode') for child in single_tree])

    grid_items = []
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * (TOTAL_W + gap_x)
            y = start_y + r * (TOTAL_H + gap_y)
            grid_items.append(f'<g transform="translate({x}, {y})">{inner_content}</g>')

    reg_marks = f\"\"\"
      <g stroke="#000000" stroke-width="0.25" fill="none">
        <circle cx="8" cy="8" r="4" />
        <line x1="2" y1="8" x2="14" y2="8" />
        <line x1="8" y1="2" x2="8" y2="14" />

        <circle cx="{sheet_w - 8}" cy="8" r="4" />
        <line x1="{sheet_w - 14}" y1="8" x2="{sheet_w - 2}" y2="8" />
        <line x1="8" y1="2" x2="8" y2="14" />

        <circle cx="8" cy="{sheet_h - 8}" r="4" />
        <line x1="2" y1="{sheet_h - 8}" x2="14" y2="{sheet_h - 8}" />
        <line x1="8" y1="{sheet_h - 14}" x2="8" y2="8" />

        <circle cx="{sheet_w - 8}" cy="{sheet_h - 8}" r="4" />
        <line x1="{sheet_w - 14}" y1="{sheet_h - 8}" x2="{sheet_w - 2}" y2="{sheet_h - 8}" />
        <line x1="{sheet_w - 8}" y1="{sheet_h - 14}" x2="{sheet_w - 8}" y2="{sheet_h - 2}" />
      </g>
    \"\"\"

    imposition_svg = f\"\"\"<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{sheet_w}mm" height="{sheet_h}mm" viewBox="0 0 {sheet_w} {sheet_h}">
  <style> text {{ font-family: Arial, sans-serif; }} </style>
  <rect width="{sheet_w}" height="{sheet_h}" fill="#FFFFFF" />
  <text x="{start_x}" y="{start_y - 5}" font-size="4" fill="#333333">IMPOSITION: Dept {dept_code} | Format: {sheet_type} | Qty: {total_stickers} units | CutContour Enabled</text>
  {''.join(grid_items)}
  {reg_marks}
</svg>\"\"\"
    return imposition_svg

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h", "HELP"]:
        print_help()
        sys.exit(0)

    arg1 = sys.argv[1].upper()
    sheet_format = sys.argv[2].upper() if len(sys.argv) > 2 else "A3"
    if sheet_format not in SHEET_SIZES:
        sheet_format = "A3"

    os.makedirs("output", exist_ok=True)
    os.makedirs("symbols", exist_ok=True)

    departments_to_process = []
    if arg1 == "ALL":
        departments_to_process = list(DEPT_WIKI_FILES.keys())
    else:
        departments_to_process = [arg1.zfill(2) if arg1.isdigit() and len(arg1) == 1 else arg1]

    for dept_code in departments_to_process:
        print(f"\\n[+] Processing Department {dept_code}...")
        symbol_path = fetch_symbol_if_needed(dept_code)

        single_svg = generate_single_sticker_svg(dept_code, symbol_path)
        single_file = os.path.join("output", f"sticker_{dept_code}_single.svg")
        with open(single_file, "w", encoding="utf-8") as f:
            f.write(single_svg)

        imposition_svg = generate_imposition_sheet(dept_code, single_svg, sheet_format)
        sheet_file = os.path.join("output", f"imposition_{dept_code}_{sheet_format}.svg")
        with open(sheet_file, "w", encoding="utf-8") as f:
            f.write(imposition_svg)
        print(f"[✓] Exported imposition sheet -> {sheet_file}")
'''
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)

if __name__ == "__main__":
    setup_project()