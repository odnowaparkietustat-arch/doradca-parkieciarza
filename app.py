import streamlit as st
from datetime import date

# ==========================================
# 1. KONFIGURACJA STRONY I WSPÓLNE FUNKCJE
# ==========================================
st.set_page_config(page_title="Ekspert Parkieciarski WAKOL", layout="wide")

# --- STAŁE TECHNOLOGICZNE (OPISY PRODUKTÓW) ---
FULL_PS275 = "* **Zalecamy aplikację gruntówki wzmacniającej Wakol PS 275 w dwóch warstwach – grubym wałkiem sznurkowym, zużycie w sumie ok. 700 g/m2. Każda z warstw po 350g/m2, aplikowane po sobie w odstępie jednej godziny. Aplikując gruntówkę Wakol PS 275 należy zwrócić uwagę, aby dobrze wchłaniała się w podłoże i unikać powstawania kałuż na powierzchni jastrychu. Po nałożeniu drugiej warstwy gruntówki w razie potrzeby wykonać posypkę z piasku kwarcowego. Po 7 dniach schnięcia powierzchnię należy przeszlifować papierem o gradacji 24 – 40 usuwając przyklejony do powierzchni piasek kwarcowy i dokładnie odkurzyć.**"
FULL_PU235_1W = "* **Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 235. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia – jedna godzina.**"
FULL_PU235_BARRIER = "* **Zalecamy wykonanie bariery przeciwwilgociowej poprzez dwukrotne zagruntowanie gruntówką wzmacniającą WAKOL PU 235. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki. 1 - warstwa nałożona wałkiem ok. 150 g/m². Czas schnięcia – 3-6 godzin. 2 warstwa zużycie ok. 100 g/m². Czas schnięcia – 3-6 godzin. Czas klejenia 72 godziny od zagruntowania.**"
FULL_PU280_1W = "* **Zalecamy wykonanie gruntowania wzmacniającego poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. Zużycie ok. 150 g/m². Czas schnięcia – jedna godzina.**"
FULL_PU280_BARRIER = "* **Z uwagi na podwyższoną wilgotność zalecamy stworzenie bariery przeciwwilgociowej poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280. Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar nie wchłoniętej gruntówki. 1 warstwa nałożona wałkiem ok. 100-150 g/m². Czas schnięcia – jedna godzina. 2 warstwa ok. 100 g/m² - czas schnięcia – jedna godzina. Czas do klejenia: 72 godziny od zagruntowania.**"
FULL_D3004 = "* **Zagruntować podłoże koncentratem gruntówki dyspersyjnej WAKOL D 3004. Proporcje mieszania: 1 część WAKOL D 3004 + 2 części wody; Czas schnięcia: na jastrychach cementowych i betonie po optycznym wyschnięciu ok. 30min. Sposób nanoszenia: wałek do gruntowania microfazer. Zużycie: ok. 50 g/m² koncentratu.**"
FULL_Z625 = "* **Wylać masę wyrównawczą WAKOL Z 625 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,00 – 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2 godzinach. Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 6 godzinach, przy warstwie do 10 mm – po 12 godzinach, przy warstwie 30 mm – po 24 godzinach.**"
FULL_Z675 = "* **Wylać masę wyrównawczą WAKOL Z 675 - wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,0 – 6,5 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2-3 godzinach. Możliwość klejenia podłóg po ok. 24 godzinach przy grubości warstwy do 3 mm, przy większych grubościach czas schnięcia ulega wydłużeniu.**"
FULL_Z635 = "* **Następnie na podłoże wylać masę wyrównawczą WAKOL Z 635 - Wylewając masę wyrównawczą WAKOL Z 635 wymieszać ją w czystym naczyniu z zimną wodą w proporcji 6,25 litrów wody na 25 kg masy. Mieszać unikając tworzenia się grudek. Prędkość obrotowa mieszadła może wynosić max. 600 obrotów na minutę. Wymieszaną masę nanosić w żądanej grubości na podłoże przy pomocy szpachli, łaty lub rakli. Przed pracą należy zwrócić uwagę na obecność wypełnień fug przy ścianach. Zużycie ok. 1,5 kg/m²/ mm. Możliwość chodzenia po 2,5 godzinach. Możliwość klejenia podłóg drewnianych przy warstwie do 5 mm – po 24 godzinach, przy warstwie do 10 mm – po 72 godzinach.**"
FULL_D3055 = "* **Zalecamy zagruntowanie całej powierzchni jastrychu gruntówką dyspersyjną WAKOL D 3055 - aplikacja wałkiem ok.150 g/m2. Czas schnięcia ok 30 min.**"

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


