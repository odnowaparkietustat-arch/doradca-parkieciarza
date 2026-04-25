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

# --- WYWIAD TECHNICZNY ---
st.header("I. Wywiad i dane podstawowe")
col_w1, col_w2 = st.columns(2)
with col_w1:
    flooring_type = st.selectbox("1. Rodzaj okładziny", ["deska warstwowa (drewno, laminat itp.)", "deska lita", "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"])
    substrate = st.selectbox("2. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane", "płytki ceramiczne", "masa samorozlewna"])
    substrate_age_val = st.number_input("Wiek podłoża (miesiące):", min_value=0.5, step=0.5, format="%.1f", value=None)

with col_w2:
    heating_exists = st.radio("3. Czy jest instalacja ogrzewania podłogowego?", ["TAK", "NIE"], index=1, horizontal=True)
    heating_info = ""
    heating_curing_done = None
    if heating_exists == "TAK":
        h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne (powierzchniowe)", "elektryczne (głębokie)", "płyta fundamentowa grzewcza"])
        heating_curing_done = st.radio("Czy przeprowadzono wygrzewanie zgodnie z protokołem?", ["TAK", "NIE"], index=1, horizontal=True)
        heating_info = h_type

needs_levelling = st.radio("4. Czy podłoże wymaga wyrównania (masy)?", ["TAK", "NIE"], index=1, horizontal=True)
leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=None) if needs_levelling == "TAK" else 0

st.subheader("Stan dylatacji i pęknięć")
col_d1, col_d2, col_d3 = st.columns(3)
with col_d1:
    dilatations_obw_ok = st.radio("5. Dylatacje obwodowe (brzegowe)?", ["PRAWIDŁOWE", "BŁĘDNE"], index=0)
with col_d2:
    cracks_klaw = st.radio("6. Klawiszujące dylatacje pozorne?", ["TAK", "NIE"], index=1)
    klaw_meters = st.number_input("Ilość mb klawiszujących:", min_value=0.1, step=0.1, value=None) if cracks_klaw == "TAK" else 0.0
with col_d3:
    cracks_pek = st.radio("7. Pęknięcia podłoża?", ["TAK", "NIE"], index=1)
    pek_meters = st.number_input("Ilość mb pęknięć:", min_value=0.1, step=0.1, value=None) if cracks_pek == "TAK" else 0.0

holes = st.radio("8. Czy występują ubytki punktowe?", ["TAK", "NIE"], index=1, horizontal=True)
hole_details = st.text_input("Opis ubytków:") if holes == "TAK" else ""

# --- BADANIA ORGANOLEPTYCZNE I MECHANICZNE ---
st.header("II. Badania organoleptyczne i mechaniczne")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    test_hammer = st.selectbox("Badanie młotkiem (opukiwanie)", ["Dźwięk czysty - podłoże spójne", "Dźwięk głuchy - lokalne odparzenia", "Dźwięk głuchy - liczne odparzenia"])
with col_m2:
    test_scratch = st.selectbox("Badanie rysikiem (metoda siatki)", ["Brak wykruszeń - jastrych twardy", "Lekkie wykruszenia na skrzyżowaniach", "Głębokie wykruszenia - jastrych słaby"])
with col_m3:
    test_brush = st.selectbox("Badanie szczotką (pylenie)", ["Brak pylenia - powierzchnia mocna", "Lekkie pylenie", "Silne pylenie - luźne frakcje"])

