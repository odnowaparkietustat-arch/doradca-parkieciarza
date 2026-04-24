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
flooring_options = [
    "deska warstwowa (drewno, laminat itp.)", 
    "deska lita", 
    "wykładzina dywanowa", 
    "pcv w rolce", 
    "lvt cienkie", 
    "lvt grube z twardym rdzeniem"
]
flooring_type = st.selectbox("1. Rodzaj okładziny", flooring_options)

substrate = st.selectbox("2. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane (parkiet, deska, OSB)", "płytki ceramiczne", "masa samorozlewna"])

substrate_age_val = st.number_input("Wiek podłoża (podaj ilość miesięcy):", min_value=0.5, step=0.5, format="%.1f", value=None, placeholder="Wpisz ilość miesięcy...")

st.write("3. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")

heating_info = ""
heating_curing_done = None

if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne (powierzchniowe)", "elektryczne (głębokie)", "płyta fundamentowa grzewcza"])
    if h_type in ["wodne klasyczne", "płyta fundamentowa grzewcza"]:
        st.write("❓ Czy został przeprowadzony proces wygrzewania zgodnie z protokołem?")
        heating_curing_done = st.radio("Proces wygrzewania:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
    mapping = {
        "wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna", 
        "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana", 
        "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie", 
        "elektryczne (powierzchniowe)": "instalacja ogrzewania podłogowego elektryczna, powierzchniowa",
        "elektryczne (głębokie)": "instalacja ogrzewania podłogowego elektryczna, umieszczona głęboko w podłożu",
        "płyta fundamentowa grzewcza": "ogrzewanie realizowane poprzez płytę fundamentową grzewczą"
    }
    heating_info = mapping.get(h_type, h_type)

st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
leveling_thickness = 0
if needs_levelling == "TAK":
    leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=None, placeholder="Wpisz mm...")

st.write("5. Czy dylatacje obwodowe zachowane prawidłowo?")
dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=0, horizontal=True, label_visibility="collapsed")