# ==========================================
# 2. LOGIKA DLA POSZCZEGÓLNYCH OKŁADZIN
# ==========================================

def render_wspolne_dane_optyczne(dane):
    age_txt = f" w wieku {dane['substrate_age_val']} miesięcy" if dane['substrate_age_val'] else ""
    heat_txt = f" Została zainstalowana {dane['heating_info']}." if dane['heating_exists'] == "TAK" else " Brak instalacji ogrzewania podłogowego."
    curing_txt = " Został przeprowadzony proces wygrzewania zgodnie z protokołem." if dane['heating_curing_done'] == "TAK" else " Nie został przeprowadzony proces wygrzewania podłoża." if dane['heating_exists'] == "TAK" else ""
    dil_txt = " Dylatacje obwodowe zostały zachowane prawidłowo." if dane['dilatations_obw_ok'] == "TAK" else " Dylatacje obwodowe nie zostały zachowane prawidłowo."
    klaw_txt = f" Stwierdzono występowanie klawiszujących dylatacji pozornych w ilości {dane['klaw_meters']} metrów bieżących." if dane['cracks_klaw'] == "TAK" else " Nie stwierdzono występowania klawiszujących dylatacji pozornych."
    pek_txt = f" Stwierdzono występowanie pęknięć podłoża wymagających zespolenia w ilości {dane['pek_meters']} metrów bieżących." if dane['cracks_pek'] == "TAK" else " Nie stwierdzono występowania pęknięć podłoża wymagających zespolenia."
    holes_txt = f" Stwierdzono ubytki lub zdegradowane miejsca wymagające wypełnienia{dane['hole_details']}." if dane['holes'] == "TAK" else " Nie stwierdzono ubytków lub zdegradowanych miejsc wymagających wypełnienia."
    level_txt = f" Podłoże wymaga wyrównania masą wyrównawczą o planowanej grubości {dane['leveling_thickness']} milimetrów." if dane['needs_levelling'] == "TAK" else " Podłoże nie wymaga wyrównania masą wyrównawczą."
    vent_txt = f" Rodzaj zastosowanej wentylacji: wentylacja {dane['ventilation_type'].lower()}."
    
    full_opt_report = f"Podłoże pod planowaną okładzinę ({dane['flooring_type']}) stanowi {dane['substrate']}{age_txt}.{heat_txt}{curing_txt}{dil_txt}{klaw_txt}{pek_txt}{holes_txt}{level_txt} {vent_txt}"
    st.write(f"**a) oględziny optyczne:** {full_opt_report}")
    
    presso_valid = [str(p) for p in dane.get('presso_results', []) if p is not None]
    presso_txt = f" Wyniki PressoMess: {', '.join(presso_valid)} N/mm²." if presso_valid else ""
    st.write(f"**b) badanie wytrzymałości:** Wynik młotka: {dane['test_hammer']}, Rysik: {dane['test_ripper']}, Szczotka: {dane['test_brush']}.{presso_txt} Ocena ogólna: **{dane['strength_labels'][dane['strength_val']]}**")
    
    moisture_status = "POZYTYWNY" if dane['moisture'] <= dane['limit'] else "NEGATYWNY"
    st.write(f"**c) badanie wilgotności:** Wynik badania wilgotności metodą CM: **{dane['moisture']} % CM** (Norma: {dane['limit']} % CM) — **Wynik: {moisture_status}**")

    klimat = []
    if dane.get('temp_air') is not None: klimat.append(f"Temperatura powietrza: {dane['temp_air']} °C")
    if dane.get('hum_air') is not None: klimat.append(f"Wilgotność powietrza: {dane['hum_air']} %")
    if klimat:
        st.write(f"**d) warunki klimatyczne:** {', '.join(klimat)}.")

