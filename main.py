from entità.configurazione_scenari import ConfigurazioneScenari
from entità.configurazione_prodotti import ConfigurazioneProdotti
from entità.simulatore_produzione_kimbo import SimulatoreProduzioneKimbo


# ===============================================
# FUNZIONI UTILI
# ===============================================

def mostra_menu_principale() -> None:
    """Mostra il menu principale dell'applicazione"""

    print("\n" + "="*60)
    print("SIMULATORE PRODUZIONE KIMBO - MENU PRINCIPALE")
    print("="*60)
    print("1. Visualizza scenari disponibili (Standard, alta produzione e personalizzata già inseriti)")
    print("2. Crea un nuovo scenario")
    print("3. Visualizza prodotti")
    print("4. Crea un nuovo prodotto")
    print("5. Esegui simulazione")
    print("6. Confronta scenari")
    print("7. Esci")
    print("-" * 60)

def visualizza_scenari(configurazione_scenari: ConfigurazioneScenari) -> None:
    """Visualizza tutti gli scenari disponibili con dettagli"""
    print("\n" + "=" * 50)
    print("SCENARI PRODUTTIVI DISPONIBILI")
    print("=" * 50)

    scenari = configurazione_scenari.get_scenari_disponibili()

    for i, scenario in enumerate(scenari, 1):
        print(f"\n{i}. {scenario['nome']}")
        print(f"   Descrizione: {scenario['descrizione']}")
        print(f"   Ore lavorative/giorno: {scenario['ore_lavorative_giorno']}h")
        print(f"   Turni/giorno: {scenario['turni_giorno']}")
        print(f"   Efficienza impianti: {scenario['efficienza_impianti'] * 100:.0f}%")
        print(f"   Range quantita: {scenario['range_quantita'][0] * 100:.0f}%-{scenario['range_quantita'][1] * 100:.0f}%")

    input("\nPremere INVIO per tornare al menu principale...")

def visualizza_prodotti(configurazione_prodotti: ConfigurazioneProdotti) -> None:
    """Visualizza tutti gli scenari disponibili con dettagli"""
    print("\n" + "=" * 50)
    print("PRODOTTI INSERITI")
    print("=" * 50)

    prodotti = configurazione_prodotti.get_prodotti()

    for i, prodotto in enumerate(prodotti, 1):
        print(f"\n{i}. {prodotto['nome']}")
        print(f"   Unità di misura: {prodotto['unita_misura']}")
        print(f"   Tempo base di produzione: {prodotto['tempo_base_produzione']}m")
        print(f"   Capacità massima giornaliera: {prodotto['capacita_max_giornaliera']}")

    input("\nPremere INVIO per tornare al menu principale...")

def crea_scenario_personalizzato() -> dict | None:
    """Permette all'utente di creare un nuovo scenario personalizzato"""
    print("\n" + "=" * 50)
    print("CREAZIONE SCENARIO PERSONALIZZATO")
    print("=" * 50)

    try:
        nome = input("Nome scenario: ").strip()
        if not nome:
            nome = "Scenario Personalizzato"

        descrizione = input("Descrizione: ").strip()
        if not descrizione:
            descrizione = "Scenario creato dall'utente"

        print("\nInserisci i parametri operativi:")
        ore_lavorative = int(input("Ore lavorative per giorno (1-24): ") or "8")
        if not ore_lavorative or ore_lavorative < 0:
            raise Exception("Errore inserimento 'ore_lavorative'")
        ore_lavorative = max(1, min(24, ore_lavorative))

        turni = int(input("Numero turni per giorno (1-3): ") or "1")
        if not turni or turni < 0:
            raise Exception("Errore inserimento 'turni'")
        turni = max(1, min(3, turni))

        efficienza = float(input("Efficienza impianti (0.1-1.0): ") or "1.0")
        if not efficienza or efficienza < 0:
            raise Exception("Errore inserimento 'efficienza'")
        efficienza = max(0.1, min(1.0, efficienza))

        var_tempi = float(input("Variabilita tempi (0.0-0.5): ") or "0.1")
        if not var_tempi or var_tempi < 0:
            raise Exception("Errore inserimento 'var_tempi'")
        var_tempi = max(0.0, min(0.5, var_tempi))

        var_capacita = float(input("Variabilita capacita (0.0-0.5): ") or "0.05")
        if not var_capacita or var_capacita < 0:
            raise Exception("Errore inserimento 'var_capacita'")
        var_capacita = max(0.0, min(0.5, var_capacita))

        print("\nRange quantita da produrre (in percentuale della capacita):")
        range_min = float(input("Minimo (0.0-1.0): ") or "0.2")
        if not range_min or range_min < 0:
            raise Exception("Errore inserimento 'range_min'")
        range_min = max(0.0, min(1.0, range_min))

        range_max = float(input("Massimo (0.0-1.0): ") or "0.8")
        if not range_max or range_max < 0:
            raise Exception("Errore inserimento 'range_max'")
        range_max = max(range_min, min(1.0, range_max))

        scenario_personalizzato = {
            'nome': nome,
            'descrizione': descrizione,
            'ore_lavorative_giorno': ore_lavorative,
            'turni_giorno': turni,
            'efficienza_impianti': efficienza,
            'variabilita_tempi': var_tempi,
            'variabilita_capacita': var_capacita,
            'range_quantita': (range_min, range_max),
        }

        return scenario_personalizzato

    except ValueError:
        print("Errore: Inserire valori numerici validi.")
        return None
    except KeyboardInterrupt:
        print("\nOperazione annullata.")
        return None

