import streamlit as st
from datetime import date
import io
import math
import io

try:
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    import fpdf
    from fpdf import FPDF
    EXPORTS_READY = True
except ImportError:
    EXPORTS_READY = False

# ==========================================
# 1. KONFIGURACJA STRONY I WSPÓLNE FUNKCJE
# ==========================================
st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="wide")

class ReportBuilder:
    def __init__(self):
        self.md_lines = []
    
    def write(self, text):
        self.md_lines.append(str(text))
        
    def markdown(self, text):
        self.md_lines.append(str(text))
        
    def error(self, text):
        st.error(text)
        
    def get_markdown(self):
        return "\n\n".join(self.md_lines)

# --- STAŁE TECHNOLOGICZNE (OPISY PRODUKTÓW) ---
FULL_PS275 = "* Zalecamy aplikację gruntówki wzmacniającej **WAKOL PS 275** w dwóch warstwach – grubym wałkiem sznurkowym, zużycie w sumie **ok. 700 g/m²**. Każda z warstw po **350 g/m²**, aplikowane po sobie w odstępie jednej godziny. Aplikując gruntówkę **WAKOL PS 275** należy zwrócić uwagę, aby dobrze wchłaniała się w podłoże i unikać powstawania kałuż na powierzchni jastrychu. Po nałożeniu drugiej warstwy gruntówki w razie potrzeby wykonać posypkę z piasku kwarcowego. **Po 7 dniach schnięcia** powierzchnię należy **przeszlifować papierem o gradacji 24 – 40** usuwając przyklejony do powierzchni piasek kwarcowy i dokładnie odkurzyć."
FULL_PU235_1W = "* Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową **WAKOL PU 235**. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. zbierać nadmiar niewchłoniętej gruntówki. Zużycie **ok. 150 g/m²**. **Czas schnięcia – jedna godzina**."
FULL_PU235_BARRIER = "* Zalecamy wykonanie **bariery przeciwwilgociowej** poprzez dwukrotne zagruntowanie gruntówką wzmacniającą **WAKOL PU 235**. Podczas aplikacji nie zostawiać kałuż tj. zbierać nadmiar niewchłoniętej gruntówki. 1. warstwa nałożona wałkiem **ok. 150 g/m²**. **Czas schnięcia – 3-6 godzin**. 2. warstwa zużycie **ok. 100 g/m²**. **Czas schnięcia – 3-6 godzin**. **Czas klejenia 72 godziny od zagruntowania**."
FULL_PU280_1W = "* Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową **WAKOL PU 280**. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. zbierać nadmiar niewchłoniętej gruntówki. Zużycie **ok. 150 g/m²**. **Czas schnięcia – jedna godzina**."
FULL_PU280_BARRIER = "* Z uwagi na podwyższoną wilgotność zalecamy stworzenie **bariery przeciwwilgociowej** poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową **WAKOL PU 280**. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. zbierać nadmiar niewchłoniętej gruntówki. 1. warstwa nałożona wałkiem **ok. 100-150 g/m²**. **Czas schnięcia – jedna godzina**. 2. warstwa **ok. 100 g/m²** - **czas schnięcia – jedna godzina**. **Czas do klejenia: 72 godziny od zagruntowania**."
FULL_D3004 = "* Zagruntować podłoże koncentratem gruntówki dyspersyjnej **WAKOL D 3004**. Proporcje mieszania: 1 część **WAKOL D 3004** + 2 części wody. **Czas schnięcia**: na jastrychach cementowych i betonie po optycznym wyschnięciu **ok. 30 min**. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: **ok. 50 g/m²** koncentratu."
FULL_Z625 = "* Wylać masę wyrównawczą **WAKOL Z 625** - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,00 – 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie **ok. 1,6 kg/m²/mm**. **Możliwość chodzenia po 2 godzinach**. **Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 6 godzinach**, przy warstwie do 10 mm – po 12 godzinach, przy warstwie 30 mm – po 24 godzinach."
FULL_Z675 = "* Wylać masę wyrównawczą **WAKOL Z 675** - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,0 – 6,5 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie **ok. 1,6 kg/m²/mm**. **Możliwość chodzenia po 2-3 godzinach**. **Możliwość klejenia podłóg po ok. 24 godzinach przy grubości warstwy do 3 mm**, przy większych grubościach czas schnięcia ulega wydłużeniu."
FULL_Z635 = "* Następnie na podłoże wylać masę wyrównawczą **WAKOL Z 635** - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie **ok. 1,6 kg/m²/mm**. **Możliwość chodzenia po 2,5 godzinach**. **Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 24 godzinach**, przy warstwie do 10 mm – po 72 godzinach."
FULL_D3055 = "* Zalecamy zagruntowanie całej powierzchni jastrychu gruntówką dyspersyjną **WAKOL D 3055** - aplikacja wałkiem **ok. 150 g/m²**. **Czas schnięcia ok. 30 min**."

