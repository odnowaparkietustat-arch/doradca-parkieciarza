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
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True)

heating_info = ""
heating_cured = None
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne"])
    heating_info = h_type
    
    if h_type == "elektryczne":
        el_pos = st.radio("Umiejscowienie ogrzewania elektrycznego:", ["wewnątrz jastrychu", "na powierzchni jastrychu"], horizontal=True)
        heating_info = f"elektryczne ({el_pos})"
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
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True)

# 7. Wilgotność
moisture = st.number_input(f"7. Poziom wilgoci podłoża (CM %)", value=None, placeholder="Wpisz wynik pomiaru CM...", format="%.1f")

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
        s_status = "pozytywna" if strength_val >= 4 else "dostateczna" if strength_val == 3 else "negatywna"

        # Nagłówek
        st.markdown("### **Loba-Wakol Polska Sp. z o.o.**")
        st.write("Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki")
        st.write(f"**Data badania:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")
        st.write(f"**Szanowni Państwo:** {klient}")
        st.markdown(f"**Dotyczy:** Protokół z oględzin inwestycji w budynku przy {adres} w miejscowości {miejscowosc}.")

        # Sekcja I - ZMIANA: Usunięto słowo "Ogrzewanie:"
        st.markdown("#### **I. Oględziny i badania**")
        st.write(f"**a) oględziny optyczne:** Podłoże stanowi {substrate}. {heating_info if heating_exists == 'TAK' else 'Brak instalacji ogrzewania podłogowego.'}")
        if heating_cured: st.write(f"**Proces wygrzewania podłoża:** {heating_cured}")
        st.write(f"**b) badanie wytrzymałości:** próba młotkiem – {s_status} | próba szczotką drucianą – {s_status} | próba rysikiem – {s_status}")
        st.write(f"* Ocena ogólna wytrzymałości: **{strength_labels[strength_val]}**")
        st.write(f"**c) badanie wilgotności podłoża:** Wynik **{moisture} % CM** (Norma: {limit} % CM) - Status: **{m_status}**")
        st.write(f"**d) warunki klimatyczne:** {temp if temp else '--'}°C | {humidity if humidity else '--'}% RH. Wentylacja: {ventilation_type}.")

        # Sekcja II
        st.markdown("#### **II. Zalecenia techniczne**")
        
        st.write("**a) przygotowanie podłoża:**")
        
        is_mandatory_cure = False
        if heating_exists == "TAK" and heating_cured == "NIE":
            if "wodne klasyczne" in heating_info or "wewnątrz jastrychu" in heating_info or substrate == "płyta fundamentowa":
                st.write("* **Przeprowadzenie pełnego procesu wygrzewania zgodnie z protokołem temperatura wody w instalacji minimum 40 stopni!**")
                is_mandatory_cure = True

        if decision_after_cure == "Kolejny proces wygrzewania":
            st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci ({limit}% CM) poprzez przeprowadzenie kolejnego procesu wygrzewania.**")

        st.write("* Szlif podłoża w celu usunięcia mleczka i otwarcia porów, dokładne odkurzenie.")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        
        if decision_after_cure == "Kolejny proces wygrzewania" or is_mandatory_cure:
            st.write(f"* **Po doprowadzeniu do normatywnego poziomu wilgoci w jastrychu (tj. {limit}% CM), zalecamy:**")
        
        if cracks == "TAK": st.write(f"    * Klawiszujące fragmenty ({cracks_meters if cracks_meters else 0} mb) zespolić żywicą laną **WAKOL PS 205**.")
        if holes == "TAK": st.write(f"    * Ubytki i zdegradowane fragmenty uzupełnić zaprawą **WAKOL Z 610**.")
        
        if moisture > limit and decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            st.write("* Wykonanie bariery przeciwwilgociowej żywicą **WAKOL PU 280** (2 warstwy).")
        else:
            if strength_val == 5 or strength_val == 4:
                st.write(f"* Gruntowanie podłoża: **WAKOL D 3055**.")
            elif strength_val == 3:
                st.write(f"* Wzmocnienie podłoża żywicą: **WAKOL PU 280**.")
            elif strength_val == 2:
                st.write(f"* Wzmocnienie podłoża żywicą: **WAKOL PU 280** bądź **WAKOL PU 235**.")
            elif strength_val == 1:
                st.write(f"* Wzmocnienie podłoża żywicą: **WAKOL PS 275**.")

        if needs_levelling == "TAK":
            st.write("* Wyrównanie: mata **WAKOL AR 150** + masa **WAKOL Z 645/635**.")

        st.markdown(f"**c) montaż okładziny:** Montaż okładziny **{flooring_type}** zgodnie z kartami technicznymi WAKOL.")
        
        st.write("---")
        st.write(f"Z poważaniem, **{autor}**")
