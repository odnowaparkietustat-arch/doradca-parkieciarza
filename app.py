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

# Wybór dylatacji klawiszujących (przeniesiony wyżej dla logiki zależności)
st.write("6. Czy występują dylatacje klawiszujące?")
cracks_klaw = st.radio("Klawiszowanie:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed", key="klaw")
klaw_meters = 0.0
if cracks_klaw == "TAK":
    klaw_meters = st.number_input("Ilość metrów bieżących dylatacji (mb)", value=0.0, step=0.5)

# PUNKT 5: Prawidłowość dylatacji (Zależna od klawiszowania)
st.write("5. Czy dylatacje zachowane prawidłowo?")
if cracks_klaw == "TAK":
    # Jeśli jest klawiszowanie, wymuszamy "NIE"
    dilatations_ok = st.radio("Dylatacje prawidłowe:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed", disabled=True)
    st.caption("⚠️ Automatycznie zaznaczono 'NIE' ze względu na występowanie klawiszowania.")
else:
    dilatations_ok = st.radio("Dylatacje prawidłowe:", ["TAK", "NIE"], index=0, horizontal=True, label_visibility="collapsed")

st.write("7. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed", key="pek")
pek_meters = 0.0
if cracks_pek == "TAK":
    pek_meters = st.number_input("Ilość metrów bieżących pęknięć (mb)", value=0.0, step=0.5)

st.write("8. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?")
holes = st.radio("Ubytki/Degradacja:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
hole_details = ""
if holes == "TAK":
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        h_depth = st.number_input("Głębokość (cm)", min_value=0.1, step=0.1, format="%.1f")
    with col_h2:
        h_width = st.number_input("Szerokość (cm)", min_value=0.1, step=0.1, format="%.1f")
    with col_h3:
        h_length = st.number_input("Długość (cm)", min_value=0.1, step=0.1, format="%.1f")
    hole_details = f" o wymiarach ok. {h_length}x{h_width} cm i głębokości {h_depth} cm"

moisture = st.number_input("9. Poziom wilgoci podłoża (CM %)", value=None, placeholder="Wpisz wynik pomiaru CM...", format="%.1f")

st.write("10. Dodatkowe uwagi")
extra_notes = st.text_area("Wpisz dodatkowe spostrzeżenia z oględzin:")

# Logika norm
substrate = st.selectbox("2. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane", "płytki ceramiczne"])
heating_exists = st.radio("3. Czy jest instalacja ogrzewania podłogowego?", ["TAK", "NIE"], index=1, horizontal=True)

if substrate == "jastrych anhydrytowy":
    limit = 0.3 if heating_exists == "TAK" else 0.5
else:
    limit = 1.5 if heating_exists == "TAK" else 1.8

decision_after_cure = None
if moisture is not None and moisture > limit:
    st.warning(f"💡 Wilgotność ponadnormatywna.")
    opt_dry = "Dalsze osuszanie" if heating_exists == "NIE" else "Kolejny proces wygrzewania"
    decision_after_cure = st.radio("Dalsze postępowanie:", [opt_dry, "Wykonanie bariery przeciwwilgociowej"], horizontal=True)

# --- GENEROWANIE PROTOKOŁU ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN"):
    if moisture is None:
        st.error("Wpisz wilgotność!")
    else:
        st.divider()
        
        st.markdown("### **Loba-Wakol Polska Sp. z o.o.**")
        st.markdown("#### **I. Oględziny i badania**")
        
        # --- NOWA LOGIKA OPISU DYLATACJI I PĘKNIĘĆ ---
        dilation_description = ""
        if dilatations_ok == "TAK":
            if cracks_klaw == "NIE":
                dilation_description = " Dylatacje zachowane prawidłowo."
            if cracks_pek == "TAK":
                dilation_description += f" Stwierdzono pęknięcia podłoża wymagające zespolenia w ilości {pek_meters} mb."
        else:
            dilation_description = " Brak prawidłowych dylatacji."

        st.write(f"**a) oględziny optyczne:** Podłoże stanowi {substrate}.{dilation_description}")
        
        if extra_notes:
            st.write(f"**Uwagi dodatkowe:** {extra_notes}")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**b) naprawa i wzmocnienie podłoża:**")
        
        total_cracks = klaw_meters + pek_meters
        if total_cracks > 0:
            st.write(f"* Wszystkie pęknięcia oraz dylatacje klawiszujące (łącznie ok. {total_cracks} mb) należy zespolić siłowo przy użyciu żywicy lanej **WAKOL PS 205**.")
        
        if holes == "TAK": 
            st.write(f"* Ubytki i zdegradowane fragmenty{hole_details} uzupełnić zaprawą **WAKOL Z 610**.")
        
        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            st.write("* **Zalecamy stworzenie bariery przeciwwilgociowej WAKOL PU 280 (2 warstwy).**")
        
        st.divider()
        st.write(f"Z poważaniem, **{autor}**")
