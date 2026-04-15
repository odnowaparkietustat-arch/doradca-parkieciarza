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

# 1. Rodzaj okładziny
flooring_type = st.selectbox("1. Rodzaj okładziny", [
    "wykładzina dywanowa", 
    "pcv w rolce", 
    "lvt cienkie", 
    "lvt grube z twardym rdzeniem", 
    "deska warstwowa (drewno, laminat itp.)", 
    "deska lita"
])

# 2. Rodzaj podłoża
substrate = st.selectbox("2. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "podłoże drewniane", "płytki ceramiczne"])

# 3. Ogrzewanie podłogowe
st.write("3. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True)

heating_info = ""
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne"])
    
    if h_type == "elektryczne":
        el_pos = st.radio("Umiejscowienie ogrzewania elektrycznego:", ["wewnątrz jastrychu", "na powierzchni jastrychu"], horizontal=True)
        if el_pos == "na powierzchni jastrychu":
            el_form = st.radio("Forma ogrzewania powierzchniowego:", ["w formie siatki", "w formie maty"], horizontal=True)
            heating_info = f"elektryczne (na powierzchni, {el_form})"
        else:
            heating_info = "elektryczne (wewnątrz jastrychu)"
    else:
        heating_info = h_type

# 4. Wyrównanie
needs_levelling = st.radio("4. Czy podłoże wymaga wyrównania (masy)?", ["TAK", "NIE"], index=1, horizontal=True)

# 5. Spękania
cracks = st.radio("5. Czy są spękania i ruchome dylatacje?", ["TAK", "NIE"], index=1, horizontal=True)
cracks_meters = 0
if cracks == "TAK":
    cracks_meters = st.number_input("Ilość metrów bieżących (mb)", 0.0, step=0.5)

# 6. Ubytki
holes = st.radio("6. Czy są ubytki w jastrychu?", ["TAK", "NIE"], index=1, horizontal=True)
if holes == "TAK":
    c1, c2, c3 = st.columns(3)
    h_l = c1.number_input("Długość (cm)", 0.0)
    h_w = c2.number_input("Szerokość (cm)", 0.0)
    h_d = c3.number_input("Głębokość (cm)", 0.0)

# 7. Wilgotność
moisture = st.number_input("7. Poziom wilgoci jastrychu (CM %)", 0.0, format="%.1f")

# 8. Wytrzymałość
st.write("8. Wytrzymałość jastrychu")
strength_labels = {1:"Bardzo słaby", 2:"Słaby", 3:"Umiarkowanie słaby", 4:"Umiarkowanie mocny", 5:"Mocny"}
strength_val = st.select_slider("Skala:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# 9. Wentylacja
ventilation = st.radio("9. Rodzaj wentylacji:", ["Grawitacyjna", "Mechaniczna (Rekuperacja)"], horizontal=True)

# 10. Warunki
temp = st.number_input("10. Temperatura powietrza (°C)", 20)
humidity = st.number_input("10. Wilgotność powietrza (%)", 50)

# --- PRZYCISK GENEROWANIA ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN"):
    st.divider()
    
    # Logika statusów
    limit = 1.5 if heating_exists == "TAK" else 1.8
    m_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY (Wymagana bariera)"
    s_status = "pozytywna" if strength_val >= 4 else "dostateczna" if strength_val == 3 else "negatywna"

    # --- WZORZEC PROTOKOŁU ---
    st.markdown(f"""
    ### **Loba-Wakol Polska Sp. z o.o.**
    Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki  
    **Data:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}
    
    **Dotyczy:** Protokół z oględzin inwestycji w budynku przy {adres} w miejscowości {miejscowosc}.
    
    **Szanowni Państwo,**
    
    W dniu {data_badania.strftime('%d.%m.%Y')}r. w budynku przy {adres} w miejscowości {miejscowosc} dokonano wstępnych oględzin i pomiarów wytrzymałości podłoża ({substrate}) oraz pomiaru wilgotności podłoża przed przyklejeniem okładziny (**{flooring_type}**).
    
    #### **I. Oględziny i badania**
    **a) oględziny optyczne**
    Podłoże stanowi {substrate}. {"Brak instalacji ogrzewania podłogowego." if heating_exists == "NIE" else "Stwierdzono instalację ogrzewania podłogowego ("+heating_info+")."}
    {"Jastrych posiada spękania/klawiszowanie w ilości " + str(cracks_meters) + " mb." if cracks == "TAK" else "Jastrych bez widocznych spękań."}
    {"Konieczne jest wyrównanie za pomocą masy samorozlewnej." if needs_levelling == "TAK" else ""}
    
    **b) badanie wytrzymałości**
    * próba młotkiem – {s_status}
    * próba szczotką drucianą – {s_status}
    * próba rysikiem – {s_status}
    
    **c) ocena ogólna wytrzymałości**
    Podłoże zostało ocenione jako: **{strength_labels[strength_val]}**.
    
    **d) test chłonności podłoża** – po przeszlifowaniu chłonne.
    
    **e) badanie wilgotności podłoża:**
    Zmierzono metodą opartą na stałej dielektrycznej za pomocą urządzenia Gann Compact B, która dała wynik:
    **{moisture} % CM – {m_status}**.
    
    **f) wilgotność i temperatura powietrza:**
    **{humidity}% / {temp}°C**
    
    **Aby bezpiecznie kleić podłogę drewnianą na jastrychu cementowym, jego wytrzymałość na ścinanie musi wynosić między 1,5 a 2,0 N/mm² a wilgotność nie może przekraczać 1,8% CM (z ogrzewaniem podłogowym max. 1,5% CM).**
    
    #### **II. Zalecenia techniczne**
    Biorąc pod uwagę w/w wyniki badań oraz klejone elementy (**{flooring_type}**), zaleca się:
    
    **a) przygotowanie podłoża:**
    * Szlif podłoża w celu usunięcia wierzchniej warstwy i uzyskania porowatej i chłonnej powierzchni.
    * Dokładne odkurzenie.
    
    **b) naprawa i wzmocnienie podłoża:**
    """)

    if cracks == "TAK":
        st.write(f"* Klawiszujące fragmenty ({cracks_meters} mb) zespolić żywicą laną **WAKOL PS 205**. Wymieszaną żywicę wlewać w pęknięcia, nadmiar zgarnąć lub zatrzeć.")
    
    if strength_val <= 3:
        st.write("* **Wzmocnienie:** Z uwagi na umiarkowanie słabe podłoże, zastosować wzmocnienie żywicą **WAKOL PU 280** lub matę odcinającą **WAKOL EM 140**.")

    if moisture > limit:
        st.write(f"* **Bariera wilgoci:** Zastosować **WAKOL PU 280** (2 warstwy) z uwagi na przekroczenie normy ({moisture}% CM przy limicie {limit}%).")
    else:
        st.write("* Podłoże zagruntować koncentratem gruntówki dyspersyjnej **WAKOL D 3004**. Proporcje: 1:1 z wodą.")

    if needs_levelling == "TAK":
        st.write("* Zastosować system: mata **WAKOL AR 150** + masa **WAKOL Z 645** z plastyfikatorem **WAKOL D 3060**. Następnie wylać masę **WAKOL Z 635**.")

    st.markdown(f"""
    **c) montaż okładziny:**
    * Prace montażowe dla okładziny: **{flooring_type}** należy przeprowadzić zgodnie z zaleceniami producenta materiału i kartami technicznymi produktów WAKOL.
    
    ---
    *Prosimy o zapoznanie się z kartami technicznymi zalecanych produktów WAKOL. Podstawą naszego zalecenia jest stosowanie materiałów firmy WAKOL w podanej kolejności, przestrzegając reguł rzemiosła i norm*.
    
    **Z poważaniem,** **Loba-Wakol Polska Sp. z o.o.** **{autor}**
    """)