def render_wspolne_zalecenia_podloze(dane):
    st.write("**a) przygotowanie podłoża:**")
    st.write("* **Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni!**")
    st.write("* **Dokładne odkurzenie powierzchni odkurzaczem przemysłowym.**")
    
    if dane['curing_not_done']:
        if dane['is_moisture_neg']:
            st.write(f"* **Konieczność przeprowadzenia pełnego procesu wygrzewania podłoża w celu uzyskania normatywnego poziomu wilgoci {dane['norm_val_bracket']}.**")
        else:
            st.write(f"* **Konieczność przeprowadzenia pełnego procesu wygrzewania podłoża zgodnie z protokołem.**")
    elif dane['is_moisture_neg']:
        if dane['decision_after_cure'] == "Wykonanie bariery przeciwwilgociowej":
            st.write("* **Zalecamy wykonanie bariery przeciwwilgociowej.**")
        else:
            st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci {dane['norm_val_bracket']} poprzez {dane['decision_after_cure']}.**")

    st.write("**b) naprawa i wzmocnienie podłoża:**")
    if dane['curing_not_done']:
        if dane['is_moisture_neg']:
            st.write(f"**Po doprowadzeniu do normatywnego poziomu wilgoci {dane['norm_val_bracket']} jastrychu poprzez przeprowadzenie procesu wygrzewania zalecamy:**")
        else:
            st.write("**Po przeprowadzeniu pełnego procesu wygrzewania zalecamy:**")
    elif dane['needs_drying_action']:
        st.write(f"**Po doprowadzeniu do normatywnego poziomu wilgoci {dane['norm_val_bracket']} zalecamy:**")
    
    if (dane['klaw_meters'] + dane['pek_meters']) > 0: st.write("- Zespolić pęknięcia i dylatacje pozorne żywicą **WAKOL PS 205**.")
    if dane['holes'] == "TAK": st.write(f"- Uzupełnić ubytki zaprawą **WAKOL Z 610**{dane['hole_details']}.")

def render_wspolna_chemia(dane):
    used_d3004 = False
    if dane['decision_after_cure'] == "Wykonanie bariery przeciwwilgociowej":
        if dane['strength_val'] <= 2: st.write(FULL_PU235_BARRIER)
        else: st.write(FULL_PU280_BARRIER)
    elif not dane['decision_after_cure'] or "Wykonanie" not in str(dane['decision_after_cure']):
        if dane['needs_levelling'] == "TAK":
            if dane['strength_val'] in [3, 4, 5]:
                if dane['substrate'] == "jastrych anhydrytowy" and dane['leveling_thickness'] and dane['leveling_thickness'] > 5:
                    st.write(FULL_PU280_1W)
                else:
                    st.write(FULL_D3004)
                    used_d3004 = True
            else:
                if dane['strength_val'] == 1:
                    if dane['substrate'] == "jastrych anhydrytowy": st.write(FULL_PU235_1W)
                    else:
                        st.write(FULL_PS275)
                        st.write(FULL_PU280_1W)
                elif dane['strength_val'] == 2: st.write(FULL_PU280_1W)
        else:
            if dane['strength_val'] == 1:
                if dane['substrate'] == "jastrych anhydrytowy": st.write(FULL_PU235_1W)
                else: st.write(FULL_PS275)
            elif dane['strength_val'] == 2: st.write(FULL_PU235_1W)
            elif dane['strength_val'] in [3, 4]: st.write(FULL_PU280_1W)
    return used_d3004

