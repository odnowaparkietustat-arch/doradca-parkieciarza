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

existing_levelling_thickness = None
if substrate == "masa samorozlewna":
    existing_levelling_thickness = st.number_input("Grubość wylanej masy (mm):", min_value=1, value=None, placeholder="Wpisz mm...")

substrate_age_val = None
if any(x in substrate for x in ["jastrych", "płyta", "masa"]):
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

st.write("13. Dodatkowe uwagi")
extra_notes = st.text_area("Wpisz spostrzeżenia z oględzin:")

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
        st.error("Konieczne jest wykonanie procesu wygrzewania (brak protokołu z poprzedniego procesu).")
        decision_after_cure = opt_dry
    elif strength_val == 1:
        st.error("⚠️ Podłoże bardzo słabe i wilgotne. Nie ma możliwości wykonania bariery. Jedyną opcją jest doprowadzenie do normy poprzez osuszanie/wygrzewanie.")
        decision_after_cure = opt_dry
    else:
        if moisture <= barrier_max:
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
        st.write(f"**Szanowni Państwo:** {klient}")
        st.markdown("#### **I. Oględziny i badania**")
        
        actual_obw_ok = dilatations_obw_ok
        if cracks_klaw == "TAK": actual_obw_ok = "NIE"
        obw_status = "Dylatacje obwodowe zachowane prawidłowo." if actual_obw_ok == "TAK" else "Dylatacje obwodowe niezachowane prawidłowo."
        klaw_desc = f" Stwierdzono klawiszujące dylatacje pozorne ({klaw_meters} mb)." if cracks_klaw == "TAK" else " Brak klawiszujących dylatacji."
        pek_desc = f" Stwierdzono pęknięcia podłoża wymagające zespolenia ({pek_meters} mb)." if cracks_pek == "TAK" else " Brak pęknięć wymagających zespolenia."
        curing_txt = " przeprowadzono proces wygrzewania zgodnie z protokołem." if heating_curing_done == "TAK" else " nieprzeprowadzono procesów wygrzewania zgodnie z protokołem." if heating_curing_done == "NIE" else ""
        heat_status_txt = f" {heating_info}.{curing_txt}" if heating_exists == "TAK" else " Brak instalacji ogrzewania podłogowego."
        age_txt = f" Podłoże wykonane {substrate_age_val} miesiąca temu." if substrate_age_val else ""
        thickness_txt = f" (grubość wylanej warstwy: {existing_levelling_thickness} mm)" if existing_levelling_thickness else ""

        st.write(f"**a) oględziny optyczne:** Podłoże stanowi {substrate}{thickness_txt}.{age_txt}{heat_status_txt} {obw_status}{klaw_desc}{pek_desc} Wentylacja: **{ventilation_type}**.")
        if extra_notes: st.write(f"**Uwagi dodatkowe:** {extra_notes}")

        st.write(f"**b) badanie wytrzymałości:**")
        st.write(f"* próba młotkiem: **{test_hammer}**")
        st.write(f"* próba szczotką drucianą: **{test_brush}**")
        st.write(f"* próba rysikiem: **{test_ripper}**")
        
        valid_presso = [v for v in presso_results if v is not None and v > 0]
        if valid_presso:
            st.write(f"**Wynik badania PressoMess:**")
            for i, val in enumerate(presso_results):
                if val: st.write(f"* Próba {i+1}: **{val} N/mm²**")
        
        st.write(f"* Ocena ogólna wytrzymałości: **{strength_labels[strength_val]}**")

        st.write(f"**c) badanie wilgotności podłoża:** Wynik **{moisture} % CM** (Norma: {limit} % CM) - Status: **{m_status}**")
        st.write(f"**d) warunki klimatyczne:** Temp. powietrza: **{temp_air if temp_air else '--'}°C** | Wilgotność powietrza: **{hum_air if hum_air else '--'}% RH**.")

        if substrate == "jastrych cementowy":
            st.info("Aby bezpiecznie kleić podłogę drewnianą na jastrychu cementowym, jego wytrzymałość na ścinanie musi wynosić między 1,5 a 2,0 N/mm² a wilgotność nie może przekraczać 1,8% CM. (z ogrzewaniem podłogowym max. 1,5% CM).")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**a) przygotowanie podłoża:**")
        st.write("* **Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni!**")
        st.write("* **Dokładne odkurzenie**")
        
        if decision_after_cure in ["dalsze osuszanie", "kolejny proces wygrzewania"]:
            st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci ({limit}% CM) poprzez {decision_after_cure}.**")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        total_cracks = (klaw_meters if klaw_meters else 0) + (pek_meters if pek_meters else 0)
        
        # ZASADA: Przed każdą gruntówką/naprawą, jeśli zalecamy suszenie
        moisture_prefix = ""
        if decision_after_cure in ["dalsze osuszanie", "kolejny proces wygrzewania"]:
            moisture_prefix = f"Po doprowadzeniu do normatywnego poziomu wilgoci tj. {limit}% CM zalecamy: "

        # Wyświetlamy sekcję B tylko jeśli są uszkodzenia lub wymagane jest wzmocnienie
        if total_cracks > 0 or holes == "TAK" or (strength_val <= 3 and decision_after_cure != "Wykonanie bariery przeciwwilgociowej"):
            if moisture_prefix and (total_cracks > 0 or holes == "TAK" or strength_val <= 3):
                st.write(f"* {moisture_prefix}")

            if total_cracks > 0:
                st.write(f"  - Wszystkie pęknięcia oraz dylatacje klawiszujące (łącznie ok. {total_cracks} mb) należy zespolić siłowo przy użyciu żywicy lanej **WAKOL PS 205**.")
            if holes == "TAK":
                st.write(f"  - Ubytki i zdegradowane fragmenty{hole_details} uzupełnić zaprawą szybkosprawną **WAKOL Z 610**.")
            
            # Gruntówka wzmacniająca Wakol PS 275
            if strength_val == 1:
                st.write("* Zalecamy aplikację gruntówki wzmacniającej **Wakol PS 275** w dwóch warstwach – grubym wałkiem sznurkowym, zużycie w sumie ok. 700 g/m2. Każda z warstw po 350g/m2, aplikowane po sobie w odstępie jednej godziny. Aplikując gruntówkę **Wakol PS 275** należy zwrócić uwagę, aby dobrze wchłaniała się w podłoże i unikać powstawania kałuż na powierzchni jastrychu. Po nałożeniu drugiej warstwy gruntówki w razie potrzeby wykonać posypkę z piasku kwarcowego. Po 7 dniach schnięcia powierzchnię należy przeszlifować papierem o gradacji 24 – 40 usuwając przyklejony do powierzchni piasek kwarcowy i dokładnie odkurzyć.")
        
        # Sekcja bariery lub gruntowania standardowego
        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            if strength_val == 2:
                st.write("* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez dwukrotne zagruntowanie gruntówką wzmacniającą WAKOL PU 235. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki.**")
                st.write("1 - warstwa nałożona wałkiem ok. 150 g/m². Czas schnięcia – 3-6 godzin.")
                st.write("2 warstwa zużycie ok. 100 g/m². Czas schnięcia – 3-6 godzin.")
                st.write("Czas klejenia 72 godziny od zagruntowania.")
            else:
                st.write("* Z uwagi na podwyższoną wilgotność zalecamy **stworzenie bariery przeciwwilgociowej** poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową **WAKOL PU 280**. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki.")
                st.write("1 warstwa nałożona wałkiem ok. 100-150 g/m². Czas schnięcia – jedna godzina.")
                st.write("2 warstwa ok. 100 g/m² - czas schnięcia – jedna godzina.")
                st.write("Czas do klejenia: 72 godziny od zagruntowania.")
            st.markdown("  *Należy zaślepić dylatacje pozorne przed aplikacją.*")
        elif decision_after_cure not in ["dalsze osuszanie", "kolejny proces wygrzewania"]:
            # Standardowe gruntowanie z uwzględnieniem prefixu wilgotności (jeśli był)
            if strength_val >= 4:
                st.write(f"* {moisture_prefix if moisture_prefix else ''}Zalecamy zagruntowanie całej powierzchni jastrychu gruntówką dyspersyjną **WAKOL D 3055** - aplikacja wałkiem ok. 150 g/m2. Czas schnięcia ok 30 min.")
            elif strength_val == 3:
                st.write(f"* {moisture_prefix if moisture_prefix else ''}Zalecamy zagruntowanie całej powierzchni podłoża gruntówką wzmacniającą **WAKOL PU 280**. Aplikować wałkiem. Nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia 1 godzina. Czas do montażu – 72 godziny.")
            elif strength_val == 2:
                st.write(f"* {moisture_prefix if moisture_prefix else ''}Zalecamy jednokrotną aplikację gruntówki **WAKOL PU 235**. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki. 1 - warstwa nałożona wałkiem ok.150 g/m². Czas schnięcia 3 – 6 godzin. Czas klejenia 72 godziny od zagruntowania.")

        if needs_levelling == "TAK": st.write(f"* Wyrównanie: montaż maty wzmacniającej **WAKOL AR 150** oraz wylanie masy samopoziomującej **WAKOL Z 645/635** o grubości **{leveling_thickness if leveling_thickness else '--'} mm**.")

        st.write(f"**c) montaż okładziny:**")
        ms_230_name = "**WAKOL MS 230** (szpachla **B13**, zużycie **1350 g/m²**)"
        pu_225_name = "**WAKOL PU 225** (szpachla **B11**, zużycie **1250 g/m²**)"

        if flooring_type == "deska lita":
            st.write(f"* Klejenie parkietu litego należy przeprowadzić przy użyciu kleju poliuretanowego {pu_225_name}. Klej nadaje się na ogrzewanie podłogowe.")
        elif flooring_type == "deska warstwowa (drewno, laminat itp.)":
            st.write(f"* Klejenie parkietu należy przeprowadzić przy użyciu jednego z poniższych klejów (do wyboru):\n  - klej elastyczny {ms_230_name}\n  - klej poliuretanowy {pu_225_name}")
        else: st.write(f"* Montaż okładziny **{flooring_type}** należy przeprowadzić zgodnie z systemem WAKOL.")
        
        st.divider()
        
        # --- OFICJALNA KLAUZULA KOŃCOWA - TŁUSTY DRUK ---
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
