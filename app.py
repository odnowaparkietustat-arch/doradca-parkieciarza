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

# --- WYWIAD TECHNICZNY ---
flooring_type = st.selectbox("1. Rodzaj okładziny", ["deska warstwowa (drewno, laminat itp.)", "deska lita", "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"])
substrate = st.selectbox("2. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane (parkiet, deska, OSB)", "płytki ceramiczne", "masa samorozlewna"])
substrate_age_val = st.number_input("Wiek podłoża (podaj ilość miesięcy):", min_value=0.5, step=0.5, format="%.1f", value=None)

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
leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=None) if needs_levelling == "TAK" else 0

# Sekcja wymagana przez MASTER RULE:
st.write("5. Czy dylatacje obwodowe zachowane prawidłowo?")
dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=0, horizontal=True, label_visibility="collapsed")
st.write("6. Czy występują klawiszujące dylatacje pozorne?")
cracks_klaw = st.radio("Klawiszowanie pozorne:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
klaw_meters = st.number_input("Ilość mb klawiszujących:", min_value=0.1, step=0.1, value=None) if cracks_klaw == "TAK" else 0.0
st.write("7. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia do zespolenia:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", min_value=0.1, step=0.1, value=None) if cracks_pek == "TAK" else 0.0
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
moisture = st.number_input("12. Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)

# Wybór kleju dla deski warstwowej
selected_glue_warstwowa = None
if flooring_type == "deska warstwowa (drewno, laminat itp.)":
    selected_glue_warstwowa = st.selectbox("Wybierz klej dla deski warstwowej:", ["WAKOL MS 230", "WAKOL PU 225"])

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
limit = 1.5 if substrate == "jastrych cementowy" and heating_exists == "TAK" else 1.8 if substrate == "jastrych cementowy" else 0.3 if substrate == "jastrych anhydrytowy" and heating_exists == "TAK" else 0.5 if substrate == "jastrych anhydrytowy" else 1.5
barrier_max = 2.5 if heating_exists == "TAK" else 3.5
decision_after_cure = None
if moisture is not None and moisture > limit:
    opt_dry = "przeprowadzenie procesu wygrzewania" if heating_exists == "TAK" else "dalsze osuszanie"
    if moisture <= barrier_max: decision_after_cure = st.radio("Postępowanie:", ["Wykonanie bariery przeciwwilgociowej", opt_dry], horizontal=True)
    else: decision_after_cure = opt_dry

# --- GENEROWANIE PROTOKOŁU ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None: st.error("Podaj wilgotność!")
    else:
        st.divider(); insert_header()
        st.write(f"**Data:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")
        st.markdown("#### **I. Oględziny i badania**")
        st.write(f"**a) oględziny optyczne:** Podłoże: {substrate}. Ogrzewanie: {heating_info if heating_exists=='TAK' else 'Brak'}. Dylatacje obwodowe: {dilatations_obw_ok}. Klawiszowanie: {klaw_meters}mb. Pęknięcia: {pek_meters}mb. Wentylacja: {ventilation_type}.")
        st.write(f"**b) badanie wytrzymałości:** Wynik PressoMess: {presso_results}. Ocena: {strength_labels[strength_val]}.")
        st.write(f"**c) badanie wilgotności:** Wynik **{moisture} % CM** (Norma: {limit} % CM)")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**a) przygotowanie podłoża:** Szlif podłoża, dokładne odkurzenie.")
        if decision_after_cure in ["dalsze osuszanie", "przeprowadzenie procesu wygrzewania"]:
            st.write(f"* **Zalecamy doprowadzenie do normy ({limit}% CM) poprzez {decision_after_cure}.**")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        if (klaw_meters + pek_meters) > 0: st.write("- Zespolić pęknięcia żywicą **WAKOL PS 205**.")
        if holes == "TAK": st.write(f"- Uzupełnić ubytki zaprawą **WAKOL Z 610**{hole_details}.")
        
        # --- BARIERY I GRUNTY (STAŁE) ---
        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            if strength_val <= 2: st.write("* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez dwukrotne zagruntowanie gruntówką wzmacniającą WAKOL PU 235. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki. 1 warstwa ok. 150 g/m² (3-6h), 2 warstwa ok. 100 g/m² (3-6h). Czas klejenia 72h.**")
            else: st.write("* **Zalecamy barierę przeciwwilgociową WAKOL PU 280. Aplikować wałkiem, zbierać nadmiar. 1 warstwa ok. 100-150 g/m² (1h), 2 warstwa ok. 100 g/m² (1h). Czas do klejenia: 72h.**")
        
        # --- NOWA RUBRYKA: KLEJENIE OKŁADZINY (STAŁE) ---
        st.write("**c) klejenie okładziny:**")
        if flooring_type == "deska lita":
            st.write("> **Do montażu podłogi litej należy użyć twardo-elastycznego kleju polimerowego WAKOL MS 260. Klej nanosić odpowiednią szpachlą ząbkowaną B13 lub B15. Podczas klejenia należy zwracać uwagę na dokładne pokrycie spodu elementów klejem. Zużycie zależne od spodu deski i szpachli ok. 1100 - 1300 g/m2. Klej charakteryzuje się bardzo wysoką siłą wiązania początkowego.**")
        elif flooring_type == "deska warstwowa (drewno, laminat itp.)":
            if selected_glue_warstwowa == "WAKOL MS 230":
                st.write("> **Do klejenia warstwowych elementów drewnianych należy użyć twardo-elastycznego kleju polimerowego WAKOL MS 230. Klej nanosić odpowiednią szpachlą ząbkowaną B11 lub B13. Podczas klejenia należy zwracać uwagę na dokładne pokrycie spodu elementów klejem. Zużycie ok. 1000 - 1200 g/m2. Czas pracy ok. 40 minut. Klej spełnia wymagania normy DIN EN ISO 17178.**")
            else:
                st.write("> **Do klejenia warstwowych elementów drewnianych należy użyć dwuskładnikowego kleju poliuretanowego WAKOL PU 225. Składniki kleju należy ze sobą wymieszać aż do uzyskania jednolitej barwy. Klej nanosić odpowiednią szpachlą ząbkowaną B11 lub B13. Zużycie ok. 1000 - 1400 g/m2. Czas pracy ok. 30 - 45 minut.**")

        st.divider()
        st.markdown("<b>Z poważaniem, Loba-Wakol Polska Sp. z o.o. | Przemysław Tyszko</b>", unsafe_allow_html=True)
