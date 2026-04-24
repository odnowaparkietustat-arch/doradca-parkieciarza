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
        klient = st.text_input("Szanowni Państwo (Klient)", "Szanowni Państwo")
        autor = st.text_input("Autor protokołu", "Przemysław Tyszko")
        data_badania = st.date_input("Data badania", date.today())

st.divider()

# --- WYWIAD TECHNICZNY ---

# 1. Rodzaj okładziny
flooring_options = [
    "deska warstwowa (drewno, laminat itp.)", 
    "deska lita", "wykładzina dywanowa", 
    "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"
]
flooring_type = st.selectbox("1. Rodzaj okładziny", flooring_options)

# 2. Rodzaj podłoża
substrate = st.selectbox("2. Rodzaj podłoża", [
    "jastrych cementowy", "jastrych anhydrytowy", 
    "płyta fundamentowa", "podłoże drewniane (parkiet, deska, OSB)", 
    "płytki ceramiczne", "masa samorozlewna"
])

# Grubość istniejącej masy
existing_levelling_thickness = None
if substrate == "masa samorozlewna":
    existing_levelling_thickness = st.number_input("Grubość wylanej masy (mm):", min_value=1, value=3)

# Wiek podłoża (w miesiącach)
substrate_age_val = None
if any(x in substrate for x in ["jastrych", "płyta", "masa"]):
    substrate_age_val = st.number_input("Wiek podłoża (podaj ilość miesięcy):", min_value=0.5, step=0.5, format="%.1f")

# 3. Ogrzewanie podłogowe - Pełna lista
st.write("3. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")

heating_info = ""
heating_curing_done = None

if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", [
        "wodne klasyczne", 
        "bruzdowane", 
        "w suchej zabudowie", 
        "elektryczne (powierzchniowe)", 
        "elektryczne (głębokie)",
        "płyta fundamentowa grzewcza"
    ])
    
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

# 4. Wyrównanie
st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
leveling_thickness = 0
if needs_levelling == "TAK":
    leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=3)

# 5. Dylatacje obwodowe
st.write("5. Czy dylatacje obwodowe zachowane prawidłowo?")
dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=0, horizontal=True, label_visibility="collapsed")

# 6. Dylatacje pozorne klawiszujące
st.write("6. Czy występują klawiszujące dylatacje pozorne?")
cracks_klaw = st.radio("Klawiszowanie pozorne:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
klaw_meters = 0.0
if cracks_klaw == "TAK":
    klaw_meters = st.number_input("Ilość mb dylatacji pozornych klawiszujących:", min_value=0.1, step=0.1)

# 7. Pęknięcia wymagające zespolenia
st.write("7. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia do zespolenia:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
pek_meters = 0.0
if cracks_pek == "TAK":
    pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", min_value=0.1, step=0.1)

# 8. Ubytki (cm)
st.write("8. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
hole_details = ""
if holes == "TAK":
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1: h_depth = st.number_input("Głębokość (cm)", min_value=0.1, format="%.1f")
    with col_h2: h_width = st.number_input("Szerokość (cm)", min_value=0.1, format="%.1f")
    with col_h3: h_length = st.number_input("Długość (cm)", min_value=0.1, format="%.1f")
    hole_details = f" o wymiarach ok. {h_length}x{h_width} cm i głębokości {h_depth} cm"

# 9. Wentylacja
st.write("9. Rodzaj wentylacji w pomieszczeniu")
ventilation_type = st.radio("Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True, label_visibility="collapsed")

# 10, 11. Warunki otoczenia - POPRAWKA LITERÓWKI
col_w1, col_w2 = st.columns(2)
with col_w1:
    temp_air = st.number_input("10. Temperatura powietrza (°C)", value=20.0, step=0.5)
with col_w2:
    hum_air = st.number_input("11. Wilgotność powietrza (%)", value=50.0, step=1.0)

# 12. Wilgotność podłoża
moisture = st.number_input("12. Poziom wilgoci podłoża (CM %)", value=None, placeholder="Wpisz wynik...", format="%.1f")

# 13. Dodatkowe uwagi
st.write("13. Dodatkowe uwagi")
extra_notes = st.text_area("Wpisz spostrzeżenia z oględzin:")

# --- LOGIKA NORM ---
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
    if moisture <= barrier_max:
        decision_after_cure = st.radio("Postępowanie:", ["Wykonanie bariery przeciwwilgociowej", opt_dry], horizontal=True)
    else:
        st.error(f"❌ Wilgotność za wysoka na barierę (max {barrier_max}%).")
        decision_after_cure = opt_dry

# --- TESTY MECHANICZNE ---
st.write("### Testy mechaniczne i Wytrzymałość")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: test_hammer = st.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t2: test_ripper = st.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t3: test_brush = st.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)

strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości podłoża:", options=[1, 2, 3, 4, 5], value
