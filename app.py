import streamlit as st
from datetime import date

# 1. KONFIGURACJA STRONY
st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="wide")

# --- NAGŁÓWEK FIRMOWY - TYLKO WAKOL ---
def insert_header():
    logo_wakol = "https://www.wakol.com/fileadmin/templates/images/wakol_logo.png"
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;">
        <div style="flex: 1;">
            <img src="{logo_wakol}" width="220">
            <div style="margin-top: 15px; font-size: 11px; color: #555; line-height: 1.4;">
                <b>Loba-Wakol Polska Sp. z o.o.</b><br>
                ul. Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki<br>
                tel.: +48 22 436 24 20 | fax: +48 22 436 24 21<br>
                KRS: 0000163623 | NIP: 118-13-89-053 | biuro@loba-wakol.pl
            </div>
        </div>
        <div style="flex: 1; text-align: right;">
            <div style="font-size: 18px; font-weight: bold; color: #000; margin-bottom: 5px;">
                PROTOKÓŁ TECHNICZNY
            </div>
            <div style="font-size: 14px; color: #333;">Anspruch verbindet</div>
        </div>
    </div>
    <br>
    """, unsafe_allow_html=True)

# --- DANE IDENTYFIKACYJNE ---
st.title("📄 Generator Protokołu Oględzin")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        inwestycja = st.text_input("Nazwa inwestycji / Obiekt", "Budynek mieszkalny")
        miejscowosc = st.text_input("Miejscowość", "Huta Dłutowska")
        adres = st.text_input("Ulica i nr", "ul. Pabianicka 15")
    with col2:
        klient = st.text_input("Szanowni Państwo (Klient)", "Szanowni Państwo")
        autor = st.text_input("Autor protokołu", "Przemysław Tyszko")
        data_badania = st.date_input("Data badania", date.today())

st.divider()

# --- WYWIAD TECHNICZNY ---
flooring_options = ["deska warstwowa (drewno, laminat itp.)", "deska lita", "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"]
flooring_type = st.selectbox("1. Rodzaj okładziny", flooring_options)
substrate = st.selectbox("2. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane (parkiet, deska, OSB)", "płytki ceramiczne", "masa samorozlewna"])
substrate_age_val = st.number_input("Wiek podłoża (podaj ilość miesięcy):", min_value=0.5, step=0.5, format="%.1f", value=None, placeholder="Wpisz ilość miesięcy...")

st.write("3. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
heating_info = ""; heating_curing_done = None
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne (powierzchniowe)", "elektryczne (głębokie)", "płyta fundamentowa grzewcza"])
    if h_type in ["wodne klasyczne", "płyta fundamentowa grzewcza"]:
        st.write("❓ Czy został przeprowadzony proces wygrzewania zgodnie z protokołem?")
        heating_curing_done = st.radio("Proces wygrzewania:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
    mapping = {"wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna", "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana", "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie", "elektryczne (powierzchniowe)": "instalacja ogrzewania podłogowego elektryczna, powierzchniowa", "elektryczne (głębokie)": "instalacja ogrzewania podłogowego elektryczna, umieszczona głęboko w podłożu", "płyta fundamentowa grzewcza": "ogrzewanie realizowane poprzez płytę fundamentową grzewczą"}
    heating_info = mapping.get(h_type, h_type)

st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
leveling_thickness = 0
if needs_levelling == "TAK": leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=None, placeholder="Wpisz mm...")

st.write("5. Czy dylatacje obwodowe zachowane prawidłowo?")
dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=0, horizontal=True, label_visibility="collapsed")
st.write("6. Czy występują klawiszujące dylatacje pozorne?")
cracks_klaw = st.radio("Klawiszowanie pozorne:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
klaw_meters = 0.0
if cracks_klaw == "TAK": klaw_meters = st.number_input("Ilość mb klawiszujących:", min_value=0.1, step=0.1, value=None, placeholder="Wpisz mb...")
st.write("7. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia do zespolenia:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
pek_meters = 0.0
if cracks_pek == "TAK": pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", min_value=0.1, step=0.1, value=None, placeholder="Wpisz mb...")
st.write("8. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
hole_details = ""
if holes == "TAK":
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1: h_depth = st.number_input("Głębokość (cm)", min_value=0.1, value=None)
    with col_h2: h_width = st.number_input("Szerokość (cm)", min_value=0.1, value=None)
    with col_h3: h_length = st.number_input("Długość (cm)", min_value=0.1, value=None)
    if h_depth and h_width and h_length: hole_details = f" o wymiarach ok. {h_length}x{h_width} cm i głębokości {h_depth} cm"

st.write("9. Rodzaj wentylacji")
ventilation_type = st.radio("Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True, label_visibility="collapsed")
col_w1, col_w2 = st.columns(2)
with col_w1: temp_air = st.number_input("10. Temperatura powietrza (°C)", step=0.5, value=None)
with col_w2: hum_air = st.number_input("11. Wilgotność powietrza (%)", step=1.0, value=None)
moisture = st.number_input("12. Poziom wilgoci podłoża (CM %)", placeholder="Wpisz wynik CM...", format="%.1f", value=None)

# --- TESTY MECHANICZNE ---
st.write("### Testy mechaniczne i Wytrzymałość")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: test_hammer = st.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t2: test_ripper = st.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t3: test_brush = st.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)
presso_results = []
for i in range(6): presso_results.append(st.number_input(f"Próba {i+1} (N/mm²)", min_value=0.0, step=0.1, key=f"p_{i}", value=None))
strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# --- LOGIKA NORM ---
if substrate == "jastrych cementowy": limit = 1.5 if heating_exists == "TAK" else 1.8
elif substrate == "jastrych anhydrytowy": limit = 0.3 if heating_exists == "TAK" else 0.5
else: limit = 1.5
barrier_max = 2.5 if heating_exists == "TAK" else 3.5
decision_after_cure = None
if moisture is not None and moisture > limit:
    # AKTUALIZACJA: Logika osuszanie vs wygrzewanie
    opt_dry = "przeprowadzenie procesu wygrzewania" if heating_exists == "TAK" else "dalsze osuszanie"
    if moisture <= barrier_max and not (strength_val == 1 and needs_levelling == "NIE"):
        decision_after_cure = st.radio("Postępowanie:", ["Wykonanie bariery przeciwwilgociowej", opt_dry], horizontal=True)
    else: decision_after_cure = opt_dry

# --- GENEROWANIE PROTOKOŁU ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None: st.error("Proszę podać wilgotność podłoża!")
    else:
        st.divider(); insert_header()
        st.write(f"**Data badania:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")
        st.markdown("#### **I. Oględziny i badania**")
        
        # Opis optyczny
        age_txt = f" (wiek: {substrate_age_val} mies.)" if substrate_age_val else ""
        heat_txt = f" Stwierdzono {heating_info}." if heating_exists == "TAK" else " Brak instalacji ogrzewania podłogowego."
        curing_txt = " Przeprowadzono proces wygrzewania zgodnie z protokołem." if heating_curing_done == "TAK" else " Brak protokołu wygrzewania." if heating_exists == "TAK" else ""
        obw_txt = " dylatacje pozorne zachowane prawidłowo." if dilatations_obw_ok == "TAK" else " Dylatacje obwodowe niezachowane prawidłowo."
        klaw_txt = f" Stwierdzono klawiszujące dylatacje pozorne ({klaw_meters} mb)." if cracks_klaw == "TAK" else " dylatacje pozorne nie klawiszują."
        pek_txt = f" Stwierdzono pęknięcia podłoża ({pek_meters} mb)." if cracks_pek == "TAK" else " Brak pęknięć podłoża."
        holes_txt = " Stwierdzono ubytki w podłożu." if holes == "TAK" else " Brak ubytków w podłożu."
        level_txt = f" Podłoże wymaga wyrównania (planowana grubość: {leveling_thickness} mm)." if needs_levelling == "TAK" else " Podłoże nie wymaga wyrównania."
        
        st.write(f"**a) oględziny optyczne:** Podłoże stanowi {substrate}{age_txt}. {heat_txt}{curing_txt}{obw_txt} {klaw_txt} {pek_txt} {holes_txt} {level_txt} Wentylacja: **{ventilation_type}**.")
        
        st.write(f"**b) badanie wytrzymałości:**")
        valid_p = [v for v in presso_results if v is not None and v > 0]
        if valid_p:
            st.write(f"**Wynik badania PressoMess:**")
            for i, val in enumerate(presso_results):
                if val: st.write(f"* Próba {i+1}: **{val} N/mm²**")
        st.write(f"* Ocena ogólna wytrzymałości: **{strength_labels[strength_val]}**")
        st.write(f"**c) badanie wilgotności:** Wynik **{moisture} % CM** (Norma: {limit} % CM)")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**a) przygotowanie podłoża:**")
        st.write("* **Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni!**")
        st.write("* **Dokładne odkurzenie**")
        
        # AKTUALIZACJA: Fraza doprowadzenie do normy
        if decision_after_cure in ["dalsze osuszanie", "przeprowadzenie procesu wygrzewania"]:
            st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci ({limit}% CM) poprzez {decision_after_cure}.**")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        total_cracks = (klaw_meters + pek_meters)
        moisture_prefix = f"**Po doprowadzeniu do normatywnego poziomu wilgoci tj. {limit}% CM zalecamy:**" if decision_after_cure in ["dalsze osuszanie", "przeprowadzenie procesu wygrzewania"] else ""

        if total_cracks > 0 or holes == "TAK":
            if moisture_prefix: st.write(f"* {moisture_prefix}")
            if total_cracks > 0: st.write(f"  - Zespolić pęknięcia i dylatacje pozorne żywicą **WAKOL PS 205**.")
            if holes == "TAK": st.write(f"  - Uzupełnić ubytki zaprawą **WAKOL Z 610**.")

        # GRUNTOWANIE / BARIERA (PU 280 PEŁNY OPIS)
        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            if strength_val <= 2:
                st.write("* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez dwukrotne zagruntowanie gruntówką wzmacniającą WAKOL PU 235 (250g/m2).**")
            else:
                st.write("* **Z uwagi na podwyższoną wilgotność zalecamy stworzenie bariery przeciwwilgociowej poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki.**")
                st.write("**1 warstwa nałożona wałkiem ok. 100-150 g/m². Czas schnięcia – jedna godzina.**")
                st.write("**2 warstwa ok. 100 g/m² - czas schnięcia – jedna godzina.**")
                st.write("**Czas do klejenia: 72 godziny od zagruntowania.**")
            if needs_levelling == "TAK": st.write(f"* **Następnie zaaplikować mostek sczepny za pomocą produktu WAKOL D 3045 (wałkiem, 150g/m2, 1h).**")
        
        elif decision_after_cure not in ["dalsze osuszanie", "przeprowadzenie procesu wygrzewania"]:
            p = moisture_prefix + " " if moisture_prefix else ""
            if strength_val == 1:
                if needs_levelling == "NIE": st.write(f"* {p}Zalecamy aplikację gruntówki wzmacniającej **Wakol PS 275** w dwóch warstwach – grubym wałkiem sznurkowym, zużycie w sumie ok. 700 g/m2. Każda z warstw po 350g/m2, aplikowane po sobie w odstępie jednej godziny. Aplikując gruntówkę **Wakol PS 275** należy zwrócić uwagę, aby dobrze wchłaniała się w podłoże i unikać powstawania kałuż na powierzchni jastrychu. Po nałożeniu drugiej warstwy gruntówki w razie potrzeby wykonać posypkę z piasku kwarcowego. Po 7 dniach schnięcia powierzchnię należy przeszlifować papierem o gradacji 24 – 40 usuwając przyklejony do powierzchni piasek kwarcowy i dokładnie odkurzyć.")
                else: 
                    st.write(f"* {p}Zalecamy gruntowanie **WAKOL PU 235** + **mostek sczepny WAKOL D 3045**.")
            elif strength_val == 2:
                st.write(f"* {p}Zalecamy gruntowanie **WAKOL PU 280**.")
                if needs_levelling == "TAK": st.write(f"* **Następnie zaaplikować mostek sczepny WAKOL D 3045.**")
            elif strength_val >= 3 and needs_levelling == "TAK":
                st.write(f"* {p}**Zagruntować podłoże koncentratem WAKOL D 3040 (1:2 z wodą, zużycie 50g/m2, 30 min).**")

        # SEKCJA MAS (Z 625, Z 635, Z 675 PEŁNE OPISY)
        if needs_levelling == "TAK":
            elastic = ["wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"]
            if flooring_type == "deska lita":
                st.write(f"* {moisture_prefix if moisture_prefix else ''} **Wylać masę wyrównawczą WAKOL Z 625 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,00 – 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2 godzinach. Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 6 godzinach, przy warstwie do 10 mm – po 12 godzinach, przy warstwie 30 mm – po 24 godzinach.**")
            elif flooring_type in elastic:
                st.write(f"* {moisture_prefix if moisture_prefix else ''} **Wylanie masy wyrównawczej Wakol Z 675 w jednej warstwie o grubości 7mm. W proporcji 25kg masy + 6,0 litrów wody. Zużycie 1,5kg/m2 przy 1mm grubości. Wymieszać w czystym pojemniku z zimną wodą w unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić maksymalnie 600 obrotów na minutę. Masę pozostawić do odparowania na ok. 2 - 3 minuty a następnie ponownie przemieszać. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Schnącą masę należy chronić przed działaniem promieni słonecznych i przeciągów. Warstwa do 2 mm - możliwość klejenia po 24 godzinach, do 5 mm - po 48 godzinach, do 10 mm - po 72 godzinach.**")
            elif flooring_type == "deska warstwowa (drewno, laminat itp.)":
                st.write(f"* {moisture_prefix if moisture_prefix else ''} **Następnie na podłoże wylać masę wyrównawczą WAKOL Z 635 - Wylewając masę wyrównawczą WAKOL Z 635 wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2,5 godzinach. Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 24 godzinach, przy warstwie do 10 mm – po 72 godzinach.**")

        st.divider()
        st.markdown(f"""
        <div style="font-size: 13px; line-height: 1.5; border-top: 1px solid #ccc; padding-top: 15px; color: #000;">
            <b>Prosimy o zapoznanie się z kartami technicznymi zalecanych produktów WAKOL.</b><br>
            <b>Podstawą naszego zalecenia jest stosowanie i prawidłowa obróbka wszystkich wymienionych materiałów firmy WAKOL w podanej kolejności, przestrzegając reguł rzemiosła i obowiązujących norm oraz instrukcji.</b><br><br>
            <b>W przypadku jakichkolwiek pytań lub wątpliwości proszę o kontakt pod numer telefonu: 603 214 218</b><br><br>
            <b>Z poważaniem,</b><br>
            <b>Loba-Wakol Polska Sp. z o.o.</b><br>
            <b>Przemysław Tyszko</b>
        </div>
        """, unsafe_allow_html=True)
