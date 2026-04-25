import streamlit as st
from datetime import date

# ==========================================
# 1. KONFIGURACJA I STAŁE TECHNOLOGICZNE
# ==========================================
st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="wide")

# Opisy produktów 1:1 (Stałe technologiczne)
FULL_D3004 = "* **Zagruntować podłoże koncentratem gruntówki dyspersyjnej WAKOL D 3004. Proporcje mieszania: 1 część WAKOL D 3004 + 2 części wody; Czas schnięcia: na jastrychach cementowych i betonie po optycznym wyschnięciu ok. 30min. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: ok. 50 g/m² koncentratu.**"
FULL_PU280_1W = "* **Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia – jedna godzina.**"
FULL_PU280_BARRIER = "* **Z uwagi na podwyższoną wilgotność zalecamy stworzenie bariery przeciwwilgociowej poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. 1 warstwa nałożona wałkiem ok. 100-150 g/m². Czas schnięcia – jedna godzina. 2 warstwa ok. 100 g/m² - czas schnięcia – jedna godzina. Czas do klejenia: 72 godziny od zagruntowania.**"
FULL_PU235_BARRIER = "* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez dwukrotne zagruntowanie gruntówką wzmacniającą WAKOL PU 235. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki. 1 - warstwa nałożona wałkiem ok. 150 g/m². Czas schnięcia – 3-6 godzin. 2 warstwa zużycie ok. 100 g/m². Czas schnięcia – 3-6 godzin. Czas klejenia 72 godziny od zagruntowania.**"
FULL_PS275 = "* **Zalecamy aplikację gruntówki wzmacniającej Wakol PS 275 w dwóch warstwach – grubym wałkiem sznurkowym, zużycie w sumie ok. 700 g/m2. Każda z warstw po 350g/m2, aplikowane po sobie w odstępie jednej godziny. Aplikując gruntówkę Wakol PS 275 należy zwrócić uwagę, aby dobrze wchłaniała się w podłoże i unikać powstawania kałuż na powierzchni jastrychu. Po nałożeniu drugiej warstwy gruntówki w razie potrzeby wykonać posypkę z piasku kwarcowego. Po 7 dniach schnięcia powierzchnię należy przeszlifować papierem o gradacji 24 – 40 usuwając przyklejony do powierzchni piasek kwarcowy i dokładnie odkurzyć.**"
FULL_Z675 = "* **Wylać masę wyrównawczą WAKOL Z 675 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,0 – 6,5 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2-3 godzinach. Możliwość klejenia podłóg po ok. 24 godzinach przy grubości warstwy do 3 mm, przy większych grubościach czas schnięcia ulega wydłużeniu.**"
FULL_Z635 = "* **Wylać masę wyrównawczą WAKOL Z 635 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,25 – 6,75 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po ok. 2 godzinach. Możliwość klejenia parkietu po ok. 12 godzinach przy grubości warstwy do 5 mm.**"
FULL_Z625 = "* **Wylać masę wyrównawczą WAKOL Z 625 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,00 – 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2 godzinach. Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 6 godzinach, przy warstwie do 10 mm – po 12 godzinach, przy warstwie 30 mm – po 24 godzinach.**"
FULL_MS230 = "* **Klejenie podłogi drewnianej należy przeprowadzić przy użyciu kleju do parkietu WAKOL MS 230, twardo-elastycznego. Klej nanosić odpowiednią szpachlą zębatą (np. B13). Zużycie ok. 1350 g/m².**"
FULL_PU225 = "* **Klejenie podłogi drewnianej należy przeprowadzić przy użyciu 2-składnikowego kleju poliuretanowego WAKOL PU 225. Składniki A i B dokładnie wymieszać mieszadłem elektrycznym. Klej nanosić szpachlą zębatą (np. B11). Zużycie ok. 1250 g/m².**"