def crea_prodotto() -> dict | None:
    """Permette all'utente di creare un nuovo prodotto"""
    print("\n" + "=" * 50)
    print("CREAZIONE PRODOTTO")
    print("=" * 50)

    try:
        nome = input("Nome prodotto: ").strip()
        if not nome:
            raise Exception("Errore inserimento 'nome prodotto'")

        unita_misura = input("Unita misura [es: kg, g, lt...]: ").strip()
        if not unita_misura:
            raise Exception("Errore inserimento 'unità di misura'")

        tempo_base_produzione = float(input("Tempo base di produzione (minuti) [es: 5, 10.5, ...]: "))
        if not tempo_base_produzione or tempo_base_produzione < 0:
            raise Exception("Errore inserimento 'Tempo base di produzione")

        capacita_max_giornaliera = int(input("Capacità massima giornaliera [intero > 0]: "))
        if not capacita_max_giornaliera or capacita_max_giornaliera < 0:
            raise Exception("Errore inserimento 'Capacità massima giornaliera")

        prodotto_personalizzato = {
            'nome': nome,
            'unita_misura': unita_misura,
            'tempo_base_produzione': tempo_base_produzione,
            'capacita_max_giornaliera': capacita_max_giornaliera
        }

        return prodotto_personalizzato

    except ValueError:
        print("Errore: Inserire valori numerici validi.")
        return None
    except KeyboardInterrupt:
        print("\nOperazione annullata.")
        return None

def seleziona_scenario(configurazione_scenari: ConfigurazioneScenari) -> dict | None:
    """Permette all'utente di selezionare uno scenario per la simulazione"""

    print("\n" + "=" * 50)
    print("SELEZIONE SCENARIO")
    print("=" * 50)

    scenari = configurazione_scenari.get_scenari_disponibili()

    print("Scenari predefiniti:")
    for i, scenario in enumerate(scenari, 1):
        print(f"{i}. {scenario['nome']}")

    print("0. Torna al menu principale")

    try:
        scelta = int(input(f"\nSeleziona scenario (0-{len(scenari)}): "))

        if scelta == 0:
            return None
        elif 1 <= scelta <= len(scenari):
            return scenari[scelta - 1]
        else:
            print("Selezione non valida.")
            return None

    except ValueError:
        print("Inserire un numero valido.")
        return None
    except KeyboardInterrupt:
        print("\nOperazione annullata.")
        return None

def esegui_simulazione(configurazione_scenari: ConfigurazioneScenari, configurazione_prodotti: ConfigurazioneProdotti) -> None:
    """Esegue una simulazione con lo scenario selezionato"""
    scenario = seleziona_scenario(configurazione_scenari)
    prodotti = configurazione_prodotti.get_prodotti()
    if scenario is None:
        return
    print(f"\nEsecuzione simulazione con scenario: {scenario['nome']}")
    print("-" * 50)

    try:
        simulatore = SimulatoreProduzioneKimbo(scenario, prodotti, 123)
        _ = simulatore.simula_produzione_completa()

        print(f"\nSimulazione completata!")

    except Exception as e:
        print(f"Errore durante la simulazione: {e}")

    input("\nPremere INVIO per tornare al menu principale...")

