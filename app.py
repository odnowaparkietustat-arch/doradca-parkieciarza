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
        autor = st.text_input("Autor protokołu", "Przemysław Tyszko")
        data_badania = st.date_input("Data badania", date.today())
        klient = st.text_input("Szanowni Państwo (Klient)", "Stylowe Wnętrza")

st.divider()

# --- WYWIAD TECHNICZNY ---

flooring_type = st.selectbox("1. Rodzaj okładziny", [
    "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", 
    "lvt grube z twardym rdzeniem", "deska warstwowa (drewno, laminat itp.)", "deska lita"
])

substrate = st.selectbox("2. Rodzaj podłoża", [
    "jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", 
    "podłoże drewniane", "płytki ceramiczne"
])

st.write("3. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True)

heating_info = ""
heating_cured = None

if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne"])
    if h_type in ["wodne klasyczne", "elektryczne"]:
        heating_info = h_type
        heating_cured = st.radio("Czy przeprowadzono proces wygrzewania?", ["TAK", "NIE"], index=1, horizontal=True)
    else:
        heating_info = h_type

needs_levelling = st.radio("4. Czy podłoże wymaga wyrównania (masy)?", ["TAK", "NIE"], index=1, horizontal=True)

cracks = st.radio("5. Czy są spękania i ruchome dylatacje?", ["TAK", "NIE"], index=1, horizontal=True)
cracks_meters = 0
if cracks == "TAK":
    cracks_meters = st.number_input("Ilość metrów bieżących (mb)", 0.0, step=0.5)

st.write("6. Czy są ubytki w jastrychu bądź niestabilne zdegradowane fragmenty wymagające skucia i uzupełnienia?")
holes = st.radio("Ubytki/Degradacja:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
h_dim = {"l":0.0, "w":0.0, "d":0.0}
if holes == "TAK":
    c1, c2, c3 = st.columns(3)
    h_dim["l"] = c1.number_input("Długość", 0.0)
    h_dim["w"] = c2.number_input("Szerokość", 0.0)
    h_dim["d"] = c3.number_input("Głębokość", 0.0)

moisture = st.number_input(f"7. Poziom wilgoci podłoża: {substrate} (CM %)", 0.0, format="%.1f")

# Określenie normy dla logiki
if substrate == "jastrych anhydrytowy":
    limit = 0.3 if heating_exists == "TAK" else 0.5
else:
    limit = 1.5 if heating_exists == "TAK" else 1.8

decision_after_cure = None
if heating_cured == "TAK" and moisture > limit:
    st.info("💡 Proces wygrzewania został przeprowadzony, ale wilgotność jest nadal ponadnormatywna.")
    decision_after_cure = st.radio(
        "Wybierz dalszy sposób postępowania:",
        ["Kolejny proces wygrzewania", "Wykonanie bariery przeciwwilgociowej"],
        horizontal=True
    )

st.write("8. Wytrzymałość jastrychu / płyty")
strength_labels = {1:"Bardzo słaby", 2:"Słaby", 3:"Umiarkowanie słaby", 4:"Umiarkowanie mocny", 5:"Mocny"}
strength_val = st.select_slider("Skala:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

ventilation_type = st.radio("9. Rodzaj wentylacji:", ["Grawitacyjna", "Mechaniczna (Rekuperacja)"], horizontal=True)
temp = st.number_input("10. Temperatura powietrza (°C)", 20)
humidity = st.number_input("10. Wilgotność powietrza (%)", 50)

# --- PRZYCISK GENEROWANIA ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN"):
    st.divider()
    
    m_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY"
    s_status = "pozytywna" if strength_val >= 4 else "dostateczna" if strength_val == 3 else "negatywna"

    st.markdown(f"### **Loba-Wakol Polska Sp. z o.o.**")
    st.write(f"**Data:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
    
    st.markdown(f"#### **I. Oględziny i badania**")
    st.write(f"**Podłoże:** {substrate}. Ogrzewanie: {heating_info if heating_exists == 'TAK' else 'Brak'}.")
    st.write(f"**Badanie wilgotności:** {moisture} % CM (Norma: {limit} % CM) - Status: {m_status}")

    st.markdown(f"#### **II. Zalecenia techniczne**")
    
    # --- PUNKT A: PRZYGOTOWANIE PODŁOŻA ---
    st.write("**a) przygotowanie podłoża:**")
    st.write("* Szlif podłoża w celu usunięcia mleczka i otwarcia porów, dokładne odkurzenie.")
    if decision_after_cure == "Kolejny proces wygrzewania":
        st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci ({limit}% CM) poprzez przeprowadzenie kolejnego procesu wygrzewania.**")

    # --- PUNKT B: NAPRAWA I WZMOCNIENIE ---
    st.write("**b) naprawa i wzmocnienie podłoża:**")
    
    # Nagłówek sekcji B przy ponownym wygrzewaniu
    if decision_after_cure == "Kolejny proces wygrzewania":
        st.write(f"* **Po doprowadzeniu do normatywnego poziomu wilgoci w jastrychu, to jest {limit}% CM, zalecamy:**")
    
    # Szczegółowe zalecenia naprawcze
    if cracks == "TAK":
        st.write(f"    * Zespolenie spękań żywicą **WAKOL PS 205**.")
    if holes == "TAK":
        st.write(f"    * Uzupełnienie ubytków zaprawą **WAKOL Z 610**.")
    if strength_val <= 3:
        st.write(f"    * Wzmocnienie podłoża żywicą **WAKOL PU 280**.")
    
    # Logika dla bariery lub standardowego gruntowania
    if moisture > limit:
        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            st.write("* Wykonanie bariery przeciwwilgociowej żywicą **WAKOL PU 280** (2 warstwy).")
    elif moisture <= limit:
        st.write("* Gruntowanie podłoża koncentratem **WAKOL D 3004** (1:1 z wodą).")

    if needs_levelling == "TAK":
        st.write("* Wyrównanie powierzchni systemem: mata **WAKOL AR 150** + masa **WAKOL Z 645/635**.")

    st.markdown(f"**c) montaż okładziny:** Montaż okładziny **{flooring_type}** zgodnie z wytycznymi producenta i kartami technicznymi WAKOL.")
