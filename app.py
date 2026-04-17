import streamlit as st
from datetime import date

# 1. KONFIGURACJA STRONY
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
flooring_type = st.selectbox("1. Rodzaj okładziny", [
    "deska warstwowa (drewno, laminat itp.)", 
    "deska lita",
    "wykładzina dywanowa", 
    "pcv w rolce", 
    "lvt cienkie", 
    "lvt grube z twardym rdzeniem"
])

substrate = st.selectbox("2. Rodzaj podłoża", [
    "jastrych cementowy", 
    "jastrych anhydrytowy", 
    "płyta fundamentowa", 
    "podłoże drewniane", 
    "płytki ceramiczne"
])

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
st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
leveling_thickness = 0
if needs_levelling == "TAK":
    leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, max_value=30, value=3)

st.write("5. Czy dylatacje zachowane prawidłowo?")
dilatations_ok = st.radio("Dylatacje prawidłowe:", ["TAK", "NIE"], index=0, horizontal=True, label_visibility="collapsed")

st.write("6. Czy są spękania i ruchome dylatacje (klawiszujące)?")
cracks = st.radio("Spękania/Klawiszowanie:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
cracks_meters = 0.0
if cracks == "TAK":
    cracks_meters = st.number_input("Ilość metrów bieżących (mb)", value=0.0, step=0.5)

# 7. Ubytki - ZMIANA: Nowy opis i pola wyboru
st.write("7. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?")
holes = st.radio("Ubytki/Degradacja:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
hole_details = ""
if holes == "TAK":
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        h_depth = st.number_input("Głębokość (mm)", min_value=1, step=1, key="h_depth")
    with col_h2:
        h_width = st.number_input("Szerokość (mm)", min_value=1, step=1, key="h_width")
    with col_h3:
        h_length = st.number_input("Długość (mm)", min_value=1, step=1, key="h_length")
    hole_details = f" o wymiarach ok. {h_length}x{h_width} mm i głębokości {h_depth} mm"

moisture = st.number_input("8. Poziom wilgoci podłoża (CM %)", value=None, placeholder="Wpisz wynik pomiaru CM...", format="%.1f")

st.write("9. Dodatkowe uwagi")
extra_notes = st.text_area("Wpisz dodatkowe spostrzeżenia z oględzin:", placeholder="Dodatkowe informacje dla klienta...")

# Logika norm
if substrate == "jastrych anhydrytowy":
    limit = 0.3 if heating_exists == "TAK" else 0.5
else:
    limit = 1.5 if heating_exists == "TAK" else 1.8

barrier_max = 2.5 if heating_exists == "TAK" else 3.5

decision_after_cure = None
if moisture is not None and moisture > limit:
    st.warning(f"💡 Wilgotność ponadnormatywna ({moisture}% CM > {limit}% CM).")
    opt_dry = "Dalsze osuszanie" if heating_exists == "NIE" else "Kolejny proces wygrzewania"
    
    if moisture > barrier_max:
        st.error(f"❌ Wilgotność {moisture}% CM przekracza dopuszczalny próg dla bariery żywicznej ({barrier_max}% CM).")
        decision_after_cure = opt_dry
    else:
        decision_after_cure = st.radio("Dalsze postępowanie:", [opt_dry, "Wykonanie bariery przeciwwilgociowej"], horizontal=True)

# --- TESTY MECHANICZNE ---
st.write("### Testy mechaniczne podłoża")
test_options_std = ["negatywny", "dostateczny", "pozytywny"]
test_options_brush = ["negatywny", "pozytywny"]

col_t1, col_t2, col_t3 = st.columns(3)
with col_t1:
    test_hammer = st.selectbox("Wynik testu młotkiem", test_options_std, index=2)
with col_t2:
    test_ripper = st.selectbox("Wynik testu rysikiem", test_options_std, index=2)
with col_t3:
    test_brush = st.selectbox("Wynik testu szczotką drucianą", test_options_brush, index=1)

default_strength = 3
if test_hammer == "negatywny" or test_brush == "negatywny":
    default_strength = 1
elif test_hammer == "dostateczny" or test_ripper == "negatywny":
    default_strength = 2
elif test_ripper == "dostateczny":
    default_strength = 3
elif test_ripper == "pozytywny":
    default_strength = 5

strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
st.write("10. Wytrzymałość jastrychu / płyty")
strength_val = st.select_slider("Skala wytrzymałości:", options=[1, 2, 3, 4, 5], value=default_strength, format_func=lambda x: strength_labels[x])

ventilation_type = st.radio("11. Rodzaj wentylacji:", ["Grawitacyjna", "Mechaniczna"], horizontal=True)
temp = st.number_input("12. Temperatura powietrza (°C)", value=None, placeholder="°C")
humidity = st.number_input("12. Wilgotność powietrza (%)", value=None, placeholder="%")

# --- GENEROWANIE PROTOKOŁU ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN"):
    if moisture is None:
        st.error("Proszę wpisać poziom wilgoci!")
    else:
        st.divider()
        m_status = "POZYTYWNY" if moisture <= limit else "NEGATWVNY"

        st.markdown("### **Loba-Wakol Polska Sp. z o.o.**")
        st.write(f"**Data badania:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")
        st.write(f"**Szanowni Państwo:** {klient}")

        st.markdown("#### **I. Oględziny i badania**")
        
        dilation_text = ""
        if dilatations_ok == "TAK":
            if cracks == "NIE":
                dilation_text = " Dylatacje zachowane prawidłowo."
        else:
            dilation_text = " Brak prawidłowych dylatacji."

        st.write(f"**a) oględziny optyczne:** Podłoże stanowi {substrate}. {heating_info if heating_exists == 'TAK' else 'Brak instalacji ogrzewania podłogowego.'}{dilation_text} Wentylacja: **{ventilation_type}**.")
        
        if extra_notes:
            st.write(f"**Uwagi dodatkowe:** {extra_notes}")
            
        if heating_exists == 'TAK':
            st.write(f"**Proces wygrzewania podłoża:** {'przeprowadzony' if heating_cured == 'TAK' else 'nie przeprowadzony'}")
        
        st.write("**b) badanie wytrzymałości:**")
        st.write(f"* próba młotkiem – **{test_hammer}**\n* próba szczotką drucianą – **{test_brush}**\n* próba rysikiem – **{test_ripper}**")
        st.write(f"* Ocena ogólna wytrzymałości: **{strength_labels[strength_val]}**")
        
        st.write(f"**c) badanie wilgotności podłoża:** Wynik **{moisture} % CM** (Norma: {limit} % CM) - Status: **{m_status}**")
        st.write(f"**d) warunki klimatyczne:** {temp if temp else '--'}°C | {humidity if humidity else '--'}% RH.")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**a) przygotowanie podłoża:**")
        
        if heating_exists == "TAK" and heating_cured == "NIE":
            if any(x in heating_info for x in ["wodna", "wewnątrz jastrychu"]) or substrate == "płyta fundamentowa":
                st.write("* **Przeprowadzenie pełnego procesu wygrzewania zgodnie z protokołem temperatura wody w instalacji minimum 40 stopni!**")

        if decision_after_cure in ["Dalsze osuszanie", "Kolejny proces wygrzewania"]:
            st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci ({limit}% CM) poprzez kontynuowanie procesu {decision_after_cure.lower()}.**")

        st.write("* Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni.\n* Dokładne odkurzenie całej powierzchni.")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        
        if cracks == "TAK": 
            st.write(f"    * Klawiszujące fragmenty ({cracks_meters} mb) zespolić żywicą laną **WAKOL PS 205**.")
        
        if holes == "TAK": 
            st.write(f"    * Ubytki i zdegradowane fragmenty{hole_details} uzupełnić zaprawą **WAKOL Z 610**.")
        
        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
