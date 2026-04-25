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
                <b>Loba-Wakol Polska Sp. z o.o.</b><br>ul. Sławęcińska 16, Macierzysz | 05-850 Ożarów Mazowiecki<br>tel.: +48 22 436 24 20 | biuro@loba-wakol.pl
            </div>
        </div>
        <div style="flex: 1; text-align: right;">
            <div style="font-size: 18px; font-weight: bold; color: #000; margin-bottom: 5px;">PROTOKÓŁ TECHNICZNY</div>
            <div style="font-size: 14px; color: #333;">Anspruch verbindet</div>
        </div>
    </div><br>
    """, unsafe_allow_html=True)

# --- DANE IDENTYFIKACYJNE ---
st.title("📄 Generator Protokołu Oględzin")
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

# --- I. WYWIAD TECHNICZNY ---
flooring_type = st.selectbox("1. Rodzaj okładziny", ["deska warstwowa (drewno, laminat itp.)", "deska lita", "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"])
substrate = st.selectbox("2. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane (parkiet, deska, OSB)", "płytki ceramiczne", "masa samorozlewna"])
substrate_age_val = st.number_input("Wiek podłoża (podaj ilość miesięcy):", min_value=0.5, step=0.5, format="%.1f", value=None)

st.write("3. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True)
heating_info = ""; heating_curing_done = None
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne (powierzchniowe)", "elektryczne (głębokie)", "płyta fundamentowa grzewcza"])
    st.write("❓ Czy został przeprowadzony proces wygrzewania zgodnie z protokołem?")
    heating_curing_done = st.radio("Proces wygrzewania:", ["TAK", "NIE"], index=1, horizontal=True)
    mapping = {"wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna", "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana", "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie", "elektryczne (powierzchniowe)": "instalacja ogrzewania podłogowego elektryczna, powierzchniowa", "elektryczne (głębokie)": "instalacja ogrzewania podłogowego elektryczna, umieszczona głęboko w podłożu", "płyta fundamentowa grzewcza": "ogrzewanie realizowane poprzez płytę fundamentową grzewczą"}
    heating_info = mapping.get(h_type, h_type)

# REGUŁA: lvt cienkie = automatycznie masa 3 mm
if flooring_type == "lvt cienkie":
    st.info("Dla okładziny 'lvt cienkie' automatycznie przyjęto konieczność wyrównania podłoża masą o grubości 3 mm.")
    needs_levelling = "TAK"
    leveling_thickness = 3
else:
    st.write("4. Czy podłoże wymaga wyrównania (masy)?")
    needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True)
    leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=None) if needs_levelling == "TAK" else 0

# Sekcja wywiadu (stałe pytania WAKOL)
st.write("5. Czy dylatacje obwodowe zachowane prawidłowo?")
dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=0, horizontal=True)
st.write("6. Czy występują klawiszujące dylatacje pozorne?")
cracks_klaw = st.radio("Klawiszowanie pozorne:", ["TAK", "NIE"], index=1, horizontal=True)
st.write("7. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia do zespolenia:", ["TAK", "NIE"], index=1, horizontal=True)
st.write("8. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True)

moisture = st.number_input("12. Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)

# --- LOGIKA NORM ---
limit = 1.5 if substrate == "jastrych cementowy" and heating_exists == "TAK" else 1.8 if substrate == "jastrych cementowy" else 0.3 if substrate == "jastrych anhydrytowy" and heating_exists == "TAK" else 0.5 if substrate == "jastrych anhydrytowy" else 1.5
barrier_max = 2.5 if heating_exists == "TAK" else 3.5

decision_after_cure = None
needs_drying_action = False
if moisture is not None and moisture > limit:
    needs_drying_action = True
    opt_dry = "przeprowadzenie procesu wygrzewania" if heating_exists == "TAK" else "dalsze osuszanie"
    if substrate == "jastrych anhydrytowy" or (heating_exists == "TAK" and heating_curing_done == "NIE"):
        decision_after_cure = opt_dry
    else:
        if moisture <= barrier_max:
            decision_after_cure = st.radio("Postępowanie:", ["Wykonanie bariery przeciwwilgociowej", opt_dry], horizontal=True)
            needs_drying_action = (decision_after_cure != "Wykonanie bariery przeciwwilgociowej")
        else:
            decision_after_cure = opt_dry

# --- STAŁE TECHNOLOGICZNE ---
FULL_D3004 = "* **Zagruntować podłoże koncentratem gruntówki dyspersyjnej WAKOL D 3004. Proporcje mieszania: 1 część WAKOL D 3004 + 2 części wody; Czas schnięcia: na jastrychach cementowych i betonie po optycznym wyschnięciu ok. 30min. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: ok. 50 g/m² koncentratu.**"
FULL_Z675 = "* **Wylać masę wyrównawczą WAKOL Z 675 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,0 – 6,5 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2-3 godzinach. Możliwość klejenia podłóg po ok. 24 godzinach przy grubości warstwy do 3 mm, przy większych grubościach czas schnięcia ulega wydłużeniu.**"

# --- GENEROWANIE ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN", type="primary", use_container_width=True):
    if moisture is None: st.error("Proszę podać wilgotność podłoża!")
    else:
        st.divider(); insert_header()
        
        moisture_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY"
        norm_val_bracket = f"({limit}% CM)"
        curing_not_done = (heating_exists == "TAK" and heating_curing_done == "NIE")
        
        st.markdown("#### **I. Oględziny i badania**")
        st.write(f"Badanie wilgotności CM: **{moisture} % CM** (Norma: {limit} % CM) — **Wynik: {moisture_status}**")

        st.markdown("#### **II. Zalecenia techniczne**")
        
        st.write("**a) przygotowanie podłoża:**")
        st.write("* **Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni!**")
        st.write("* **Dokładne odkurzenie powierzchni odkurzaczem przemysłowym.**")
        
        if curing_not_done:
            msg = f"w celu uzyskania normatywnego poziomu wilgoci {norm_val_bracket}." if moisture_status == "NEGATYWNY" else "zgodnie z protokołem."
            st.write(f"* **Konieczność przeprowadzenia pełnego procesu wygrzewania podłoża {msg}**")
        elif moisture_status == "NEGATYWNY":
            st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci {norm_val_bracket} poprzez {decision_after_cure}.**")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        if curing_not_done:
            poczatek = f"Po doprowadzeniu do normatywnego poziomu wilgoci {norm_val_bracket} jastrychu poprzez przeprowadzenie procesu wygrzewania" if moisture_status == "NEGATYWNY" else "Po przeprowadzeniu pełnego procesu wygrzewania"
            st.write(f"**{poczatek} zalecamy:**")
        elif needs_drying_action:
            st.write(f"**Po doprowadzeniu do normatywnego poziomu wilgoci {norm_val_bracket} zalecamy:**")
        
        # REGUŁA: lvt cienkie = BRAK GRUNTÓWKI przed masą
        if flooring_type == "lvt cienkie":
            st.write("* **Z uwagi na rodzaj okładziny (lvt cienkie), po przygotowaniu podłoża należy przejść bezpośrednio do wylewania masy wyrównawczej bez gruntowania powierzchni.**")
            st.write(FULL_Z675)
        else:
            st.write(FULL_D3004)
            if needs_levelling == "TAK": st.write(FULL_Z675)

        st.write("**c) klejenie okładziny:**")
        if flooring_type == "lvt cienkie":
            st.write("Klejenie podłogi winylowej należy przeprowadzić przy użyciu kleju WAKOL D 3318 (szpachla TKB A2, zużycie: 350 g/m²). · Czas wstępnego odparowania: ok. 5 - 10 minut. · Czas układania: ok. 10 minut")
        else:
            st.write("Klejenie okładziny należy przeprowadzić zgodnie z systemem WAKOL dla wybranego rodzaju podłogi.")

        st.divider(); st.markdown(f"<b>Z poważaniem, Loba-Wakol Polska Sp. z o.o. | {autor}</b>", unsafe_allow_html=True)