def insert_header():
    logo_wakol = "https://www.wakol.com/fileadmin/templates/images/wakol_logo.png"
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;">
        <div style="flex: 1;"><img src="{logo_wakol}" width="220">
            <div style="margin-top: 15px; font-size: 11px; color: #555; line-height: 1.4;">
                <b>Loba-Wakol Polska Sp. z o.o.</b><br>ul. Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki
            </div>
        </div>
        <div style="flex: 1; text-align: right;">
            <div style="font-size: 18px; font-weight: bold;">PROTOKÓŁ TECHNICZNY</div>
        </div>
    </div><br>""", unsafe_allow_html=True)

# ==========================================
# 2. INTERFEJS UŻYTKOWNIKA (WYWIAD)
# ==========================================
st.title("📄 Generator Protokołu Oględzin WAKOL")
with st.container():
    c1, c2 = st.columns(2)
    inwestycja = c1.text_input("Inwestycja", "Budynek mieszkalny")
    autor = c2.text_input("Autor protokołu", "Przemysław Tyszko")
    data_badania = c2.date_input("Data", date.today())

st.divider()

# Sekcja wywiadu - Stałe pozycje
st.header("I. Wywiad Techniczny")
col1, col2 = st.columns(2)
with col1:
    flooring_type = st.selectbox("1. Rodzaj okładziny", ["deska warstwowa (drewno, laminat itp.)", "deska lita", "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"])
    substrate = st.selectbox("2. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane", "płytki ceramiczne", "masa samorozlewna"])
    substrate_age = st.number_input("Wiek podłoża (miesiące)", min_value=0.5, step=0.5, value=None)

with col2:
    heating_exists = st.radio("3. Czy jest instalacja ogrzewania podłogowego?", ["TAK", "NIE"], index=1, horizontal=True)
    heating_info = ""
    heating_curing_done = "NIE"
    if heating_exists == "TAK":
        h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne", "płyta fundamentowa grzewcza"])
        heating_curing_done = st.radio("Czy wygrzewanie zostało zakończone?", ["TAK", "NIE"], index=1, horizontal=True)
        heating_info = h_type

# Logika LVT Cienkie (Automatyzacja bez rozjazdu formularza)
is_lvt_thin = (flooring_type == "lvt cienkie")
lev_def_idx = 0 if is_lvt_thin else 1
thick_def_val = 3.0 if is_lvt_thin else 0.0

st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=lev_def_idx, horizontal=True)
leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=0.0, value=thick_def_val)

# Stałe pytania WAKOL
st.subheader("Parametry jastrychu")
cw1, cw2 = st.columns(2)
with cw1:
    dil_obw = st.radio("Czy dylatacje obwodowe zachowane prawidłowo?", ["TAK", "NIE"], index=0)
    cracks_klaw = st.radio("Czy występują klawiszujące dylatacje pozorne?", ["TAK", "NIE"], index=1)
    klaw_mb = st.number_input("Ilość mb klawiszujących:", min_value=0.0) if cracks_klaw == "TAK" else 0.0
with cw2:
    cracks_pek = st.radio("Czy występują pęknięcia podłoża wymagające zespolenia?", ["TAK", "NIE"], index=1)
    pek_mb = st.number_input("Ilość mb pęknięć:", min_value=0.0) if cracks_pek == "TAK" else 0.0
    holes = st.radio("Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?", ["TAK", "NIE"], index=1)

moisture = st.number_input("Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)

# Testy mechaniczne
st.header("II. Testy mechaniczne")
ct1, ct2, ct3 = st.columns(3)
test_hammer = ct1.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
test_ripper = ct2.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
test_brush = ct3.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)

strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# ==========================================
# 3. SILNIK LOGICZNY (REGUŁY)
# ==========================================
# Limity CM
limit = 1.5 if substrate == "jastrych cementowy" and heating_exists == "TAK" else 1.8 if substrate == "jastrych cementowy" else 0.3 if substrate == "jastrych anhydrytowy" and heating_exists == "TAK" else 0.5 if substrate == "jastrych anhydrytowy" else 1.5
is_moisture_neg = (moisture > limit) if moisture else False
barrier_max = 2.5 if heating_exists == "TAK" else 3.5

# Decyzja o wilgoci
decision_after_cure = None
if moisture and is_moisture_neg:
    opt_dry = "przeprowadzenie procesu wygrzewania" if heating_exists == "TAK" else "dalsze osuszanie"
    if not (substrate == "jastrych anhydrytowy" or (heating_exists == "TAK" and heating_curing_done == "NIE")):
        if moisture <= barrier_max:
            decision_after_cure = "Wykonanie bariery przeciwwilgociowej"

# ==========================================
# 4. GENEROWANIE RAPORTU
# ==========================================
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None: st.error("Podaj wilgotność!")
    else:
        st.divider(); insert_header()
        
        # --- a) Oględziny optyczne (Pełne raportowanie) ---
        age_txt = f" w wieku {substrate_age} miesięcy" if substrate_age else ""
        h_full = f" Zainstalowano {heating_info}." if heating_exists == "TAK" else " Brak ogrzewania podłogowego."
        c_full = f" Wygrzewanie: {heating_curing_done}." if heating_exists == "TAK" else ""
        dil_txt = " Dylatacje obwodowe: OK." if dil_obw == "TAK" else " Dylatacje obwodowe: NIEPRAWIDŁOWE."
        klaw_txt = f" Klawiszowanie: {klaw_mb} mb." if cracks_klaw == "TAK" else " Brak klawiszowania."
        pek_txt = f" Pęknięcia: {pek_mb} mb." if cracks_pek == "TAK" else " Brak pęknięć."
        lev_txt = f" Planowana masa: {leveling_thickness} mm." if needs_levelling == "TAK" else " Brak masy."
        
        st.markdown(f"**a) oględziny optyczne:** Podłoże pod okładzinę ({flooring_type}) stanowi {substrate}{age_txt}.{h_full}{c_full}{dil_txt}{klaw_txt}{pek_txt}{lev_txt}")
        st.write(f"**b) badanie wilgotności:** Wynik: {moisture}% (Norma: {limit}%) — **{'NEGATYWNY' if is_moisture_neg else 'POZYTYWNY'}**")
        st.write(f"**c) wytrzymałość:** Ocena: {strength_labels[strength_val]} (Młotek: {test_hammer}, Rysik: {test_ripper})")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**a) przygotowanie podłoża:**")
        st.write("* **Szlif podłoża i odkurzenie przemysłowe.**")
        
        # Logika Wygrzewania / Bariery
        norm_txt = f"({limit}% CM)"
        if heating_exists == "TAK" and heating_curing_done == "NIE":
            msg = f"w celu uzyskania wilgotności {norm_txt}." if is_moisture_neg else "zgodnie z protokołem."
            st.write(f"* **Konieczność przeprowadzenia pełnego procesu wygrzewania {msg}**")
        elif decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            st.write("* **Zalecam Wykonanie bariery przeciwwilgociowej.**")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        if holes == "TAK": st.write("- Uzupełnić ubytki zaprawą **WAKOL Z 610**.")
        if klaw_mb > 0 or pek_mb > 0: st.write("- Zespolić pęknięcia/dylatacje żywicą **WAKOL PS 205**.")

        # Wybór gruntu i masy (Reguła LVT + wytrzymałość)
        if needs_levelling == "TAK":
            if is_lvt_thin and strength_val <= 2:
                st.write(FULL_PU280_1W)
                st.write("* **Zastosować mostek sczepny WAKOL D 3045 (150 g/m²).**")
            else:
                st.write(FULL_D3004)
            
            # Masa zależna od okładziny
            if flooring_type in ["wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"]: st.write(FULL_Z675)
            elif flooring_type == "deska warstwowa (drewno, laminat itp.)": st.write(FULL_Z635)
            elif flooring_type == "deska lita": st.write(FULL_Z625)
        else:
            if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
                st.write(FULL_PU280_BARRIER if strength_val > 2 else FULL_PU235_BARRIER)
            else: st.write(FULL_D3004)

        st.write("**c) klejenie okładziny:**")
        if is_lvt_thin:
            st.write("Klejenie winylu: **WAKOL D 3318** (szpachla A2, 350 g/m²). Odparowanie 5-10 min, układanie 10 min.")
        elif substrate == "płyta fundamentowa" or flooring_type == "deska lita":
            st.write("Klejenie klejem **WAKOL MS 260**.")
        elif flooring_type == "deska warstwowa (drewno, laminat itp.)":
            if substrate == "jastrych anhydrytowy" and strength_val == 1: st.write(FULL_MS230)
            else: st.write(f"{FULL_MS230}\n{FULL_PU225}")

        st.divider(); st.write(f"Z poważaniem, Loba-Wakol Polska Sp. z o.o. | {autor}")