def render_chemia_deska_warstwowa(dane):
    used_d3004 = False
    if dane['decision_after_cure'] == "Wykonanie bariery przeciwwilgociowej":
        if dane['strength_val'] <= 2: st.write(FULL_PU235_BARRIER)
        else: st.write(FULL_PU280_BARRIER)
    elif not dane['decision_after_cure'] or "Wykonanie" not in str(dane['decision_after_cure']):
        if dane['needs_levelling'] == "TAK":
            if dane['strength_val'] in [3, 4, 5]:
                if dane['substrate'] == "jastrych anhydrytowy" and dane['leveling_thickness'] and dane['leveling_thickness'] > 5:
                    st.write(FULL_PU280_1W)
                else:
                    st.write(FULL_D3004)
                    used_d3004 = True
            elif dane['strength_val'] == 2:
                st.write(FULL_PU280_1W)
            elif dane['strength_val'] == 1:
                if dane['substrate'] == "jastrych anhydrytowy": st.write(FULL_PU235_1W)
                else:
                    st.write(FULL_PS275)
                    st.write(FULL_PU280_1W)
        else:
            if dane['strength_val'] == 1:
                if dane['substrate'] == "jastrych anhydrytowy": st.write(FULL_PU235_1W)
                else: st.write(FULL_PS275)
            elif dane['strength_val'] == 2: st.write(FULL_PU235_1W)
            elif dane['strength_val'] == 3: st.write(FULL_PU280_1W)
            elif dane['strength_val'] in [4, 5]: st.write(FULL_D3055)
    return used_d3004

def render_chemia_deska_lita(dane):
    used_d3004 = False
    if dane['decision_after_cure'] == "Wykonanie bariery przeciwwilgociowej":
        if dane['strength_val'] <= 2: st.write(FULL_PU235_BARRIER)
        else: st.write(FULL_PU280_BARRIER)
    elif not dane['decision_after_cure'] or "Wykonanie" not in str(dane['decision_after_cure']):
        if dane['needs_levelling'] == "TAK":
            if dane['strength_val'] in [3, 4, 5]:
                if dane['substrate'] == "jastrych anhydrytowy" and dane['leveling_thickness'] and dane['leveling_thickness'] > 5:
                    st.write(FULL_PU280_1W)
                else:
                    st.write(FULL_D3004)
                    used_d3004 = True
            else:
                if dane['strength_val'] == 1:
                    if dane['substrate'] == "jastrych anhydrytowy": st.write(FULL_PU235_1W)
                    else:
                        st.write(FULL_PS275)
                        st.write(FULL_PU280_1W)
                elif dane['strength_val'] == 2: st.write(FULL_PU280_1W)
        else:
            if dane['strength_val'] == 1:
                if dane['substrate'] == "jastrych anhydrytowy": st.write(FULL_PU235_1W)
                else: st.write(FULL_PS275)
            elif dane['strength_val'] == 2: st.write(FULL_PU235_1W)
            elif dane['strength_val'] in [3, 4]: st.write(FULL_PU280_1W)
            elif dane['strength_val'] == 5: st.write(FULL_D3055)
    return used_d3004

# --- SEKCJA: DESKA WARSTWOWA ---
def generate_report_deska_warstwowa(dane):
    render_wspolne_dane_optyczne(dane)
    st.markdown("#### **II. Zalecenia techniczne (Deska Warstwowa)**")
    render_wspolne_zalecenia_podloze(dane)
    used_d3004 = render_chemia_deska_warstwowa(dane)

    if dane['needs_levelling'] == "TAK":
        if not used_d3004:
            st.write("* **Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu WAKOL D 3045. Aplikować równomiernie za pomocą wałka. Zużycie wynosi ok. 150 g/m². Czas schnięcia 1 godzina.**")
        st.write(FULL_Z635)

    st.write("**c) klejenie okładziny:**")
    if dane['substrate'] == "jastrych anhydrytowy" and dane['strength_val'] == 1:
        st.write("Klejenie podłogi drewnianej należy przeprowadzić przy użyciu kleju do parkietu **WAKOL MS 230** (szpachla B13, zużycie: 1350 g/m²).")
    else:
        st.write("Klejenie podłogi drewnianej należy przeprowadzić przy użyciu kleju do parkietu **WAKOL MS 230** (szpachla B13, zużycie: 1350 g/m²) bądź kleju do parkietu **WAKOL PU 225** (szpachla B11, zużycie: 1250 g/m²).")

