import streamlit as st
from datetime import date

# 1. KONFIGURACJA STRONY
st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="wide")

# --- NAGŁÓWEK FIRMOWY ---
def insert_header():
    logo_wakol = "https://www.wakol.com/fileadmin/templates/images/wakol_logo.png"
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;">
        <div style="flex: 1;"><img src="{logo_wakol}" width="220">
            <div style="margin-top: 15px; font-size: 11px; color: #555; line-height: 1.4;">
                <b>Loba-Wakol Polska Sp. z o.o.</b><br>ul. Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki<br>
                tel.: +48 22 436 24 20 | fax: +48 22 436 24 21<br>KRS: 0000163623 | NIP: 118-13-89-053 | biuro@loba-wakol.pl
            </div>
        </div>
        <div style="flex: 1; text-align: right;">
            <div style="font-size: 18px; font-weight: bold; color: #000; margin-bottom: 5px;">PROTOKÓŁ TECHNICZNY</div>
            <div style="font-size: 14px; color: #333;">Anspruch verbindet</div>
        </div>
    </div><br>
    """, unsafe_allow_html=True)

st.title("📄 Generator Protokołu Oględzin")

# --- DANE ---
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

# --- WYWIAD ---
flooring_type = st.selectbox("1. Rodzaj okładziny", ["deska warstwowa (drewno, laminat itp.)", "deska lita", "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"])
substrate = st.selectbox("2. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane", "płytki ceramiczne", "masa samorozlewna"])
substrate_age_val = st.number_input("Wiek podłoża (miesiące):", min_value=0.5, step=0.5, format="%.1f", value=None)

heating_exists = st.radio("3. Czy jest instalacja ogrzewania podłogowego?", ["TAK", "NIE"], index=1, horizontal=True)
heating_info = ""; heating_curing_done = None
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne (powierzchniowe)", "elektryczne (głębokie)", "płyta fundamentowa grzewcza"])
    heating_curing_done = st.radio("Czy przeprowadzono wygrzewanie?", ["TAK", "NIE"], index=1, horizontal=True)
    mapping = {"wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna", "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana", "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie", "elektryczne (powierzchniowe)": "instalacja ogrzewania podłogowego elektryczna, powierzchniowa", "elektryczne (głębokie)": "instalacja ogrzewania podłogowego elektryczna, umieszczona głęboko w podłożu", "płyta fundamentowa grzewcza": "ogrzewanie realizowane poprzez płytę fundamentową grzewczą"}
    heating_info = mapping.get(h_type, h_type)

needs_levelling = st.radio("4. Czy podłoże wymaga wyrównania (masy)?", ["TAK", "NIE"], index=1, horizontal=True)
leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=None) if needs_levelling == "TAK" else 0

dilatations_obw_ok = st.radio("5. Czy dylatacje obwodowe zachowane prawidłowo?", ["TAK", "NIE"], index=0, horizontal=True)
cracks_klaw = st.radio("6. Czy występują klawiszujące dylatacje pozorne?", ["TAK", "NIE"], index=1, horizontal=True)
klaw_meters = st.number_input("Ilość mb klawiszujących:", min_value=0.1, step=0.1, value=None) if cracks_klaw == "TAK" else 0.0
cracks_pek = st.radio("7. Czy występują pęknięcia podłoża?", ["TAK", "NIE"], index=1, horizontal=True)
pek_meters = st.number_input("Ilość mb pęknięć:", min_value=0.1, step=0.1, value=None) if cracks_pek == "TAK" else 0.0

holes = st.radio("8. Czy są ubytki?", ["TAK", "NIE"], index=1, horizontal=True)
hole_details = st.text_input("Wymiary ubytków (opcjonalnie):") if holes == "TAK" else ""

ventilation_type = st.radio("9. Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True)
moisture = st.number_input("12. Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)

# --- WYTRZYMAŁOŚĆ ---
presso_results = []
for i in range(6): presso_results.append(st.number_input(f"Próba {i+1} (N/mm²)", min_value=0.0, step=0.1, value=None))
strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# --- LOGIKA DECYZJI ---
limit = 1.5 if (substrate == "jastrych cementowy" and heating_exists == "TAK") else 1.8 if substrate == "jastrych cementowy" else 0.3 if (substrate == "jastrych anhydrytowy" and heating_exists == "TAK") else 0.5
barrier_max = 2.5 if heating_exists == "TAK" else 3.5

decision_after_cure = None
if moisture is not None and moisture > limit:
    if heating_exists == "TAK": opt_dry = "konieczność wykonania kolejnego procesu wygrzewania" if heating_curing_done == "TAK" else "konieczność przeprowadzenia procesu wygrzewania"
    else: opt_dry = "dalsze osuszanie"
    
    if strength_val == 1 or moisture > barrier_max: decision_after_cure = opt_dry
    else: decision_after_cure = st.radio("Postępowanie:", ["konieczność wykonania bariery przeciwwilgociowej", opt_dry], horizontal=True)

# --- STAŁE TEKSTOWE ---
# 1. PU 280 jako bariera (TYLKO dla wilgotnego podłoża)
DESC_PU280_BARRIER = "* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. 1 warstwa nałożona wałkiem ok. 100-150 g/m². Czas schnięcia – jedna godzina. 2 warstwa ok. 100 g/m² - czas schnięcia – jedna godzina. Czas do klejenia: 72 godziny od zagruntowania.**"

# 2. PU 280 jako wzmocnienie (Dla podłoża suchego/osuszonego)
DESC_PU280_REINFORCE = "* **Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia – jedna godzina.**"

DESC_D3045 = "* **Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu WAKOL D 3045. Produkt należy dokładnie wymieszać przed użyciem. Aplikować równomiernie za pomocą wałka. Zużycie wynosi ok. 150 g/m². Należy zachować czas schnięcia wynoszący minimum 1 godzinę przed przystąpieniem do dalszych prac.**"

# --- GENERATOR ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None: st.error("Podaj wilgotność!")
    else:
        st.divider(); insert_header()
        st.write(f"**Data:** {data_badania.strftime('%d.%m.%Y')} | **Inwestycja:** {inwestycja}, {adres}")
        st.markdown("#### **I. Oględziny i badania**")
        obw_txt = " Dylatacje obwodowe zachowane prawidłowo." if dilatations_obw_ok == "TAK" else " Dylatacje obwodowe niezachowane prawidłowo."
        klaw_txt = f" Stwierdzono klawiszujące dylatacje pozorne ({klaw_meters} mb)." if cracks_klaw == "TAK" else " Dylatacje pozorne nie klawiszują."
        st.write(f"**a) oględziny optyczne:** Podłoże: {substrate}. {obw_txt} {klaw_txt} Wentylacja: {ventilation_type}.")
        st.write(f"**c) badanie wilgotności:** Wynik **{moisture} % CM** (Norma: {limit} % CM)")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**a) przygotowanie podłoża:**\n* **Szlif i odkurzenie.**")
        
        if decision_after_cure and ("wygrzewania" in decision_after_cure or "osuszanie" in decision_after_cure):
            st.write(f"* **Stwierdzono {decision_after_cure} celem doprowadzenia jastrychu do normy tj. {limit}% CM.**")

        st.write("**b) naprawa, gruntowanie i wyrównanie:**")
        after_dry = f"**Po doprowadzeniu do normatywnego poziomu wilgoci jastrychu tj. {limit}% CM zalecamy:**" if decision_after_cure and ("wygrzewania" in decision_after_cure or "osuszanie" in decision_after_cure) else ""
        if after_dry: st.write(f"* {after_dry}")

        # LOGIKA GRUNTOWANIA
        if decision_after_cure == "konieczność wykonania bariery przeciwwilgociowej":
            st.write(DESC_PU280_BARRIER)
            if needs_levelling == "TAK": st.write(DESC_D3045)
        else:
            # Podłoże już suche / po osuszeniu
            if strength_val == 1:
                st.write("* Zalecamy **Wakol PS 275** (2x350g/m2, 7 dni schnięcia, szlif).")
                if needs_levelling == "TAK": 
                    st.write(DESC_PU280_REINFORCE)
                    st.write(DESC_D3045)
            elif strength_val == 2:
                st.write(DESC_PU280_REINFORCE)
                if needs_levelling == "TAK": st.write(DESC_D3045)
            elif strength_val >= 3 and needs_levelling == "TAK":
                st.write("* **Zagruntować WAKOL D 3040 (1:2 z wodą, 50g/m2, 30 min).**")

        # MASAL
        if needs_levelling == "TAK":
            if "lita" in flooring_type: st.write("* **Masa WAKOL Z 625 (proporcja 6,0-6,25l wody, zużycie 1,5kg/m2/mm).**")
            elif "warstwowa" in flooring_type: st.write("* **Masa WAKOL Z 635 (proporcja 6,25l wody, zużycie 1,5kg/m2/mm).**")
            else: st.write("* **Masa WAKOL Z 675 (proporcja 6,0l wody, zużycie 1,5kg/m2/mm).**")

        st.divider()
        st.markdown("<b>Z poważaniem, Loba-Wakol Polska Sp. z o.o. Przemysław Tyszko</b>", unsafe_allow_html=True)
