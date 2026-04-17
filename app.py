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
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne"])
    mapping = {"wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna", "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana", "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie", "elektryczne": "instalacja ogrzewania podłogowego elektryczna"}
    heating_info = mapping.get(h_type, h_type)

# 4. Wyrównanie
st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
leveling_thickness = 0
if needs_levelling == "TAK":
    leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=3)

# 6. Dylatacje pozorne klawiszujące (WYŻEJ DLA LOGIKI ZALEŻNOŚCI)
st.write("6. Czy występują klawiszujące dylatacje pozorne?")
cracks_klaw = st.radio("Klawiszowanie pozorne:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
klaw_meters = 0.0
if cracks_klaw == "TAK":
    klaw_meters = st.number_input("Ilość mb dylatacji pozornych klawiszujących:", value=0.0, step=0.5)

# 5. Dylatacje obwodowe
st.write("5. Czy dylatacje obwodowe zachowane prawidłowo?")
if cracks_klaw == "TAK":
    dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed", disabled=True)
    st.caption("⚠️ Automatycznie 'NIE' ze względu na klawiszowanie.")
else:
    dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=0, horizontal=True, label_visibility="collapsed")

# 7. Pęknięcia wymagające zespolenia
st.write("7. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia do zespolenia:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
pek_meters = 0.0
if cracks_pek == "TAK":
    pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", value=0.0, step=0.5)

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

# 9, 10, 11 - Wentylacja i warunki
st.write("9. Rodzaj wentylacji w pomieszczeniu")
ventilation_type = st.radio("Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True, label_visibility="collapsed")

col_w1, col_w2 = st.columns(2)
with col_w1: temp_air = st.number_input("10. Temperatura powietrza (°C)", value=20.0)
with col_w2: hum_air = st.number_input("11. Wilgotność powietrza (%)", value=50.0)

# 12. Wilgotność podłoża
moisture = st.number_input("12. Poziom wilgoci podłoża (CM %)", value=None, placeholder="Wpisz wynik...", format="%.1f")

# 13. Dodatkowe uwagi
st.write("13. Dodatkowe uwagi")
extra_notes = st.text_area("Wpisz spostrzeżenia:")

# Logika norm
if substrate == "jastrych anhydrytowy": limit = 0.3 if heating_exists == "TAK" else 0.5
else: limit = 1.5 if heating_exists == "TAK" else 1.8
barrier_max = 2.5 if heating_exists == "TAK" else 3.5

decision_after_cure = None
if moisture is not None and moisture > limit:
    st.warning("💡 Wilgotność ponadnormatywna.")
    opt_dry = "Dalsze osuszanie" if heating_exists == "NIE" else "Kolejny proces wygrzewania"
    if moisture > barrier_max:
        st.error(f"❌ Wilgotność za wysoka na barierę (max {barrier_max}%).")
        decision_after_cure = opt_dry
    else:
        decision_after_cure = st.radio("Postępowanie:", [opt_dry, "Wykonanie bariery przeciwwilgociowej"], horizontal=True)

# --- TESTY MECHANICZNE ---
st.divider()
st.write("### Testy mechaniczne i Wytrzymałość")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: test_hammer = st.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t2: test_ripper = st.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t3: test_brush = st.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)

strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# --- GENERATOR ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN"):
    if moisture is None: st.error("Podaj wilgotność!")
    else:
        st.divider()
        st.markdown("### **Loba-Wakol Polska Sp. z o.o.**")
        st.write(f"**Data:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")
        
        st.markdown("#### **I. Oględziny i badania**")
        obw_txt = "Dylatacje obwodowe zachowane prawidłowo." if dilatations_obw_ok == "TAK" else "Dylatacje obwodowe niezachowane prawidłowo."
        klaw_txt = f" Stwierdzono klawiszujące dylatacje pozorne ({klaw_meters} mb)." if cracks_klaw == "TAK" else ""
        pek_txt = f" Stwierdzono pęknięcia podłoża wymagające zespolenia ({pek_meters} mb)." if cracks_pek == "TAK" else ""
        
        st.write(f"**a) oględziny optyczne:** Podłoże: {substrate}. {heating_info if heating_exists == 'TAK' else 'Brak ogrzewania.'} {obw_txt}{klaw_txt}{pek_txt} Wentylacja: {ventilation_type}.")
        if extra_notes: st.write(f"**Uwagi:** {extra_notes}")
        st.write(f"**b) wytrzymałość:** Młotek: {test_hammer}, Rysik: {test_ripper}, Szczotka: {test_brush}. Ocena: **{strength_labels[strength_val]}**.")
        st.write(f"**c) wilgotność:** {moisture}% CM (Norma: {limit}% CM). Warunki: {temp_air}°C, {hum_air}% RH.")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**a) przygotowanie:** Szlifowanie i odkurzanie podłoża.")
        if decision_after_cure in ["Dalsze osuszanie", "Kolejny proces wygrzewania"]:
            st.write(f"* **Kontynuować {decision_after_cure.lower()} do poziomu {limit}% CM.**")

        st.write("**b) naprawa i wzmocnienie:**")
        total_cracks = klaw_meters + pek_meters
        if total_cracks > 0:
            st.write(f"* Zespolić pęknięcia i dylatacje ({total_cracks} mb) żywicą **WAKOL PS 205**.")
        if holes == "TAK":
            st.write(f"* Ubytki{hole_details} wypełnić zaprawą **WAKOL Z 610**.")

        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            st.write("* **Zalecamy barierę przeciwwilgociową WAKOL PU 280.**")
            st.write("  1 warstwa: 100-150 g/m². 2 warstwa: 100 g/m². Schnięcie 1h/warstwę. Należy zaślepić dylatacje pozorne.")
        else:
            if strength_val >= 4: st.write("* Zalecamy gruntówkę dyspersyjną **WAKOL D 3055** (150 g/m², schnięcie 30 min).")
            elif strength_val == 3: st.write("* Zalecamy gruntówkę wzmacniającą **WAKOL PU 280**.")
            else: st.write("* Zalecamy wzmocnienie żywicą **WAKOL PS 275**.")

        st.write(f"**c) montaż:** Klejenie okładziny **{flooring_type}**.")
        st.divider()
        st.write(f"Z poważaniem, **{autor}**")
