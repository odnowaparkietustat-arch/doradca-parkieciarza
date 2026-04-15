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

st.write("8. Wytrzymałość jastrychu / płyty")
strength_labels = {1:"Bardzo słaby", 2:"Słaby", 3:"Umiarkowanie słaby", 4:"Umiarkowanie mocny", 5:"Mocny"}
strength_val = st.select_slider("Skala:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

ventilation_type = st.radio("9. Rodzaj wentylacji:", ["Grawitacyjna", "Mechaniczna (Rekuperacja)"], horizontal=True)
temp = st.number_input("10. Temperatura powietrza (°C)", 20)
humidity = st.number_input("10. Wilgotność powietrza (%)", 50)

# --- PRZYCISK GENEROWANIA ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN"):
    st.divider()
    
    # Logika statusów wilgotności (NORMY)
    if substrate == "jastrych anhydrytowy":
        limit = 0.3 if heating_exists == "TAK" else 0.5
    else: # jastrych cementowy lub płyta fundamentowa
        limit = 1.5 if heating_exists == "TAK" else 1.8
        
    m_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY"
    s_status = "pozytywna" if strength_val >= 4 else "dostateczna" if strength_val == 3 else "negatywna"

    # --- WZORZEC PROTOKOŁU ---
    st.markdown(f"""
    ### **Loba-Wakol Polska Sp. z o.o.**
    Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki  
    **Data:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}
    
    **Dotyczy:** Protokół z oględzin inwestycji w budynku przy {adres} w miejscowości {miejscowosc}.
    
    **Szanowni Państwo,**
    
    W dniu {data_badania.strftime('%d.%m.%Y')}r. dokonano wstępnych oględzin i pomiarów podłoża ({substrate}) przed montażem okładziny (**{flooring_type}**).
    
    #### **I. Oględziny i badania**
    **a) oględziny optyczne**
    Podłoże stanowi {substrate}. 
    {f"Stwierdzono instalację ogrzewania podłogowego ({heating_info})." if heating_exists == "TAK" else "Brak instalacji ogrzewania podłogowego."}
    {f"**Proces wygrzewania podłoża:** {heating_cured}." if heating_cured is not None else ""}
    {"Podłoże posiada spękania/klawiszowanie w ilości " + str(cracks_meters) + " mb." if cracks == "TAK" else "Podłoże bez widocznych spękań."}
    {f"Stwierdzono ubytki lub zdegradowane fragmenty o wymiarach ok. {h_dim['l']}x{h_dim['w']}x{h_dim['d']} cm." if holes == "TAK" else ""}
    
    **b) badanie wytrzymałości**
    * próba młotkiem – {s_status} | próba szczotką drucianą – {s_status} | próba rysikiem – {s_status}
    
    **c) ocena ogólna wytrzymałości**
    Podłoże zostało ocenione jako: **{strength_labels[strength_val]}**.
    
    **d) test chłonności podłoża** – po przeszlifowaniu chłonne.
    
    **e) badanie wilgotności podłoża:**
    Wynik pomiaru: **{moisture} % CM – Status: {m_status}**. (Norma dla {substrate}: {limit}% CM).
    
    **f) warunki klimatyczne:** {humidity}% RH / {temp}°C
    
    **Aby bezpiecznie kleić podłogę drewnianą na jastrychu cementowym lub płycie fundamentowej, jego wytrzymałość na ścinanie musi wynosić między 1,5 a 2,0 N/mm² a wilgotność nie może przekraczać 1,8% CM (z ogrzewaniem podłogowym max. 1,5% CM).**
    
    #### **II. Zalecenia techniczne**
    Biorąc pod uwagę wyniki badań, zaleca się:
    
    **a) przygotowanie podłoża:**
    * Szlif podłoża w celu usunięcia mleczka cementowego/anhydrytowego i uzyskania chłonnej powierzchni.
    * Dokładne odkurzenie.
    """)

    # Logika zaleceń dot. wilgotności (TWOJA NOWA WYTYCZNA)
    if moisture > limit:
        st.warning("⚠️ UWAGA: Przekroczona norma wilgotności podłoża.")
        if heating_exists == "TAK":
            st.write("* **Wymagane działanie:** Uzyskanie normatywnego poziomu wilgoci poprzez ponowne przeprowadzenie procesu wygrzewania jastrychu.")
        else:
            st.write(f"* **Wymagane działanie:** Naturalne wysuszenie podłoża poprzez zapewnienie optymalnych warunków temperaturowych i intensywnej wentylacji (obecna wentylacja: {ventilation_type}).")
        
        st.write("* **Rozwiązanie alternatywne:** W przypadku braku efektów osuszania naturalnego/wygrzewania, dopuszcza się wykonanie bariery przeciwwilgociowej przy użyciu żywicy **WAKOL PU 280** (2 warstwy).")
    else:
        st.write("* Podłoże zagruntować koncentratem **WAKOL D 3004** (1:1 z wodą).")

    if cracks == "TAK":
        st.write(f"* Klawiszujące fragmenty ({cracks_meters} mb) zespolić żywicą laną **WAKOL PS 205**.")
    
    if holes == "TAK":
        st.write(f"* Ubytki i zdegradowane fragmenty uzupełnić zaprawą **WAKOL Z 610**.")

    if strength_val <= 3:
        st.write("* **Wzmocnienie:** Z uwagi na słabe podłoże, zastosować żywicę **WAKOL PU 280** lub matę **WAKOL EM 140**.")

    if needs_levelling == "TAK":
        st.write("* Zastosować system wyrównujący: mata **WAKOL AR 150** + masa **WAKOL Z 645** / **WAKOL Z 635**.")

    st.markdown(f"""
    **c) montaż okładziny:**
    * Prace montażowe dla okładziny: **{flooring_type}** należy przeprowadzić zgodnie z kartami technicznymi produktów WAKOL.
    
    ---
    **Z poważaniem,** **Loba-Wakol Polska Sp. z o.o.** **{autor}**
    """)
