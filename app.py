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

needs_levelling = st.radio("4. Czy podłoże wymaga wyrównania (masy)?", ["TAK", "NIE"], index=1, horizontal=True)

cracks = st.radio("5. Czy są spękania i ruchome dylatacje?", ["TAK", "NIE"], index=1, horizontal=True)
cracks_meters = 0
if cracks == "TAK":
    cracks_meters = st.number_input("Ilość metrów bieżących (mb)", value=None, placeholder="Wpisz mb...", step=0.5)

st.write("6. Czy są ubytki lub degradacja podłoża?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")

moisture = st.number_input(f"7. Poziom wilgoci podłoża (CM %)", value=None, placeholder="Wpisz wynik pomiaru CM...", format="%.1f")

# Logika norm i progów bariery
if substrate == "jastrych anhydrytowy":
    limit = 0.3 if heating_exists == "TAK" else 0.5
else:
    limit = 1.5 if heating_exists == "TAK" else 1.8

barrier_max = 2.5 if heating_exists == "TAK" else 3.5

decision_after_cure = None
if moisture is not None and moisture > limit:
    st.warning(f"💡 Wilgotność ponadnormatywna ({moisture}% CM > {limit}% CM).")
    
    if heating_exists == "NIE":
        opt_dry = "Dalsze osuszanie"
    else:
        opt_dry = "Kolejny proces wygrzewania"
    
    if moisture > barrier_max:
        st.error(f"❌ Wilgotność {moisture}% CM przekracza dopuszczalny próg dla bariery żywicznej ({barrier_max}% CM). Dopuszczalne jedynie dalsze osuszanie/wygrzewanie.")
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
st.write("8. Wytrzymałość jastrychu / płyty")
strength_val = st.select_slider("Skala wytrzymałości:", options=[1, 2, 3, 4, 5], value=default_strength, format_func=lambda x: strength_labels[x])

ventilation_type = st.radio("9. Rodzaj wentylacji:", ["Grawitacyjna", "Mechaniczna"], horizontal=True)
temp = st.number_input("10. Temperatura powietrza (°C)", value=None, placeholder="°C")
humidity = st.number_input("10. Wilgotność powietrza (%)", value=None, placeholder="%")

# --- GENEROWANIE PROTOKOŁU ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN
