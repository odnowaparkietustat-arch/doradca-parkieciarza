# --- GENEROWANIE PROTOKOŁU ---
if st.button("GENERUJ PROTOKÓŁ OGLĘDZIN"):
    if moisture is None:
        st.error("Proszę wpisać poziom wilgoci przed generowaniem protokołu!")
    else:
        st.divider()
        # Logika statusu wilgotności
        m_status = "POZYTYWNY" if moisture <= limit else "NEGATYWNY"

        st.markdown("### **Loba-Wakol Polska Sp. z o.o.**")
        st.write(f"**Data badania:** {data_badania.strftime('%d.%m.%Y')} | **Autor:** {autor}")
        st.write(f"**Inwestycja:** {inwestycja}, {adres}, {miejscowosc}")
        st.write(f"**Szanowni Państwo:** {klient}")

        st.markdown("#### **I. Oględziny i badania**")
        st.write(f"**a) oględziny optyczne:** Podłoże stanowi {substrate}. {heating_info if heating_exists == 'TAK' else 'Brak instalacji ogrzewania podłogowego.'} Wentylacja: **{ventilation_type}**.")
        
        if heating_exists == 'TAK':
            st.write(f"**Proces wygrzewania podłoża:** {'przeprowadzony' if heating_cured == 'TAK' else 'nie przeprowadzony'}")
        
        st.write(f"**b) badanie wytrzymałości:**")
        st.write(f"* próba młotkiem – **{test_hammer}**")
        st.write(f"* próba szczotką drucianą – **{test_brush}**")
        st.write(f"* próba rysikiem – **{test_ripper}**")
        st.write(f"* Ocena ogólna wytrzymałości: **{strength_labels[strength_val]}**")
        
        st.write(f"**c) badanie wilgotności podłoża:** Wynik **{moisture} % CM** (Norma: {limit} % CM) - Status: **{m_status}**")
        st.write(f"**d) warunki klimatyczne:** {temp if temp else '--'}°C | {humidity if humidity else '--'}% RH.")

        st.markdown("#### **II. Zalecenia techniczne**")
        st.write("**a) przygotowanie podłoża:**")
        
        is_mandatory_cure = False
        if heating_exists == "TAK" and heating_cured == "NIE":
            if any(x in heating_info for x in ["wodna", "wewnątrz jastrychu"]) or substrate == "płyta fundamentowa":
                st.write("* **Przeprowadzenie pełnego procesu wygrzewania zgodnie z protokołem temperatura wody w instalacji minimum 40 stopni!**")
                is_mandatory_cure = True

        if decision_after_cure in ["Dalsze osuszanie", "Kolejny proces wygrzewania"]:
            st.write(f"* **Zalecamy doprowadzenie do normatywnego poziomu wilgoci ({limit}% CM) poprzez kontynuowanie procesu {decision_after_cure.lower()}.**")

        st.write("* Szlif podłoża w celu uzyskania porowatej i chłonnej powierzchni.")
        st.write("* Dokładne odkurzenie całej powierzchni.")

        st.write("**b) naprawa i wzmocnienie podłoża:**")
        if (decision_after_cure in ["Dalsze osuszanie", "Kolejny proces wygrzewania"] or is_mandatory_cure):
            st.write(f"* **Po doprowadzeniu do normatywnego poziomu wilgoci w jastrychu (tj. {limit}% CM), zalecamy:**")
        
        if cracks == "TAK": 
            st.write(f"    * Klawiszujące fragmenty ({cracks_meters} mb) zespolić żywicą laną **WAKOL PS 205**.")
        if holes == "TAK": 
            st.write(f"    * Ubytki uzupełnić zaprawą **WAKOL Z 610**.")
        
        if decision_after_cure == "Wykonanie bariery przeciwwilgociowej":
            st.write("* **Z uwagi na podwyższoną wilgotność zalecamy stworzenie bariery przeciwwilgociowej poprzez zagruntowanie powierzchni jastrychu gruntówką poliuretanową WAKOL PU 280.**")
            st.write("  Aplikować wałkiem. Podczas aplikacji nie zostawiać kałuż tj. Zbierać nadmiar niewchłoniętej gruntówki.")
            st.write("  - **1 warstwa:** nałożona wałkiem ok. 100-150 g/m². Czas schnięcia – jedna godzina.")
            st.write("  - **2 warstwa:** ok. 100 g/m² – czas schnięcia – jedna godzina.")
            st.markdown("  *W zależności od chłonności podłoża zużycie gruntówki może być większe bądź mniejsze. Większa ilość nałożonego materiału wydłuża czas schnięcia. Należy zaślepić dylatacje pozorne.*")
        else:
            if strength_val >= 4:
                st.write(f"* Gruntowanie podłoża: **WAKOL D 3055**.")
            elif strength_val == 3:
                st.write("* Zalecamy zagruntowanie całej powierzchni podłoża gruntówką wzmacniającą **WAKOL PU 280**. Aplikować wałkiem. Zużycie ok. 150 g/m². Czas schnięcia 1 godzina. Czas do montażu – 72 godziny.")
            elif strength_val == 2:
                st.write("* Zalecamy jednokrotną aplikację gruntówki **WAKOL PU 235**. Zużycie ok. 150 g/m². Czas schnięcia 3 – 6 godzin. Czas klejenia 72 godziny od zagruntowania.")
            elif strength_val == 1:
                st.write(f"* Wzmocnienie podłoża żywicą: **WAKOL PS 275**.")

        if needs_levelling == "TAK":
            st.write("* Wyrównanie: mata **WAKOL AR 150** + masa **WAKOL Z 645/635**.")

        st.write("**c) montaż okładziny:**")
        if flooring_type == "deska warstwowa (drewno, laminat itp.)":
            st.write("* Klejenie deski należy przeprowadzić przy użyciu kleju do parkietu **WAKOL PU 225** (szpachla **B11**, zużycie: **1250 g/m²**).")
        else:
            st.write(f"* Montaż okładziny **{flooring_type}** zgodnie z kartami technicznymi WAKOL.")
        
        st.divider()
        st.write(f"Z poważaniem, **{autor}**")
