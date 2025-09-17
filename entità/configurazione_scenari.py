# ===============================================
# CONFIGURAZIONE SCENARI
# ===============================================
class ConfigurazioneScenari:
    """
    Classe per gestire diverse configurazioni di scenari produttivi
    Permette di modificare facilmente i parametri per simulare diverse situazioni operative
    """
    scenari = []

    def __init__(self):
        self.scenari = [

            {   # Scenario Produzione Standard
                'nome': 'produzione_standard',
                'descrizione': 'Configurazione normale di produzione giornaliera',
                'ore_lavorative_giorno': 8,
                'turni_giorno': 1,
                'efficienza_impianti': 1.0,
                'variabilita_tempi': 0.1,  # ±10%
                'variabilita_capacita': 0.05,  # ±5%
                'range_quantita': (0.3, 0.7),  # 30%-70% della capacità
            },

            {    # Scenario Alta Produzione
                'nome': 'alta_produzione',
                'descrizione': 'Configurazione per periodi di alta domanda',
                'ore_lavorative_giorno': 16,
                'turni_giorno': 2,
                'efficienza_impianti': 0.9,
                'variabilita_tempi': 0.15,  # ±15%
                'variabilita_capacita': 0.1,  # ±10%
                'range_quantita': (0.6, 0.9),  # 60%-90% della capacità
            },

            {    # Scenario Personalizzato
                'nome': 'personalizzato',
                'descrizione': 'Produzione ridotta per periodo festivo',
                'ore_lavorative_giorno': 4,
                'turni_giorno': 1,
                'efficienza_impianti': 0.6,
                'variabilita_tempi': 0.3,
                'variabilita_capacita': 0.25,
                'range_quantita': (0.1, 0.3),
            }
        ]

    def get_scenari_disponibili(self) -> list[dict]:
        """Restituisce la lista di tutti gli scenari configurabili"""
        return self.scenari

    def add_scenario(self, nuovo_scenario: dict) -> None:
        for s in self.scenari:
            if s['nome'] == nuovo_scenario['nome']:
                raise Exception(f"Scenario '{nuovo_scenario['nome']}' già presente")

        self.scenari.append(nuovo_scenario)



