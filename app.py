import streamlit as st
from datetime import date

st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="centered")

# --- DANE IDENTYFIKACYJNE ---
st.title("📄 Generator Protokołu Oględzin WAKOL")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        inwestycja = st.text_input("Nazwa inwestycji / Obiekt", "Budynek mieszkalny")
        miejscowosc = st.text_input("Miejscowość", "Huta Dłutowska")
        adres = st.text_input("Ulica i nr", "ul. Pabianicka 15")
    with col2:
        klient = st.text_input("Szanowni Państwo (Klient)", "Stylowe Wnętrza")
        autor = st.text_input("Autor protokołu", "Przemysław Tyszko")
        data_badania = st.date_input("Data badania", date.today())

st.divider()

# --- WYWIAD TECHNICZNY ---

# 1. Rodzaj okładziny
flooring_type = st.selectbox("1. Rodzaj okładziny", [
    "deska warstwowa (drewno, laminat itp.)", 
    "deska lita",
    "wykładzina dywanowa", 
    "pcv w rolce", 
    "lvt cienkie", 
    "lvt grube z twardym rdzeniem"
])

# 2. Rodzaj podłoża
substrate = st.selectbox("2. Rodzaj podłoża", [
    "jastrych cementowy", 
    "jastrych anhydrytowy", 
    "płyta fundamentowa", 
    "podłoże drewniane", 
    "płytki ceramiczne"
])

