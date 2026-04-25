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

# REGUŁA AUTO-PODPOWIEDZI DLA LVT CIENKIE (BEZ "ROZJEŻDŻANIA" FORMULARZA)
is_lvt_thin = (flooring_type == "lvt cienkie")
lev_idx = 0 if is_lvt_thin else 1
thick_val = 3.0 if is_lvt_thin else 0.0

st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=lev_idx, horizontal=True)
leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=0.0, value=thick_val)

# STAŁE PYTANIA WAKOL
st.subheader("Parametry jastrychu")
col_wak1, col_wak2 = st.columns(2)
with col_wak1:
    dilatations_obw_ok = st.radio("1. Czy dylatacje obwodowe zachowane prawidłowo?", ["TAK", "NIE"], index=0)
    cracks_klaw = st.radio("2. Czy występują klawiszujące dylatacje pozorne?", ["TAK", "NIE"], index=1)
    klaw_meters = st.number_input("Ilość mb klawiszujących:", min_value=0.0, step=0.1) if cracks_klaw == "TAK" else 0.0
with col_wak2:
    cracks_pek = st.radio("3. Czy występują pęknięcia podłoża wymagające zespolenia?", ["TAK", "NIE"], index=1)
    pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", min_value=0.0, step=0.1) if cracks_pek == "TAK" else 0.0
    holes = st.radio("4. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?", ["TAK", "NIE"], index=1)
    hole_details_input = ""
    if holes == "TAK":
        hole_details_input = st.text_input("Opisz ubytki (wymiary/głębokość):", "ubytki o głębokości ok. 1-2 cm")

