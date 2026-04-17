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
flooring_options = [
    "deska warstwowa (drewno, laminat itp.)", 
    "deska lita", "wykładzina dywanowa", 
    "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"
]
flooring_type = st.selectbox("1. Rodzaj okładziny", flooring_options)

# 2. Rodzaj podłoża
substrate = st.selectbox("2. Rodzaj podłoża", [
    "jastrych cementowy", "jastrych anhydrytowy", 
    "płyta fundamentowa", "podłoże drewniane (parkiet, deska, OSB)", 
    "płytki ceramiczne", "masa samorozlewna"
])

# Grubość istniejącej masy
existing_levelling_thickness = None
if substrate == "masa samorozlewna":
    existing_levelling_thickness = st.number_input("Grubość wylanej masy (mm):", min_value=1, value=3)

# Wiek podłoża (w miesiącach)
substrate_age_val = None
if any(x in substrate for x in ["jastrych", "płyta", "masa"]):
    substrate_age_val = st.number_input("Wiek podłoża (podaj ilość miesięcy):", min_value=0.5, step=0.5, format="%.1f")

# 3. Ogrzewanie podłogowe
st.write("3. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")

heating_info = ""
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne"])
    mapping = {
        "wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna", 
        "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana", 
        "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie", 
        "elektryczne": "instalacja ogrzewania podłogowego elektryczna"
    }
    heating_info = mapping.get(h_type, h_type)

# 4. Wyrównanie
st.write("4. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
leveling_thickness = 0
if needs_levelling == "TAK":
    leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=3)

# 5. Dylatacje obwodowe
st.write("5. Czy dylatacje obwodowe zachowane prawidłowo?")
dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=0, horizontal=True, label_visibility="collapsed")

