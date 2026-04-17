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
flooring_type = st.selectbox("1. Rodzaj okładziny", [
    "deska warstwowa (drewno, laminat itp.)", 
    "deska lita", "wykładzina dywanowa", 
    "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"
])

# 2. Rodzaj podłoża
substrate = st.selectbox("2. Rodzaj podłoża", [
    "jastrych cementowy", "jastrych anhydrytowy", 
    "płyta fundamentowa", "podłoże drewniane", "płytki ceramiczne"
])

# 3. Ogrzewanie podłogowe
st.write("3. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")

heating_info = ""
heating_cured = "nie dotyczy"
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne"])
    mapping = {"wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna", "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana", "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie", "elektryczne": "instalacja ogrzewania podłogowego elektryczna"}
    heating_info = mapping.get(h_type, h_type)
    heating_cured = st.radio("Czy przeprowadzono proces wygrzewania?", ["TAK", "NIE"], index=1, horizontal=True)

# 4. Wyrównanie
st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
leveling_thickness = 0
if needs_levelling == "TAK":
    leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=3)

# 5, 6, 7 - Logika dylatacji i pęknięć (Domyślna kolejność)
st.write("6. Czy występują dylatacje klawiszujące?")
cracks_klaw = st.radio("Klawiszowanie:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
klaw_meters = 0.0
if cracks_klaw == "TAK":
    klaw_meters = st.number_input("Ilość mb dylatacji klawiszujących:", value=0.0, step=0.5)

st.write("5. Czy dylatacje zachowane prawidłowo?")
# Jeśli klaw_meters > 0 lub cracks_klaw == "TAK", wymuszamy "NIE"
def_dil_idx = 1 if cracks_klaw == "TAK" else 0
dilatations_ok = st.radio("Dylatacje prawidłowe:", ["TAK", "NIE"], index=def_dil_idx, horizontal=True, label_visibility="collapsed")

st.write("7. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
pek_meters = 0.0
if cracks_pek == "TAK":
    pek_meters = st.number_input("Ilość mb pęknięć:", value=0.0, step=0.5)

# 8. Ubytki
st.write("8. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
hole_details = ""
if holes == "TAK":
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1: h_depth = st.number_input("Głębokość (cm)", min_value=0.1, format="%.1f")
    with col_h2: h_width = st.number_input("Szerokość (cm)", min_value=0.1, format="%.1f")
    with col_h3: h_length = st.number_input("Długość (cm)", min_value=0.1, format="%.1f")
    hole_details = f" o wymiarach ok. {h_length}x{h_width} cm i głębokości {h_depth} cm"

# 9. Wilgotność
moisture = st.number_input("9. Poziom wilgoci podłoża (CM %)", value=None, placeholder="Wpisz wynik...", format="%.1f")

# 10. Dodatkowe uwagi
st.write("10. Dodatkowe uwagi")
extra_notes = st.text_area("Wpisz spostrzeżenia:", placeholder="Dodatkowe informacje...")

# Logika norm
if substrate == "jastrych anhydrytowy": limit = 0.3 if heating_exists == "TAK" else 0.5
else: limit = 1.5 if heating_exists == "TAK" else 1.8
barrier_max = 2.5 if heating_exists == "TAK" else 3.5

decision_after_cure = None
if moisture is not None and moisture > limit:
    st.warning(f"💡 Wilgotność ponadnormatywna.")
    opt_dry = "Dalsze osuszanie" if heating_exists == "NIE" else "Kolejny proces wygrzewania"
    if moisture > barrier_max:
        st.error(f"❌ Wilgotność za wysoka na barierę.")
        decision_after_cure = opt_dry
    else:
        decision_after_cure = st.radio("Postępowanie:", [opt_dry, "Wykonanie bariery przeciwwilgociowej"], horizontal=True)

# --- TESTY I WARUNKI ---
st.write("### Testy mechaniczne i warunki")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: test_hammer = st.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t2: test_ripper = st.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t3: test_brush = st.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)

strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("11. Wytrzymałość:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

ventilation_type = st.radio("12. Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True)
col_c1, col_c2 = st.columns(2)
with col_c1: temp = st.number_input("13. Temp. powietrza (°C)", value=None)
with col_c2: humidity = st.number_input("13. Wilgotność pow. (%)", value=None)

# --- GENEROWANIE ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN"):
    if moisture is None: st.error("Brak wilgotności!")
    else:
        st.divider()
        st.markdown("### **Loba-Wakol Polska Sp. z o.o.**")
        st.write(f"**Data:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")

        st.markdown("#### **I. Oględziny i badania**")
        
        # Logika opisu dylatacji i pęknięć
        dil_desc = ""
        if dilatations_ok == "TAK" and cracks_klaw == "NIE":
            dil_desc = " Dylatacje zachowane prawidłowo."
        elif dilatations_ok == "NIE" or cracks_klaw == "TAK":
            dil_desc = " Brak prawidłowych dylatacji."
        
        pek_desc = f" Stwierdzono pęknięcia podłoża wymagające zespolenia ({pek_meters} mb)." if cracks_pek == "TAK" else ""
        
        st.write(f"**a) oględziny optyczne:** Podłoże: {substrate}. {heating_info if heating_exists == 'TAK' else 'Brak ogrzewania.'}{dil_desc}{pek_desc}")
        if extra_notes: st.write(f"**Uwagi:** {extra_notes}")
        
        st.write(f"**b) badanie wytrzymałości:** Młotek: {test_hammer}, Szczotka: {test_brush}, Rysik: {test_ripper}. Ocena: **{strength_labels[strength_val]}**")
        st.write(f"**c) wilgotność:** {moisture}% CM (Norma: {limit}% CM). Warunki: {temp}°C, {humidity}% RH.")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**a) przygotowanie:** Szlif i odkurzanie podłoża.")
        if decision_after_cure in ["Dalsze osuszanie", "Kolejny proces wygrzewania"]:
            st.write(f"* **Kontynuować {decision_after_cure.lower()} do poziomu {limit}% CM.**")

        st.write("**b) naprawa i wzmocnienie:**")
        total_cracks = klaw_meters + pek_meters
        if total_cracks > 0:
            st.write(f"* Zespolić pęknięcia/dylatacje ({total_cracks} mb) żywicą **WAKOL PS 205**.")
        if holes == "TAK":
            st.write(f"* Ubytki{hole_details} wypełnić zaprawą **WAKOL Z 610**.")
        
        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            st.write("* **Zalecamy barierę WAKOL PU 280 (2 warstwy). 1 warstwa 100-150g, 2 warstwa 100g. Schnięcie 1h/warstwa. Zaślepić dylatacje pozorne.**")
        else:
            if strength_val >= 4: st.write("* Gruntowanie: **WAKOL D 3055** (150g/m2, schnięcie 30 min).")
            elif strength_val == 3: st.write("* Gruntowanie wzmacniające: **WAKOL PU 280**.")
            elif strength_val <= 2: st.write("* Gruntowanie: **WAKOL PU 235** lub **PS 275**.")

        st.write(f"**c) montaż:** Klejenie okładziny **{flooring_type}** klejem **WAKOL PU 225** (lub zgodnie z systemem).")
        st.divider()
        st.write(f"Z poważaniem, **{autor}**")
