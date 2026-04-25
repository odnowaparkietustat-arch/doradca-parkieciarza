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
                <b>Loba-Wakol Polska Sp. z o.o.</b><br>ul. Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki<br>
                tel.: +48 22 436 24 20 | fax: +48 22 436 24 21<br>KRS: 0000163623 | NIP: 118-13-89-053 | biuro@loba-wakol.pl
            </div>
        </div>
        <div style="flex: 1; text-align: right;">
            <div style="font-size: 18px; font-weight: bold; color: #000; margin-bottom: 5px;">PROTOKÓŁ TECHNICZNY</div>
            <div style="font-size: 14px; color: #333;">Anspruch verbindet</div>
        </div>
    </div><br>
    """, unsafe_allow_html=True)

st.title("📄 Generator Protokołu Oględzin")

# --- WYWIAD TECHNICZNY (STAŁE PYTANIA) ---
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

st.header("I. Wywiad i dane podstawowe")
flooring_type = st.selectbox("Rodzaj planowanej okładziny", ["deska warstwowa (drewno, laminat itp.)", "deska lita", "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"])
substrate = st.selectbox("Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane", "płytki ceramiczne", "masa samorozlewna"])
substrate_age_val = st.number_input("Wiek podłoża (miesiące):", min_value=0.5, step=0.5, format="%.1f", value=None)

st.write("3. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
heating_info = ""; heating_curing_done = None
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne (powierzchniowe)", "elektryczne (głębokie)", "płyta fundamentowa grzewcza"])
    heating_curing_done = st.radio("Czy został przeprowadzony proces wygrzewania zgodnie z protokołem?", ["TAK", "NIE"], index=1, horizontal=True)
    heating_info = h_type

st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=None) if needs_levelling == "TAK" else 0

st.write("1. Czy dylatacje obwodowe zachowane prawidłowo?")
dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=0, horizontal=True, label_visibility="collapsed")
st.write("2. Czy występują klawiszujące dylatacje pozorne?")
cracks_klaw = st.radio("Klawiszowanie:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
klaw_meters = st.number_input("Ilość mb klawiszujących:", min_value=0.1, step=0.1, value=None) if cracks_klaw == "TAK" else 0.0
st.write("3. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", min_value=0.1, step=0.1, value=None) if cracks_pek == "TAK" else 0.0
st.write("4. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
hole_details = st.text_input("Opis/wymiary ubytków:") if holes == "TAK" else ""

# --- BADANIA ---
st.header("II. Parametry mechaniczne")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1: test_hammer = st.selectbox("Młotek (opukiwanie)", ["pozytywny", "negatywny", "dostateczny"])
with col_m2: test_scratch = st.selectbox("Rysik (twardość)", ["pozytywny", "negatywny", "dostateczny"])
with col_m3: test_brush = st.selectbox("Szczotka (pylenie)", ["pozytywny", "negatywny"])
strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena końcowa wytrzymałości:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# --- POMIARY ---
st.header("III. Parametry fizyczne")
col_cl1, col_cl2, col_cl3 = st.columns(3)
with col_cl1: moisture = st.number_input("Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)
with col_cl2: hum_air = st.number_input("Wilgotność powietrza (%)", step=1.0, value=None)
with col_cl3: temp_air = st.number_input("Temperatura powietrza (°C)", step=0.5, value=None)

# --- STAŁE TECHNOLOGICZNE WAKOL (1:1) ---
FULL_PREP = "* **Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni!**\n* **Dokładne odkurzenie powierzchni odkurzaczem przemysłowym.**"
FULL_PS275 = "* **Zalecamy aplikację gruntówki wzmacniającej Wakol PS 275 w dwóch warstwach – grubym wałkiem sznurkowym, zużycie w sumie ok. 700 g/m2. Każda z warstw po 350g/m2, aplikowane po sobie w odstępie jednej godziny. Aplikując gruntówkę Wakol PS 275 należy zwrócić uwagę, aby dobrze wchłaniała się w podłoże i unikać powstawania kałuż na powierzchni jastrychu. Po nałożeniu drugiej warstwy gruntówki w razie potrzeby wykonać posypkę z piasku kwarcowego. Po 7 dniach schnięcia powierzchnię należy przeszlifować papierem o gradacji 24 – 40 usuwając przyklejony do powierzchni piasek kwarcowy i dokładnie odkurzyć.**"
FULL_PU280_BARRIER = "* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. 1 warstwa nałożona wałkiem ok. 100-150 g/m². Czas schnięcia – jedna godzina. 2 warstwa ok. 100 g/m² - czas schnięcia – jedna godzina. Czas do klejenia: 72 godziny od zagruntowania.**"
FULL_PU280_REINFORCE = "* **Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia – jedna godzina.**"
FULL_D3045 = "* **Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu WAKOL D 3045. Aplikować równomiernie za pomocą wałka. Zużycie wynosi ok. 150 g/m². Czas schnięcia 1 godzina.**"
FULL_D3040 = "* **Zagruntować podłoże koncentratem gruntówki dyspersyjnej WAKOL D 3040. Proporcje mieszania: 1 część WAKOL D 3040 + 2 części wody; Czas schnięcia: na jastrychach cementowych i betonie po optycznym wyschnięciu ok. 30min. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: ok. 50 g/m² koncentratu.**"
FULL_MS260 = "* **Do montażu okładziny należy użyć twardo-elastycznego kleju polimerowego WAKOL MS 260. Klej nanosić odpowiednią szpachlą ząbkowaną. Należy zwracać uwagę na pełne pokrycie spodu deski klejem. Zużycie zależne od szpachli i podłoża wynosi ok. 800-1200 g/m².**"

# --- LOGIKA DECYZJI ---
limit = 1.5 if (substrate == "jastrych cementowy" and heating_exists == "TAK") else 1.8 if substrate == "jastrych cementowy" else 0.5
moisture_eval = "pozytywny" if (moisture is not None and moisture <= limit) else "negatywny"
decision_after_cure = None
if moisture is not None and moisture > limit:
    if heating_exists == "TAK" and heating_curing_done == "NIE":
        decision_after_cure = f"Konieczność doprowadzenia do normatywnego poziomu wilgoci w jastrychu tj. {limit}% CM poprzez wykonanie procesu wygrzewania."
    else:
        decision_after_cure = f"Konieczność osuszenia podłoża do poziomu {limit}% CM."

# --- GENERATOR ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None: st.error("Podaj wilgotność!")
    else:
        st.divider(); insert_header()
        st.write(f"**Data badania:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.markdown(f"#### **I. Oględziny optyczne i wywiad techniczny**")
        st.write(f"Podłoże pod planowaną okładzinę ({flooring_type}) stanowi {substrate}. Ogrzewanie: {heating_info}. Wygrzewanie: {heating_curing_done}. {('Dylatacje obwodowe ok.' if dilatations_obw_ok == 'TAK' else 'Błąd dylatacji obwodowych.')}")

        st.markdown("#### **II. Parametry mechaniczne**")
        st.write(f"Badanie wytrzymałości:\nMłotek: {test_hammer}\nRysik: {test_scratch}\nSzczotka: {test_brush}\nOcena końcowa: **{strength_labels[strength_val]}**")

        st.markdown("#### **III. Parametry fizyczne**")
        st.write(f"Poziom wilgoci podłoża: **{moisture} % CM** (Norma: {limit} % CM) – **Wynik {moisture_eval}**")

        st.markdown("#### **IV. Zalecenia technologiczne**")
        if decision_after_cure: st.write(f"* **{decision_after_cure}**")
        st.write("**a) Przygotowanie podłoża:**"); st.write(FULL_PREP)

        st.write("**b) Naprawa i wzmocnienie podłoża:**")
        if decision_after_cure: st.write(f"**Po doprowadzeniu do normatywnego poziomu wilgoci tj. {limit}% CM zalecamy:**")
        
        # LOGIKA WYBORU GRUNTÓWKI (STAŁE)
        if strength_val == 1: st.write(FULL_PS275)
        elif strength_val == 2: st.write(FULL_PU280_REINFORCE)
        elif strength_val >= 3:
            if needs_levelling == "TAK": st.write(FULL_D3040)
            else: st.write("* Podłoże o wystarczającej wytrzymałości pod bezpośrednie klejenie.")
        
        if needs_levelling == "TAK":
            st.write(FULL_PU280_REINFORCE); st.write(FULL_D3045)
            if "lita" in flooring_type: st.write("* Wylać masę WAKOL Z 625 (Pełny opis...)")
            else: st.write("* Wylać masę WAKOL Z 635 (Pełny opis...)")
        
        st.write("**c) Montaż okładziny:**")
        st.write(FULL_MS260)

        st.divider(); st.markdown(f"**Z poważaniem, Loba-Wakol Polska Sp. z o.o. | Przemysław Tyszko**")