# --- SEKCJA: DESKA LITA ---
def generate_report_deska_lita(dane):
    render_wspolne_dane_optyczne(dane)
    st.markdown("#### **II. Zalecenia techniczne (Deska Lita)**")
    render_wspolne_zalecenia_podloze(dane)
    used_d3004 = render_chemia_deska_lita(dane)

    if dane['needs_levelling'] == "TAK":
        if not used_d3004:
            st.write("* **Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu WAKOL D 3045. Aplikować równomiernie za pomocą wałka. Zużycie wynosi ok. 150 g/m². Czas schnięcia 1 godzina.**")
        st.write(FULL_Z625)

    st.write("**c) klejenie okładziny:**")
    st.write("Klejenie podłogi z deski litej należy przeprowadzić przy użyciu kleju polimerowego twardo-elastycznego WAKOL MS 260. (szpachla B13, zużycie: 1350 g/m²).")

# --- SEKCJA: LVT CIENKIE ---
def generate_report_lvt_cienkie(dane):
    if dane['needs_levelling'] == "NIE" and dane['already_levelled'] == "NIE":
        st.error("BŁĄD: Pod okładzinę LVT cienkie wymagane jest wyrównanie podłoża. Poinformuj klienta o konieczności wylania masy!")
        return
        
    render_wspolne_dane_optyczne(dane)
    st.markdown("#### **II. Zalecenia techniczne (LVT Cienkie)**")
    
    if dane['already_levelled'] == "TAK":
        st.write("**a) klejenie okładziny:**")
        st.write("Klejenie podłogi winylowej (LVT) należy przeprowadzić przy użyciu kleju WAKOL D 3318 (szpachla TKB A2, zużycie: 350 g/m²). · Czas wstępnego odparowania: ok. 5 - 10 minut. · Czas układania: ok. 10 minut")
        return

    render_wspolne_zalecenia_podloze(dane)
    used_d3004 = render_wspolna_chemia(dane)

    if dane['needs_levelling'] == "TAK":
        if not used_d3004:
            st.write("* **Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu WAKOL D 3045. Aplikować równomiernie za pomocą wałka. Zużycie wynosi ok. 150 g/m². Czas schnięcia 1 godzina.**")
        st.write(FULL_Z675)

    st.write("**c) klejenie okładziny:**")
    st.write("Klejenie podłogi winylowej (LVT) należy przeprowadzić przy użyciu kleju WAKOL D 3318 (szpachla TKB A2, zużycie: 350 g/m²). · Czas wstępnego odparowania: ok. 5 - 10 minut. · Czas układania: ok. 10 minut")

# --- SEKCJA: LVT GRUBE ---
def generate_report_lvt_grube(dane):
    render_wspolne_dane_optyczne(dane)
    st.markdown("#### **II. Zalecenia techniczne (LVT Grube z twardym rdzeniem)**")
    render_wspolne_zalecenia_podloze(dane)
    used_d3004 = render_chemia_deska_warstwowa(dane)

    if dane['needs_levelling'] == "TAK":
        if not used_d3004:
            st.write("* **Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu WAKOL D 3045. Aplikować równomiernie za pomocą wałka. Zużycie wynosi ok. 150 g/m². Czas schnięcia 1 godzina.**")
        # Domyślnie używamy tu Z 675 tak jak w cienkim, ale możemy to zmienić
        st.write(FULL_Z675)

    st.write("**c) klejenie okładziny:**")
    st.write("Klejenie podłogi LVT z twardym rdzeniem należy przeprowadzić przy użyciu kleju **WAKOL MS 230** (szpachla B13, zużycie: 1350 g/m²) bądź kleju **WAKOL PU 225** (szpachla B11, zużycie: 1250 g/m²).")