def insert_header():
    logo_wakol = "https://www.wakol.com/fileadmin/templates/images/wakol_logo.png"
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;">
        <div style="flex: 1;"><img src="{logo_wakol}" width="220">
            <div style="margin-top: 15px; font-size: 11px; color: #555; line-height: 1.4;">
                <b>Loba-Wakol Polska Sp. z o.o.</b><br>ul. Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki<br>tel.: +48 22 436 24 20 | biuro@loba-wakol.pl
            </div>
        </div>
        <div style="flex: 1; text-align: right;">
            <div style="font-size: 18px; font-weight: bold; color: #000; margin-bottom: 5px;">PROTOKÓŁ TECHNICZNY</div>
            <div style="font-size: 14px; color: #333;">Anspruch verbindet</div>
        </div>
    </div><br>
    """, unsafe_allow_html=True)

# ==========================================
# 2. LOGIKA DLA POSZCZEGÓLNYCH OKŁADZIN
# ==========================================

def render_wspolne_dane_optyczne(dane, rep):
    age_txt = f" w wieku {dane['substrate_age_val']} miesięcy" if dane['substrate_age_val'] else ""
    heat_txt = f" Została zainstalowana {dane['heating_info']}." if dane['heating_exists'] == "TAK" else " Brak instalacji ogrzewania podłogowego."
    curing_txt = " Został przeprowadzony proces wygrzewania zgodnie z protokołem." if dane['heating_curing_done'] == "TAK" else " Nie został przeprowadzony proces wygrzewania podłoża." if dane['heating_exists'] == "TAK" else ""
    dil_txt = " Dylatacje obwodowe zachowane prawidłowo." if dane['dilatations_obw_ok'] == "TAK" else " Dylatacje obwodowe nie zachowane prawidłowo."
    klaw_m = dane.get('klaw_meters') or 0
    pek_m = dane.get('pek_meters') or 0
    klaw_txt = f" Zaobserwowano {klaw_m} metrów bieżących dylatacji pozornych wymagających zespolenia." if dane['cracks_klaw'] == "TAK" else " Nie zaobserwowano dylatacji pozornych wymagających zespolenia."
    pek_txt = f" Zaobserwowano {pek_m} metrów bieżących pęknięć wymagających zespolenia." if dane['cracks_pek'] == "TAK" else " Nie zaobserwowano pęknięć wymagających zespolenia."
    holes_txt = f" Zaobserwowano fragmenty wymagające wypełnienia masą naprawczą{dane['hole_details']}." if dane['holes'] == "TAK" else " Nie stwierdzono ubytków lub zdegradowanych miejsc wymagających wypełnienia."
    level_txt = f" Podłoże wymaga wyrównania masą wyrównawczą o planowanej grubości {dane['leveling_thickness']} milimetrów." if dane['needs_levelling'] == "TAK" else " Podłoże nie wymaga wyrównania masą wyrównawczą."
    vent_txt = f" Rodzaj zastosowanej wentylacji: wentylacja {dane['ventilation_type'].lower()}."
    
    area_txt = f" o powierzchni {dane['area_m2']} m²" if dane.get('area_m2') else ""
    full_opt_report = f"Podłoże pod planowaną okładzinę ({dane['flooring_type']}) stanowi {dane['substrate']}{area_txt}{age_txt}.{heat_txt}{curing_txt}{dil_txt}{klaw_txt}{pek_txt}{holes_txt}{level_txt} {vent_txt}"
    rep.write(f"**a) oględziny optyczne:** {full_opt_report}")
    
    presso_valid = [str(p) for p in dane.get('presso_results', []) if p is not None]
    presso_txt = f"\n- Wyniki PressoMess: {', '.join(presso_valid)} N/mm²" if presso_valid else ""
    rep.write(f"**b) badanie wytrzymałości:**\n- Młotek: {dane['test_hammer']}\n- Rysik: {dane['test_ripper']}\n- Szczotka: {dane['test_brush']}{presso_txt}\n- Ocena ogólna: **{dane['strength_labels'][dane['strength_val']]}**")
    
    moisture_status = "POZYTYWNY" if dane['moisture'] <= dane['limit'] else "NEGATYWNY"
    rep.write(f"**c) badanie wilgotności:** Wynik badania wilgotności metodą CM: **{dane['moisture']} % CM** (Norma: {dane['limit']} % CM) — **Wynik: {moisture_status}**")

    klimat = []
    if dane.get('temp_air') is not None: klimat.append(f"Temperatura powietrza: {dane['temp_air']} °C")
    if dane.get('hum_air') is not None: klimat.append(f"Wilgotność powietrza: {dane['hum_air']} %")
    if klimat:
        rep.write(f"**d) warunki klimatyczne:** {', '.join(klimat)}.")

PRODUCTS = {
    'PU 280 (1W)': {'name': 'WAKOL PU 280 (1 warstwa)', 'usage': 150, 'sizes': [11, 5], 'text': FULL_PU280_1W},
    'PU 280 (Bariera)': {'name': 'WAKOL PU 280 (bariera)', 'usage': 250, 'sizes': [11, 5], 'text': FULL_PU280_BARRIER},
    'PU 235 (1W)': {'name': 'WAKOL PU 235 (1 warstwa)', 'usage': 150, 'sizes': [11], 'text': FULL_PU235_1W},
    'PU 235 (Bariera)': {'name': 'WAKOL PU 235 (bariera)', 'usage': 250, 'sizes': [11], 'text': FULL_PU235_BARRIER},
    'PS 275': {'name': 'WAKOL PS 275', 'usage': 700, 'sizes': [11], 'text': FULL_PS275},
    'D 3004': {'name': 'WAKOL D 3004', 'usage': 50, 'sizes': [10, 5], 'text': FULL_D3004},
    'D 3055': {'name': 'WAKOL D 3055', 'usage': 150, 'sizes': [10, 5], 'text': FULL_D3055},
    'PU 225': {'name': 'WAKOL PU 225 (klej)', 'usage': 1250, 'sizes': [10], 'text': ""},
    'MS 230': {'name': 'WAKOL MS 230 (klej)', 'usage': 1350, 'sizes': [18], 'text': ""},
    'MS 260': {'name': 'WAKOL MS 260 (klej)', 'usage': 1350, 'sizes': [18], 'text': ""},
    'D 3318': {'name': 'WAKOL D 3318 (klej)', 'usage': 350, 'sizes': [13], 'text': ""},
    'Z 645': {'name': 'WAKOL Z 645 (masa naprawcza)', 'usage': 1.6, 'sizes': [25], 'text': ""},
    'Z 645 (bruzdowane)': {'name': 'WAKOL Z 645 (masa szpachlowa)', 'usage': 2000, 'sizes': [25], 'text': ""},
    'Z 625': {'name': 'WAKOL Z 625 (masa samorozlewna)', 'usage_per_mm': 1.6, 'sizes': [25], 'text': FULL_Z625},
    'Z 635': {'name': 'WAKOL Z 635 (masa samorozlewna)', 'usage_per_mm': 1.6, 'sizes': [25], 'text': FULL_Z635},
    'Z 675': {'name': 'WAKOL Z 675 (masa samorozlewna)', 'usage_per_mm': 1.6, 'sizes': [25], 'text': FULL_Z675},
    'D 3004 (bruzdowane)': {'name': 'WAKOL D 3004 (koncentrat)', 'usage': 75, 'sizes': [10, 5], 'text': ""},
    'AR 150': {'name': 'WAKOL AR 150 (mata kompensacyjna)', 'usage': 1000, 'sizes': [50], 'text': ""},
    'D 3060': {'name': 'WAKOL D 3060 (plastyfikator)', 'usage': 1000, 'sizes': [10], 'text': ""},
    'PU 280 (RP)': {'name': 'WAKOL PU 280 (grunt dla RP)', 'usage': 200, 'sizes': [11, 5], 'text': "* Zalecamy zagruntowanie całej powierzchni podłoża gruntówką wzmacniającą **WAKOL PU 280**. Aplikować wałkiem. Nie zostawiać kałuż tj. zbierać nadmiar niewchłoniętej gruntówki. Zużycie ok. 200 g/m². Czas schnięcia 1 godzina. Czas do montażu – 72 godziny."},
    'Płyta RP': {'name': 'WAKOL RP 704 (płyta odprzęgająca)', 'usage': 1000, 'sizes': [1], 'unit': 'szt', 'text': "* Na tak przygotowane podłoże zalecamy przyklejenie płyty odprzęgającej o grubości 4 mm **WAKOL RP 704**. Należy przyklejać klejem 2K PU (**WAKOL PU 225**). Płytę odprzęgającą po ułożeniu należy docisnąć. Płytę można docinać używając noża trapezowego. Można układać parkiet, jeśli tylko klejona płyta nie przesuwa się w trakcie chodzenia po niej."},
    'PS 205': {'name': 'WAKOL PS 205 (żywica lana)', 'sizes': [1], 'unit': 'kpl.', 'text': ""}
}

def write_and_track(dane, rep, prod_key, custom_kg=None):
    prod = PRODUCTS[prod_key]
    if prod['text']:
        rep.write(prod['text'])
    if 'materials' not in dane:
        dane['materials'] = []
        
    needed_kg = 0
    if custom_kg is not None:
        needed_kg = custom_kg
    else:
        area = dane.get('area_m2')
        if not area: return
        
        if 'usage_per_mm' in prod:
            thick = dane.get('leveling_thickness')
            if not thick: return
            needed_kg = area * thick * prod['usage_per_mm']
        else:
            needed_kg = (area * prod['usage']) / 1000.0
            
    if needed_kg <= 0: return
    sizes = sorted(prod['sizes'], reverse=True)
    best_combo = None
    best_waste = float('inf')
    import math
    max_large = int(math.ceil(needed_kg / sizes[0])) if sizes else 0
    for i in range(max_large + 1):
        rem = needed_kg - i * sizes[0]
        if rem <= 0:
            waste = -rem
            if waste < best_waste:
                best_waste = waste
                best_combo = {sizes[0]: i}
                if len(sizes) > 1: best_combo[sizes[1]] = 0
        else:
            if len(sizes) > 1:
                j = int(math.ceil(rem / sizes[1]))
                waste = (i * sizes[0] + j * sizes[1]) - needed_kg
                if waste < best_waste:
                    best_waste = waste
                    best_combo = {sizes[0]: i, sizes[1]: j}
    unit = prod.get('unit', 'kg')
    combo_str = []
    if best_combo:
        for size in sizes:
            if best_combo.get(size, 0) > 0:
                if unit != 'kg' and size == 1:
                    combo_str.append(f"{best_combo[size]} {unit}")
                else:
                    combo_str.append(f"{best_combo[size]}x {size} {unit}")
    # check if material already added to prevent duplicates (e.g. glue when falling through if-else)
    if not any(m['name'] == prod['name'] for m in dane['materials']):
        dane['materials'].append({
            'name': prod['name'],
            'kg': round(needed_kg, 2),
            'combo': " + ".join(combo_str) if combo_str else f"{math.ceil(needed_kg)} {unit}",
            'unit': unit
        })

def render_potrzebne_materialy(dane, rep):
    if not dane.get('area_m2'): return
    if not dane.get('materials'): return
    rep.write("**Potrzebne materiały (szacunkowo na podstawie powierzchni):**")
    for m in dane['materials']:
        unit = m.get('unit', 'kg')
        if unit == 'kg':
            rep.write(f"- {m['name']}: **{m['kg']} kg** ({m['combo']})")
        else:
            rep.write(f"- {m['name']}: **{math.ceil(m['kg'])} {unit}**")

def render_wspolne_zalecenia_podloze(dane, rep):
    rep.write("**a) przygotowanie podłoża:**")
    if dane['dilatations_obw_ok'] == "NIE":
        rep.write("* Odtworzenie dylatacji obwodowych.")
    if dane['cracks_klaw'] == "TAK":
        rep.write("* Rozbruzdowanie klawiszujących dylatacji pozornych.")
    if dane['cracks_pek'] == "TAK":
        rep.write("* Rozbruzdowanie pęknięć wymagających zespolenia.")
    rep.write("* **Szlif podłoża** w celu uzyskania porowatej i chłonnej powierzchni!")
    rep.write("* Dokładne odkurzenie powierzchni odkurzaczem przemysłowym.")
    
    if dane['curing_not_done']:
        if dane['is_moisture_neg']:
            rep.write(f"* **Konieczność przeprowadzenia pełnego procesu wygrzewania podłoża** w celu uzyskania normatywnego poziomu wilgoci **{dane['norm_val_bracket']}**.")
        else:
            rep.write(f"* **Konieczność przeprowadzenia pełnego procesu wygrzewania podłoża** zgodnie z protokołem.")
    elif dane['is_moisture_neg']:
        if dane['decision_after_cure'] == "Wykonanie bariery przeciwwilgociowej":
            rep.write("* Zalecamy wykonanie **bariery przeciwwilgociowej**.")
        else:
            rep.write(f"* Zalecamy doprowadzenie do normatywnego poziomu wilgoci **{dane['norm_val_bracket']}** poprzez {dane['decision_after_cure']}.")

    rep.write("**b) naprawa i wzmocnienie podłoża:**")
    if dane['curing_not_done']:
        if dane['is_moisture_neg']:
            rep.write(f"Po doprowadzeniu do normatywnego poziomu wilgoci **{dane['norm_val_bracket']}** jastrychu poprzez **przeprowadzenie procesu wygrzewania** zalecamy:")
        else:
            rep.write("Po **przeprowadzeniu pełnego procesu wygrzewania** zalecamy:")
    elif dane['needs_drying_action']:
        rep.write(f"Po doprowadzeniu do normatywnego poziomu wilgoci **{dane['norm_val_bracket']}** zalecamy:")
    
    if dane['cracks_klaw'] == "TAK" or dane['cracks_pek'] == "TAK":
        if dane['strength_val'] == 1 and dane['substrate'] != "jastrych anhydrytowy":
            write_and_track(dane, rep, 'PS 275')
        rep.write("* Pęknięcia / Klawiszujące dylatacje - zespolić żywicą laną **WAKOL PS 205**. Wymieszaną żywicę wlewać w pęknięcia, nadmiar zgarnąć lub zatrzeć.")
        total_meters = 0
        if dane['cracks_klaw'] == "TAK":
            total_meters += dane.get('klaw_meters') or 0
        if dane['cracks_pek'] == "TAK":
            total_meters += dane.get('pek_meters') or 0
        if total_meters > 0:
            write_and_track(dane, rep, 'PS 205', custom_kg=total_meters / 6.5)

    if dane['holes'] == "TAK":
        kg_z645 = None
        if dane.get('holes_width') and dane.get('holes_length') and dane.get('holes_depth'):
            area_h = (dane['holes_width'] / 100.0) * (dane['holes_length'] / 100.0)
            thick_mm = dane['holes_depth'] * 10.0
            kg_z645 = area_h * thick_mm * 1.6

        if dane.get('holes_depth') and dane['holes_depth'] >= 1.0:
            if kg_z645 is not None: kg_z645 /= 2.0
            rep.write("* Ubytki zaszpachlować masą **WAKOL Z 645** wymieszaną z piaskiem kwarcowym w proporcji 1:1  – czas schnięcia 1 godzina.")
        else:
            rep.write("* Ubytki zaszpachlować masą szpachlową **WAKOL Z 645** z dodatkiem plastyfikatora **WAKOL D 3060** (7 litrów WAKOL D 3060 na 25 kg WAKOL Z 645). Czas schnięcia min. 3h. W razie potrzeby użyć siatki zbrojeniowej WAKOL AR 150.")
        
        if kg_z645 is not None:
            write_and_track(dane, rep, 'Z 645', custom_kg=kg_z645)

    if dane['heating_exists'] == "TAK" and dane['h_type'] == "bruzdowane":
        if dane['bruzdowane_wybor'] == "masa samorozlewna":
            rep.write("* Podłoże zagruntować koncentratem gruntówki dyspersyjnej **WAKOL D 3004**. Proporcje mieszania: 1 część WAKOL D 3004 + 1 część wody; Czas schnięcia: 1h. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: ok. 75 g/m² koncentratu.")
            write_and_track(dane, rep, 'D 3004 (bruzdowane)')
            
            rep.write("* Na tak przygotowane podłoże należy rozłożyć matę **WAKOL AR 150** i zaszpachlować ją masą szpachlową **WAKOL Z 645** z dodatkiem plastyfikatora **WAKOL D 3060** (7 litrów WAKOL D 3060 na 25 kg WAKOL Z 645). Czas schnięcia min. 3h.")
            area = dane.get('area_m2') or 0
            if area > 0:
                write_and_track(dane, rep, 'AR 150', custom_kg=area)
                kg_z645_bruzdowane = area * 2.0
                write_and_track(dane, rep, 'Z 645 (bruzdowane)', custom_kg=kg_z645_bruzdowane)
                bags_z645 = math.ceil(kg_z645_bruzdowane / 25.0)
                write_and_track(dane, rep, 'D 3060', custom_kg=bags_z645 * 7.0)
            write_and_track(dane, rep, 'Z 635', custom_kg=area * 5 * 1.5)
        elif dane['bruzdowane_wybor'] == "płyta RP":
            area = dane.get('area_m2') or 0
            write_and_track(dane, rep, 'PU 280 (RP)')
            write_and_track(dane, rep, 'Płyta RP', custom_kg=math.ceil(area / 0.6) if area > 0 else 0)
            write_and_track(dane, rep, 'PU 225')

def render_wspolna_chemia(dane, rep):
    used_d3004 = False
    if dane.get('h_type') == "bruzdowane" and dane.get('bruzdowane_wybor'):
        return True # Pomijamy standardową chemię, obsłużona w naprawie podłoża

    if dane['decision_after_cure'] == "Wykonanie bariery przeciwwilgociowej":
        if dane['strength_val'] <= 2: write_and_track(dane, rep, 'PU 235 (Bariera)')
        else: write_and_track(dane, rep, 'PU 280 (Bariera)')
    elif not dane['decision_after_cure'] or "Wykonanie" not in str(dane['decision_after_cure']):
        if dane['needs_levelling'] == "TAK":
            if dane['strength_val'] in [3, 4, 5]:
                if dane['substrate'] == "jastrych anhydrytowy" and dane['leveling_thickness'] and dane['leveling_thickness'] > 5:
                    write_and_track(dane, rep, 'PU 280 (1W)')
                else:
                    write_and_track(dane, rep, 'D 3004')
                    used_d3004 = True
            else:
                if dane['strength_val'] == 1:
                    if dane['substrate'] == "jastrych anhydrytowy": write_and_track(dane, rep, 'PU 235 (1W)')
                    else:
                        if not any(m['name'] == 'WAKOL PS 275' for m in dane.get('materials', [])): write_and_track(dane, rep, 'PS 275')
                        write_and_track(dane, rep, 'PU 280 (1W)')
                elif dane['strength_val'] == 2: write_and_track(dane, rep, 'PU 280 (1W)')
        else:
            if dane['strength_val'] == 1:
                if dane['substrate'] == "jastrych anhydrytowy": write_and_track(dane, rep, 'PU 235 (1W)')
                else:
                    if not any(m['name'] == 'WAKOL PS 275' for m in dane.get('materials', [])): write_and_track(dane, rep, 'PS 275')
            elif dane['strength_val'] == 2: write_and_track(dane, rep, 'PU 235 (1W)')
            elif dane['strength_val'] in [3, 4]: write_and_track(dane, rep, 'PU 280 (1W)')
    return used_d3004

def render_chemia_deska_warstwowa(dane, rep):
    used_d3004 = False
    if dane.get('h_type') == "bruzdowane" and dane.get('bruzdowane_wybor'):
        return True

    if dane['decision_after_cure'] == "Wykonanie bariery przeciwwilgociowej":
        if dane['strength_val'] <= 2: write_and_track(dane, rep, 'PU 235 (Bariera)')
        else: write_and_track(dane, rep, 'PU 280 (Bariera)')
    elif not dane['decision_after_cure'] or "Wykonanie" not in str(dane['decision_after_cure']):
        if dane['needs_levelling'] == "TAK":
            if dane['strength_val'] in [3, 4, 5]:
                if dane['substrate'] == "jastrych anhydrytowy" and dane['leveling_thickness'] and dane['leveling_thickness'] > 5:
                    write_and_track(dane, rep, 'PU 280 (1W)')
                else:
                    write_and_track(dane, rep, 'D 3004')
                    used_d3004 = True
            elif dane['strength_val'] == 2:
                write_and_track(dane, rep, 'PU 280 (1W)')
            elif dane['strength_val'] == 1:
                if dane['substrate'] == "jastrych anhydrytowy": write_and_track(dane, rep, 'PU 235 (1W)')
                else:
                    if not any(m['name'] == 'WAKOL PS 275' for m in dane.get('materials', [])): write_and_track(dane, rep, 'PS 275')
                    write_and_track(dane, rep, 'PU 280 (1W)')
        else:
            if dane['strength_val'] == 1:
                if dane['substrate'] == "jastrych anhydrytowy": write_and_track(dane, rep, 'PU 235 (1W)')
                else:
                    if not any(m['name'] == 'WAKOL PS 275' for m in dane.get('materials', [])): write_and_track(dane, rep, 'PS 275')
            elif dane['strength_val'] == 2: write_and_track(dane, rep, 'PU 235 (1W)')
            elif dane['strength_val'] == 3: write_and_track(dane, rep, 'PU 280 (1W)')
            elif dane['strength_val'] in [4, 5]: write_and_track(dane, rep, 'D 3055')
    return used_d3004

def render_chemia_deska_lita(dane, rep):
    used_d3004 = False
    if dane.get('h_type') == "bruzdowane" and dane.get('bruzdowane_wybor'):
        return True

    if dane['decision_after_cure'] == "Wykonanie bariery przeciwwilgociowej":
        if dane['strength_val'] <= 2: write_and_track(dane, rep, 'PU 235 (Bariera)')
        else: write_and_track(dane, rep, 'PU 280 (Bariera)')
    elif not dane['decision_after_cure'] or "Wykonanie" not in str(dane['decision_after_cure']):
        if dane['needs_levelling'] == "TAK":
            if dane['strength_val'] in [3, 4, 5]:
                if dane['substrate'] == "jastrych anhydrytowy" and dane['leveling_thickness'] and dane['leveling_thickness'] > 5:
                    write_and_track(dane, rep, 'PU 280 (1W)')
                else:
                    write_and_track(dane, rep, 'D 3004')
                    used_d3004 = True
            else:
                if dane['strength_val'] == 1:
                    if dane['substrate'] == "jastrych anhydrytowy": write_and_track(dane, rep, 'PU 235 (1W)')
                    else:
                        if not any(m['name'] == 'WAKOL PS 275' for m in dane.get('materials', [])): write_and_track(dane, rep, 'PS 275')
                        write_and_track(dane, rep, 'PU 280 (1W)')
                elif dane['strength_val'] == 2: write_and_track(dane, rep, 'PU 280 (1W)')
        else:
            if dane['strength_val'] == 1:
                if dane['substrate'] == "jastrych anhydrytowy": write_and_track(dane, rep, 'PU 235 (1W)')
                else:
                    if not any(m['name'] == 'WAKOL PS 275' for m in dane.get('materials', [])): write_and_track(dane, rep, 'PS 275')
            elif dane['strength_val'] == 2: write_and_track(dane, rep, 'PU 235 (1W)')
            elif dane['strength_val'] in [3, 4]: write_and_track(dane, rep, 'PU 280 (1W)')
            elif dane['strength_val'] == 5: write_and_track(dane, rep, 'D 3055')
    return used_d3004

# --- SEKCJA: DESKA WARSTWOWA ---
def generate_report_deska_warstwowa(dane, rep):
    render_wspolne_dane_optyczne(dane, rep)
    
    nazwa_okladziny = "podłogę drewnianą" if dane['flooring_type'] == "deska warstwowa" else "podłogę laminowaną"
    tytul_sekcji = "Deska Warstwowa" if dane['flooring_type'] == "deska warstwowa" else "Podłoga laminowana"
    
    if dane['substrate'] == "jastrych cementowy":
        rep.write(f"**Aby bezpiecznie kleić {nazwa_okladziny} na jastrychu cementowym, jego wytrzymałość na ścinanie musi wynosić między 1,5 a 2,0 N/mm² a wilgotność nie może przekraczać 1,8% CM. (z ogrzewaniem podłogowym max. 1,5% CM).**")
    elif dane['substrate'] == "jastrych anhydrytowy":
        rep.write(f"**Aby bezpiecznie kleić {nazwa_okladziny} na jastrychu anhydrytowym zgodnie z wytycznymi ITB, jego wytrzymałość na ścinanie musi wynosić 2,0 N/mm² a wilgotność nie może przekraczać 0,5% CM. (z ogrzewaniem podłogowym max. 0,3% CM).**")
    
    rep.markdown(f"#### **II. Zalecenia techniczne ({tytul_sekcji})**")
    
    render_wspolne_zalecenia_podloze(dane, rep)
    used_d3004 = render_chemia_deska_warstwowa(dane, rep)

    if dane['needs_levelling'] == "TAK" and dane.get('bruzdowane_wybor') != "masa samorozlewna":
        if not used_d3004:
            rep.write("* Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu **WAKOL D 3045**. Aplikować równomiernie za pomocą wałka. Zużycie wynosi **ok. 150 g/m²**. **Czas schnięcia 1 godzina**.")
        write_and_track(dane, rep, 'Z 635')

    rep.write("**c) klejenie okładziny:**")
    if dane['substrate'] == "jastrych anhydrytowy" and dane['strength_val'] == 1:
        rep.write(f"Klejenie {nazwa_okladziny} należy przeprowadzić przy użyciu kleju do parkietu **WAKOL MS 230** (szpachla B13, zużycie: 1350 g/m²).")
        write_and_track(dane, rep, 'MS 230')
    elif dane.get('klej_typ') == "bezprzesuwny":
        rep.write(f"Klejenie {nazwa_okladziny} należy przeprowadzić przy użyciu kleju do parkietu **WAKOL PU 225** (szpachla B11, zużycie: 1250 g/m²).")
        write_and_track(dane, rep, 'PU 225')
    else:
        rep.write(f"Klejenie {nazwa_okladziny} należy przeprowadzić przy użyciu kleju do parkietu **WAKOL MS 230** (szpachla B13, zużycie: 1350 g/m²).")
        write_and_track(dane, rep, 'MS 230')
        
    render_potrzebne_materialy(dane, rep)

# --- SEKCJA: DESKA LITA ---
def generate_report_deska_lita(dane, rep):
    render_wspolne_dane_optyczne(dane, rep)
    if dane['substrate'] == "jastrych cementowy":
        rep.write("**Aby bezpiecznie kleić podłogę drewnianą na jastrychu cementowym, jego wytrzymałość na ścinanie musi wynosić między 1,5 a 2,0 N/mm² a wilgotność nie może przekraczać 1,8% CM. (z ogrzewaniem podłogowym max. 1,5% CM).**")
    elif dane['substrate'] == "jastrych anhydrytowy":
        rep.write("**Aby bezpiecznie kleić podłogę drewnianą na jastrychu anhydrytowym zgodnie z wytycznymi ITB, jego wytrzymałość na ścinanie musi wynosić 2,0 N/mm² a wilgotność nie może przekraczać 0,5% CM. (z ogrzewaniem podłogowym max. 0,3% CM).**")
    rep.markdown("#### **II. Zalecenia techniczne (Deska Lita)**")
    render_wspolne_zalecenia_podloze(dane, rep)
    used_d3004 = render_chemia_deska_lita(dane, rep)

    if dane['needs_levelling'] == "TAK" and dane.get('bruzdowane_wybor') != "masa samorozlewna":
        if not used_d3004:
            rep.write("* Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu **WAKOL D 3045**. Aplikować równomiernie za pomocą wałka. Zużycie wynosi **ok. 150 g/m²**. **Czas schnięcia 1 godzina**.")
        write_and_track(dane, rep, 'Z 625')

    rep.write("**c) klejenie okładziny:**")
    if dane.get('klej_typ') == "bezprzesuwny":
        rep.write("Klejenie podłogi z deski litej należy przeprowadzić przy użyciu kleju **WAKOL PU 225** (szpachla B11, zużycie: 1250 g/m²).")
        write_and_track(dane, rep, 'PU 225')
    else:
        rep.write("Klejenie podłogi z deski litej należy przeprowadzić przy użyciu kleju polimerowego twardo-elastycznego **WAKOL MS 260** (szpachla B13, zużycie: 1350 g/m²).")
        write_and_track(dane, rep, 'MS 260')
    render_potrzebne_materialy(dane, rep)

# --- SEKCJA: LVT CIENKIE ---
def generate_report_lvt_cienkie(dane, rep):
    if dane['needs_levelling'] == "NIE" and dane['already_levelled'] == "NIE":
        rep.error("BŁĄD: Pod okładzinę LVT cienkie wymagane jest wyrównanie podłoża. Poinformuj klienta o konieczności wylania masy!")
        return
        
    render_wspolne_dane_optyczne(dane, rep)
    rep.markdown("#### **II. Zalecenia techniczne (LVT Cienkie)**")
    
    if dane['already_levelled'] == "TAK":
        rep.write("**a) klejenie okładziny:**")
        rep.write("Klejenie podłogi winylowej (LVT) należy przeprowadzić przy użyciu kleju WAKOL D 3318 (szpachla TKB A2, zużycie: 350 g/m²). · Czas wstępnego odparowania: ok. 5 - 10 minut. · Czas układania: ok. 10 minut")
        write_and_track(dane, rep, 'D 3318')
        render_potrzebne_materialy(dane, rep)
        return

    render_wspolne_zalecenia_podloze(dane, rep)
    used_d3004 = render_wspolna_chemia(dane, rep)

    if dane['needs_levelling'] == "TAK" and dane.get('bruzdowane_wybor') != "masa samorozlewna":
        if not used_d3004:
            rep.write("* Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu **WAKOL D 3045**. Aplikować równomiernie za pomocą wałka. Zużycie wynosi **ok. 150 g/m²**. **Czas schnięcia 1 godzina**.")
        write_and_track(dane, rep, 'Z 675')

    rep.write("**c) klejenie okładziny:**")
    rep.write("Klejenie podłogi winylowej (LVT) należy przeprowadzić przy użyciu kleju WAKOL D 3318 (szpachla TKB A2, zużycie: 350 g/m²). · Czas wstępnego odparowania: ok. 5 - 10 minut. · Czas układania: ok. 10 minut")
    write_and_track(dane, rep, 'D 3318')
    render_potrzebne_materialy(dane, rep)

# --- SEKCJA: LVT GRUBE ---
def generate_report_lvt_grube(dane, rep):
    render_wspolne_dane_optyczne(dane, rep)
    rep.markdown("#### **II. Zalecenia techniczne (LVT Grube z twardym rdzeniem)**")
    render_wspolne_zalecenia_podloze(dane, rep)
    used_d3004 = render_chemia_deska_warstwowa(dane, rep)

    if dane['needs_levelling'] == "TAK" and dane.get('bruzdowane_wybor') != "masa samorozlewna":
        if not used_d3004:
            rep.write("* Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu **WAKOL D 3045**. Aplikować równomiernie za pomocą wałka. Zużycie wynosi **ok. 150 g/m²**. **Czas schnięcia 1 godzina**.")
        write_and_track(dane, rep, 'Z 675')

    rep.write("**c) klejenie okładziny:**")
    if dane.get('klej_typ') == "bezprzesuwny":
        rep.write("Klejenie podłogi LVT z twardym rdzeniem należy przeprowadzić przy użyciu kleju **WAKOL PU 225** (szpachla B11, zużycie: 1250 g/m²).")
        write_and_track(dane, rep, 'PU 225')
    else:
        rep.write("Klejenie podłogi LVT z twardym rdzeniem należy przeprowadzić przy użyciu kleju **WAKOL MS 230** (szpachla B13, zużycie: 1350 g/m²).")
        write_and_track(dane, rep, 'MS 230')
    render_potrzebne_materialy(dane, rep)

# --- SEKCJA: PCV W ROLCE ---
def generate_report_pcv_w_rolce(dane, rep):
    if dane['needs_levelling'] == "NIE" and dane['already_levelled'] == "NIE":
        rep.error("BŁĄD: Pod okładzinę PCV w rolce wymagane jest wyrównanie podłoża. Poinformuj klienta o konieczności wylania masy!")
        return
        
    render_wspolne_dane_optyczne(dane, rep)
    rep.markdown("#### **II. Zalecenia techniczne (PCV w rolce)**")
    
    if dane['already_levelled'] == "TAK":
        rep.write("**a) klejenie okładziny PCV:**")
        rep.write("Klejenie wykładziny PCV w rolce należy przeprowadzić przy użyciu kleju WAKOL D 3307 (szpachla TKB A2, zużycie: 300 – 330 g/m²). · Czas wstępnego odparowania: ok. 10 - 20 minut. · Czas układania: ok. 15 - 20 minut")
        render_potrzebne_materialy(dane, rep)
        return

    render_wspolne_zalecenia_podloze(dane, rep)
    used_d3004 = render_wspolna_chemia(dane, rep)

    if dane['needs_levelling'] == "TAK" and dane.get('bruzdowane_wybor') != "masa samorozlewna":
        if not used_d3004:
            rep.write("* Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu **WAKOL D 3045**. Aplikować równomiernie za pomocą wałka. Zużycie wynosi **ok. 150 g/m²**. **Czas schnięcia 1 godzina**.")
        write_and_track(dane, rep, 'Z 675')

    rep.write("**c) klejenie okładziny PCV:**")
    rep.write("Klejenie wykładziny PCV w rolce należy przeprowadzić przy użyciu kleju WAKOL D 3307 (szpachla TKB A2, zużycie: 300 – 330 g/m²). · Czas wstępnego odparowania: ok. 10 - 20 minut. · Czas układania: ok. 15 - 20 minut")
    render_potrzebne_materialy(dane, rep)

# --- SEKCJA: WYKŁADZINA DYWANOWA ---
def generate_report_wykladzina_dywanowa(dane, rep):
    if dane['needs_levelling'] == "NIE" and dane['already_levelled'] == "NIE":
        rep.error("BŁĄD: Pod wykładzinę dywanową wymagane jest wyrównanie podłoża. Poinformuj klienta o konieczności wylania masy!")
        return
        
    render_wspolne_dane_optyczne(dane, rep)
    rep.markdown("#### **II. Zalecenia techniczne (Wykładzina dywanowa)**")
    
    if dane['already_levelled'] == "TAK":
        rep.write("**a) klejenie wykładziny tekstylnej:**")
        rep.write("Klejenie wykładziny tekstylnej należy przeprowadzić przy użyciu kleju WAKOL D 3308 (szpachla TKB B1 400-450 g/m²). · Czas wstępnego odparowania: ok. 5-10 minut. · Czas otwarty kleju ok. 10-15 minut")
        render_potrzebne_materialy(dane, rep)
        return

    render_wspolne_zalecenia_podloze(dane, rep)
    used_d3004 = render_wspolna_chemia(dane, rep)

    if dane['needs_levelling'] == "TAK" and dane.get('bruzdowane_wybor') != "masa samorozlewna":
        if not used_d3004:
            rep.write("* Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu **WAKOL D 3045**. Aplikować równomiernie za pomocą wałka. Zużycie wynosi **ok. 150 g/m²**. **Czas schnięcia 1 godzina**.")
        write_and_track(dane, rep, 'Z 675')

    rep.write("**c) klejenie wykładziny tekstylnej:**")
    rep.write("Klejenie wykładziny tekstylnej należy przeprowadzić przy użyciu kleju WAKOL D 3308 (szpachla TKB B1 400-450 g/m²). · Czas wstępnego odparowania: ok. 5-10 minut. · Czas otwarty kleju ok. 10-15 minut")
    render_potrzebne_materialy(dane, rep)

# ==========================================
# EXPORT DO DOCX I PDF
# ==========================================
def _add_docx_footer(doc):
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False

    # Wyczyść element stopki
    ft_elem = footer._element
    for child in list(ft_elem):
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag in ('p', 'tbl', 'sdt'):
            ft_elem.remove(child)

    # Niebieski pasek jako górna ramka paragrafu
    p_border = OxmlElement('w:p')
    pPr_b = OxmlElement('w:pPr')
    pBdr = OxmlElement('w:pBdr')
    top_b = OxmlElement('w:top')
    top_b.set(qn('w:val'), 'single')
    top_b.set(qn('w:sz'), '24')
    top_b.set(qn('w:space'), '4')
    top_b.set(qn('w:color'), '005293')
    pBdr.append(top_b)
    pPr_b.append(pBdr)
    p_border.append(pPr_b)
    ft_elem.append(p_border)

    # Pomocnicze funkcje do budowania XML
    def make_run(text, bold=False, size_half=16, color=None):
        r = OxmlElement('w:r')
        rPr = OxmlElement('w:rPr')
        if bold:
            rPr.append(OxmlElement('w:b'))
        sz = OxmlElement('w:sz')
        sz.set(qn('w:val'), str(size_half))
        rPr.append(sz)
        if color:
            cl = OxmlElement('w:color')
            cl.set(qn('w:val'), color)
            rPr.append(cl)
        r.append(rPr)
        t = OxmlElement('w:t')
        t.text = text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        r.append(t)
        return r

    # Trzy kolumny przez tabstopy — niezawodne w stopkach Word
    # A4 17cm użytkowe = 9639 twipsów; center=4819, right=9639
    TAB_C = '4819'
    TAB_R = '9639'

    def make_tab_row(left, center, right, is_title=False):
        p = OxmlElement('w:p')
        pPr = OxmlElement('w:pPr')
        tabs_el = OxmlElement('w:tabs')
        for val, pos in [('center', TAB_C), ('right', TAB_R)]:
            t = OxmlElement('w:tab')
            t.set(qn('w:val'), val)
            t.set(qn('w:pos'), pos)
            tabs_el.append(t)
        pPr.append(tabs_el)
        p.append(pPr)
        sz = 14 if is_title else 16
        col = '005293' if is_title else None
        bd = is_title
        for i, txt in enumerate([left, center, right]):
            if i > 0:
                r_tab = OxmlElement('w:r')
                r_tab.append(OxmlElement('w:tab'))
                p.append(r_tab)
            if txt:
                p.append(make_run(txt, bold=bd, size_half=sz, color=col))
        return p

    footer_rows = [
        ('ZARZĄD',              'ADRES FIRMY',                       'DANE REJESTROWE',  True),
        ('Stephane Moulin',     'ul. Sławęcińska 16, Macierzysz',    'KRS: 0000163623',  False),
        ('Andreas Taddäus Ziobro', '05-850 Ożarów Mazowiecki',       'NIP: 118-13-89-053', False),
        ('biuro@loba-wakol.pl', 'tel.: +48 22 436 24 20',            'REGON: 013285030', False),
        ('',                    'fax: +48 22 436 24 21',             '',                 False),
    ]
    for left, center, right, is_title in footer_rows:
        ft_elem.append(make_tab_row(left, center, right, is_title))

    ft_elem.append(OxmlElement('w:p'))

def _add_docx_header(doc, data_badania_str='', autor_str=''):
    from docx.shared import Inches, Cm, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    import os

    section = doc.sections[0]
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(4.5)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)

    # Pusty nagłówek Word na wszystkich stronach (brak miejsca na nagłówek)
    hdr = section.header
    hdr_el = hdr._element
    for child in list(hdr_el):
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag in ('p', 'tbl', 'sdt'):
            hdr_el.remove(child)
    hdr_el.append(OxmlElement('w:p'))

    # Logo + dane firmy jako tabela w TREŚCI dokumentu (pierwsza strona naturalnie)
    tbl = doc.add_table(rows=1, cols=2)
    tbl_el = tbl._tbl
    tbl_pr = tbl_el.find(qn('w:tblPr'))
    if tbl_pr is None:
        tbl_pr = OxmlElement('w:tblPr')
        tbl_el.insert(0, tbl_pr)
    tbl_bdr = OxmlElement('w:tblBorders')
    for bn in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        b = OxmlElement(f'w:{bn}')
        b.set(qn('w:val'), 'none')
        tbl_bdr.append(b)
    tbl_pr.append(tbl_bdr)

    left_cell = tbl.rows[0].cells[0]
    right_cell = tbl.rows[0].cells[1]

    # Lewa komórka: logo
    para_logo = left_cell.paragraphs[0]
    para_logo.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if os.path.exists('loba_wakol_logo.png'):
        try:
            para_logo.add_run().add_picture('loba_wakol_logo.png', width=Inches(3.5))
        except:
            pass

    # Prawa komórka: dane firmy
    info_lines = [
        ('Loba-Wakol Polska Sp. z o.o.', True, 14),
        ('ul. Sławęcińska 16, Macierzysz', False, 9),
        ('05-850 Ożarów Mazowiecki', False, 9),
        (f'data: {data_badania_str}', False, 9),
        (f'autor: {autor_str}', False, 9),
        ('tel.: +48 22 436 24 20  |  fax: +48 22 436 24 21', False, 9),
        ('biuro@loba-wakol.pl', False, 9),
    ]
    for i, (text, bold, size) in enumerate(info_lines):
        para = right_cell.paragraphs[0] if i == 0 else right_cell.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = para.add_run(text)
        run.bold = bold
        run.font.size = Pt(size)
        if bold:
            run.font.color.rgb = RGBColor(0x00, 0x52, 0x93)

    # Niebieski separator po tabeli nagłówka
    sep = doc.add_paragraph()
    sep_pPr = sep._p.get_or_add_pPr()
    sep_bdr = OxmlElement('w:pBdr')
    bot = OxmlElement('w:bottom')
    bot.set(qn('w:val'), 'single')
    bot.set(qn('w:sz'), '12')
    bot.set(qn('w:space'), '4')
    bot.set(qn('w:color'), '005293')
    sep_bdr.append(bot)
    sep_pPr.append(sep_bdr)


def generate_docx(md_text, data_badania_str='', autor_str=''):
    doc = Document()
    # Usuń domyślny pusty paragraf
    for p in list(doc.paragraphs):
        p._element.getparent().remove(p._element)

    # Nagłówek (logo + dane firmy) jako treść — PRZED resztą
    _add_docx_header(doc, data_badania_str, autor_str)

    for line in md_text.split('\n\n'):
        line = line.strip()
        if not line: continue
        if line.startswith('#### '):
            p = doc.add_heading(level=2)
            _add_runs(p, line.replace('#### ', ''))
        elif line.startswith('### '):
            p = doc.add_heading(level=1)
            _add_runs(p, line.replace('### ', ''))
        elif line.startswith('* ') or line.startswith('- '):
            p = doc.add_paragraph(style='List Bullet')
            _add_runs(p, line[2:])
        else:
            p = doc.add_paragraph()
            _add_runs(p, line)

    _add_docx_footer(doc)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

def _add_runs(p, text):
    parts = text.split('**')
    for i, part in enumerate(parts):
        run = p.add_run(part)
        if i % 2 != 0:
            run.bold = True

class WakolPDF(FPDF):
    def __init__(self, data_badania_str, autor_str):
        super().__init__()
        self.data_badania_str = data_badania_str
        self.autor_str = autor_str

    def header(self):
        if self.page_no() == 1:
            try:
                import os
                if os.path.exists('loba_wakol_logo.png'):
                    self.image('loba_wakol_logo.png', x=10, y=8, w=90)
            except:
                pass
            try:
                self.set_font('Arial', 'B', 16)
            except:
                pass
            self.cell(0, 10, 'Loba-Wakol Polska Sp. z o.o.', ln=True, align='R')
            try:
                self.set_font('Arial', '', 9)
            except:
                pass
            label_x = 140
            value_x = 155
            
            def print_row(lbl, val):
                self.set_x(label_x)
                self.cell(15, 4, lbl)
                self.set_x(value_x)
                self.cell(0, 4, val, ln=True)

            print_row("adres:", "Sławęcińska 16, Macierzysz")
            print_row("", "05-850 Ożarów Mazowiecki")
            print_row("data:", self.data_badania_str)
            print_row("autor:", self.autor_str)
            print_row("telefon:", "+48 22 436 24 20")
            print_row("telefax:", "+48 22 436 24 21")
            print_row("e-mail:", "biuro@loba-wakol.pl")
            print_row("strona:", f"{self.page_no()} z {{nb}}")
            self.set_y(60)
        else:
            try:
                self.set_font('Arial', '', 9)
            except:
                pass
            self.cell(0, 10, f"strona {self.page_no()} z {{nb}}", ln=True, align='L')
            self.set_y(20)

    def footer(self):
        footer_y = -32
        try:
            self.set_font('Arial', '', 7)
        except:
            pass

        # Niebieska linia
        self.set_y(footer_y)
        self.set_draw_color(0, 82, 147)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)

        col1_x = 10
        col2_x = 75
        col3_x = 150
        row_y = self.get_y()

        # Kolumna 1: ZARZĄD
        try: self.set_font('Arial', 'B', 6)
        except: pass
        self.set_xy(col1_x, row_y); self.cell(60, 3, "ZARZĄD", ln=True)
        try: self.set_font('Arial', '', 7)
        except: pass
        self.set_x(col1_x); self.cell(60, 3, "Stephane Moulin", ln=True)
        self.set_x(col1_x); self.cell(60, 3, "Andreas Taddaeus Ziobro", ln=True)
        self.set_x(col1_x); self.cell(60, 3, "biuro@loba-wakol.pl", ln=True)

        # Kolumna 2: ADRES FIRMY
        try: self.set_font('Arial', 'B', 6)
        except: pass
        self.set_xy(col2_x, row_y); self.cell(70, 3, "ADRES FIRMY", ln=True)
        try: self.set_font('Arial', '', 7)
        except: pass
        self.set_x(col2_x); self.cell(70, 3, "ul. Slawecinska 16, Macierzysz", ln=True)
        self.set_x(col2_x); self.cell(70, 3, "05-850 Ozarow Mazowiecki", ln=True)
        self.set_x(col2_x); self.cell(70, 3, "tel.: +48 22 436 24 20 | fax: +48 22 436 24 21", ln=True)

        # Kolumna 3: DANE REJESTROWE
        try: self.set_font('Arial', 'B', 6)
        except: pass
        self.set_xy(col3_x, row_y); self.cell(50, 3, "DANE REJESTROWE", ln=True)
        try: self.set_font('Arial', '', 7)
        except: pass
        self.set_x(col3_x); self.cell(50, 3, "KRS: 0000163623", ln=True)
        self.set_x(col3_x); self.cell(50, 3, "NIP: 118-13-89-053", ln=True)
        self.set_x(col3_x); self.cell(50, 3, "REGON: 013285030", ln=True)
        
        try:
            import urllib.request
            if not __import__('os').path.exists('wakol_logo.png'):
                urllib.request.urlretrieve('https://www.wakol.com/fileadmin/templates/images/wakol_logo.png', 'wakol_logo.png')
            self.image('wakol_logo.png', x=160, y=-25, w=35)
        except:
            pass

def generate_pdf(md_text, data_badania_str, autor_str):
    pdf = WakolPDF(data_badania_str, autor_str)
    pdf.alias_nb_pages()
    import os
    try:
        if os.path.exists(r'C:\Windows\Fonts\arial.ttf'):
            pdf.add_font('Arial', '', r'C:\Windows\Fonts\arial.ttf')
            pdf.add_font('Arial', 'B', r'C:\Windows\Fonts\arialbd.ttf')
        elif os.path.exists('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
            pdf.add_font('Arial', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
            pdf.add_font('Arial', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
        else:
            # Download a very reliable font source (Google Fonts - Roboto)
            import urllib.request
            url_reg = 'https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Regular.ttf'
            url_bold = 'https://github.com/googlefonts/roboto/raw/main/src/hinted/Roboto-Bold.ttf'
            if not os.path.exists('Roboto-Regular.ttf'):
                urllib.request.urlretrieve(url_reg, 'Roboto-Regular.ttf')
            if not os.path.exists('Roboto-Bold.ttf'):
                urllib.request.urlretrieve(url_bold, 'Roboto-Bold.ttf')
            pdf.add_font('Arial', '', 'Roboto-Regular.ttf')
            pdf.add_font('Arial', 'B', 'Roboto-Bold.ttf')
        pdf.set_font('Arial', size=11)
    except Exception as e:
        import streamlit as st
        st.error(f"Błąd ładowania czcionki: {str(e)}")
        pdf.set_font('helvetica', size=11)
        
    pdf.set_auto_page_break(auto=True, margin=38)
    pdf.add_page()
    for line in md_text.split('\n\n'):
        line = line.strip()
        if not line: continue
        
        # Proste parsowanie nagłówków
        if line.startswith('#### '):
            pdf.set_font(pdf.font_family, 'B', 14)
            line = line.replace('#### ', '').replace('**', '')
            pdf.multi_cell(0, 8, txt=line)
            pdf.set_font(pdf.font_family, '', 11)
        elif line.startswith('### '):
            pdf.set_font(pdf.font_family, 'B', 16)
            line = line.replace('### ', '').replace('**', '')
            pdf.multi_cell(0, 10, txt=line)
            pdf.set_font(pdf.font_family, '', 11)
        else:
            # Ręczna obsługa pogrubień dla FPDF
            if '**' in line:
                try:
                    pdf.multi_cell(0, 6, txt=line, markdown=True)
                except TypeError:
                    pdf.multi_cell(0, 6, txt=line.replace('**', ''))
            else:
                pdf.multi_cell(0, 6, txt=line)
        pdf.ln(2)
        
    output = pdf.output(dest='S')
    if type(output) is str:
        return output.encode('latin-1')
    return bytes(output)

# ==========================================
# 3. INTERFEJS UŻYTKOWNIKA (FORMULARZ)
# ==========================================

st.title("📄 Generator Protokołu Oględzin")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        nazwa_klienta = st.text_input("Nazwa Klienta", "Jan Kowalski")
        miejscowosc = st.text_input("Miejscowość", "Huta Dłutowska")
        adres = st.text_input("Ulica i nr", "ul. Pabianicka 15")
    with col2:
        autor = st.text_input("Autor protokołu", "Przemysław Tyszko")
        data_badania = st.date_input("Data badania", date.today())

st.divider()

flooring_type = st.selectbox("Wybierz rodzaj okładziny (Sekcja):", ["deska warstwowa", "podłoga laminowana", "deska lita", "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"])

klej_typ = None
if flooring_type in ["deska warstwowa", "podłoga laminowana", "deska lita", "lvt grube z twardym rdzeniem"]:
    klej_typ = st.radio("Rodzaj kleju:", ["elastyczny", "bezprzesuwny"], horizontal=True)

st.markdown(f"### Wywiad Techniczny dla: **{flooring_type.upper()}**")

substrate = st.selectbox("1. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane (parkiet, deska, OSB)", "płytki ceramiczne", "masa samorozlewna"])
area_m2 = st.number_input("Powierzchnia inwestycji (m²):", min_value=1.0, step=1.0, format="%.1f", value=None)
substrate_age_val = st.number_input("Wiek podłoża (podaj ilość miesięcy):", min_value=0.5, step=0.5, format="%.1f", value=None)

st.write("2. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True)
heating_info = ""; heating_curing_done = None; h_type = None; bruzdowane_wybor = None
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne (powierzchniowe)", "elektryczne (głębokie)", "płyta fundamentowa grzewcza"])
    if h_type == "bruzdowane":
        bruzdowane_wybor = st.radio("Wybierz technologię (ogrzewanie bruzdowane):", ["masa samorozlewna", "płyta RP"], horizontal=True)
        
    if h_type != "bruzdowane":
        st.write("❓ Czy został przeprowadzony proces wygrzewania zgodnie z protokołem?")
        heating_curing_done = st.radio("Proces wygrzewania:", ["TAK", "NIE"], index=1, horizontal=True)
    else:
        heating_curing_done = "TAK"
    mapping = {"wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna", "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana", "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie", "elektryczne (powierzchniowe)": "instalacja ogrzewania podłogowego elektryczna, powierzchniowa", "elektryczne (głębokie)": "instalacja ogrzewania podłogowego elektryczna, umieszczona głęboko w podłożu", "płyta fundamentowa grzewcza": "ogrzewanie realizowane poprzez płytę fundamentową grzewczą"}
    heating_info = mapping.get(h_type, h_type)

st.write("3. Czy podłoże wymaga wyrównania (masy)?")
leveling_thickness = 0
already_levelled = "NIE"

if h_type == "bruzdowane" and bruzdowane_wybor == "masa samorozlewna":
    st.info("Wyrównanie jest wymuszone przez technologię 'masa samorozlewna' na ogrzewaniu bruzdowanym.")
    needs_levelling = "TAK"
    leveling_thickness = 5
    st.info("Grubość masy została automatycznie ustalona na 5 mm.")
else:
    needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True)
    if needs_levelling == "TAK":
        leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=None)
    elif flooring_type in ["wykładzina dywanowa", "pcv w rolce", "lvt cienkie"]:
        st.warning("Pod wybraną okładzinę wymagane jest wyrównanie podłoża.")
        already_levelled = st.radio("Czy podłoże zostało już wcześniej wyrównane?", ["TAK", "NIE"], index=1, horizontal=True)


st.write("4. Czy dylatacje obwodowe zachowane prawidłowo?")
dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=0, horizontal=True)
st.write("5. Czy występują klawiszujące dylatacje pozorne?")
cracks_klaw = st.radio("Klawiszowanie pozorne:", ["TAK", "NIE"], index=1, horizontal=True)
klaw_meters = st.number_input("Ilość mb klawiszujących:", min_value=0.1, step=0.1, value=None) if cracks_klaw == "TAK" else 0.0
st.write("6. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia do zespolenia:", ["TAK", "NIE"], index=1, horizontal=True)
pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", min_value=0.1, step=0.1, value=None) if cracks_pek == "TAK" else 0.0
st.write("7. Czy są ubytki bądź zdegradowane fragmenty wymagające wypełnienia masą naprawczą?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True)
hole_details = ""
holes_depth = None
if holes == "TAK":
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1: h_depth = st.number_input("Grubość (cm)", min_value=0.1, value=None)
    with col_h2: h_width = st.number_input("Szerokość (cm)", min_value=0.1, value=None)
    with col_h3: h_length = st.number_input("Długość (cm)", min_value=0.1, value=None)
    if h_depth and h_width and h_length: hole_details = f" o wymiarach ok. {h_length}x{h_width} cm i grubości {h_depth} cm"
    holes_depth = h_depth

st.write("8. Rodzaj wentylacji")
ventilation_type = st.radio("Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True)

col_w1, col_w2 = st.columns(2)
with col_w1: temp_air = st.number_input("9. Temperatura powietrza (°C)", step=0.5, value=None)
with col_w2: hum_air = st.number_input("10. Wilgotność powietrza (%)", step=1.0, value=None)
moisture = st.number_input("11. Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)

# --- LOGIKA NORM I BARIER ---
limit = 1.5 if substrate == "jastrych cementowy" and heating_exists == "TAK" else 1.8 if substrate == "jastrych cementowy" else 0.3 if substrate == "jastrych anhydrytowy" and heating_exists == "TAK" else 0.5 if substrate == "jastrych anhydrytowy" else 1.5
barrier_max = 2.5 if heating_exists == "TAK" else 3.5

# --- TESTY MECHANICZNE I WYTRZYMAŁOŚĆ ---
st.write("### 12. Testy mechaniczne i Wytrzymałość")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: test_hammer = st.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t2: test_ripper = st.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t3: test_brush = st.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)

st.write("**Badanie PressoMess**")
presso_results = []
for i in range(6):
    presso_results.append(st.number_input(f"Próba {i+1} (N/mm²)", min_value=0.0, step=0.1, key=f"p_{i}", value=None))
strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości podłoża:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

decision_after_cure = None
needs_drying_action = False
if moisture is not None and moisture > limit:
    needs_drying_action = True
    opt_dry = "przeprowadzenie procesu wygrzewania" if (heating_exists == "TAK" and heating_curing_done == "NIE") else "dalsze osuszanie"
    if h_type == "bruzdowane":
        st.warning(f"Podłoże jest zbyt wilgotne. Konieczność doprowadzenia do normatywnego poziomu wilgoci ({limit}% CM) przed przystąpieniem do dalszych prac.")
        decision_after_cure = "dalsze osuszanie"
    elif substrate == "jastrych anhydrytowy":
        decision_after_cure = opt_dry
    elif strength_val == 1:
        st.warning("Podłoże bardzo słabe — bariera przeciwwilgociowa niedostępna. Wymagane doprowadzenie do normatywnego poziomu wilgoci przed gruntowaniem PS 275.")
        decision_after_cure = opt_dry
    else:
        barrier_max = 2.5 if heating_exists == "TAK" else 3.5
        if moisture <= barrier_max:
            decision_after_cure = st.radio("Postępowanie z podwyższoną wilgocią:", ["Wykonanie bariery przeciwwilgociowej", opt_dry], horizontal=True)
            needs_drying_action = (decision_after_cure != "Wykonanie bariery przeciwwilgociowej")
        else:
            decision_after_cure = opt_dry

# PAKOWANIE DANYCH DO SŁOWNIKA DLA FUNKCJI GENERUJĄCYCH
dane_protokolu = {
    "flooring_type": flooring_type,
    "substrate": substrate,
    "area_m2": area_m2,
    "klej_typ": klej_typ,
    "substrate_age_val": substrate_age_val,
    "heating_exists": heating_exists,
    "heating_info": heating_info,
    "heating_curing_done": heating_curing_done,
    "h_type": h_type,
    "bruzdowane_wybor": bruzdowane_wybor,
    "needs_levelling": needs_levelling,
    "leveling_thickness": leveling_thickness,
    "already_levelled": already_levelled,
    "dilatations_obw_ok": dilatations_obw_ok,
    "cracks_klaw": cracks_klaw,
    "klaw_meters": klaw_meters,
    "cracks_pek": cracks_pek,
    "pek_meters": pek_meters,
    "holes": holes,
    "holes_depth": holes_depth if 'holes_depth' in locals() else None,
    "holes_width": h_width if 'h_width' in locals() else None,
    "holes_length": h_length if 'h_length' in locals() else None,
    "hole_details": hole_details,
    "ventilation_type": ventilation_type,
    "moisture": moisture,
    "limit": limit,
    "curing_not_done": (heating_exists == "TAK" and heating_curing_done == "NIE"),
    "is_moisture_neg": (moisture is not None and moisture > limit),
    "norm_val_bracket": f"({limit}% CM)",
    "decision_after_cure": decision_after_cure,
    "needs_drying_action": needs_drying_action,
    "test_hammer": test_hammer,
    "test_ripper": test_ripper,
    "test_brush": test_brush,
    "strength_labels": strength_labels,
    "strength_val": strength_val,
    "temp_air": temp_air,
    "hum_air": hum_air,
    "presso_results": presso_results
}

# --- GENEROWANIE PROTOKOŁU W ZALEŻNOŚCI OD WYBRANEJ OKŁADZINY ---
if st.button(f"GENERUJ PROTOKÓŁ OGLĘDZIN DLA: {flooring_type.upper()}", type="primary", use_container_width=True):
    if moisture is None:
        st.error("Proszę podać wilgotność podłoża!")
    else:
        st.divider()
        insert_header()
        
        rep = ReportBuilder()
        
        # Generowanie nagłówka do DOC/PDF
        tytul = f"Dotyczy: Protokół z oględzin inwestycji w obiekcie:\nAdres: {adres}, {miejscowosc}\nDla: {nazwa_klienta}\n\nSzanowni Państwo,\n\nW dniu {data_badania.strftime('%d.%m.%Y')} dokonano wstępnych oględzin i pomiarów wytrzymałości podłoża ({substrate}) oraz pomiaru wilgotności przed przyklejeniem okładziny ({flooring_type}).\n\n"
        rep.write(tytul)
        
        rep.markdown("#### **I. Oględziny i badania**")
        
        if flooring_type in ["deska warstwowa", "podłoga laminowana"]:
            generate_report_deska_warstwowa(dane_protokolu, rep)
        elif flooring_type == "deska lita":
            generate_report_deska_lita(dane_protokolu, rep)
        elif flooring_type == "lvt cienkie":
            generate_report_lvt_cienkie(dane_protokolu, rep)
        elif flooring_type == "pcv w rolce":
            generate_report_pcv_w_rolce(dane_protokolu, rep)
        elif flooring_type == "wykładzina dywanowa":
            generate_report_wykladzina_dywanowa(dane_protokolu, rep)
        elif flooring_type == "lvt grube z twardym rdzeniem":
            generate_report_lvt_grube(dane_protokolu, rep)
        else:
            rep.error("Nieobsługiwany typ okładziny.")
            
        rep.write("\n**Prosimy o zapoznanie się z kartami technicznymi zalecanych produktów WAKOL.**\n\nPodstawą naszego zalecenia jest stosowanie i prawidłowa obróbka wszystkich wymienionych materiałów firmy WAKOL w podanej kolejności, przestrzegając reguł rzemiosła i obowiązujących norm oraz instrukcji.\n\nW przypadku jakichkolwiek pytań lub wątpliwości proszę o kontakt pod numer telefonu: 603 214 218\n\nZ poważaniem,\n\nLoba-Wakol Polska Sp. z o.o.\n" + autor)
        
        # Wyświetlenie na ekranie (cel użytkownika)
        st.markdown(rep.get_markdown())

        st.markdown("""
