#!/usr/bin/env python3
import os
import urllib.request
import urllib.error
import json
import ssl
import time
import random
import xml.etree.ElementTree as ET

SHEET_SIZES = {
    "A6": (105.0, 148.0),
    "A5": (148.0, 210.0),
    "A4": (210.0, 297.0),
    "A3": (297.0, 420.0),
    "SRA3": (320.0, 450.0),
}

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
    "74": "Blason département fr Haute-Savoie.svg", "75": "Armoiries de la ville de Paris (1949).svg",
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
    "971": "Coat of arms of Guadeloupe.svg",
    "972": "Coat of arms of Martinique.svg",
    "973": "Coat of arms of French Guiana, according to the original displayed at the Museum Franconie, at Cayenne.svg",
    "974": "Armoiries Réunion.svg",
    "976": "Blason département fr Mayotte.svg"
}

def print_help():
    print("French License Plate Multi-Format Decal Generator")
    print("=================================================")
    print("Usage:")
    print("  python license_plates_sticker.py <dept_code> [sheet_format]")
    print("  Supported formats: A6, A5, A4, A3, SRA3")
    print("  python license_plates_sticker.py ALL [sheet_format]")

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
    "A6": (105.0, 148.0),
    "A5": (148.0, 210.0),
    "A4": (210.0, 297.0),
    "A3": (297.0, 420.0),
    "SRA3": (320.0, 450.0),
}

FLAG_W, FLAG_H = 32.0, 21.33
SYMBOL_SIZE = 32.0
MARGIN_CUT = 2.0
CORNER_RADIUS = 2.0  # Subtle rounded corners for kiss-cut contours

CUT_COLOR = "#FF007F"
ROYAL_BLUE = "#0055A5"

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
    "74": "Blason département fr Haute-Savoie.svg", "75": "Armoiries de la ville de Paris (1949).svg",
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
    "971": "Coat of arms of Guadeloupe.svg",
    "972": "Coat of arms of Martinique.svg",
    "973": "Coat of arms of French Guiana, according to the original displayed at the Museum Franconie, at Cayenne.svg",
    "974": "Armoiries Réunion.svg",
    "976": "Blason département fr Mayotte.svg"
}

def fetch_symbol_if_needed(dept_code):
    sym_path = os.path.join("symbols", f"{dept_code}.svg")
    if os.path.exists(sym_path) and os.path.getsize(sym_path) > 50:
        return sym_path
    
    if dept_code not in DEPT_WIKI_FILES:
        return None

    filename = DEPT_WIKI_FILES[dept_code]
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles=File:{urllib.parse.quote(filename)}&prop=imageinfo&iiprop=url&format=json"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    max_wait = 120
    interval = 10
    elapsed = 0

    while elapsed <= max_wait:
        try:
            req = urllib.request.Request(api_url, headers={'User-Agent': 'LicensePlateStickerBot/1.0'})
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
                            time.sleep(random.uniform(1.0, 3.0))
                            return sym_path
                return None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                if elapsed == 0:
                    print(f"[!] HTTP 429 Too Many Requests on {dept_code}. Waiting up to {max_wait}s...")
                time.sleep(interval)
                elapsed += interval
            else:
                print(f"[!] HTTP Error {e.code} for {dept_code}: {e.reason}")
                return None
        except Exception as e:
            print(f"[!] Error fetching {dept_code}: {e}")
            return None
    return None

def parse_svg_symbol(symbol_path):
    if not symbol_path or not os.path.exists(symbol_path) or os.path.getsize(symbol_path) < 50:
        return '<rect x="10" y="10" width="80" height="80" fill="none" stroke="#999" stroke-width="2"/>', "0 0 100 100"
    try:
        tree = ET.parse(symbol_path)
        root = tree.getroot()
        
        viewbox = root.attrib.get('viewBox')
        if not viewbox:
            w = root.attrib.get('width', '').replace('px', '').replace('mm', '').strip()
            h = root.attrib.get('height', '').replace('px', '').replace('mm', '').strip()
            if w and h:
                try:
                    viewbox = f"0 0 {float(w)} {float(h)}"
                except ValueError:
                    viewbox = "0 0 500 500"
            else:
                viewbox = "0 0 500 500"
                
        inner_parts = []
        for child in root:
            inner_parts.append(ET.tostring(child, encoding='unicode'))
        symbol_inner = "".join(inner_parts)
        if not symbol_inner.strip():
            symbol_inner = ET.tostring(root, encoding='unicode')
            
        return symbol_inner, viewbox
    except Exception as e:
        print(f"[!] Error parsing symbol {symbol_path}: {e}")
        return '<rect x="10" y="10" width="80" height="80" fill="none" stroke="#999" stroke-width="2"/>', "0 0 100 100"

