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

# --- DANE IDENTYFIKACYJNE ---
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

# --- WYWIAD TECHNICZNY (BEZ ZMIAN TREŚCI PYTAŃ) ---
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

# --- PARAMETRY MECHANICZNE ---
st.header("II. Parametry mechaniczne")
st.subheader("Badanie wytrzymałości")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1: test_hammer = st.selectbox("Młotek (opukiwanie)", ["pozytywny", "negatywny", "dostateczny"])
with col_m2: test_scratch = st.selectbox("Rysik (twardość)", ["pozytywny", "negatywny", "dostateczny"])
with col_m3: test_brush = st.selectbox("Szczotka (pylenie)", ["pozytywny", "negatywny"])

# --- POMIARY KLIMATYCZNE ---
st.header("III. Pomiary i warunki klimatyczne")
col_cl1, col_cl2, col_cl3 = st.columns(3)
with col_cl1: moisture = st.number_input("Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)
with col_cl2: hum_air = st.number_input("Wilgotność powietrza (%)", step=1.0, value=None)
with col_cl3: temp_air = st.number_input("Temperatura powietrza (°C)", step=0.5, value=None)

presso_results = []
col_p1, col_p2, col_p3 = st.columns(3)
for i in range(6):
    with [col_p1, col_p2, col_p3][i % 3]:
        presso_results.append(st.number_input(f"Próba {i+1} (N/mm²)", min_value=0.0, step=0.1, value=None))

strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena końcowa wytrzymałości:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# --- LOGIKA DECYZJI I NORM ---
limit = 1.5 if (substrate == "jastrych cementowy" and heating_exists == "TAK") else 1.8 if substrate == "jastrych cementowy" else 0.3 if (substrate == "jastrych anhydrytowy" and heating_exists == "TAK") else 0.5
barrier_max = 2.5 if heating_exists == "TAK" else 3.5

decision_after_cure = None
if moisture is not None and moisture > limit:
    if heating_exists == "TAK":
        if heating_curing_done == "NIE":
            decision_after_cure = f"Konieczność doprowadzenia do normatywnego poziomu wilgoci w jastrychu tj. {limit}% CM poprzez wykonanie procesu wygrzewania."
        else:
            opt_dry = f"Konieczność wykonania kolejnego procesu wygrzewania celem doprowadzenia do normatywnego poziomu wilgoci w jastrychu tj. {limit}% CM."
            if strength_val == 1 or moisture > barrier_max: 
                decision_after_cure = opt_dry
            else: 
                decision_after_cure = st.radio("Postępowanie:", ["konieczność wykonania bariery przeciwwilgociowej", opt_dry], horizontal=True)
    else: 
        opt_dry = "dalsze osuszanie"
        if strength_val == 1 or moisture > barrier_max: 
            decision_after_cure = opt_dry
        else: 
            decision_after_cure = st.radio("Postępowanie:", ["konieczność wykonania bariery przeciwwilgociowej", opt_dry], horizontal=True)

# --- STAŁE TECHNOLOGICZNE WAKOL (BEZWZGLĘDNY ZAKAZ SKRACANIA) ---
FULL_PREP = "* **Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni!**\n* **Dokładne odkurzenie powierzchni odkurzaczem przemysłowym.**"
FULL_PS275 = "* **Zalecamy aplikację gruntówki wzmacniającej Wakol PS 275 w dwóch warstwach – grubym wałkiem sznurkowym, zużycie w sumie ok. 700 g/m2. Każda z warstw po 350g/m2, aplikowane po sobie w odstępie jednej godziny. Aplikując gruntówkę Wakol PS 275 należy zwrócić uwagę, aby dobrze wchłaniała się w podłoże i unikać powstawania kałuż na powierzchni jastrychu. Po nałożeniu drugiej warstwy gruntówki w razie potrzeby wykonać posypkę z piasku kwarcowego. Po 7 dniach schnięcia powierzchnię należy przeszlifować papierem o gradacji 24 – 40 usuwając przyklejony do powierzchni piasek kwarcowy i dokładnie odkurzyć.**"
FULL_PU280_BARRIER = "* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. 1 warstwa nałożona wałkiem ok. 100-150 g/m². Czas schnięcia – jedna godzina. 2 warstwa ok. 100 g/m² - czas schnięcia – jedna godzina. Czas do klejenia: 72 godziny od zagruntowania.**"
FULL_PU280_REINFORCE = "* **Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia – jedna godzina.**"
FULL_D3045 = "* **Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu WAKOL D 3045. Aplikować równomiernie za pomocą wałka. Zużycie wynosi ok. 150 g/m². Czas schnięcia 1 godzina.**"
FULL_D3040 = "* **Zagruntować podłoże koncentratem gruntówki dyspersyjnej WAKOL D 3040. Proporcje mieszania: 1 część WAKOL D 3040 + 2 części wody; Czas schnięcia: na jastrychach cementowych i betonie po optycznym wyschnięciu ok. 30min. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: ok. 50 g/m² koncentratu.**"

# --- GENERATOR ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None: st.error("Podaj wilgotność!")
    else:
        st.divider(); insert_header()
        st.write(f"**Data badania:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}")
        
        st.markdown("#### **I. Oględziny optyczne i wywiad techniczny**")
        heating_txt = f"z zainstalowanym ogrzewaniem podłogowym ({heating_info})" if heating_exists == "TAK" else "bez ogrzewania podłogowego"
        curing_txt = f" (wygrzewanie: {heating_curing_done})" if heating_exists == "TAK" else ""
        dil_txt = "Dylatacje obwodowe zachowane prawidłowo." if dilatations_obw_ok == "TAK" else "Dylatacje obwodowe niezachowane prawidłowo."
        klaw_txt = f"Stwierdzono klawiszujące dylatacje pozorne ({klaw_meters} mb)." if cracks_klaw == "TAK" else "Dylatacje pozorne nie klawiszują."
        pek_txt = f"Stwierdzono pęknięcia podłoża ({pek_meters} mb)." if cracks_pek == "TAK" else "Brak pęknięć podłoża."
        holes_txt = f"Występują ubytki lub zdegradowane miejsca: {hole_details}." if holes == "TAK" else "Nie stwierdzono ubytków wymagających wypełnienia."
        level_txt = f"Podłoże wymaga wyrównania masą (grubość ok. {leveling_thickness} mm)." if needs_levelling == "TAK" else "Podłoże nie wymaga wyrównania masą."
        
        full_opt_desc = f"Podłoże pod planowaną okładzinę ({flooring_type}) stanowi {substrate} {f'w wieku ok. {substrate_age_val} mies.' if substrate_age_val else ''}, {heating_txt}{curing_txt}. "
        full_opt_desc += f"{dil_txt} {klaw_txt} {pek_txt} {holes_txt} {level_txt}"
        st.write(full_opt_desc)

        st.markdown("#### **II. Parametry mechaniczne**")
        st.write("**Badanie wytrzymałości:**")
        st.write(f"Młotek (opukiwanie): **{test_hammer}**")
        st.write(f"Rysik (twardość powierzchniowa): **{test_scratch}**")
        st.write(f"Szczotka (pylenie): **{test_brush}**")

        st.markdown("#### **III. Parametry fizyczne**")
        moisture_eval = "pozytywny" if moisture <= limit else "negatywny"
        st.write(f"* Poziom wilgoci podłoża: **{moisture} % CM** (Norma: {limit} % CM) – **Wynik {moisture_eval}**")
        st.write(f"* Temp. powietrza: **{temp_air}°C** | Wilgotność powietrza: **{hum_air}%**")
        valid_p = [v for v in presso_results if v is not None and v > 0]
        if valid_p: st.write(f"* Wytrzymałość PressoMess: {', '.join([str(v) for v in valid_p])} N/mm²")
        st.write(f"* Ocena wytrzymałości końcowa: **{strength_labels[strength_val]}**")

        st.markdown("#### **IV. Zalecenia technologiczne**")
        if decision_after_cure:
            st.write(f"* **{decision_after_cure}**")

        st.write("**a) Przygotowanie podłoża:**")
        st.write(FULL_PREP)
        if (klaw_meters + pek_meters) > 0: st.write(f"* **Zespolenie pęknięć i dylatacje pozorne żywicą WAKOL PS 205.**")

        st.write("**b) Naprawa i wzmocnienie podłoża:**")
        
        # LOGIKA: Jeśli jest formuła "Po doprowadzeniu...", podajemy zalecenia bez ostrzeżeń o blokadzie.
        if heating_exists == "TAK" and heating_curing_done == "NIE":
            after_dry_prefix = f"**Po doprowadzeniu normatywnego poziomu wilgoci tj. {limit}% CM poprzez wykonanie procesu wygrzewania Zalecamy:**"
        else:
            after_dry_prefix = f"**Po doprowadzeniu do normatywnego poziomu wilgoci jastrychu tj. {limit}% CM zalecamy:**" if decision_after_cure and ("osuszanie" in decision_after_cure or "wygrzewania" in decision_after_cure) else ""
        
        if after_dry_prefix: st.write(after_dry_prefix)

        if decision_after_cure == "konieczność wykonania bariery przeciwwilgociowej":
            st.write(FULL_PU280_BARRIER)
            if needs_levelling == "TAK": st.write(FULL_D3045)
        else:
            # W scenariuszu osuszania/wygrzewania podajemy zalecenia tak, jakby podłoże było już gotowe
            if strength_val == 1:
                st.write(FULL_PS275)
                if needs_levelling == "TAK": 
                    st.write(FULL_PU280_REINFORCE)
                    st.write(FULL_D3045)
            elif strength_val == 2:
                st.write(FULL_PU280_REINFORCE)
                if needs_levelling == "TAK": st.write(FULL_D3045)
            elif strength_val >= 3 and needs_levelling == "TAK":
                st.write(FULL_D3040)

        if needs_levelling == "TAK":
            # Wyświetlamy masy bez blokad, ponieważ instrukcja dotyczy stanu "po osuszeniu"
            if "lita" in flooring_type: st.write("* **Wylać masę wyrównawczą WAKOL Z 625 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,00 – 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2 godzinach. Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 6 godzinach, przy warstwie do 10 mm – po 12 godzinach, przy warstwie 30 mm – po 24 godzinach.**")
            elif "warstwowa" in flooring_type: st.write("* **Następnie na podłoże wylać masę wyrównawczą WAKOL Z 635 - Wylewając masę wyrównawczą WAKOL Z 635 wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2,5 godzinach. Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 24 godzinach, przy warstwie do 10 mm – po 72 godzinach.**")
            else: st.write("* **Wylanie masy wyrównawczej Wakol Z 675 w jednej warstwie o grubości 7mm. W proporcji 25kg masy + 6,0 litrów wody. Zużycie 1,5kg/m2 przy 1mm grubości. Wymieszać w czystym pojemniku z zimną wodą w unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić maksymalnie 600 obrotów na minutę. Masę pozostawić do odparowania na ok. 2 - 3 minuty a następnie ponownie przemieszać. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Schnącą masę należy chronić przed działaniem promieni słonecznych i przeciągów. Warstwa do 2 mm - możliwość klejenia i układania po 24 godzinach, do 5 mm - po 48 godzinach, do 10 mm - po 72 godzinach.**")

        st.divider()
        st.markdown(f"**Z poważaniem, Loba-Wakol Polska Sp. z o.o. | Przemysław Tyszko**")