# --- SEKCJA: PCV W ROLCE ---
def generate_report_pcv_w_rolce(dane):
    if dane['needs_levelling'] == "NIE" and dane['already_levelled'] == "NIE":
        st.error("BŁĄD: Pod okładzinę PCV w rolce wymagane jest wyrównanie podłoża. Poinformuj klienta o konieczności wylania masy!")
        return
        
    render_wspolne_dane_optyczne(dane)
    st.markdown("#### **II. Zalecenia techniczne (PCV w rolce)**")
    
    if dane['already_levelled'] == "TAK":
        st.write("**a) klejenie okładziny PCV:**")
        st.write("Klejenie wykładziny PCV w rolce należy przeprowadzić przy użyciu kleju WAKOL D 3307 (szpachla TKB A2, zużycie: 300 – 330 g/m²). · Czas wstępnego odparowania: ok. 10 - 20 minut. · Czas układania: ok. 15 - 20 minut")
        return

    render_wspolne_zalecenia_podloze(dane)
    used_d3004 = render_wspolna_chemia(dane)

    if dane['needs_levelling'] == "TAK":
        if not used_d3004:
            st.write("* **Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu WAKOL D 3045. Aplikować równomiernie za pomocą wałka. Zużycie wynosi ok. 150 g/m². Czas schnięcia 1 godzina.**")
        st.write(FULL_Z675)

    st.write("**c) klejenie okładziny PCV:**")
    st.write("Klejenie wykładziny PCV w rolce należy przeprowadzić przy użyciu kleju WAKOL D 3307 (szpachla TKB A2, zużycie: 300 – 330 g/m²). · Czas wstępnego odparowania: ok. 10 - 20 minut. · Czas układania: ok. 15 - 20 minut")

# --- SEKCJA: WYKŁADZINA DYWANOWA ---
def generate_report_wykladzina_dywanowa(dane):
    if dane['needs_levelling'] == "NIE" and dane['already_levelled'] == "NIE":
        st.error("BŁĄD: Pod wykładzinę dywanową wymagane jest wyrównanie podłoża. Poinformuj klienta o konieczności wylania masy!")
        return
        
    render_wspolne_dane_optyczne(dane)
    st.markdown("#### **II. Zalecenia techniczne (Wykładzina dywanowa)**")
    
    if dane['already_levelled'] == "TAK":
        st.write("**a) klejenie wykładziny tekstylnej:**")
        st.write("Klejenie wykładziny tekstylnej należy przeprowadzić przy użyciu kleju WAKOL D 3308 (szpachla TKB B1 400-450 g/m²). · Czas wstępnego odparowania: ok. 5-10 minut. · Czas otwarty kleju ok. 10-15 minut")
        return

    render_wspolne_zalecenia_podloze(dane)
    used_d3004 = render_wspolna_chemia(dane)

    if dane['needs_levelling'] == "TAK":
        if not used_d3004:
            st.write("* **Następnie należy zaaplikować specjalistyczny mostek sczepny za pomocą produktu WAKOL D 3045. Aplikować równomiernie za pomocą wałka. Zużycie wynosi ok. 150 g/m². Czas schnięcia 1 godzina.**")
        st.write(FULL_Z675)

    st.write("**c) klejenie wykładziny tekstylnej:**")
    st.write("Klejenie wykładziny tekstylnej należy przeprowadzić przy użyciu kleju WAKOL D 3308 (szpachla TKB B1 400-450 g/m²). · Czas wstępnego odparowania: ok. 5-10 minut. · Czas otwarty kleju ok. 10-15 minut")


# ==========================================
# 3. INTERFEJS UŻYTKOWNIKA (FORMULARZ)
# ==========================================

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

flooring_type = st.selectbox("Wybierz rodzaj okładziny (Sekcja):", ["deska warstwowa (drewno, laminat itp.)", "deska lita", "wykładzina dywanowa", "pcv w rolce", "lvt cienkie", "lvt grube z twardym rdzeniem"])
st.markdown(f"### Wywiad Techniczny dla: **{flooring_type.upper()}**")

substrate = st.selectbox("1. Rodzaj podłoża", ["jastrych cementowy", "jastrych anhydrytowy", "płyta fundamentowa", "podłoże drewniane (parkiet, deska, OSB)", "płytki ceramiczne", "masa samorozlewna"])
substrate_age_val = st.number_input("Wiek podłoża (podaj ilość miesięcy):", min_value=0.5, step=0.5, format="%.1f", value=None)