def generate_independent_decals(dept_code, symbol_path):
    symbol_inner, viewbox = parse_svg_symbol(symbol_path)
    
    flag_cut_w = FLAG_W + (2 * MARGIN_CUT)
    flag_cut_h = FLAG_H + (2 * MARGIN_CUT)
    crest_cut_w = SYMBOL_SIZE + (2 * MARGIN_CUT)
    crest_cut_h = SYMBOL_SIZE + (2 * MARGIN_CUT)

    flag_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{flag_cut_w}mm" height="{flag_cut_h}mm" viewBox="0 0 {flag_cut_w} {flag_cut_h}">
      <g transform="translate({MARGIN_CUT}, {MARGIN_CUT})">
        <rect x="0" y="0" width="{FLAG_W}" height="{FLAG_H}" fill="#FFFFFF" rx="1" />
        <rect x="0" y="0" width="{FLAG_W/3}" height="{FLAG_H}" fill="{ROYAL_BLUE}" />
        <rect x="{FLAG_W/3}" y="0" width="{FLAG_W/3}" height="{FLAG_H}" fill="#FFFFFF" />
        <rect x="{2*FLAG_W/3}" y="0" width="{FLAG_W/3}" height="{FLAG_H}" fill="#ED2939" />
      </g>
      <rect x="0" y="0" width="{flag_cut_w}" height="{flag_cut_h}" fill="none" stroke="{CUT_COLOR}" stroke-width="0.25" rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}" id="CutContour" />
    </svg>"""

    crest_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{crest_cut_w}mm" height="{crest_cut_h}mm" viewBox="0 0 {crest_cut_w} {crest_cut_h}">
      <g transform="translate({MARGIN_CUT}, {MARGIN_CUT})">
        <svg x="0" y="0" width="{SYMBOL_SIZE}" height="{SYMBOL_SIZE}" viewBox="{viewbox}" preserveAspectRatio="xMidYMid meet">
          {symbol_inner}
        </svg>
      </g>
      <rect x="0" y="0" width="{crest_cut_w}" height="{crest_cut_h}" fill="none" stroke="{CUT_COLOR}" stroke-width="0.25" rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}" id="CutContour" />
    </svg>"""

    return flag_svg, crest_svg, symbol_inner, viewbox