st.write("6. Czy występują klawiszujące dylatacje pozorne?")
cracks_klaw = st.radio("Klawiszowanie pozorne:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
klaw_meters = 0.0
if cracks_klaw == "TAK":
    klaw_meters = st.number_input("Ilość mb dylatacji pozornych klawiszujących:", min_value=0.1, step=0.1, value=None, placeholder="Wpisz mb...")

st.write("7. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia do zespolenia:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
pek_meters = 0.0
if cracks_pek == "TAK":
    pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", min_value=0.1, step=0.1, value=None, placeholder="Wpisz mb...")

st.write("8. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
hole_details = ""
if holes == "TAK":
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1: h_depth = st.number_input("Głębokość (cm)", min_value=0.1, format="%.1f", value=None, placeholder="cm...")
    with col_h2: h_width = st.number_input("Szerokość (cm)", min_value=0.1, format="%.1f", value=None, placeholder="cm...")
    with col_h3: h_length = st.number_input("Długość (cm)", min_value=0.1, format="%.1f", value=None, placeholder="cm...")
    if h_depth and h_width and h_length:
        hole_details = f" o wymiarach ok. {h_length}x{h_width} cm i głębokości {h_depth} cm"

st.write("9. Rodzaj wentylacji w pomieszczeniu")
ventilation_type = st.radio("Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True, label_visibility="collapsed")

col_w1, col_w2 = st.columns(2)
with col_w1:
    temp_air = st.number_input("10. Temperatura powietrza (°C)", step=0.5, value=None, placeholder="°C...")
with col_w2:
    hum_air = st.number_input("11. Wilgotność powietrza (%)", step=1.0, value=None, placeholder="% RH...")

moisture = st.number_input("12. Poziom wilgoci podłoża (CM %)", placeholder="Wpisz wynik CM...", format="%.1f", value=None)

# --- TESTY MECHANICZNE ---
st.write("### Testy mechaniczne i Wytrzymałość")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: test_hammer = st.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t2: test_ripper = st.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t3: test_brush = st.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)

presso_results = []
for i in range(6):
    res = st.number_input(f"Próba {i+1} (N/mm²)", min_value=0.0, step=0.1, format="%.1f", key=f"presso_{i}", value=None, placeholder="N/mm²...")
    presso_results.append(res)

strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości podłoża:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# --- LOGIKA NORM I POSTĘPOWANIA ---
if substrate == "jastrych cementowy":
    limit = 1.5 if heating_exists == "TAK" else 1.8
elif substrate == "jastrych anhydrytowy":
    limit = 0.3 if heating_exists == "TAK" else 0.5
else:
    limit = 1.5

barrier_max = 2.5 if heating_exists == "TAK" else 3.5
decision_after_cure = None

if moisture is not None and moisture > limit:
    st.warning("💡 Wilgotność ponadnormatywna.")
    opt_dry = "dalsze osuszanie" if heating_exists == "NIE" else "kolejny proces wygrzewania"
    
    if heating_exists == "TAK" and heating_curing_done == "NIE":
        st.error("Konieczne jest wykonanie procesu wygrzewania.")
        decision_after_cure = opt_dry
    else:
        if moisture <= barrier_max:
            if strength_val == 1 and needs_levelling == "NIE":
                st.error("⚠️ Podłoże bardzo słabe. Bariera możliwa tylko w systemie z masą wyrównawczą.")
                decision_after_cure = opt_dry
            else:
                decision_after_cure = st.radio("Postępowanie:", ["Wykonanie bariery przeciwwilgociowej", opt_dry], horizontal=True)
        else:
            decision_after_cure = opt_dry

# --- GENEROWANIE PROTOKOŁU ---
st.divider()
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None:
        st.error("Proszę podać wilgotność podłoża!")
    else:
        st.divider()
        insert_header()
        m_status = "POZYTYWNY" if moisture <= limit else "NEGATWVNY"
        st.write(f"**Data badania:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")
        st.markdown("#### **I. Oględziny i badania**")
        
        actual_obw_ok = dilatations_obw_ok if cracks_klaw == "NIE" else "NIE"
        obw_status = "Dylatacje obwodowe zachowane prawidłowo." if actual_obw_ok == "TAK" else "Dylatacje obwodowe niezachowane prawidłowo."
        klaw_desc = f" Stwierdzono klawiszujące dylatacje pozorne ({klaw_meters} mb)." if cracks_klaw == "TAK" else ""
        pek_desc = f" Stwierdzono pęknięcia podłoża wymagające zespolenia ({pek_meters} mb)." if cracks_pek == "TAK" else ""
        st.write(f"**a) oględziny optyczne:** Podłoże stanowi {substrate}. {obw_status}{klaw_desc}{pek_desc} Wentylacja: **{ventilation_type}**.")
        
        st.write(f"**b) badanie wytrzymałości:**")
        valid_presso = [v for v in presso_results if v is not None and v > 0]
        if valid_presso:
            st.write(f"**Wynik badania PressoMess:**")
            for i, val in enumerate(presso_results):
                if val: st.write(f"* Próba {i+1}: **{val} N/mm²**")
        st.write(f"* Ocena ogólna wytrzymałości: **{strength_labels[strength_val]}**")

        st.write(f"**c) badanie wilgotności:** Wynik **{moisture} % CM** (Norma: {limit} % CM) - Status: **{m_status}**")
        
        if substrate == "jastrych cementowy":
            st.info(f"Aby bezpiecznie kleić podłogę drewnianą na jastrychu cementowym, jego wytrzymałość na ścinanie musi wynosić między 1,5 a 2,0 N/mm² a wilgotność nie może przekraczać 1,8% CM. (z ogrzewaniem podłogowym max. 1,5% CM).")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**a) przygotowanie podłoża:**")
        st.write("* **Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni!**")
        st.write("* **Dokładne odkurzenie**")
        
        if decision_after_cure in ["dalsze osuszanie", "kolejny proces wygrzewania"]:
            st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci ({limit}% CM) poprzez {decision_after_cure}.**")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        total_cracks = (klaw_meters if klaw_meters else 0) + (pek_meters if pek_meters else 0)
        moisture_prefix = f"**Po doprowadzeniu do normatywnego poziomu wilgoci tj. {limit}% CM zalecamy:**" if decision_after_cure in ["dalsze osuszanie", "kolejny proces wygrzewania"] else ""

        if total_cracks > 0 or holes == "TAK":
            if moisture_prefix: st.write(f"* {moisture_prefix}")
            if total_cracks > 0: st.write(f"  - Zespolić pęknięcia żywicą **WAKOL PS 205**.")
            if holes == "TAK": st.write(f"  - Uzupełnić ubytki zaprawą **WAKOL Z 610**.")

        # LOGIKA GRUNTOWANIA
        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            if strength_val <= 2:
                st.write("* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez dwukrotne zagruntowanie gruntówką wzmacniającą WAKOL PU 235.**\n1 - warstwa nałożona wałkiem ok. 150 g/m². Czas schnięcia – 3-6 godzin.\n2 warstwa zużycie ok. 100 g/m². Czas schnięcia – 3-6 godzin.\nCzas klejenia 72 godziny od zagruntowania.")
            else:
                st.write("* Z uwagi na podwyższoną wilgotność zalecamy **stworzenie bariery przeciwwilgociowej** gruntówką **WAKOL PU 280**.\n1 warstwa ok. 100-150 g/m². Czas schnięcia – jedna godzina.\n2 warstwa ok. 100 g/m² - czas schnięcia – jedna godzina.\nCzas do klejenia: 72 godziny od zagruntowania.")
            
            if needs_levelling == "TAK":
                st.write(f"* **Następnie należy zaaplikować mostek sczepny za pomocą produktu WAKOL D 3045. Aplikacja wałkiem. Zużycie - 150 gr. Czas schnięcia - 1 godzina.**")
        
        elif decision_after_cure not in ["dalsze osuszanie", "kolejny proces wygrzewania"]:
            p = moisture_prefix + " " if moisture_prefix else ""
            if strength_val == 1:
                if needs_levelling == "NIE":
                    st.write(f"* {p}Zalecamy aplikację gruntówki wzmacniającej **Wakol PS 275** w dwóch warstwach – grubym wałkiem sznurkowym, zużycie w sumie ok. 700 g/m2. Każda z warstw po 350g/m2, aplikowane po sobie w odstępie jednej godziny. Aplikując gruntówkę **Wakol PS 275** należy zwrócić uwagę, aby dobrze wchłaniała się w podłoże i unikać powstawania kałuż na powierzchni jastrychu. Po nałożeniu drugiej warstwy gruntówki w razie potrzeby wykonać posypkę z piasku kwarcowego. Po 7 dniach schnięcia powierzchnię należy przeszlifować papierem o gradacji 24 – 40 usuwając przyklejony do powierzchni piasek kwarcowy i dokładnie odkurzyć.")
                else:
                    st.write(f"* {p}Zalecamy gruntowanie wzmacniające **WAKOL PU 235** (zużycie 150g/m2).")
                    st.write(f"* **Następnie należy zaaplikować mostek sczepny za pomocą produktu WAKOL D 3045.**")
            elif strength_val == 2:
                st.write(f"* {p}Zalecamy gruntowanie **WAKOL PU 280**.")
                if needs_levelling == "TAK":
                    st.write(f"* **Następnie należy zaaplikować mostek sczepny za pomocą produktu WAKOL D 3045.**")
            elif strength_val >= 3 and needs_levelling == "TAK":
                st.write(f"* {p}**Zagruntować podłoże koncentratem WAKOL D 3040 (1:2 z wodą).**")
            elif strength_val >= 4 and needs_levelling == "NIE":
                st.write(f"* {p}Zalecamy zagruntowanie gruntówką **WAKOL D 3055**.")

        # SEKCJA WYRÓWNANIA
        if needs_levelling == "TAK":
            elastic_floors = ["wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"]
            if flooring_type in elastic_floors:
                # AKTUALIZACJA: Pełny opis technologiczny Z 675
                st.write(f"* {moisture_prefix if moisture_prefix else ''} **Wylanie masy wyrównawczej Wakol Z 675 w jednej warstwie o grubości 7mm. W proporcji 25kg masy + 6,0 litrów wody. Zużycie 1,5kg/m2 przy 1mm grubości. Wymieszać w czystym pojemniku z zimną wodą w unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić maksymalnie 600 obrotów na minutę. Masę pozostawić do odparowania na ok. 2 - 3 minuty a następnie ponownie przemieszać. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Schnącą masę należy chronić przed działaniem promieni słonecznych i przeciągów. Warstwa do 2 mm - możliwość klejenia i układania po 24 godzinach, do 5 mm - po 48 godzinach, do 10 mm - po 72 godzinach.**")
            else:
                st.write(f"* {moisture_prefix if moisture_prefix else ''} Wyrównanie: montaż maty **WAKOL AR 150** oraz masy **WAKOL Z 645/635** o grubości {leveling_thickness if leveling_thickness else '--'} mm.")

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
