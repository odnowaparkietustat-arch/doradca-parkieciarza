import streamlit as st

st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="centered")

st.title("🛠️ System Doradztwa Technicznego")
st.subheader("Wywiad Techniczny wg Twoich Wytycznych")

# --- MODUŁ WYWIADU (DYNAMICZNY) ---

# Q1 - Rodzaj podłoża
substrate = st.selectbox("1. Rodzaj podłoża", [
    "Cementowy", 
    "Anhydrytowy", 
    "Inny mineralny (masa szpachlowa)", 
    "OSB", 
    "Parkiet/deski", 
    "Płytki ceramiczne", 
    "Płyta fundamentowa"
])

# Q2 - Ogrzewanie podłogowe (Dynamiczne)
st.write("2. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Wybierz odpowiedź:", ["TAK", "NIE"], index=1, label_visibility="collapsed")

heating_type = None

# Lista pojawia się natychmiast po zaznaczeniu TAK
if heating_exists == "TAK":
    heating_type = st.selectbox("Wybierz główny rodzaj ogrzewania:", [
        "Ogrzewanie wodne klasyczne", 
        "Ogrzewanie bruzdowane", 
        "Ogrzewanie w suchej zabudowie",
        "Ogrzewanie elektryczne głęboko w jastrychu/pod jastrychem", 
        "Ogrzewanie elektryczne na siatce/na powierzchni jastrychu"
    ])

# Q3 - Wyrównanie (Dynamiczne)
needs_levelling = st.radio("3. Czy podłoże wymaga wyrównania (masy)?", ["TAK", "NIE"], index=1)
thickness = 0
if needs_levelling == "TAK":
    thickness = st.number_input("Podaj planowaną grubość masy (mm)", min_value=0, value=0)

# Pozostałe pytania
cracks = st.radio("4. Czy są spękania i ruchome dylatacje?", ["TAK", "NIE"], index=1)
holes = st.radio("5. Czy są ubytki w jastrychu?", ["TAK", "NIE"], index=1)
moisture = st.number_input("6. Poziom wilgoci jastrychu (CM %)", min_value=0.0, format="%.1f")
strength = st.slider("7. Wytrzymałość jastrychu (1-Słaby, 5-Mocny)", 1, 5, 3)
temp = st.number_input("8. Temperatura powietrza (°C)", value=20)
humidity = st.number_input("8. Wilgotność powietrza (%)", value=50)

# Przycisk generowania
submit = st.button("GENERUJ SYSTEM POSTĘPOWANIA")

# --- LOGIKA DECYZYJNA ---
if submit:
    st.divider()
    st.header("📋 Rekomendacja Techniczna")

    if heating_exists == "TAK":
        st.info(f"System grzewczy: {heating_type}")

    # 1. Logika Wilgotności
    if substrate == "Cementowy":
        limit = 1.5 if heating_exists == "TAK" else 1.8
        if moisture > limit:
            st.error(f"PRZEKROCZONA WILGOTNOŚĆ DLA CEMENTU! (Norma: {limit}% CM)")
            st.write("**SYSTEM:** Wymagana blokada przeciwwilgociowa: **WAKOL PU 280 (2 warstwy)**.")
            
    elif substrate == "Anhydrytowy":
        limit = 0.3 if heating_exists == "TAK" else 0.5
        if moisture > limit:
            st.error(f"PRZEKROCZONA WILGOTNOŚĆ DLA ANHYDRYTU! (Norma: {limit}% CM)")
            st.write("**SYSTEM:** Blokada wilgoci: **WAKOL PU 280**.")

    # 2. Logika Masy na Anhydrycie
    if substrate == "Anhydrytowy" and needs_levelling == "TAK":
        if thickness > 5:
            st.error("UWAGA: Grubość masy powyżej 5mm na anhydrycie!")
            st.write("**SYSTEM:** ZAKAZ gruntowania D 3004. Wymagane: **WAKOL PU 280 + zasyp piaskiem kwarcowym**.")
        else:
            st.info("Grubość masy do 5mm na anhydrycie.")
            st.write("**SYSTEM:** Gruntowanie: **WAKOL D 3004** (po szlifowaniu i odpyleniu).")

    # 3. Mechanika
    if cracks == "TAK":
        st.warning("Wykryto spękania lub ruchome dylatacje.")
        st.write("**AKCJA:** Szycie podłoża: **WAKOL PS 205 + klamry stalowe**.")
    
    if holes == "TAK":
        st.write("**AKCJA:** Naprawa ubytków: **WAKOL Z 610**.")

    # 4. Wytrzymałość
    if strength <= 2:
        st.warning("Niska wytrzymałość podłoża.")
        st.write("**REKOMENDACJA:** Wzmocnienie żywicą **WAKOL PU 280** lub zastosowanie maty odcinającej **WAKOL EM 140**.")

    st.success("Analiza techniczna zakończona."))
