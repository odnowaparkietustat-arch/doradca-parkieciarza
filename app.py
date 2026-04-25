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
st.header("I. Wywiad Techniczny")
col_base1, col_base2 = st.columns(2)
with col_base1:
    flooring_type = st.selectbox("1. Rodzaj okładziny", ["deska warstwowa (drewno, laminat itp.)", "deska lita", "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"])
    substrate = st.selectbox("2. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane (parkiet, deska, OSB)", "płytki ceramiczne", "masa samorozlewna"])
with col_base2:
    substrate_age_val = st.number_input("Wiek podłoża (podaj ilość miesięcy):", min_value=0.5, step=0.5, format="%.1f", value=None)
    heating_exists = st.radio("3. Czy jest instalacja ogrzewania podłogowego?", ["TAK", "NIE"], index=1, horizontal=True)

# Logika Ogrzewania
heating_info = ""; heating_curing_done = None
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne (powierzchniowe)", "elektryczne (głębokie)", "płyta fundamentowa grzewcza"])
    heating_curing_done = st.radio("❓ Czy został przeprowadzony proces wygrzewania zgodnie z protokołem?", ["TAK", "NIE"], index=1, horizontal=True)
    mapping = {"wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna", "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana", "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie", "elektryczne (powierzchniowe)": "instalacja ogrzewania podłogowego elektryczna, powierzchniowa", "elektryczne (głębokie)": "instalacja ogrzewania podłogowego elektryczna, umieszczona głęboko w podłożu", "płyta fundamentowa grzewcza": "ogrzewanie realizowane poprzez płytę fundamentową grzewczą"}
    heating_info = mapping.get(h_type, h_type)

# REGUŁA AUTO-PODPOWIEDZI DLA LVT CIENKIE
is_lvt_thin = (flooring_type == "lvt cienkie")
lev_idx = 0 if is_lvt_thin else 1
thick_val = 3.0 if is_lvt_thin else 0.0

st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=lev_idx, horizontal=True)
leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=0.0, value=thick_val)

# Parametry jastrychu (Bezwzględne pytania WAKOL)
st.subheader("Parametry jastrychu")
col_wak1, col_wak2 = st.columns(2)
with col_wak1:
    dilatations_obw_ok = st.radio("1. Czy dylatacje obwodowe zachowane prawidłowo? (Opcje: TAK/NIE)", ["TAK", "NIE"], index=0)
    cracks_klaw = st.radio("2. Czy występują klawiszujące dylatacje pozorne? (Opcje: TAK/NIE)", ["TAK", "NIE"], index=1)
    klaw_meters = st.number_input("Ilość mb klawiszujących:", min_value=0.0, step=0.1) if cracks_klaw == "TAK" else 0.0
with col_wak2:
    cracks_pek = st.radio("3. Czy występują pęknięcia podłoża wymagające zespolenia? (Opcje: TAK/NIE)", ["TAK", "NIE"], index=1)
    pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", min_value=0.0, step=0.1) if cracks_pek == "TAK" else 0.0
    holes = st.radio("4. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia? (Opcje: TAK/NIE)", ["TAK", "NIE"], index=1)
    hole_details_input = ""
    if holes == "TAK":
        hole_details_input = st.text_input("Opisz ubytki:", "ubytki o głębokości ok. 1-2 cm")