st.write("2. Czy jest instalacja ogrzewania podłogowego?")
heating_exists = st.radio("Ogrzewanie:", ["TAK", "NIE"], index=1, horizontal=True)
heating_info = ""; heating_curing_done = None
if heating_exists == "TAK":
    h_type = st.selectbox("Typ ogrzewania:", ["wodne klasyczne", "bruzdowane", "w suchej zabudowie", "elektryczne (powierzchniowe)", "elektryczne (głębokie)", "płyta fundamentowa grzewcza"])
    st.write("❓ Czy został przeprowadzony proces wygrzewania zgodnie z protokołem?")
    heating_curing_done = st.radio("Proces wygrzewania:", ["TAK", "NIE"], index=1, horizontal=True)
    mapping = {"wodne klasyczne": "instalacja ogrzewania podłogowego wodna, klasyczna", "bruzdowane": "instalacja ogrzewania podłogowego wodna, bruzdowana", "w suchej zabudowie": "instalacja ogrzewania podłogowego wodna, w suchej zabudowie", "elektryczne (powierzchniowe)": "instalacja ogrzewania podłogowego elektryczna, powierzchniowa", "elektryczne (głębokie)": "instalacja ogrzewania podłogowego elektryczna, umieszczona głęboko w podłożu", "płyta fundamentowa grzewcza": "ogrzewanie realizowane poprzez płytę fundamentową grzewczą"}
    heating_info = mapping.get(h_type, h_type)

st.write("3. Czy podłoże wymaga wyrównania (masy)?")
needs_levelling = st.radio("Wymaga wyrównania:", ["TAK", "NIE"], index=1, horizontal=True)
leveling_thickness = 0
already_levelled = "NIE"

if needs_levelling == "TAK":
    leveling_thickness = st.number_input("Planowana grubość masy (mm):", min_value=1, value=None)
elif flooring_type in ["wykładzina dywanowa", "pcv w rolce", "lvt cienkie"]:
    st.warning("Pod wybraną okładzinę wymagane jest wyrównanie podłoża.")
    already_levelled = st.radio("Czy podłoże zostało już wcześniej wyrównane?", ["TAK", "NIE"], index=1, horizontal=True)

st.write("4. Czy dylatacje obwodowe zachowane prawidłowo?")
dilatations_obw_ok = st.radio("Dylatacje obwodowe:", ["TAK", "NIE"], index=0, horizontal=True)
st.write("5. Czy występują klawiszujące dylatacje pozorne?")
cracks_klaw = st.radio("Klawiszowanie pozorne:", ["TAK", "NIE"], index=1, horizontal=True)
klaw_meters = st.number_input("Ilość mb klawiszujących:", min_value=0.1, step=0.1, value=None) if cracks_klaw == "TAK" else 0.0
st.write("6. Czy występują pęknięcia podłoża wymagające zespolenia?")
cracks_pek = st.radio("Pęknięcia do zespolenia:", ["TAK", "NIE"], index=1, horizontal=True)
pek_meters = st.number_input("Ilość mb pęknięć do zespolenia:", min_value=0.1, step=0.1, value=None) if cracks_pek == "TAK" else 0.0
st.write("7. Czy są ubytki lub zdegradowane miejsca wymagające wypełnienia?")
holes = st.radio("Ubytki:", ["TAK", "NIE"], index=1, horizontal=True)
hole_details = ""
if holes == "TAK":
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1: h_depth = st.number_input("Głębokość (cm)", min_value=0.1, value=None)
    with col_h2: h_width = st.number_input("Szerokość (cm)", min_value=0.1, value=None)
    with col_h3: h_length = st.number_input("Długość (cm)", min_value=0.1, value=None)
    if h_depth and h_width and h_length: hole_details = f" o wymiarach ok. {h_length}x{h_width} cm i głębokości {h_depth} cm"

st.write("8. Rodzaj wentylacji")
ventilation_type = st.radio("Wentylacja:", ["Grawitacyjna", "Mechaniczna"], horizontal=True)

col_w1, col_w2 = st.columns(2)
with col_w1: temp_air = st.number_input("9. Temperatura powietrza (°C)", step=0.5, value=None)
with col_w2: hum_air = st.number_input("10. Wilgotność powietrza (%)", step=1.0, value=None)
moisture = st.number_input("11. Poziom wilgoci podłoża (CM %)", format="%.1f", value=None)

