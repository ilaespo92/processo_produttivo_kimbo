class ConfigurazioneProdotti:
    prodotti = []

    def __init__(self):
        # Configurazione prodotti base
        self.prodotti = [
            {
                'nome': 'Caffè in Grani',
                'unita_misura': 'kg',
                'tempo_base_produzione': 2.5,  # minuti per kg
                'capacita_max_giornaliera': 5000  # kg/giorno
            },
            {
                'nome': 'Caffè Macinato',
                'unita_misura': 'kg',
                'tempo_base_produzione': 3.2,  # minuti per kg (include macinazione)
                'capacita_max_giornaliera': 4000  # kg/giorno
            },

            {
                'nome': 'Capsule/Cialde',
                'unita_misura': 'confezioni',
                'tempo_base_produzione': 1.8,  # minuti per confezione
                'capacita_max_giornaliera': 8000  # confezioni/giorno
            }
        ]

    def get_prodotti(self) -> list[dict]:
        return self.prodotti

    def add_prodotto(self, nuovo_prodotto:dict) -> None:
        for p in self.prodotti:
            if p['nome'] == nuovo_prodotto['nome']:
                raise Exception(f"Prodotto '{nuovo_prodotto['nome']}' già presente")

        self.prodotti.append(nuovo_prodotto)

