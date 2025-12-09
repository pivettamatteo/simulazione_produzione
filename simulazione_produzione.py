import random

# Costanti globali per generare un menu di selezione (funzione mostra_menu)
PRIORITA_CASUALE = 1
PRIORITA_PRODOTTI_LENTI = 2
PRIORITA_DOMANDA_ALTA = 3
ESCI = 4

def genera_quantita_prodotti():
    # Genera casualmente le quantità da produrre per ciascun prodotto (tavoli, sedie, sgabelli)
    prodotti = ["Tavoli", "Sedie", "Sgabelli"]
    quantita = {p: random.randint(20, 200) for p in prodotti}
    return quantita


def genera_parametri_produttivi():
    # Genera casualmente i parametri produttivi
    prodotti = ["Tavoli", "Sedie", "Sgabelli"]
    parametri = {}

    for p in prodotti:
        # Tempo medio di produzione per unità (in ore)
        tempo_unitario = round(random.uniform(0.5, 2.0), 2)
        # Capacità produttiva giornaliera per tipo di prodotto (unità/giorno)
        capacita_giornaliera = random.randint(30, 150)
        parametri[p] = {
            "tempo_unitario": tempo_unitario,
            "capacita_giornaliera": capacita_giornaliera
        }

    # Calcolo della capacità totale giornaliera complessiva
    capacita_totale_giornaliera = sum(v["capacita_giornaliera"] for v in parametri.values())
    parametri["capacita_complessiva"] = capacita_totale_giornaliera
    return parametri

def ordine_casuale(produzione_rimanente):
    # Funzione per ordinare casualmente la produzione. Restituisce una lista
    prodotti = list(produzione_rimanente.keys())
    random.shuffle(prodotti)
    return prodotti

def ordine_t_decrescente(produzione_rimanente, parametri):
    # Funzione per ordinare la produzione per tempo decrescente. Prima i prodotti più lenti
    def chiave_tempo(prodotto):
        return parametri[prodotto]["tempo_unitario"]

    prodotti = list(produzione_rimanente.keys())
    prodotti_ordinati = sorted(prodotti, key=chiave_tempo, reverse=True)
    return prodotti_ordinati
    
def ordine_q_decrescente(produzione_rimanente):
    # Funzione per ordinare la produzione per quantità decrescente. Prima i prodotti con più quantità
    def chiave_domanda(prodotto):
        return produzione_rimanente[prodotto]

    prodotti = list(produzione_rimanente.keys())
    prodotti_ordinati = sorted(prodotti, key=chiave_domanda, reverse=True)
    return prodotti_ordinati
    
def det_ordine_prodotti(produzione_rimanente, parametri, priorita):
    # Selezione della priorità
    if priorita == PRIORITA_CASUALE:
        return ordine_casuale(produzione_rimanente)
    elif priorita == PRIORITA_PRODOTTI_LENTI:
        return ordine_t_decrescente(produzione_rimanente, parametri)
    elif priorita == PRIORITA_DOMANDA_ALTA:
        return ordine_q_decrescente(produzione_rimanente)
    else:
        # Ordine di default: come sono nella struttura dati
        return list(produzione_rimanente.keys())


def calcola_tempo_totale(quantita, parametri, priorita):
    # Simula giorno per giorno la produzione. Restituisce tempo tot di produzione e numero giorni necessari
    tempo_totale_ore = 0
    giorni = 0
    # Copia delle quantità per non modificare il dizionario originale
    produzione_rimanente = quantita.copy()

    print("\n=== SIMULAZIONE GIORNALIERA ===")

    while any(qta > 0 for qta in produzione_rimanente.values()):
        giorni += 1
        capacita_disponibile = parametri["capacita_complessiva"]
        produzione_giorno = {}

        # Determina l'ordine con cui tentare di produrre i prodotti
        ordine_prodotti = det_ordine_prodotti(
            produzione_rimanente, parametri, priorita
        )

        for prodotto in ordine_prodotti:
            qta = produzione_rimanente[prodotto]

            if qta <= 0:
                produzione_giorno[prodotto] = 0
                continue

            # Massimo producibile oggi = min(capacità prodotto, capacità residua impianto, quantità rimanente)
            max_producibile = min(
                parametri[prodotto]["capacita_giornaliera"],
                capacita_disponibile,
                qta
            )

            produzione_giorno[prodotto] = max_producibile
            produzione_rimanente[prodotto] -= max_producibile
            capacita_disponibile -= max_producibile

        # Calcolo ore giornaliere effettive
        tempo_giornaliero = sum(
            produzione_giorno[p] * parametri[p]["tempo_unitario"]
            for p in produzione_giorno
        )
        tempo_totale_ore += tempo_giornaliero

        print(f"Giorno {giorni}: {produzione_giorno} -> {tempo_giornaliero:.2f} h")

    return tempo_totale_ore, giorni

def mostra_menu():
    print(f"{PRIORITA_CASUALE} - Produzione con priorità casuale")
    print(f"{PRIORITA_PRODOTTI_LENTI} - Produzione con priorità ai prodotti più lenti")
    print(f"{PRIORITA_DOMANDA_ALTA} - Produzione con priorità alla domanda più alta")
    print(f"{ESCI} - Esci")
    print()
    scelta = input("Seleziona un'opzione: ")
    try:
        scelta_int = int(scelta)
    except ValueError:
        scelta_int = 0
    return scelta_int

def criterio(priorita):
    if priorita == PRIORITA_CASUALE:
        return "priorità casuale"
    elif priorita == PRIORITA_PRODOTTI_LENTI:
        return "priorità ai prodotti più lenti"
    elif priorita == PRIORITA_DOMANDA_ALTA:
        return "priorità alla domanda più alta"
    else:
        return "criterio non specificato"

def main():
    print("\n=== SIMULAZIONE PROCESSO PRODUTTIVO ARREDIDESIGN S.r.l. ===\n")

    scelta = 0

    while scelta != ESCI:
        scelta = mostra_menu()

        if scelta == ESCI:
            print("Uscita dal programma.")
            break

        # Controllo validità scelta
        if scelta not in (PRIORITA_CASUALE,
                          PRIORITA_PRODOTTI_LENTI,
                          PRIORITA_DOMANDA_ALTA):
            print("Scelta non valida. Riprovare.\n")
            continue

        print(f"\nHai scelto di dare {criterio(scelta)}.\n")

        # Generazione dati casuali
        quantita = genera_quantita_prodotti()
        parametri = genera_parametri_produttivi()

        print("Quantità da produrre:")
        for p, q in quantita.items():
            print(f"  {p}: {q} unità")

        print("\nParametri di produzione:")
        for p in ["Tavoli", "Sedie", "Sgabelli"]:
            print(f"  {p} -> Tempo/unità: {parametri[p]['tempo_unitario']}h, "
              f"Capacità max/giorno: {parametri[p]['capacita_giornaliera']} unità")

        print(f"\nCapacità produttiva complessiva giornaliera: {parametri['capacita_complessiva']} unità/giorno")

        # Calcolo dei risultati con il criterio scelto
                
        tempo_totale, giorni = calcola_tempo_totale(quantita, parametri, scelta)

        print("\n=== RISULTATO FINALE ===")
        print(f"Tempo totale di produzione: {tempo_totale:.2f} ore")
        print(f"Giorni necessari (in base alle capacità): {giorni}")
        print("\n========================\n")


# Esecuzione del programma
if __name__ == "__main__":
    main()