st.write("9. Rodzaj wentylacji")
ventilation_type = st.radio("Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True)

col_w1, col_w2 = st.columns(2)
with col_w1: temp_air = st.number_input("10. Temperatura powietrza (°C)", step=0.5, value=None)
with col_w2: hum_air = st.number_input("11. Wilgotność powietrza (%)", step=1.0, value=None)
moisture = st.number_input("12. Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)

# --- II. TESTY MECHANICZNE ---
st.header("II. Testy mechaniczne i Wytrzymałość")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: test_hammer = st.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t2: test_ripper = st.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t3: test_brush = st.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)

st.write("**Badanie PressoMess**")
presso_col = st.columns(6)
p_vals = []
for i in range(6):
    p_vals.append(presso_col[i].number_input(f"P{i+1}", min_value=0.0, step=0.1))

strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości podłoża:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# --- LOGIKA TECHNOLOGICZNA ---
limit = 1.5 if substrate == "jastrych cementowy" and heating_exists == "TAK" else 1.8 if substrate == "jastrych cementowy" else 0.3 if substrate == "jastrych anhydrytowy" and heating_exists == "TAK" else 0.5 if substrate == "jastrych anhydrytowy" else 1.5
decision_after_cure = None
needs_drying_action = False
if moisture is not None and moisture > limit:
    needs_drying_action = True
    opt_dry = "przeprowadzenie procesu wygrzewania" if heating_exists == "TAK" else "dalsze osuszanie"
    if substrate == "jastrych anhydrytowy" or (heating_exists == "TAK" and heating_curing_done == "NIE"):
        decision_after_cure = opt_dry
    else:
        decision_after_cure = st.radio("Postępowanie z wilgocią:", ["Wykonanie bariery przeciwwilgociowej", opt_dry], horizontal=True)
        needs_drying_action = (decision_after_cure != "Wykonanie bariery przeciwwilgociowej")

# STAŁE TECHNOLOGICZNE WAKOL
FULL_D3004 = "* **Zagruntować podłoże koncentratem gruntówki dyspersyjnej WAKOL D 3004. Proporcje mieszania: 1 część WAKOL D 3004 + 2 części wody; Czas schnięcia: na jastrychach cementowych i betonie po optycznym wyschnięciu ok. 30min. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: ok. 50 g/m² koncentratu.**"
FULL_PU280_1W = "* **Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia – jedna godzina.**"
FULL_Z675 = "* **Wylać masę wyrównawczą WAKOL Z 675 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,0 – 6,5 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2-3 godzinach. Możliwość klejenia podłóg po ok. 24 godzinach przy grubości warstwy do 3 mm, przy większych grubościach czas schnięcia ulega wydłużeniu.**"

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
        dil_info = " Dylatacje obwodowe zostały zachowane prawidłowo." if dilatations_obw_ok == "TAK" else " Dylatacje obwodowe nie zostały zachowane prawidłowo."
        klaw_info = f" Stwierdzono występowanie klawiszujących dylatacji pozornych w ilości {klaw_meters} metrów bieżących." if cracks_klaw == "TAK" else " Nie stwierdzono występowania klawiszujących dylatacji pozornych."
        pek_info = f" Stwierdzono występowanie pęknięć podłoża wymagających zespolenia in ilości {pek_meters} metrów bieżących." if cracks_pek == "TAK" else " Nie stwierdzono występowania pęknięć podłoża wymagających zespolenia."
        holes_info = f" Stwierdzono ubytki lub zdegradowane miejsca wymagające wypełnienia ({hole_details_input})." if holes == "TAK" else " Nie stwierdzono ubytków lub zdegradowanych miejsc wymagających wypełnienia."
        lev_info = f" Podłoże wymaga wyrównania masą wyrównawczą o planowanej grubości {leveling_thickness} milimetrów." if needs_levelling == "TAK" else " Podłoże nie wymaga wyrównania masą wyrównawczą."
        vent_info = f" Rodzaj zastosowanej wentylacji: wentylacja {ventilation_type.lower()}."
        
        full_optical_description = f"Podłoże pod planowaną okładzinę ({flooring_type}) stanowi {substrate}{age_info}.{heat_info_full}{curing_info_full} {dil_info} {klaw_info} {pek_info} {holes_info} {lev_info} {vent_info}"
        st.write(f"**a) oględziny optyczne:** {full_optical_description}")
        
        moisture_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY"
        st.write(f"**b) badanie wilgotności:** Wynik: **{moisture} % CM** (Norma: {limit} % CM) — **Wynik: {moisture_status}**")
        st.write(f"**c) wytrzymałość:** Ocena: **{strength_labels[strength_val]}** (Młotek: {test_hammer}, Rysik: {test_ripper}, Szczotka: {test_brush})")

        st.markdown("#### **II. Zalecenia techniczne**")
        
        curing_not_done = (heating_exists == "TAK" and heating_curing_done == "NIE")
        is_moisture_neg = (moisture > limit)
        norm_val_bracket = f"({limit}% CM)"
        
        st.write("**a) przygotowanie podłoża:**")
        st.write("* **Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni!**")
        st.write("* **Dokładne odkurzenie powierzchni odkurzaczem przemysłowym.**")
        
        if curing_not_done:
            msg = f"w celu uzyskania normatywnego poziomu wilgoci {norm_val_bracket}." if is_moisture_neg else "zgodnie z protokołem."
            st.write(f"* **Konieczność przeprowadzenia pełnego procesu wygrzewania podłoża {msg}**")
        elif is_moisture_neg:
            st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci {norm_val_bracket} poprzez {decision_after_cure}.**")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        if curing_not_done:
            poczatek = f"Po doprowadzeniu do normatywnego poziomu wilgoci {norm_val_bracket} jastrychu poprzez przeprowadzenie procesu wygrzewania" if is_moisture_neg else "Po przeprowadzeniu pełnego procesu wygrzewania"
            st.write(f"**{poczatek} zalecamy:**")
        
        if holes == "TAK": st.write("- Uzupełnić ubytki zaprawą **WAKOL Z 610**.")
        if (klaw_meters + pek_meters) > 0: st.write("- Zespolić pęknięcia/dylatacje żywicą **WAKOL PS 205**.")

        # --- NOWA REGUŁA: DOBÓR GRUNTU POD LVT CIENKIE ---
        if is_lvt_thin:
            if strength_val <= 2:
                st.write("* **Z uwagi na słabą wytrzymałość podłoża pod okładzinę lvt cienkie, należy wykonać gruntowanie wzmacniające:**")
                st.write(FULL_PU280_1W)
                st.write("* **Następnie, w celu zapewnienia przyczepności masy do gruntówki PU, należy zaaplikować specjalistyczny mostek sczepny WAKOL D 3045 (zużycie ok. 150 g/m², czas schnięcia 1h).**")
            else:
                st.write("* **Z uwagi na dobrą wytrzymałość podłoża pod okładzinę lvt cienkie, należy wykonać gruntowanie dyspersyjne:**")
                st.write(FULL_D3004)
            st.write(FULL_Z675)
        else:
            st.write(FULL_D3004)
            if needs_levelling == "TAK": st.write(FULL_Z675)

        st.write("**c) klejenie okładziny:**")
        if is_lvt_thin:
            st.write("Klejenie podłogi winylowej należy przeprowadzić przy użyciu kleju WAKOL D 3318 (szpachla TKB A2, zużycie: 350 g/m²). · Czas wstępnego odparowania: ok. 5 - 10 minut. · Czas układania: ok. 10 minut")
        else:
            st.write("Klejenie okładziny zgodnie z systemem WAKOL dla wybranego rodzaju podłogi.")

        st.divider(); st.markdown(f"<b>Z poważaniem, Loba-Wakol Polska Sp. z o.o. | {autor}</b>", unsafe_allow_html=True)
