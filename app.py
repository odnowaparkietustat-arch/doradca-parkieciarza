import streamlit as st
from datetime import date

# 1. KONFIGURACJA STRONY
st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="wide")

# --- NAGŁÓWEK FIRMOWY ---
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

# --- I. WYWIAD TECHNICZNY ---
flooring_type = st.selectbox("1. Rodzaj okładziny", ["deska warstwowa (drewno, laminat itp.)", "deska lita", "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"])
substrate = st.selectbox("2. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane (parkiet, deska, OSB)", "płytki ceramiczne", "masa samorozlewna"])
substrate_age_val = st.number_input("Wiek podłoża (podaj ilość miesięcy):", min_value=0.5, step=0.5, format="%.1f", value=None)

st.write("3. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True)
heating_info = ""; heating_curing_done = None
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne (powierzchniowe)", "elektryczne (głębokie)", "płyta fundamentowa grzewcza"])
    st.write("❓ Czy został przeprowadzony proces wygrzewania zgodnie z protokołem?")
    heating_curing_done = st.radio("Proces wygrzewania:", ["TAK", "NIE"], index=1, horizontal=True)
    mapping = {"wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna", "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana", "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie", "elektryczne (powierzchniowe)": "instalacja ogrzewania podłogowego elektryczna, powierzchniowa", "elektryczne (głębokie)": "instalacja ogrzewania podłogowego elektryczna, umieszczona głęboko w podłożu", "płyta fundamentowa grzewcza": "ogrzewanie realizowane poprzez płytę fundamentową grzewczą"}
    heating_info = mapping.get(h_type, h_type)

st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True)
leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=None) if needs_levelling == "TAK" else 0