# 6. Dylatacje pozorne klawiszujące
st.write("6. Czy występują klawiszujące dylatacje pozorne?")
cracks_klaw = st.radio("Klawiszowanie pozorne:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
klaw_meters = 0.0
if cracks_klaw == "TAK":
    klaw_meters = st.number_input("Ilość mb dylatacji pozornych klawiszujących:", min_value=0.1, step=0.1)

# 7. Pęknięcia wymagające zespolenia
st.write("7. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia do zespolenia:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
pek_meters = 0.0
if cracks_pek == "TAK":
    pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", min_value=0.1, step=0.1)

# 8. Ubytki (cm)
st.write("8. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True, label_visibility="collapsed")
hole_details = ""
if holes == "TAK":
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1: h_depth = st.number_input("Głębokość (cm)", min_value=0.1, format="%.1f")
    with col_h2: h_width = st.number_input("Szerokość (cm)", min_value=0.1, format="%.1f")
    with col_h3: h_length = st.number_input("Długość (cm)", min_value=0.1, format="%.1f")
    hole_details = f" o wymiarach ok. {h_length}x{h_width} cm i głębokości {h_depth} cm"

# 9. Wentylacja
st.write("9. Rodzaj wentylacji w pomieszczeniu")
ventilation_type = st.radio("Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True, label_visibility="collapsed")

# 10, 11. Warunki otoczenia
col_w1, col_w2 = st.columns(2)
with col_w1:
    temp_air = st.number_input("10. Temperatura powietrza (°C)", value=20.0, step=0.5)
with col_w2:
    hum_air = st.number_input("11. Wilgotność powietrza (%)", value=50.0, step=1.0)

# 12. Wilgotność podłoża
moisture = st.number_input("12. Poziom wilgoci podłoża (CM %)", value=None, placeholder="Wpisz wynik...", format="%.1f")

# 13. Dodatkowe uwagi
st.write("13. Dodatkowe uwagi")
extra_notes = st.text_area("Wpisz spostrzeżenia z oględzin:")

# --- LOGIKA NORM ---
if substrate == "jastrych cementowy":
    limit = 1.5 if heating_exists == "TAK" else 1.8
elif substrate == "jastrych anhydrytowy":
    limit = 0.3 if heating_exists == "TAK" else 0.5
else:
    limit = 1.5

barrier_max = 2.5 if heating_exists == "TAK" else 3.5

decision_after_cure = None
if moisture is not None and moisture > limit:
    st.warning("💡 Wilgotność ponadnormatywna.")
    opt_dry = "Dalsze osuszanie" if heating_exists == "NIE" else "Kolejny proces wygrzewania"
    if moisture <= barrier_max:
        decision_after_cure = st.radio("Postępowanie:", [opt_dry, "Wykonanie bariery przeciwwilgociowej"], horizontal=True)
    else:
        st.error(f"❌ Wilgotność za wysoka na barierę (max {barrier_max}%).")
        decision_after_cure = opt_dry

# --- TESTY MECHANICZNE ---
st.write("### Testy mechaniczne i Wytrzymałość")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: test_hammer = st.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t2: test_ripper = st.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t3: test_brush = st.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)

strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości podłoża:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# --- SEKCJA GENEROWANIA PROTOKOŁU ---
st.divider()
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None:
        st.error("Proszę podać wilgotność podłoża!")
    else:
        st.divider()
        m_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY"

        st.markdown("### **Loba-Wakol Polska Sp. z o.o.**")
        st.write(f"**Data badania:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")
        st.write(f"**Szanowni Państwo:** {klient}")

        st.markdown("#### **I. Oględziny i badania**")
        
        actual_obw_ok = dilatations_obw_ok
        if cracks_klaw == "TAK": actual_obw_ok = "NIE"
        obw_status = "Dylatacje obwodowe zachowane prawidłowo." if actual_obw_ok == "TAK" else "Dylatacje obwodowe niezachowane prawidłowo."

        klaw_desc = f" Stwierdzono klawiszujące dylatacje pozorne ({klaw_meters} mb)." if cracks_klaw == "TAK" else " Brak klawiszujących dylatacji."
        pek_desc = f" Stwierdzono pęknięcia podłoża wymagające zespolenia ({pek_meters} mb)." if cracks_pek == "TAK" else " Brak pęknięć wymagających zespolenia."
        
        heat_status_txt = f" {heating_info}." if heating_exists == "TAK" else " Brak instalacji ogrzewania podłogowego."
        
        age_txt = ""
        if substrate_age_val:
            suffix = "miesiąca" if substrate_age_val == 1 or substrate_age_val == 0.5 else "miesiące"
            age_txt = f" Podłoże wykonane {substrate_age_val} {suffix} temu."

        thickness_txt = f" (grubość wylanej warstwy: {existing_levelling_thickness} mm)" if existing_levelling_thickness else ""

        st.write(f"**a) oględziny optyczne:** Podłoże stanowi {substrate}{thickness_txt}.{age_txt}{heat_status_txt} {obw_status}{klaw_desc}{pek_desc} Wentylacja: **{ventilation_type}**.")
        
        if extra_notes:
            st.write(f"**Uwagi dodatkowe:** {extra_notes}")

        st.write(f"**b) badanie wytrzymałości:**")
        st.write(f"* próba młotkiem: **{test_hammer}**")
        st.write(f"* próba szczotką drucianą: **{test_brush}**")
        st.write(f"* próba rysikiem: **{test_ripper}**")
        st.write(f"* Ocena ogólna wytrzymałości: **{strength_labels[strength_val]}**")

        st.write(f"**c) badanie wilgotności podłoża:** Wynik **{moisture} % CM** (Norma: {limit} % CM) - Status: **{m_status}**")
        st.write(f"**d) warunki klimatyczne:** Temp. powietrza: **{temp_air}°C** | Wilgotność powietrza: **{hum_air}% RH**.")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**a) przygotowanie podłoża:**")
        st.write("* Szlifowanie podłoża w celu usunięcia mleczka jastrychowego i otwarcia porów.")
        st.write("* Dokładne odkurzenie powierzchni.")
        
        if decision_after_cure in ["Dalsze osuszanie", "Kolejny proces wygrzewania"]:
            st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci ({limit}% CM) poprzez kontynuowanie procesu {decision_after_cure.lower()}.**")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        total_cracks = klaw_meters + pek_meters
        if total_cracks > 0:
            st.write(f"* Wszystkie pęknięcia oraz dylatacje klawiszujące (łącznie ok. {total_cracks} mb) należy zespolić siłowo przy użyciu żywicy lanej **WAKOL PS 205**.")
        
        if holes == "TAK":
            st.write(f"* Ubytki i zdegradowane fragmenty{hole_details} uzupełnić zaprawą szybkosprawną **WAKOL Z 610**.")
            
        # LOGIKA GRUNTOWANIA PU
        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            if strength_val == 2:
                # PU 235 BARIERA (2 WARSTWY) - WEDŁUG NAJNOWSZEGO WZORU
                st.write("* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez dwukrotne zagruntowanie gruntówką wzmacniającą WAKOL PU 235. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki.**")
                st.write("  - 1 - warstwa nałożona wałkiem ok. 150 g/m². Czas schnięcia – 3-6 godzin.")
                st.write("  - 2 warstwa zużycie ok. 100 g/m². Czas schnięcia – 3-6 godzin.")
                st.write("  - Czas klejenia 72 godziny od zagruntowania.")
            else:
                # PU 280 BARIERA (2 WARSTWY)
                st.write("* **Z uwagi na podwyższoną wilgotność zalecamy stworzenie bariery przeciwwilgociowej poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki.**")
                st.write("  - 1 warstwa nałożona wałkiem ok. 100-150 g/m². Czas schnięcia – jedna godzina.")
                st.write("  - 2 warstwa ok. 100 g/m² - czas schnięcia – jedna godzina.")
                st.write("  - *W zależności od chłonności podłoża zużycie gruntówki może być większe bądź mniejsze, większa ilość nałożonego materiału wydłuża czas schnięcia.*")
                st.write("  - Czas do klejenia: 72 godziny od zagruntowania.")
            st.markdown("  *Należy zaślepić dylatacje pozorne przed aplikacją.*")
        else:
            # GRUNTOWANIE WZMOCNIAJĄCE (1 WARSTWA)
            if strength_val >= 4:
                st.write("* Zalecamy zagruntowanie całej powierzchni jastrychu gruntówką dyspersyjną **WAKOL D 3055** - aplikacja wałkiem ok. 150 g/m2. Czas schnięcia ok 30 min.")
            elif strength_val == 3:
                st.write("* Zalecamy zagruntowanie całej powierzchni podłoża gruntówką wzmacniającą **WAKOL PU 280**. Aplikować wałkiem. Nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia 1 godzina. W zależności od chłonności podłoża zużycie może być większe bądź mniejsze. Czas do montażu – 72 godziny.")
            elif strength_val == 2:
                st.write("* Zalecamy jednokrotną aplikację gruntówki **WAKOL PU 235**. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki. 1 - warstwa nałożona wałkiem ok.150 g/m². Czas schnięcia 3 – 6 godzin. Czas klejenia 72 godziny od zagruntowania.")
            else:
                st.write("* Wzmocnienie głębokie żywicą: **WAKOL PS 275**.")

        if needs_levelling == "TAK":
            st.write(f"* Wyrównanie: montaż maty wzmacniającej **WAKOL AR 150** oraz wylanie masy samopoziomującej **WAKOL Z 645/635** o grubości **{leveling_thickness} mm**.")

        st.write(f"**c) montaż okładziny:**")
        ms_230_desc = "kleju elastycznego **WAKOL MS 230** (szpachla **B13**, zużycie **1350 g/m²**)"
        ms_260_desc = "kleju twardo-elastycznego **WAKOL MS 260** (szpachla **B13**, zużycie **1350 g/m²**)"
        pu_225_desc = "kleju poliuretanowego **WAKOL PU 225** (szpachla **B11**, zużycie **1250 g/m²**)"

        if flooring_type == "deska lita":
            if strength_val <= 2:
                st.write(f"* Klejenie parkietu litego należy przeprowadzić przy użyciu {ms_260_desc}. Klej nadaje się na ogrzewanie podłogowe.")
            else:
                st.write(f"* Klejenie parkietu litego należy przeprowadzić przy użyciu {pu_225_desc}. Klej nadaje się na ogrzewanie podłogowe.")
        
        elif flooring_type == "deska warstwowa (drewno, laminat itp.)":
            st.write(f"* Klejenie parkietu należy przeprowadzić przy użyciu jednego z poniższych klejów (do wyboru):")
            st.write(f"  - Klej elastyczny {ms_230_desc}")
            st.write(f"  - Klej poliuretanowy {pu_225_desc}")
        else:
            st.write(f"* Montaż okładziny **{flooring_type}** należy przeprowadzić zgodnie z systemem WAKOL dedykowanym dla tego typu materiału.")
        
        st.divider()
        st.write(f"Z poważaniem, **{autor}**")
