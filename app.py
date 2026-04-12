import streamlit as st

st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="centered")

st.title("🛠️ System Doradztwa Technicznego")
st.subheader("Wywiad Techniczny wg Twoich Wytycznych")

# --- MODUŁ WYWIADU (8 PYTAŃ) ---
with st.form("interview_form"):
    # Q1
    substrate = st.selectbox("1. Rodzaj podłoża", ["Cementowy", "Anhydrytowy", "OSB/MFP", "Stary Lepik"])
    
    # Q2
    heating = st.radio("2. Czy jest instalacja ogrzewania podłogowego?", ["TAK", "NIE"])
    
    # Q3
    needs_levelling = st.radio("3. Czy podłoże wymaga wyrównania (masy)?", ["TAK", "NIE"])
    if needs_levelling == "TAK":
        thickness = st.number_input("Podaj planowaną grubość masy (mm)", min_value=0, value=0)
    
    # Q4
    cracks = st.radio("4. Czy są spękania i ruchome dylatacje?", ["TAK", "NIE"])
    
    # Q5
    holes = st.radio("5. Czy są ubytki w jastrychu?", ["TAK", "NIE"])
    
    # Q6
    moisture = st.number_input("6. Poziom wilgoci jastrychu (CM %)", min_value=0.0, format="%.1f")
    
    # Q7
    strength = st.slider("7. Wytrzymałość jastrychu (1-Słaby, 5-Mocny)", 1, 5, 3)
    
    # Q8
    temp = st.number_input("8. Temperatura powietrza (°C)", value=20)
    humidity = st.number_input("8. Wilgotność powietrza (%)", value=50)

    submit = st.form_submit_button("GENERUJ SYSTEM POSTĘPOWANIA")

# --- LOGIKA DECYZYJNA (TWOJE ZASADY) ---
if submit:
    st.divider()
    st.header("📋 Rekomendacja Techniczna")

    # Logika Wilgotności (Q6 + Q2 + Q1)
    if substrate == "Cementowy":
        limit = 1.5 if heating == "TAK" else 1.8
        if moisture > limit:
            st.error(f"PRZEKROCZONA WILGOTNOŚĆ! (Norma: {limit}% CM)")
            st.write("**WYMÓG:** Zastosuj barierę WAKOL PU 280 (2 warstwy).")
            
    if substrate == "Anhydrytowy":
        limit = 0.3 if heating == "TAK" else 0.5
        if moisture > limit:
            st.error(f"PRZEKROCZONA WILGOTNOŚĆ! (Norma: {limit}% CM)")
            st.write("**WYMÓG:** Zastosuj barierę WAKOL PU 280.")

    # Logika Masy na Anhydrycie (Q3 + Q1)
    if substrate == "Anhydrytowy" and needs_levelling == "TAK" and thickness > 5:
        st.error("UWAGA: Grubość masy powyżej 5mm na anhydrycie!")
        st.write("**SYSTEM:** ZAKAZ D 3004. Obowiązkowo WAKOL PU 280 + zasyp piaskiem kwarcowym.")
    elif substrate == "Anhydrytowy" and needs_levelling == "TAK" and thickness <= 5:
        st.info("Grubość masy do 5mm na anhydrycie.")
        st.write("**SYSTEM:** Można użyć WAKOL D 3004 (po szlifowaniu i odpyleniu).")

    # Logika Mechaniczna (Q4, Q5, Q7)
    if cracks == "TAK":
        st.warning("Wykryto spękania.")
        st.write("**AKCJA:** Klamrowanie żywicą WAKOL PS 205 + klamry stalowe.")
    
    if holes == "TAK":
        st.write("**AKCJA:** Uzupełnienie ubytków szybką zaprawą (np. WAKOL Z 610).")

    if strength <= 2:
        st.warning("Słabe podłoże.")
        st.write("**REKOMENDACJA:** Rozważ wzmocnienie PU 280 lub użycie maty WAKOL EM 140.")

    st.success("Wywiad zakończony. Postępuj zgodnie z powyższą listą.")