# Sekcja wywiadu (stałe pytania)
st.write("5. Czy dylatacje obwodowe zachowane prawidłowo?")
dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=0, horizontal=True)
st.write("6. Czy występują klawiszujące dylatacje pozorne?")
cracks_klaw = st.radio("Klawiszowanie pozorne:", ["TAK", "NIE"], index=1, horizontal=True)
klaw_meters = st.number_input("Ilość mb klawiszujących:", min_value=0.1, step=0.1, value=None) if cracks_klaw == "TAK" else 0.0
st.write("7. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia do zespolenia:", ["TAK", "NIE"], index=1, horizontal=True)
pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", min_value=0.1, step=0.1, value=None) if cracks_pek == "TAK" else 0.0
st.write("8. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True)
hole_details = ""
if holes == "TAK":
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1: h_depth = st.number_input("Głębokość (cm)", min_value=0.1, value=None)
    with col_h2: h_width = st.number_input("Szerokość (cm)", min_value=0.1, value=None)
    with col_h3: h_length = st.number_input("Długość (cm)", min_value=0.1, value=None)
    if h_depth and h_width and h_length: hole_details = f" o wymiarach ok. {h_length}x{h_width} cm i głębokości {h_depth} cm"

st.write("9. Rodzaj wentylacji")
ventilation_type = st.radio("Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True)

col_w1, col_w2 = st.columns(2)
with col_w1: temp_air = st.number_input("10. Temperatura powietrza (°C)", step=0.5, value=None)
with col_w2: hum_air = st.number_input("11. Wilgotność powietrza (%)", step=1.0, value=None)
moisture = st.number_input("12. Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)

# --- TESTY MECHANICZNE ---
st.write("### Testy mechaniczne i Wytrzymałość")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: test_hammer = st.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t2: test_ripper = st.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t3: test_brush = st.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)

st.write("**Badanie PressoMess**")
presso_results = []
for i in range(6): 
    presso_results.append(st.number_input(f"Próba {i+1} (N/mm²)", min_value=0.0, step=0.1, key=f"p_{i}", value=None))
strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# --- LOGIKA NORM I BARIER ---
limit = 1.5 if substrate == "jastrych cementowy" and heating_exists == "TAK" else 1.8 if substrate == "jastrych cementowy" else 0.3 if substrate == "jastrych anhydrytowy" and heating_exists == "TAK" else 0.5 if substrate == "jastrych anhydrytowy" else 1.5
barrier_max = 2.5 if heating_exists == "TAK" else 3.5

decision_after_cure = None
needs_drying_action = False
if moisture is not None and moisture > limit:
    needs_drying_action = True
    opt_dry = "przeprowadzenie procesu wygrzewania" if heating_exists == "TAK" else "dalsze osuszanie"
    if substrate == "jastrych anhydrytowy" or (heating_exists == "TAK" and heating_curing_done == "NIE"):
        decision_after_cure = opt_dry
    else:
        if moisture <= barrier_max:
            decision_after_cure = st.radio("Postępowanie:", ["Wykonanie bariery przeciwwilgociowej", opt_dry], horizontal=True)
            needs_drying_action = (decision_after_cure != "Wykonanie bariery przeciwwilgociowej")
        else:
            decision_after_cure = opt_dry

# --- STAŁE TECHNOLOGICZNE ---
FULL_PS275 = "* **Zalecamy aplikację gruntówki wzmacniającej Wakol PS 275 w dwóch warstwach – grubym wałkiem sznurkowym, zużycie w sumie ok. 700 g/m2. Każda z warstw po 350g/m2, aplikowane po sobie w odstępie jednej godziny. Aplikując gruntówkę Wakol PS 275 należy zwrócić uwagę, aby dobrze wchłaniała się w podłoże i unikać powstawania kałuż na powierzchni jastrychu. Po nałożeniu drugiej warstwy gruntówki w razie potrzeby wykonać posypkę z piasku kwarcowego. Po 7 dniach schnięcia powierzchnię należy przeszlifować papierem o gradacji 24 – 40 usuwając przyklejony do powierzchni piasek kwarcowy i dokładnie odkurzyć.**"
FULL_PU235_1W = "* **Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 235. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia – jedna godzina.**"
FULL_PU235_BARRIER = "* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez dwukrotne zagruntowanie gruntówką wzmacniającą WAKOL PU 235. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki. 1 - warstwa nałożona wałkiem ok. 150 g/m². Czas schnięcia – 3-6 godzin. 2 warstwa zużycie ok. 100 g/m². Czas schnięcia – 3-6 godzin. Czas klejenia 72 godziny od zagruntowania.**"
FULL_PU280_1W = "* **Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia – jedna godzina.**"
FULL_PU280_BARRIER = "* **Z uwagi na podwyższoną wilgotność zalecamy stworzenie bariery przeciwwilgociowej poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. 1 warstwa nałożona wałkiem ok. 100-150 g/m². Czas schnięcia – jedna godzina. 2 warstwa ok. 100 g/m² - czas schnięcia – jedna godzina. Czas do klejenia: 72 godziny od zagruntowania.**"
FULL_D3004 = "* **Zagruntować podłoże koncentratem gruntówki dyspersyjnej WAKOL D 3004. Proporcje mieszania: 1 część WAKOL D 3004 + 2 części wody; Czas schnięcia: na jastrychach cementowych i betonie po optycznym wyschnięciu ok. 30min. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: ok. 50 g/m² koncentratu.**"
FULL_Z625 = "* **Wylać masę wyrównawczą WAKOL Z 625 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,00 – 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2 godzinach. Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 6 godzinach, przy warstwie do 10 mm – po 12 godzinach, przy warstwie 30 mm – po 24 godzinach.**"

# --- GENEROWANIE PROTOKOŁU ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None: st.error("Proszę podać wilgotność podłoża!")
    else:
        st.divider(); insert_header()
        st.write(f"**Data badania:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")
        st.markdown("#### **I. Oględziny i badania**")
        
        # PEŁNY OPIS OPTYCZNY
        age_txt = f" w wieku {substrate_age_val} miesięcy" if substrate_age_val else ""
        heat_txt = f" Została zainstalowana {heating_info}." if heating_exists == "TAK" else " Brak instalacji ogrzewania podłogowego."
        curing_txt = " Został przeprowadzony proces wygrzewania zgodnie z protokołem." if heating_curing_done == "TAK" else " Nie został przeprowadzony proces wygrzewania podłoża." if heating_exists == "TAK" else ""
        dil_txt = " Dylatacje obwodowe zostały zachowane prawidłowo." if dilatations_obw_ok == "TAK" else " Dylatacje obwodowe nie zostały zachowane prawidłowo."
        klaw_txt = f" Stwierdzono występowanie klawiszujących dylatacji pozornych w ilości {klaw_meters} metrów bieżących." if cracks_klaw == "TAK" else " Nie stwierdzono występowania klawiszujących dylatacji pozornych."
        pek_txt = f" Stwierdzono występowanie pęknięć podłoża wymagających zespolenia w ilości {pek_meters} metrów bieżących." if cracks_pek == "TAK" else " Nie stwierdzono występowania pęknięć podłoża wymagających zespolenia."
        holes_txt = f" Stwierdzono ubytki lub zdegradowane miejsca wymagające wypełnienia{hole_details}." if holes == "TAK" else " Nie stwierdzono ubytków lub zdegradowanych miejsc wymagających wypełnienia."
        level_txt = f" Podłoże wymaga wyrównania masą wyrównawczą o planowanej grubości {leveling_thickness} milimetrów." if needs_levelling == "TAK" else " Podłoże nie wymaga wyrównania masą wyrównawczą."
        vent_txt = f" Rodzaj zastosowanej wentylacji: wentylacja {ventilation_type.lower()}."
        
        full_opt_report = f"Podłoże pod planowaną okładzinę ({flooring_type}) stanowi {substrate}{age_txt}.{heat_txt}{curing_txt}{dil_txt}{klaw_txt}{pek_txt}{holes_txt}{level_txt} {vent_txt}"
        st.write(f"**a) oględziny optyczne:** {full_opt_report}")
        
        st.markdown("**b) badanie wytrzymałości:**")
        st.write(f"Wynik badania młotkiem: {test_hammer}")
        st.write(f"Wynik badania szczotką: {test_brush}")
        st.write(f"Wynik badania rysikiem: {test_ripper}")
        valid_presso = [v for v in presso_results if v is not None and v > 0]
        if valid_presso:
            st.write("Wyniki badania PressoMess:")
            for i, val in enumerate(valid_presso): st.write(f"- Próba {i+1}: {val} N/mm²")
        st.write(f"Ocena ogólna wytrzymałości podłoża: **{strength_labels[strength_val]}**")
        
        # BADANIE WILGOTNOŚCI Z WYNIKIEM
        moisture_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY"
        st.write(f"**c) badanie wilgotności:** Wynik badania wilgotności metodą CM: **{moisture} % CM** (Norma: {limit} % CM) — **Wynik: {moisture_status}**")

        if substrate == "jastrych cementowy" and flooring_type in ["deska warstwowa (drewno, laminat itp.)", "deska lita"]:
            st.info("Aby bezpiecznie kleić podłogę drewnianą na jastrychu cementowym, jego wytrzymałość na ścinanie musi wynosić między 1,5 a 2,0 N/mm² a wilgotność nie może przekraczać 1,8% CM. (z ogrzewaniem podłogowym max. 1,5% CM).")

        st.markdown("#### **II. Zalecenia techniczne**")
        
        # LOGIKA NOWEJ REGUŁY:
        heating_curing_needed = (heating_exists == "TAK" and heating_curing_done == "NIE")
        
        st.write("**a) przygotowanie podłoża:**")
        st.write("* **Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni!**")
        st.write("* **Dokładne odkurzenie powierzchni odkurzaczem przemysłowym.**")
        
        if moisture > limit:
            if heating_curing_needed:
                st.write(f"* **Konieczność doprowadzenia do normatywnego poziomu wilgoci w jastrychu poprzez przeprowadzenie procesu wygrzewania.**")
            else:
                st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci ({limit}% CM) poprzez {decision_after_cure}.**")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        if moisture > limit and heating_curing_needed:
            st.write("**Po doprowadzeniu do normatywnego poziomu wilgoci w jastrychu zalecamy:**")
        elif needs_drying_action:
            st.write("**Po doprowadzeniu do normatywnego poziomu wilgoci zalecamy:**")
        
        if (klaw_meters + pek_meters) > 0: st.write("- Zespolić pęknięcia i dylatacje pozorne żywicą **WAKOL PS 205**.")
        if holes == "TAK": st.write(f"- Uzupełnić ubytki zaprawą **WAKOL Z 610**{hole_details}.")

        used_d3004 = False
        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            if strength_val <= 2: st.write(FULL_PU235_BARRIER)
            else: st.write(FULL_PU280_BARRIER)
        elif not decision_after_cure or "Wykonanie" not in str(decision_after_cure):
            if needs_levelling == "TAK":
                if strength_val in [3, 4, 5]:
                    if substrate == "jastrych anhydrytowy" and leveling_thickness and leveling_thickness > 5: st.write(FULL_PU280_1W)
                    else:
                        st.write(FULL_D3004)
                        used_d3004 = True
                else:
                    if strength_val == 1:
                        if substrate == "jastrych anhydrytowy": st.write(FULL_PU235_1W)
                        else: (st.write(FULL_PS275), st.write(FULL_PU280_1W))
                    elif strength_val == 2: st.write(FULL_PU280_1W)
            else:
                if strength_val == 1:
                    if substrate == "jastrych anhydrytowy": st.write(FULL_PU235_1W)
                    else: st.write(FULL_PS275)
                elif strength_val == 2: st.write(FULL_PU235_1W)
                elif strength_val in [3, 4]: st.write(FULL_PU280_1W)
                elif strength_val == 5: st.write("* **Zalecamy zagruntowanie podłoża gruntówką dyspersyjną WAKOL D 3055. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: ok. 150 g/m². Czas schnięcia: ok. 30 min.**")

        if needs_levelling == "TAK":
            if not used_d3004: st.write("* **Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu WAKOL D 3045. Aplikować równomiernie za pomocą wałka. Zużycie wynosi ok. 150 g/m². Czas schnięcia 1 godzina.**")
            if flooring_type == "deska lita": st.write(FULL_Z625)
            elif flooring_type == "deska warstwowa (drewno, laminat itp.)": st.write("* **Następnie na podłoże wylać masę wyrównawczą WAKOL Z 635 [Pełny opis...]**")
            else: st.write("* **Wylanie masy wyrównawczej Wakol Z 675 [Pełny opis...]**")

        st.write("**c) klejenie okładziny:**")
        ms260_desc = "Klejenie podłogi drewnianej należy przeprowadzić przy użyciu kleju polimerowego twardo-elastycznego WAKOL MS 260. (szpachla B13, zużycie: 1350 g/m²)."
        if substrate == "płyta fundamentowa" or flooring_type == "deska lita": st.write(ms260_desc)
        elif flooring_type == "deska warstwowa (drewno, laminat itp.)":
            if substrate == "jastrych anhydrytowy" and strength_val == 1: st.write("Klejenie podłogi drewnianej należy przeprowadzić przy użyciu kleju do parkietu **WAKOL MS 230** (szpachla B13, zużycie: 1350 g/m²).")
            else: st.write("Klejenie podłogi drewnianej należy przeprowadzić przy użyciu kleju do parkietu **WAKOL MS 230** (szpachla B13, zużycie: 1350 g/m²) bądź kleju do parkietu **WAKOL PU 225** (szpachla B11, zużycie: 1250 g/m²).")

        st.divider(); st.markdown("<b>Z poważaniem, Loba-Wakol Polska Sp. z o.o. | Przemysław Tyszko</b>", unsafe_allow_html=True)