<div style="font-family: Arial, sans-serif; color: #333; max-width: 800px;">
    <div style="width: 100%; height: 4px; background-color: #005293; margin-bottom: 20px;"></div>
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 25px;">
        <tr>
            <td style="width: 20%; text-align: left; vertical-align: middle;">
                <img src="https://www.loba-wakol.pl/fileadmin/templates/images/loba_logo.png" alt="Loba" style="height: 50px; width: auto; display: block;">
            </td>
            <td style="width: 60%; text-align: center; vertical-align: middle;">
                <h1 style="font-size: 12.5pt; margin: 0; color: #005293; text-transform: uppercase; white-space: nowrap; letter-spacing: 0.2px;">
                    LOBA-WAKOL POLSKA SPÓŁKA Z O.O.
                </h1>
            </td>
            <td style="width: 20%; text-align: right; vertical-align: middle;">
                <img src="https://www.loba-wakol.pl/fileadmin/templates/images/wakol_logo.png" alt="Wakol" style="height: 50px; width: auto; display: block; margin-left: auto;">
            </td>
        </tr>
    </table>
    <div style="border-top: 1px solid #005293; padding-top: 15px;">
        <table style="width: 100%; font-size: 9pt; line-height: 1.5; border-collapse: collapse;">
            <tr>
                <td style="width: 33%; vertical-align: top;">
                    <span style="color: #005293; font-size: 8pt; font-weight: bold; display: block; margin-bottom: 4px; text-transform: uppercase;">ZARZĄD</span>
                    <strong>Stephane Moulin</strong><br>
                    <strong>Andreas Taddäus Ziobro</strong><br>
                    <a href="mailto:biuro@loba-wakol.pl" style="color: #005293; text-decoration: none;">biuro@loba-wakol.pl</a>
                </td>
                <td style="width: 34%; vertical-align: top; text-align: center;">
                    <span style="color: #005293; font-size: 8pt; font-weight: bold; display: block; margin-bottom: 4px; text-transform: uppercase;">ADRES FIRMY</span>
                    ul. Sławęcińska 16, Macierzysz<br>
                    05-850 Ożarów Mazowiecki<br>
                    tel.: +48 22 436 24 20<br>
                    fax: +48 22 436 24 21
                </td>
                <td style="width: 33%; vertical-align: top; text-align: right;">
                    <span style="color: #005293; font-size: 8pt; font-weight: bold; display: block; margin-bottom: 4px; text-transform: uppercase;">DANE REJESTROWE</span>
                    KRS: 0000163623<br>
                    NIP: 118-13-89-053<br>
                    REGON: 013285030
                </td>
            </tr>
        </table>
    </div>