# --- LOGIKA NORM I BARIER ---
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
            decision_after_cure = st.radio("Postępowanie z podwyższoną wilgocią:", ["Wykonanie bariery przeciwwilgociowej", opt_dry], horizontal=True)
            needs_drying_action = (decision_after_cure != "Wykonanie bariery przeciwwilgociowej")
        else:
            decision_after_cure = opt_dry

# --- TESTY MECHANICZNE I WYTRZYMAŁOŚĆ ---
st.write("### 12. Testy mechaniczne i Wytrzymałość")
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1: test_hammer = st.selectbox("Młotek", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t2: test_ripper = st.selectbox("Rysik", ["negatywny", "dostateczny", "pozytywny"], index=2)
with col_t3: test_brush = st.selectbox("Szczotka", ["negatywny", "pozytywny"], index=1)

st.write("**Badanie PressoMess**")
presso_results = []
for i in range(6):
    presso_results.append(st.number_input(f"Próba {i+1} (N/mm²)", min_value=0.0, step=0.1, key=f"p_{i}", value=None))
strength_labels = {1: "bardzo słaby", 2: "słaby", 3: "umiarkowanie słaby", 4: "umiarkowanie mocny", 5: "mocny"}
strength_val = st.select_slider("Ocena ogólna wytrzymałości podłoża:", options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: strength_labels[x])

# PAKOWANIE DANYCH DO SŁOWNIKA DLA FUNKCJI GENERUJĄCYCH
dane_protokolu = {
    "flooring_type": flooring_type,
    "substrate": substrate,
    "substrate_age_val": substrate_age_val,
    "heating_exists": heating_exists,
    "heating_info": heating_info,
    "heating_curing_done": heating_curing_done,
    "needs_levelling": needs_levelling,
    "leveling_thickness": leveling_thickness,
    "already_levelled": already_levelled,
    "dilatations_obw_ok": dilatations_obw_ok,
    "cracks_klaw": cracks_klaw,
    "klaw_meters": klaw_meters,
    "cracks_pek": cracks_pek,
    "pek_meters": pek_meters,
    "holes": holes,
    "hole_details": hole_details,
    "ventilation_type": ventilation_type,
    "moisture": moisture,
    "limit": limit,
    "curing_not_done": (heating_exists == "TAK" and heating_curing_done == "NIE"),
    "is_moisture_neg": (moisture is not None and moisture > limit),
    "norm_val_bracket": f"({limit}% CM)",
    "decision_after_cure": decision_after_cure,
    "needs_drying_action": needs_drying_action,
    "test_hammer": test_hammer,
    "test_ripper": test_ripper,
    "test_brush": test_brush,
    "strength_labels": strength_labels,
    "strength_val": strength_val,
    "temp_air": temp_air,
    "hum_air": hum_air,
    "presso_results": presso_results
}

# --- GENEROWANIE PROTOKOŁU W ZALEŻNOŚCI OD WYBRANEJ OKŁADZINY ---
if st.button(f"GENERUJ PROTOKÓŁ OGLĘDZIN DLA: {flooring_type.upper()}", type="primary", use_container_width=True):
    if moisture is None:
        st.error("Proszę podać wilgotność podłoża!")
    else:
        st.divider()
        insert_header()
        st.markdown("#### **I. Oględziny i badania**")
        
        if flooring_type == "deska warstwowa (drewno, laminat itp.)":
            generate_report_deska_warstwowa(dane_protokolu)
        elif flooring_type == "deska lita":
            generate_report_deska_lita(dane_protokolu)
        elif flooring_type == "lvt cienkie":
            generate_report_lvt_cienkie(dane_protokolu)
        elif flooring_type == "pcv w rolce":
            generate_report_pcv_w_rolce(dane_protokolu)
        elif flooring_type == "wykładzina dywanowa":
            generate_report_wykladzina_dywanowa(dane_protokolu)
        elif flooring_type == "lvt grube z twardym rdzeniem":
            generate_report_lvt_grube(dane_protokolu)
        else:
            st.error("Nieobsługiwany typ okładziny.")
            
        st.divider()
        st.markdown(f"<b>Z poważaniem, Loba-Wakol Polska Sp. z o.o. | {autor}</b>", unsafe_allow_html=True)