# 3. Ogrzewanie podłogowe
st.write("3. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Czy jest instalacja ogrzewania podłogowego?", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")

heating_info = ""
heating_cured = None
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne"])
    
    mapping = {
        "wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna",
        "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana",
        "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie",
        "elektryczne": "instalacja ogrzewania podłogowego elektryczna"
    }
    heating_info = mapping.get(h_type, h_type)
    
    if h_type == "elektryczne":
        el_pos = st.radio("Umiejscowienie ogrzewania elektrycznego:", ["wewnątrz jastrychu", "na powierzchni jastrychu"], horizontal=True)
        heating_info = f"{heating_info} ({el_pos})"
        heating_cured = st.radio("Czy przeprowadzono proces wygrzewania?", ["TAK", "NIE"], index=1, horizontal=True)
    else:
        heating_cured = st.radio("Czy przeprowadzono proces wygrzewania?", ["TAK", "NIE"], index=1, horizontal=True)

# 4. Wyrównanie
needs_levelling = st.radio("4. Czy podłoże wymaga wyrównania (masy)?", ["TAK", "NIE"], index=1, horizontal=True)

# 5. Spękania
cracks = st.radio("5. Czy są spękania i ruchome dylatacje?", ["TAK", "NIE"], index=1, horizontal=True)
cracks_meters = 0
if cracks == "TAK":
    cracks_meters = st.number_input("Ilość metrów bieżących (mb)", value=None, placeholder="Wpisz mb...", step=0.5)

# 6. Ubytki
st.write("6. Czy są ubytki lub degradacja podłoża?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")

# 7. Wilgotność
moisture = st.number_input(f"7. Poziom wilgoci podłoża (CM %)", value=None, placeholder="Wpisz wynik pomiaru CM...", format="%.1f")

# Testy mechaniczne
st.write("### Testy mechaniczne podłoża")
test_options = ["negatywny", "dostateczny", "pozytywny"]
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1:
    test_hammer = st.selectbox("Wynik testu młotkiem", test_options, index=2)
with col_t2:
    test_ripper = st.selectbox("Wynik testu rysikiem", test_options, index=2)
with col_t3:
    test_brush = st.selectbox("Wynik testu szczotką drucianą", test_options, index=2)

# Logika norm
if substrate == "jastrych anhydrytowy":
    limit = 0.3 if heating_exists == "TAK" else 0.5
else:
    limit = 1.5 if heating_exists == "TAK" else 1.8

# Wywiad po wygrzewaniu
decision_after_cure = None
if heating_cured == "TAK" and moisture is not None and moisture > limit:
    st.info("💡 Wilgotność ponadnormatywna mimo wygrzewania.")
    decision_after_cure = st.radio("Dalsze postępowanie:", ["Kolejny proces wygrzewania", "Wykonanie bariery przeciwwilgociowej"], horizontal=True)

# 8. Wytrzymałość
strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
st.write("8. Wytrzymałość jastrychu / płyty")
strength_val = st.select_slider("Skala wytrzymałości:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# 9. Wentylacja i warunki
ventilation_type = st.radio("9. Rodzaj wentylacji:", ["Grawitacyjna", "Mechaniczna"], horizontal=True)
temp = st.number_input("10. Temperatura powietrza (°C)", value=None, placeholder="°C")
humidity = st.number_input("10. Wilgotność powietrza (%)", value=None, placeholder="%")

# --- GENEROWANIE PROTOKOŁU ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN"):
    if moisture is None:
        st.error("Proszę wpisać poziom wilgoci przed generowaniem protokołu!")
    else:
        st.divider()
        m_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY"

        # Nagłówek
        st.markdown("### **Loba-Wakol Polska Sp. z o.o.**")
        st.write("Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki")
        st.write(f"**Data badania:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")
        st.write(f"**Szanowni Państwo:** {klient}")
        st.markdown(f"**Dotyczy:** Protokół z oględzin inwestycji w budynku przy {adres} w miejscowości {miejscowosc}.")

        # Sekcja I
        st.markdown("#### **I. Oględziny i badania**")
        st.write(f"**a) oględziny optyczne:** Podłoże stanowi {substrate}. {heating_info if heating_exists == 'TAK' else 'Brak instalacji ogrzewania podłogowego.'} Wentylacja w pomieszczeniu: **{ventilation_type}**.")
        
        if heating_exists == 'TAK':
            cured_status = "przeprowadzony" if heating_cured == "TAK" else "nie przeprowadzony"
            st.write(f"**Proces wygrzewania podłoża:** {cured_status}")
            
        st.write(f"**b) badanie wytrzymałości:**")
        st.write(f"* próba młotkiem – **{test_hammer}**")
        st.write(f"* próba szczotką drucianą – **{test_brush}**")
        st.write(f"* próba rysikiem – **{test_ripper}**")
        st.write(f"* Ocena ogólna wytrzymałości: **{strength_labels[strength_val]}**")
        
        st.write(f"**c) badanie wilgotności podłoża:** Wynik **{moisture} % CM** (Norma: {limit} % CM) - Status: **{m_status}**")
        st.write(f"**d) warunki klimatyczne:** Temperatura powietrza: **{temp if temp else '--'}°C** | Wilgotność powietrza: **{humidity if humidity else '--'}% RH**.")

        # Sekcja II
        st.markdown("#### **II. Zalecenia techniczne**")
        
        # --- a) PRZYGOTOWANIE PODŁOŻA ---
        st.write("**a) przygotowanie podłoża:**")
        is_mandatory_cure = False
        if heating_exists == "TAK" and heating_cured == "NIE":
            if any(x in heating_info for x in ["wodna", "wewnątrz jastrychu"]) or substrate == "płyta fundamentowa":
                st.write("* **Przeprowadzenie pełnego procesu wygrzewania zgodnie z protokołem temperatura wody w instalacji minimum 40 stopni!**")
                is_mandatory_cure = True

        if decision_after_cure == "Kolejny proces wygrzewania":
            st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci ({limit}% CM) poprzez przeprowadzenie kolejnego procesu wygrzewania.**")

        st.write("* Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni.")
        st.write("* Dokładne odkurzenie całej powierzchni.")

        # --- b) NAPRAWA I WZMOCNIENIE PODŁOŻA ---
        st.write("**b) naprawa i wzmocnienie podłoża:**")
        
        if decision_after_cure == "Kolejny proces wygrzewania" or is_mandatory_cure:
            st.write(f"* **Po doprowadzeniu do normatywnego poziomu wilgoci w jastrychu (tj. {limit}% CM), zalecamy:**")
        
        if cracks == "TAK": st.write(f"    * Klawiszujące fragmenty ({cracks_meters if cracks_meters else 0} mb) zespolić żywicą laną **WAKOL PS 205**.")
        if holes == "TAK": st.write(f"    * Ubytki i zdegradowane fragmenty uzupełnić zaprawą **WAKOL Z 610**.")
        
        if moisture > limit and decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            st.write("* Wykonanie bariery przeciwwilgociowej żywicą **WAKOL PU 280** (2 warstwy).")
        else:
            if strength_val >= 4:
                st.write(f"* Gruntowanie podłoża: **WAKOL D 3055**.")
            elif strength_val == 3: # Umiarkowanie słaby
                st.write("* Zalecamy zagruntowanie całej powierzchni podłoża gruntówką wzmacniającą **WAKOL PU 280**.")
                st.write("  Aplikować wałkiem. Nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki.")
                st.write("  **Zużycie:** ok. 150 g/m². **Czas schnięcia:** 1 godzina. (W zależności od chłonności podłoża zużycie może być większe bądź mniejsze).")
                st.write("  **Czas do montażu:** 72 godziny.")
            elif strength_val == 2: # Słaby (NOWA LOGIKA PU 235)
                st.write("* Zalecamy jednokrotną aplikację gruntówki **WAKOL PU 235**.")
                st.write("  Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki.")
                st.write("  **Zużycie:** 1-warstwa nałożona wałkiem ok. 150 g/m².")
                st.write("  **Czas schnięcia:** 3 – 6 godzin. **Czas klejenia:** 72 godziny od zagruntowania.")
            elif strength_val == 1: # Bardzo słaby
                st.write(f"* Wzmocnienie podłoża żywicą: **WAKOL PS 275**.")

        if needs_levelling == "TAK":
            st.write("* Wyrównanie: mata **WAKOL AR 150** + masa **WAKOL Z 645/635**.")

        # --- c) MONTAŻ OKŁADZINY ---
        st.write("**c) montaż okładziny:**")
        if flooring_type == "deska warstwowa (drewno, laminat itp.)":
            st.write("* Klejenie deski należy przeprowadzić przy użyciu kleju do parkietu **WAKOL PU 225** (szpachla **B11**, zużycie: **1250 g/m²**).")
        else:
            st.write(f"* Montaż okładziny **{flooring_type}** zgodnie z kartami technicznymi WAKOL.")
        
        st.divider()
        st.write(f"Z poważaniem, **{autor}**")