</div>
""", unsafe_allow_html=True)

        st.divider()
        
        # Przyciski pobierania
        if EXPORTS_READY:
            col_d1, col_d2 = st.columns(2)
            
            safe_adres = adres.replace(' ', '_').replace('/', '_').replace('.', '')
            data_str = data_badania.strftime('%d-%m-%Y')
            safe_klient = nazwa_klienta.replace(' ', '_').replace('/', '_')
            base_filename = f"Protokol_Wakol_{safe_klient}_{safe_adres}_{data_str}"
            
            with col_d1:
                docx_file = generate_docx(rep.get_markdown(), data_badania.strftime('%d.%m.%Y'), autor)
                st.download_button(
                    label="📄 Pobierz jako plik Word (.docx)",
                    data=docx_file,
                    file_name=f"{base_filename}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            with col_d2:
                pdf_file = generate_pdf(rep.get_markdown(), data_badania.strftime('%d.%m.%Y'), autor)
                if pdf_file:
                    st.download_button(
                        label="📕 Pobierz jako plik PDF (.pdf)",
                        data=pdf_file,
                        file_name=f"{base_filename}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        else:
            st.error("⚠️ Brak bibliotek do generowania Word/PDF. Dodaj plik `requirements.txt` w swoim repozytorium na GitHubie z zawartością:\n```\npython-docx\nfpdf2\n```")