st.write("Rodzaj wentylacji")
ventilation_type = st.radio("Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True)

col_w1, col_w2 = st.columns(2)
with col_w1: temp_air = st.number_input("Temperatura powietrza (°C)", step=0.5, value=None)
with col_w2: hum_air = st.number_input("Wilgotność powietrza (%)", step=1.0, value=None)
moisture = st.number_input("Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)

# --- II. TESTY MECHANICZNE ---
st.header("II. Testy mechaniczne i Wytrzymałość")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: test_hammer = st.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t2: test_ripper = st.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t3: test_brush = st.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)

strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości podłoża:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# --- LOGIKA TECHNOLOGICZNA ---
limit = 1.5 if substrate == "jastrych cementowy" and heating_exists == "TAK" else 1.8 if substrate == "jastrych cementowy" else 0.3 if substrate == "jastrych anhydrytowy" and heating_exists == "TAK" else 0.5 if substrate == "jastrych anhydrytowy" else 1.5
decision_after_cure = None
if moisture is not None and moisture > limit:
    opt_dry = "przeprowadzenie procesu wygrzewania" if heating_exists == "TAK" else "dalsze osuszanie"
    if not (substrate == "jastrych anhydrytowy" or (heating_exists == "TAK" and heating_curing_done == "NIE")):
        decision_after_cure = st.radio("Postępowanie z wilgocią:", ["Wykonanie bariery przeciwwilgociowej", opt_dry], horizontal=True)

# --- STAŁE TECHNOLOGICZNE (OPISY 1:1) ---
FULL_D3004 = "* **Zagruntować podłoże koncentratem gruntówki dyspersyjnej WAKOL D 3004. Proporcje mieszania: 1 część WAKOL D 3004 + 2 części wody; Czas schnięcia: na jastrychach cementowych i betonie po optycznym wyschnięciu ok. 30min. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: ok. 50 g/m² koncentratu.**"
FULL_PU280_1W = "* **Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia – jedna godzina.**"

# MASZ SAMOPOZIOMUJĄCE (REGUŁA DOBORU)
FULL_Z675 = "* **Wylać masę wyrównawczą WAKOL Z 675 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,0 – 6,5 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2-3 godzinach. Możliwość klejenia podłóg po ok. 24 godzinach przy grubości warstwy do 3 mm, przy większych grubościach czas schnięcia ulega wydłużeniu.**"
FULL_Z635 = "* **Wylać masę wyrównawczą WAKOL Z 635 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,25 – 6,75 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po ok. 2 godzinach. Możliwość klejenia parkietu po ok. 12 godzinach przy grubości warstwy do 5 mm.**"
FULL_Z625 = "* **Wylać masę wyrównawczą WAKOL Z 625 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,00 – 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2 godzinach. Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 6 godzinach, przy warstwie do 10 mm – po 12 godzinach, przy warstwie 30 mm – po 24 godzinach.**"

# KLEJE
FULL_MS230 = "* **Klejenie podłogi drewnianej należy przeprowadzić przy użyciu kleju do parkietu WAKOL MS 230, twardo-elastycznego. Klej nanosić odpowiednią szpachlą zębatą (np. B13). Zużycie ok. 1350 g/m².**"
FULL_PU225 = "* **Klejenie podłogi drewnianej należy przeprowadzić przy użyciu 2-składnikowego kleju poliuretanowego WAKOL PU 225. Składniki A i B dokładnie wymieszać mieszadłem elektrycznym. Klej nanosić szpachlą zębatą (np. B11). Zużycie ok. 1250 g/m².**"

# --- GENEROWANIE PROTOKOŁU ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None: st.error("Proszę podać wilgotność podłoża!")
    else:
        st.divider(); insert_header()
        st.markdown("#### **I. Oględziny i badania**")
        
        # PEŁNY OPIS OPTYCZNY
        age_info = f" w wieku {substrate_age_val} miesięcy" if substrate_age_val else ""
        heat_info_full = f" Została zainstalowana {heating_info}." if heating_exists == "TAK" else " Brak instalacji ogrzewania podłogowego."
        curing_info_full = " Został przeprowadzony proces wygrzewania zgodnie z protokołem." if heating_curing_done == "TAK" else " Nie został przeprowadzony proces wygrzewania podłoża." if heating_exists == "TAK" else ""
        dil_info = " Czy dylatacje obwodowe zachowane prawidłowo? TAK." if dilatations_obw_ok == "TAK" else " Czy dylatacje obwodowe zachowane prawidłowo? NIE."
        klaw_info = f" Czy występują klawiszujące dylatacje pozorne? TAK, w ilości {klaw_meters} mb." if cracks_klaw == "TAK" else " Czy występują klawiszujące dylatacje pozorne? NIE."
        pek_info = f" Czy występują pęknięcia podłoża wymagające zespolenia? TAK, w ilości {pek_meters} mb." if cracks_pek == "TAK" else " Czy występują pęknięcia podłoża wymagające zespolenia? NIE."
        holes_info = f" Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia? TAK ({hole_details_input})." if holes == "TAK" else " Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia? NIE."
        lev_info = f" Podłoże wymaga wyrównania masą o grubości {leveling_thickness} mm." if needs_levelling == "TAK" else " Podłoże nie wymaga wyrównania."
        
        full_report = f"Podłoże pod okładzinę ({flooring_type}) stanowi {substrate}{age_info}.{heat_info_full}{curing_info_full} {dil_info} {klaw_info} {pek_info} {holes_info} {lev_info} Wentylacja: {ventilation_type}."
        st.write(f"**a) oględziny optyczne:** {full_report}")
        
        moisture_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY"
        st.write(f"**b) badanie wilgotności:** Wynik: **{moisture} % CM** (Norma: {limit} % CM) — **Wynik: {moisture_status}**")
        st.write(f"**c) wytrzymałość:** Ocena: **{strength_labels[strength_val]}** (Młotek: {test_hammer}, Rysik: {test_ripper})")

        st.markdown("#### **II. Zalecenia techniczne**")
        
        curing_not_done = (heating_exists == "TAK" and heating_curing_done == "NIE")
        norm_val_bracket = f"({limit}% CM)"
        
        st.write("**a) przygotowanie podłoża:**")
        st.write("* **Szlif podłoża i odkurzenie przemysłowe.**")
        
        if curing_not_done:
            msg = f"w celu uzyskania normatywnego poziomu wilgoci {norm_val_bracket}." if moisture > limit else "zgodnie z protokołem."
            st.write(f"* **Konieczność przeprowadzenia pełnego procesu wygrzewania {msg}**")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        if curing_not_done:
            poczatek = f"Po doprowadzeniu do normatywnego poziomu wilgoci {norm_val_bracket} jastrychu poprzez wygrzewanie" if moisture > limit else "Po przeprowadzeniu pełnego procesu wygrzewania"
            st.write(f"**{poczatek} zalecamy:**")
        
        if holes == "TAK": st.write("- Uzupełnić ubytki zaprawą **WAKOL Z 610**.")
        if (klaw_meters + pek_meters) > 0: st.write("- Zespolić pęknięcia żywicą **WAKOL PS 205**.")

        # LOGIKA DOBORU GRUNTU I MASY (NOWA REGUŁA)
        if needs_levelling == "TAK":
            # Gruntowanie
            if is_lvt_thin and strength_val <= 2:
                st.write(FULL_PU280_1W)
                st.write("* **Zastosować mostek sczepny WAKOL D 3045 (150 g/m²).**")
            else:
                st.write(FULL_D3004)
            
            # Masa w zależności od okładziny
            if flooring_type in ["wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"]:
                st.write(FULL_Z675)
            elif flooring_type == "deska warstwowa (drewno, laminat itp.)":
                st.write(FULL_Z635)
            elif flooring_type == "deska lita":
                st.write(FULL_Z625)
        else:
            st.write(FULL_D3004)

        st.write("**c) klejenie okładziny:**")
        if flooring_type == "lvt cienkie":
            st.write("Klejenie podłogi winylowej: **WAKOL D 3318** (szpachla A2, 350 g/m²). Odparowanie 5-10 min, układanie 10 min.")
        elif substrate == "płyta fundamentowa" or flooring_type == "deska lita":
            st.write("Klejenie przy użyciu kleju **WAKOL MS 260**.")
        elif flooring_type == "deska warstwowa (drewno, laminat itp.)":
            if substrate == "jastrych anhydrytowy" and strength_val == 1:
                st.write(FULL_MS230)
            else:
                st.write(f"{FULL_MS230}\n{FULL_PU225}")

        st.divider(); st.markdown(f"<b>Z poważaniem, Loba-Wakol Polska Sp. z o.o. | {autor}</b>", unsafe_allow_html=True)