# --- POMIARY KLIMATYCZNE I SIŁOWE ---
st.header("III. Pomiary klimatyczne i wytrzymałościowe")
col_cl1, col_cl2, col_cl3 = st.columns(3)
with col_cl1: moisture = st.number_input("Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)
with col_cl2: hum_air = st.number_input("Wilgotność powietrza (%)", step=1.0, value=None)
with col_cl3: temp_air = st.number_input("Temperatura powietrza (°C)", step=0.5, value=None)

st.write("### Wyniki badania metodą PressoMess")
presso_results = []
col_p1, col_p2, col_p3 = st.columns(3)
for i in range(6):
    with [col_p1, col_p2, col_p3][i % 3]:
        presso_results.append(st.number_input(f"Próba {i+1} (N/mm²)", min_value=0.0, step=0.1, value=None))

strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena końcowa wytrzymałości podłoża:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# --- LOGIKA DECYZJI ---
limit = 1.5 if (substrate == "jastrych cementowy" and heating_exists == "TAK") else 1.8 if substrate == "jastrych cementowy" else 0.3 if (substrate == "jastrych anhydrytowy" and heating_exists == "TAK") else 0.5
barrier_max = 2.5 if heating_exists == "TAK" else 3.5

decision_after_cure = None
if moisture is not None and moisture > limit:
    if heating_exists == "TAK":
        opt_dry = "konieczność wykonania kolejnego procesu wygrzewania" if heating_curing_done == "TAK" else "konieczność przeprowadzenia procesu wygrzewania"
    else:
        opt_dry = "dalsze osuszanie"
    
    if strength_val == 1 or moisture > barrier_max:
        decision_after_cure = opt_dry
    else:
        decision_after_cure = st.radio("Rekomendacja osuszania/bariery:", ["konieczność wykonania bariery przeciwwilgociowej", opt_dry], horizontal=True)

# --- STAŁE TECHNOLOGICZNE WAKOL (1:1) ---
FULL_PS275 = "* **Zalecamy aplikację gruntówki wzmacniającej Wakol PS 275 w dwóch warstwach – grubym wałkiem sznurkowym, zużycie w sumie ok. 700 g/m2. Każda z warstw po 350g/m2, aplikowane po sobie w odstępie jednej godziny. Aplikując gruntówkę Wakol PS 275 należy zwrócić uwagę, aby dobrze wchłaniała się w podłoże i unikać powstawania kałuż na powierzchni jastrychu. Po nałożeniu drugiej warstwy gruntówki w razie potrzeby wykonać posypkę z piasku kwarcowego. Po 7 dniach schnięcia powierzchnię należy przeszlifować papierem o gradacji 24 – 40 usuwając przyklejony do powierzchni piasek kwarcowy i dokładnie odkurzyć.**"
FULL_PU280_BARRIER = "* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. 1 warstwa nałożona wałkiem ok. 100-150 g/m². Czas schnięcia – jedna godzina. 2 warstwa ok. 100 g/m² - czas schnięcia – jedna godzina. Czas do klejenia: 72 godziny od zagruntowania.**"
FULL_PU280_REINFORCE = "* **Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia – jedna godzina.**"
FULL_D3045 = "* **Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu WAKOL D 3045. Produkt należy dokładnie wymieszać przed użyciem. Aplikować równomiernie za pomocą wałka. Zużycie wynosi ok. 150 g/m². Należy zachować czas schnięcia wynoszący minimum 1 godzinę przed przystąpieniem do dalszych prac.**"
FULL_D3040 = "* **Zagruntować podłoże koncentratem gruntówki dyspersyjnej WAKOL D 3040. Proporcje mieszania: 1 część WAKOL D 3040 + 2 części wody; Czas schnięcia: na jastrychach cementowych i betonie po optycznym wyschnięciu ok. 30min. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: ok. 50 g/m² koncentratu.**"

# --- GENERATOR PROTOKOŁU ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None: st.error("Błąd: Wprowadź wilgotność CM!")
    else:
        st.divider(); insert_header()
        st.write(f"**Data badania:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")
        st.write(f"**Szanowni Państwo:** {klient}")
        
        st.markdown("#### **I. Oględziny optyczne i wywiad techniczny**")
        
        # Opis optyczny wzbogacony o pełny wywiad
        heating_txt = f"z aktywnym ogrzewaniem podłogowym ({heating_info})" if heating_exists == "TAK" else "bez instalacji grzewczej"
        curing_txt = f" (wygrzewanie: {heating_curing_done})" if heating_exists == "TAK" else ""
        age_txt = f", wiek podłoża: {substrate_age_val} mies." if substrate_age_val else ""
        
        opt_report = f"Podłoże stanowi {substrate} {age_txt} pod planowaną okładzinę: {flooring_type}. "
        opt_report += f"Zidentyfikowano podłoże {heating_txt}{curing_txt}. "
        opt_report += f"Dylatacje obwodowe oceniono jako: {dilatations_obw_ok}. "
        
        if cracks_klaw == "TAK": opt_report += f"Stwierdzono klawiszujące dylatacje pozorne w ilości {klaw_meters} mb. "
        else: opt_report += "Dylatacje pozorne są stabilne, brak klawiszowania. "
        
        if cracks_pek == "TAK": opt_report += f"Zidentyfikowano pęknięcia jastrychu w ilości {pek_meters} mb. "
        else: opt_report += "Nie stwierdzono pęknięć powierzchniowych podłoża. "
        
        if holes == "TAK": opt_report += f"Występują ubytki punktowe: {hole_details}. "
        
        st.write(opt_report)
        
        st.write(f"**Badania mechaniczne:**")
        st.write(f"* Metoda opukiwania (młotek): **{test_hammer}**")
        st.write(f"* Metoda nacinania (rysik): **{test_scratch}**")
        st.write(f"* Odporność na ścieranie (szczotka): **{test_brush}**")

        st.markdown("#### **II. Warunki klimatyczne i parametry fizyczne**")
        st.write(f"* Poziom wilgoci podłoża: **{moisture} % CM** (Dopuszczalna norma: {limit} % CM)")
        st.write(f"* Temperatura powietrza: **{temp_air if temp_air else '--'}°C** | Wilgotność powietrza: **{hum_air if hum_air else '--'}%**")
        
        valid_p = [v for v in presso_results if v is not None and v > 0]
        if valid_p: st.write(f"* Wytrzymałość PressoMess: {', '.join([str(v) for v in valid_p])} N/mm²")
        st.write(f"* Ocena ogólna wytrzymałości: **{strength_labels[strength_val]}**")

        st.markdown("#### **III. Zalecenia i dobór technologii**")
        st.write("**a) Prace przygotowawcze:**")
        st.write("* **Mechaniczne usunięcie mleczka wapiennego/cementowego poprzez szlifowanie.**")
        st.write("* **Dokładne odkurzenie powierzchni odkurzaczem przemysłowym.**")
        
        if decision_after_cure and ("wygrzewania" in decision_after_cure or "osuszanie" in decision_after_cure):
            st.write(f"* **UWAGA: Stwierdzono {decision_after_cure} celem uzyskania {limit}% CM.**")

        st.write("**b) Gruntowanie i wyrównanie:**")
        if (klaw_meters + pek_meters) > 0: st.write(f"* **Zespolenie pęknięć i dylatacji pozornych żywicą WAKOL PS 205.**")

        if decision_after_cure == "konieczność wykonania bariery przeciwwilgociowej":
            st.write(FULL_PU280_BARRIER)
            if needs_levelling == "TAK": st.write(FULL_D3045)
        else:
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

        # LOGIKA MASY WYRÓWNAWCZEJ (1:1)
        if needs_levelling == "TAK":
            if "lita" in flooring_type:
                st.write("* **Wylać masę wyrównawczą WAKOL Z 625 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,00 – 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2 godzinach. Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 6 godzinach, przy warstwie do 10 mm – po 12 godzinach, przy warstwie 30 mm – po 24 godzinach.**")
            elif "warstwowa" in flooring_type:
                st.write("* **Następnie na podłoże wylać masę wyrównawczą WAKOL Z 635 - Wylewając masę wyrównawczą WAKOL Z 635 wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2,5 godzinach. Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 24 godzinach, przy warstwie do 10 mm – po 72 godzinach.**")
            else:
                st.write("* **Wylanie masy wyrównawczej Wakol Z 675 w jednej warstwie o grubości 7mm. W proporcji 25kg masy + 6,0 litrów wody. Zużycie 1,5kg/m2 przy 1mm grubości. Wymieszać w czystym pojemniku z zimną wodą w unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić maksymalnie 600 obrotów na minutę. Masę pozostawić do odparowania na ok. 2 - 3 minuty a następnie ponownie przemieszać. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Schnącą masę należy chronić przed działaniem promieni słonecznych i przeciągów. Warstwa do 2 mm - możliwość klejenia i układania po 24 godzinach, do 5 mm - po 48 godzinach, do 10 mm - po 72 godzinach.**")

        st.divider()
        st.markdown(f"""
        <div style="font-size: 13px; color: #444; border-top: 1px solid #ccc; padding-top: 10px;">
            <b>Ważne:</b> Zaleca się zapoznanie z aktualnymi Kartami Technicznymi produktów WAKOL.<br>
            Doradztwo techniczne: 603 214 218<br><br>
            Z poważaniem,<br><b>Loba-Wakol Polska Sp. z o.o. | Przemysław Tyszko</b>
        </div>
        """, unsafe_allow_html=True)
