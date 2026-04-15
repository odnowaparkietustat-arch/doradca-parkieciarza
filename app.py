import streamlit as st
from datetime import date

st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="centered")

# --- DANE IDENTYFIKACYJNE (Zgodnie z tabelą wzorcową) ---
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

# --- DYNAMICZNY WYWIAD TECHNICZNY ---
substrate = st.selectbox("1. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "podłoże drewniane", "płytki ceramiczne"])

st.write("2. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True)
heating_type = ""
if heating_exists == "TAK":
    heating_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne"])

needs_levelling = st.radio("3. Czy podłoże wymaga wyrównania (masy)?", ["TAK", "NIE"], index=1, horizontal=True)

cracks = st.radio("4. Czy są spękania i ruchome dylatacje?", ["TAK", "NIE"], index=1, horizontal=True)
cracks_meters = 0
if cracks == "TAK":
    cracks_meters = st.number_input("Ilość metrów bieżących (mb)", 0.0, step=0.5)

holes = st.radio("5. Czy są ubytki w jastrychu?", ["TAK", "NIE"], index=1, horizontal=True)
h_dim = {"l":0.0, "w":0.0, "d":0.0}
if holes == "TAK":
    c1, c2, c3 = st.columns(3)
    h_dim["l"] = c1.number_input("Długość (cm)", 0.0)
    h_dim["w"] = c2.number_input("Szerokość (cm)", 0.0)
    h_dim["d"] = c3.number_input("Głębokość (cm)", 0.0)

moisture = st.number_input("6. Poziom wilgoci jastrychu (CM %)", 0.0, format="%.1f")

st.write("7. Wytrzymałość jastrychu")
strength_labels = {1:"Bardzo słaby", 2:"Słaby", 3:"Umiarkowanie słaby", 4:"Umiarkowanie mocny", 5:"Mocny"}
strength_val = st.select_slider("Skala:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

ventilation = st.radio("8. Rodzaj wentylacji:", ["Grawitacyjna", "Mechaniczna (Rekuperacja)"], horizontal=True)
temp = st.number_input("9. Temperatura powietrza (°C)", 20)
humidity = st.number_input("9. Wilgotność powietrza (%)", 50)

# --- PRZYCISK GENEROWANIA ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN"):
    st.divider()
    
    # Logika statusów [cite: 33, 34, 95, 96]
    limit = 1.5 if heating_exists == "TAK" else 1.8
    m_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY (Wymagana bariera)"
    s_status = "Pozytywna" if strength_val >= 4 else "Dostateczna" if strength_val == 3 else "Negatywna"

    # --- WZORZEC PROTOKOŁU (Zgodnie z plikiem PDF/DOCX) ---
    st.markdown(f"""
    ### **Loba-Wakol Polska Sp. z o.o.**
    Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki  
    **Data:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor} | **Strona:** 1 z 1
    
    **Dotyczy:** Protokół z oględzin inwestycji w budynku przy {adres} w miejscowości {miejscowosc}.
    
    **Szanowni Państwo,**
    
    W dniu {data_badania.strftime('%d.%m.%Y')}r. w budynku przy {adres} w miejscowości {miejscowosc} dokonano wstępnych oględzin i pomiarów wytrzymałości podłoża ({substrate}) oraz pomiaru wilgotności podłoża przed przyklejeniem okładziny warstwowej.
    
    #### **I. Oględziny i badania**
    **a) oględziny optyczne** [cite: 7, 78]
    Podłoże stanowi {substrate}. {"Brak instalacji ogrzewania podłogowego." if heating_exists == "NIE" else "Stwierdzono instalację ogrzewania podłogowego ("+heating_type+")."} [cite: 8, 79]
    {"Jastrych posiada spękania/klawiszowanie w ilości " + str(cracks_meters) + " mb." if cracks == "TAK" else "Jastrych bez widocznych spękań."} [cite: 8, 79]
    {"Konieczne jest wyrównanie za pomocą masy samorozlewnej." if needs_levelling == "TAK" else ""} [cite: 9, 80]
    
    **b) badanie wytrzymałości** [cite: 11, 82]
    * próba młotkiem – {s_status} [cite: 12, 83]
    * próba szczotką drucianą – {s_status} [cite: 13, 84]
    * próba rysikiem – {s_status} 
    * Ocena ogólna: **{strength_labels[strength_val]}**
    
    **c) test chłonności podłoża** – po przeszlifowaniu chłonne[cite: 14, 86].
    
    **d) badanie wilgotności podłoża:** [cite: 28, 90]
    Zmierzono metodą opartą na stałej dielektrycznej za pomocą urządzenia Gann Compact B[cite: 29, 91], która dała wynik:
    **{moisture} % CM – {m_status}**[cite: 30, 92].
    
    **e) wilgotność i temperatura powietrza:** [cite: 31, 93]
    **{humidity}% / {temp}°C** [cite: 32, 94]
    
    *Aby bezpiecznie kleić podłogę drewnianą na jastrychu cementowym, jego wytrzymałość na ścinanie musi wynosić między 1,5 a 2,0 N/mm² a wilgotność nie może przekraczać 1,8% CM (z ogrzewaniem podłogowym max. 1,5% CM)*[cite: 33, 34, 95, 96].
    
    #### **II. Zalecenia techniczne** [cite: 35, 97]
    Biorąc pod uwagę w/w wyniki badań oraz klejone elementy, zaleca się: [cite: 36, 98]
    
    **a) przygotowanie podłoża:** [cite: 37, 99]
    * Szlif podłoża w celu usunięcia wierzchniej warstwy i uzyskania porowatej i chłonnej powierzchni[cite: 38, 100].
    * Dokładne odkurzenie[cite: 39, 101].
    
    **b) naprawa i wzmocnienie podłoża:** [cite: 40, 102]
    """)

    # Logika produktowa na podstawie wyników [cite: 42, 44, 46, 103, 105, 107]
    if cracks == "TAK":
        st.write(f"* Klawiszujące fragmenty ({cracks_meters} mb) zespolić żywicą laną **WAKOL PS 205**[cite: 42, 103]. Wymieszaną żywicę wlewać w pęknięcia, nadmiar zgarnąć lub zatrzeć[cite: 43, 104].")
    
    if strength_val <= 3:
        st.write("* **Wzmocnienie:** Z uwagi na umiarkowanie słabe podłoże, zastosować wzmocnienie żywicą **WAKOL PU 280** lub matę odcinającą **WAKOL EM 140**.")

    if moisture > limit:
        st.write(f"* **Bariera wilgoci:** Zastosować **WAKOL PU 280** (2 warstwy) z uwagi na przekroczenie normy ({moisture}% CM przy limicie {limit}%)[cite: 46, 107].")
    else:
        st.write("* Podłoże zagruntować koncentratem gruntówki dyspersyjnej **WAKOL D 3004**[cite: 44, 105]. Proporcje: 1:1 z wodą[cite: 44, 105].")

    if needs_levelling == "TAK":
        st.write("* Zastosować system: mata **WAKOL AR 150** + masa **WAKOL Z 645** z plastyfikatorem **WAKOL D 3060**[cite: 46, 107]. Następnie wylać masę **WAKOL Z 635**[cite: 48, 109].")

    st.markdown(f"""
    **c) klejenie desek:** [cite: 61, 116]
    * Klejenie podłogi drewnianej należy przeprowadzić przy użyciu kleju **WAKOL MS 230** (szpachla B11, zużycie: 1250 g/m²)[cite: 62, 117].
    
    ---
    *Prosimy o zapoznanie się z kartami technicznymi zalecanych produktów WAKOL. Podstawą naszego zalecenia jest stosowanie materiałów firmy WAKOL w podanej kolejności, przestrzegając reguł rzemiosła i norm*[cite: 63, 64, 118, 119].
    
    **Z poważaniem,** **Loba-Wakol Polska Sp. z o.o.** **{autor}** Kontakt: 603 214 218 [cite: 65, 120]
    """)