def confronta_scenari(configurazione_scenari: ConfigurazioneScenari, configurazione_prodotti: ConfigurazioneProdotti) -> None:
    """Confronta i risultati di diversi scenari"""

    print("\n" + "=" * 50)
    print("CONFRONTO SCENARI")
    print("=" * 50)

    print("Seleziona il primo scenario:")
    scenario1 = seleziona_scenario(configurazione_scenari)
    if scenario1 is None:
        return

    print("\nSeleziona il secondo scenario:")
    scenario2 = seleziona_scenario(configurazione_scenari)
    if scenario2 is None:
        return

    print(f"\nConfronto tra '{scenario1['nome']}' e '{scenario2['nome']}'")
    print("-" * 60)

    prodotti = configurazione_prodotti.get_prodotti()
    try:
        # Simula primo scenario
        simulatore1 = SimulatoreProduzioneKimbo(scenario1, prodotti)
        print(f"\nSimulazione {scenario1['nome']}:")
        risultati1 = simulatore1.simula_produzione_completa()

        print("\n" + "=" * 60)

        # Simula secondo scenario
        simulatore2 = SimulatoreProduzioneKimbo(scenario2, prodotti)
        print(f"\nSimulazione {scenario2['nome']}:")
        risultati2 = simulatore2.simula_produzione_completa()

        # Mostra confronto
        print("\n" + "=" * 60)
        print("RIEPILOGO CONFRONTO:")
        print(f"{scenario1['nome']}: {risultati1['risultati_produzione']['tempo_totale_ore']} ore totali")
        print(f"{scenario2['nome']}: {risultati2['risultati_produzione']['tempo_totale_ore']} ore totali")

        diff_ore = risultati2['risultati_produzione']['tempo_totale_ore'] - risultati1['risultati_produzione']['tempo_totale_ore']
        if diff_ore > 0:
            print(f"Il secondo scenario richiede {abs(diff_ore):.1f} ore in piu")
        elif diff_ore < 0:
            print(f"Il secondo scenario richiede {abs(diff_ore):.1f} ore in meno")
        else:
            print("I due scenari richiedono lo stesso tempo")

    except Exception as e:
        print(f"Errore durante il confronto: {e}")

    input("\nPremere INVIO per tornare al menu principale...")



# ===============================================
# MAIN
# ===============================================

if __name__ == "__main__":
    print("========== SIMULAZIONE PROCESSO PRODUTTIVO KIMBO ==========\n\n")

    """Funzione principale per eseguire la simulazione"""
    configurazione_scenari = ConfigurazioneScenari()
    configurazione_prodotti = ConfigurazioneProdotti()

    while True:
        try:
            mostra_menu_principale()
            scelta = input("Seleziona un'opzione (1-7): ").strip()

            if scelta == '1':
                visualizza_scenari(configurazione_scenari)
            elif scelta == '2':
                nuovo_scenario = crea_scenario_personalizzato()
                if nuovo_scenario:
                    configurazione_scenari.add_scenario(nuovo_scenario)
                    print(f"Scenario '{nuovo_scenario['nome']}' creato con successo!")
                    input("Premere INVIO per continuare...")
            elif scelta == '3':
                visualizza_prodotti(configurazione_prodotti)
            elif scelta == '4':
                nuovo_prodotto = crea_prodotto()
                if nuovo_prodotto:
                    configurazione_prodotti.add_prodotto(nuovo_prodotto)
                    print(f"Prodotto '{nuovo_prodotto['nome']}' inserito con successo!")
                    input("Premere INVIO per continuare...")
            elif scelta == '5':
                esegui_simulazione(configurazione_scenari, configurazione_prodotti)
            elif scelta == '6':
                confronta_scenari(configurazione_scenari, configurazione_prodotti)
            elif scelta == '7':
                print("\nGrazie per aver usato il Simulatore Produzione Kimbo!")
                print("Arrivederci!")
                break
            else:
                print("Selezione non valida. Riprova.")
                input("Premere INVIO per continuare...")

        except KeyboardInterrupt:
            print("\n\nUscita dal programma...")
            break
        except Exception as e:
            print(f"Errore imprevisto: {e}")
            input("Premere INVIO per continuare...")