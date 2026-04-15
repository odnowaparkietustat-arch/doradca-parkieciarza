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
        if h_type == "elektryczne":
            el_pos = st.radio("Umiejscowienie ogrzewania elektrycznego:", ["wewnątrz jastrychu", "na powierzchni jastrychu"], horizontal=True)
            if el_pos == "wewnątrz jastrychu":
                heating_info = "elektryczne (wewnątrz jastrychu)"
                heating_cured = st.radio("Czy przeprowadzono proces wygrzewania?", ["TAK", "NIE"], index=1, horizontal=True)
            else:
                el_form = st.radio("Forma ogrzewania powierzchniowego:", ["w formie siatki", "w formie maty"], horizontal=True)
                heating_info = f"elektryczne (na powierzchni, {el_form})"
        else:
            heating_info = "wodne klasyczne"
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

# --- Logika nowej decyzji przy wygrzewaniu ---
decision_after_cure = None
if substrate == "jastrych anhydrytowy":
    limit_check = 0.3 if heating_exists == "TAK" else 0.5
else:
    limit_check = 1.5 if heating_exists == "TAK" else 1.8

if heating_cured == "TAK" and moisture > limit_check:
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
    
    # Logika statusów wilgotności
    if substrate == "jastrych anhydrytowy":
        limit = 0.3 if heating_exists == "TAK" else 0.5
    else:
        limit = 1.5 if heating_exists == "TAK" else 1.8
        
    m_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY"
    s_status = "pozytywna" if strength_val >= 4 else "dostateczna" if strength_val == 3 else "negatywna"

    # --- WZORZEC PROTOKOŁU ---
    st.markdown(f"""
    ### **Loba-Wakol Polska Sp. z o.o.**
    Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki  
    **Data:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}
    
    **Dotyczy:** Protokół z oględzin inwestycji w budynku przy {adres} w miejscowości {miejscowosc}.
    
    #### **I. Oględziny i badania**
    **a) oględziny optyczne**
    Podłoże stanowi {substrate}. 
    {f"Stwierdzono instalację ogrzewania podłogowego ({heating_info})." if heating_exists == "TAK" else "Brak instalacji ogrzewania podłogowego."}
    {f"**Proces wygrzewania podłoża:** {heating_cured}." if heating_cured is not None else ""}
    {f"**Decyzja po wygrzewaniu:** {decision_after_cure}." if decision_after_cure else ""}
    {"Podłoże posiada spękania/klawiszowanie w ilości " + str(cracks_meters) + " mb." if cracks == "TAK" else "Podłoże bez widocznych spękań."}
    
    **b) badanie wytrzymałości**
    * próba młotkiem – {s_status} | próba szczotką drucianą – {s_status} | próba rysikiem – {s_status}
    
    **c) badanie wilgotności podłoża:**
    Wynik pomiaru: **{moisture} % CM – Status: {m_status}**. (Norma: {limit}% CM).
    
    #### **II. Zalecenia techniczne**
    
    **a) przygotowanie podłoża:**
    * Szlif podłoża w celu usunięcia mleczka cementowego/anhydrytowego i uzyskania chłonnej powierzchni.
    * Dokładne odkurzenie.

    **b) naprawa i wzmocnienie podłoża:**
    """)

    # Treść sekcji (b) - Logika naprawcza i wilgotnościowa
    if cracks == "TAK":
        st.write(f"* Klawiszujące fragmenty ({cracks_meters} mb) zespolić żywicą laną **WAKOL PS 205**.")
    
    if holes == "TAK":
        st.write(f"* Ubytki i zdegradowane fragmenty uzupełnić zaprawą **WAKOL Z 610**.")

    if strength_val <= 3:
        st.write("* **Wzmocnienie:** Z uwagi na niewystarczającą wytrzymałość, zastosować żywicę **WAKOL PU 280** lub matę **WAKOL EM 140**.")

    # Specyficzne zalecenie dla wilgotności na podstawie wywiadu
    if moisture > limit:
        if decision_after_cure == "Kolejny proces wygrzewania":
            st.write("* **Osuszanie:** Z uwagi na ponadnormatywną wilgoć mimo wygrzewania, zadecydowano o przeprowadzeniu kolejnego pełnego cyklu wygrzewania jastrychu.")
        elif decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            st.write("* **Bariera:** Z uwagi na brak pożądanych rezultatów wygrzewania, zadecydowano o wykonaniu bariery przeciwwilgociowej żywicą **WAKOL PU 280** (2 warstwy).")
        else:
            if heating_exists == "TAK":
                st.write("* **Osuszanie:** Wymagane wygrzewanie jastrychu. W przypadku braku efektu – bariera **WAKOL PU 280**.")
            else:
                st.write(f"* **Osuszanie:** Naturalne suszenie (wentylacja: {ventilation_type}). W przypadku braku efektu – bariera **WAKOL PU 280**.")
    else:
        st.write("* Podłoże zagruntować koncentratem **WAKOL D 3004** (1:1 z wodą).")

    if needs_levelling == "TAK":
        st.write("* **Wyrównanie:** Mata **WAKOL AR 150** + masa **WAKOL Z 645** / **WAKOL Z 635**.")

    st.markdown(f"""
    **c) montaż okładziny:**
    * Prace montażowe dla okładziny: **{flooring_type}** należy przeprowadzić zgodnie z kartami technicznymi produktów WAKOL.
    
    ---
    **Z poważaniem,** **Loba-Wakol Polska Sp. z o.o.** **{autor}**
    """)
