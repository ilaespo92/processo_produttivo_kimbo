from entità.configurazione_stabilimento import ConfigurazioneStabilimento
import random

# ===============================================
# GENERAZIONE SIMULAZIONI
# ===============================================
def formatta_hms(ore:float) -> str:
    """
    Converte un valore in ore (float) nel formato "Hh Mm Ss".
    Gestisce arrotondamenti e carry-over (es. 59.6s -> 60s -> +1m).
    """

    total_seconds = int(round(ore*3600))
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60

    return f"{h}h {m}m {s}s"


class SimulatoreProduzioneKimbo:
    """
    Simulatore del processo produttivo dell'azienda Kimbo
    Simula la produzione di tre tipologie principali di prodotto
    """

    def __init__(self, scenario: dict, prodotti: list[dict], seed: int | None = None):
        """
        Inizializza il simulatore con uno scenario configurabile

        Args:
            scenario (dict): Configurazione dello scenario produttivo, lista di prodotti e seed (opzionale) per i dati casuali
        """

        if seed is not None:
            random.seed(seed)

        # Configurazione prodotti base
        self.prodotti = prodotti
        self.capacita_totale_giornaliera = ConfigurazioneStabilimento.capacita_totale_giornaliera
        self.scenario_corrente = scenario

        # Carica scenario o usa quello standard
        if scenario is None:
            raise Exception("Immettere uno scenario")

        # Applica configurazioni dello scenario
        self._applica_scenario()

    def _applica_scenario(self) -> None:
        """
        Applica le configurazioni dello scenario ai parametri di produzione
        """
        efficienza = self.scenario_corrente['efficienza_impianti']

        # Modifica capacità e tempi in base all'efficienza dello scenario
        for prodotto in self.prodotti:
            # Riduce capacità se efficienza < 1.0
            capacita_originale = prodotto['capacita_max_giornaliera']
            prodotto['capacita_scenario'] = int(capacita_originale * efficienza)

            # Aumenta tempi se efficienza < 1.0
            tempo_originale = prodotto['tempo_base_produzione']

            if efficienza == 0:
                raise Exception("Impossibile calcolare il 'tempo necessario di produzione' \
                                perchè per lo scenario in questione, l'efficienza è uguale a zero")

            prodotto['tempo_scenario'] = tempo_originale / efficienza

    def genera_quantita_casuali(self) -> dict:
        """
        Genera casualmente le quantità da produrre per ogni tipo di prodotto
        Utilizza i range definiti nello scenario corrente

        Returns:
            dict: Dizionario con le quantità per ogni prodotto
        """
        quantita = {}
        range_min, range_max = self.scenario_corrente['range_quantita']

        for prodotto in self.prodotti:
            # Usa capacità modificata dallo scenario
            capacita_max = prodotto['capacita_scenario']
            quantita_min = int(capacita_max * range_min)
            quantita_max = int(capacita_max * range_max)

            quantita[prodotto['nome']] = random.randint(quantita_min, quantita_max)

        return quantita

    def genera_parametri_casuali(self) -> dict:
        """
        Genera casualmente i parametri operativi della produzione
        Utilizza le variabilità definite nello scenario corrente

        Returns:
            dict: Parametri di configurazione casuali
        """
        parametri = {}
        var_tempi = self.scenario_corrente['variabilita_tempi']
        var_capacita = self.scenario_corrente['variabilita_capacita']

        for prodotto in self.prodotti:
            # Variazione casuale del tempo di produzione
            tempo_base = prodotto['tempo_scenario']
            variazione = random.uniform(-var_tempi, var_tempi)
            tempo_effettivo = tempo_base * (1 + variazione)

            # Variazione casuale della capacità
            capacita_base = prodotto['capacita_scenario']
            variazione_cap = random.uniform(-var_capacita, var_capacita)
            capacita_effettiva = int(capacita_base * (1 + variazione_cap))

            parametri[prodotto['nome']] = {
                'tempo_produzione_unitario': round(tempo_effettivo, 2),
                'capacita_giornaliera_effettiva': capacita_effettiva
            }

        # Capacità totale con variabilità dello scenario
        variazione_totale = random.uniform(-var_capacita, var_capacita)
        capacita_scenario = self.capacita_totale_giornaliera * self.scenario_corrente['efficienza_impianti']
        parametri['capacita_totale_effettiva'] = int(capacita_scenario * (1 + variazione_totale))

        return parametri

    def get_product_by_name(self, nome: str) -> dict | None:
        """
        Cerca in una lista di dizionari quello che ha 'nome' uguale al parametro.
        Ritorna il dizionario trovato oppure None se non esiste.
        """
        for p in self.prodotti:
            if p.get("nome") == nome:
                return p

        raise Exception("Prodotto non trovato!")

    def calcola_tempo_produzione(self, quantita: dict, parametri: dict) -> dict:
        """
        Calcola il tempo di produzione complessivo del lotto

        Args:
            quantita (dict): Quantità da produrre per ogni prodotto
            parametri (dict): Parametri operativi

        Returns:
            dict: Dettagli della produzione e tempo totale
        """

        risultati = {
            'dettagli_prodotti': {},
            'tempo_totale_minuti': 0,
            'capacita_utilizzata': {},
            'vincoli_rispettati': True
        }

        tempo_totale = 0

        for nome_prodotto, qta in quantita.items():
            product = self.get_product_by_name(nome_prodotto)

            unita = product['unita_misura']

            # Tempo di produzione per questo prodotto
            tempo_unitario = parametri[nome_prodotto]['tempo_produzione_unitario']
            tempo_prodotto = qta * tempo_unitario

            # Verifica capacità
            capacita_max = parametri[nome_prodotto]['capacita_giornaliera_effettiva']

            if capacita_max == 0:
                raise Exception("Impossibile calcolare la percentuale di crescita. La capacità massima è uguale a zero")

            percentuale_capacita = (qta / capacita_max) * 100

            if qta > capacita_max:
                risultati['vincoli_rispettati'] = False

            risultati['dettagli_prodotti'][nome_prodotto] = {
                'nome': nome_prodotto,
                'quantita': qta,
                'unita_misura': unita,
                'tempo_produzione_minuti': round(tempo_prodotto, 2),
                'tempo_produzione_ore': round(tempo_prodotto / 60, 2),
                'capacita_utilizzata_percentuale': round(percentuale_capacita, 1),
                'capacita_superata': qta > capacita_max
            }

            tempo_totale += tempo_prodotto

        risultati['tempo_totale_minuti'] = round(tempo_totale, 2)
        risultati['tempo_totale_ore'] = round(tempo_totale / 60, 2)

        # Calcola giorni lavorativi in base alle ore dello scenario
        ore_lavorative = self.scenario_corrente['ore_lavorative_giorno']
        if ore_lavorative == 0:
            raise Exception("Impossibile calcolare il tempo totale in giorni. Le ore lavorate sono uguale a zero")

        risultati['tempo_totale_giorni'] = round(tempo_totale / (60 * ore_lavorative), 2)

        return risultati

    def simula_produzione_completa(self) -> dict:
        """
        Esegue una simulazione completa del processo produttivo

        Returns:
            dict: Risultati completi della simulazione
        """
        print(f"Descrizione: {self.scenario_corrente['descrizione']}\n")

        # Genera dati casuali
        quantita = self.genera_quantita_casuali()
        parametri = self.genera_parametri_casuali()

        # Calcola tempi di produzione
        risultati = self.calcola_tempo_produzione(quantita, parametri)

        # Visualizza risultati
        self.stampa_risultati(quantita, parametri, risultati)

        return {
            'scenario': self.scenario_corrente,
            'quantita_prodotti': quantita,
            'parametri_operativi': parametri,
            'risultati_produzione': risultati
        }

    def stampa_risultati(self, quantita: dict, parametri: dict, risultati: dict) -> None:
        """
        Stampa i risultati della simulazione in formato leggibile
        """
        print("QUANTITA DA PRODURRE (generate casualmente):")
        for nome_prodotto, qta in quantita.items():
            prodotto = self.get_product_by_name(nome_prodotto)
            unita = prodotto['unita_misura']
            print(f"  - {nome_prodotto}: {qta:,} {unita}")

        print("\nPARAMETRI OPERATIVI (generati casualmente):")
        for nome_prodotto, param in parametri.items():
            if nome_prodotto != 'capacita_totale_effettiva':
                prodotto = self.get_product_by_name(nome_prodotto)
                tempo = param['tempo_produzione_unitario']
                capacita = param['capacita_giornaliera_effettiva']
                unita = prodotto['unita_misura']
                print(f"  - {nome_prodotto}: {tempo} min/{unita}, Capacita: {capacita:,} {unita}/giorno")

        print(f"  - Capacita Totale Impianto: {parametri['capacita_totale_effettiva']:,} unita/giorno")

        print("\nRISULTATI PRODUZIONE:")
        for _, dettaglio in risultati['dettagli_prodotti'].items():
            print(f"  - {dettaglio['nome']}:")
            print(f"    Quantita: {dettaglio['quantita']:,} {dettaglio['unita_misura']}")
            print(f"    Tempo produzione: {formatta_hms(dettaglio['tempo_produzione_ore'])}")
            print(f"    Capacita utilizzata: {dettaglio['capacita_utilizzata_percentuale']}%")
            if dettaglio['capacita_superata']:
                print("    ATTENZIONE: Capacita superata!")

        ore_scenario = self.scenario_corrente['ore_lavorative_giorno']
        print(f"\nTEMPO TOTALE PRODUZIONE:")
        print(f"  - {formatta_hms(risultati['tempo_totale_ore'])} ")
        print(f"  - {risultati['tempo_totale_giorni']} giorni lavorativi ({ore_scenario}h/giorno)")

        if not risultati['vincoli_rispettati']:
            print("\nAVVISO: Alcuni vincoli di capacita non sono stati rispettati!")
        else:
            print("\nTutti i vincoli di capacita sono stati rispettati")