def generate_imposition_sheet(dept_code, symbol_inner, viewbox, sheet_type="A3"):
    sheet_w, sheet_h = SHEET_SIZES.get(sheet_type.upper(), SHEET_SIZES["A3"])
    min_margin = 8.0
    gap = 2.0
    
    flag_cut_w = FLAG_W + (2 * MARGIN_CUT)
    flag_cut_h = FLAG_H + (2 * MARGIN_CUT)
    crest_cut_w = SYMBOL_SIZE + (2 * MARGIN_CUT)
    crest_cut_h = SYMBOL_SIZE + (2 * MARGIN_CUT)
    
    item_w = max(flag_cut_w, crest_cut_w)
    item_pair_h = flag_cut_h + crest_cut_h + gap
    
    usable_w = sheet_w - (2 * min_margin)
    cols = int((usable_w + gap) // (item_w + gap))
    if cols < 1: cols = 1
    
    usable_h = sheet_h - (2 * min_margin)
    rows = int((usable_h + gap) // (item_pair_h + gap))
    if rows < 1: rows = 1
    
    total_pairs = cols * rows
    
    grid_w = cols * item_w + (cols - 1) * gap
    grid_h = rows * item_pair_h + (rows - 1) * gap
    
    margin_x = (sheet_w - grid_w) / 2.0
    margin_y = (sheet_h - grid_h) / 2.0

    defs_section = f"""
    <defs>
      <g id="decal-flag">
        <g transform="translate({MARGIN_CUT}, {MARGIN_CUT})">
          <rect x="0" y="0" width="{FLAG_W}" height="{FLAG_H}" fill="#FFFFFF" rx="1" />
          <rect x="0" y="0" width="{FLAG_W/3}" height="{FLAG_H}" fill="{ROYAL_BLUE}" />
          <rect x="{FLAG_W/3}" y="0" width="{FLAG_W/3}" height="{FLAG_H}" fill="#FFFFFF" />
          <rect x="{2*FLAG_W/3}" y="0" width="{FLAG_W/3}" height="{FLAG_H}" fill="#ED2939" />
        </g>
        <rect x="0" y="0" width="{flag_cut_w}" height="{flag_cut_h}" fill="none" stroke="{CUT_COLOR}" stroke-width="0.25" rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}" id="CutContour" />
      </g>

      <g id="decal-crest">
        <g transform="translate({MARGIN_CUT}, {MARGIN_CUT})">
          <svg x="0" y="0" width="{SYMBOL_SIZE}" height="{SYMBOL_SIZE}" viewBox="{viewbox}" preserveAspectRatio="xMidYMid meet">
            {symbol_inner}
          </svg>
        </g>
        <rect x="0" y="0" width="{crest_cut_w}" height="{crest_cut_h}" fill="none" stroke="{CUT_COLOR}" stroke-width="0.25" rx="{CORNER_RADIUS}" ry="{CORNER_RADIUS}" id="CutContour" />
      </g>
    </defs>
    """

    grid_items = []
    for r in range(rows):
        for c in range(cols):
            x = margin_x + c * (item_w + gap)
            y = margin_y + r * (item_pair_h + gap)
            grid_items.append(f'<use href="#decal-flag" x="{x}" y="{y}" />')
            grid_items.append(f'<use href="#decal-crest" x="{x}" y="{y + flag_cut_h + gap}" />')

    reg_marks = f"""
      <g stroke="#000000" stroke-width="0.25" fill="none">
        <circle cx="8" cy="8" r="4" />
        <line x1="2" y1="8" x2="14" y2="8" /> <line x1="8" y1="2" x2="8" y2="14" />
        <circle cx="{sheet_w - 8}" cy="8" r="4" />
        <line x1="{sheet_w - 14}" y1="8" x2="{sheet_w - 2}" y2="8" /> <line x1="8" y1="2" x2="8" y2="14" />
        <circle cx="8" cy="{sheet_h - 8}" r="4" />
        <line x1="2" y1="{sheet_h - 8}" x2="14" y2="{sheet_h - 8}" /> <line x1="8" y1="{sheet_h - 14}" x2="8" y2="{sheet_h - 2}" />
        <circle cx="{sheet_w - 8}" cy="{sheet_h - 8}" r="4" />
        <line x1="{sheet_w - 14}" y1="{sheet_h - 8}" x2="{sheet_w - 2}" y2="{sheet_h - 8}" /> <line x1="8" y1="{sheet_h - 14}" x2="8" y2="{sheet_h - 2}" />
      </g>
    """

    imposition_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{sheet_w}mm" height="{sheet_h}mm" viewBox="0 0 {sheet_w} {sheet_h}">
  <style> text {{ font-family: Arial, sans-serif; }} </style>
  <rect width="{sheet_w}" height="{sheet_h}" fill="#FFFFFF" />
  <text x="8" y="5" font-size="2.5" fill="#333333">CENTERED SHEET: Dept {dept_code} | Format: {sheet_type} | Pairs: {total_pairs} | Rounded CutContour (r=2mm)</text>
  {defs_section}
  {''.join(grid_items)}
  {reg_marks}
</svg>"""
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
        if not symbol_path:
            print(f"[!] Skipping Dept {dept_code} due to missing symbol.")
            continue

        flag_svg, crest_svg, symbol_inner, viewbox = generate_independent_decals(dept_code, symbol_path)
        
        with open(os.path.join("output", f"decal_flag_{dept_code}.svg"), "w", encoding="utf-8") as f:
            f.write(flag_svg)
        with open(os.path.join("output", f"decal_crest_{dept_code}.svg"), "w", encoding="utf-8") as f:
            f.write(crest_svg)

        imposition_svg = generate_imposition_sheet(dept_code, symbol_inner, viewbox, sheet_format)
        sheet_file = os.path.join("output", f"imposition_independent_{dept_code}_{sheet_format}.svg")
        with open(sheet_file, "w", encoding="utf-8") as f:
            f.write(imposition_svg)
        print(f"[✓] Exported centered imposition sheet -> {sheet_file}")
'''
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)

if __name__ == "__main__":
    setup_project()