import random

def genera_quantita_prodotti():
    prodotti = ["Tavoli", "Sedie", "Sgabelli"]
    quantita = {p: random.randint(20, 200) for p in prodotti}
    return quantita


def genera_parametri_produttivi():
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


def calcola_tempo_totale(quantita, parametri):
    tempo_totale_ore = 0
    giorni = 0
    produzione_rimanente = quantita.copy()

    print("\n=== SIMULAZIONE GIORNALIERA ===")

    while any(qta > 0 for qta in produzione_rimanente.values()):
        giorni += 1
        capacita_disponibile = parametri["capacita_complessiva"]
        produzione_giorno = {}

        for prodotto, qta in produzione_rimanente.items():
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


def main():
    print("=== SIMULAZIONE PROCESSO PRODUTTIVO ARREDIDESIGN S.r.l. ===\n")

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

    # Calcolo dei risultati
    tempo_totale, giorni = calcola_tempo_totale(quantita, parametri)

    print("\n=== RISULTATO FINALE ===")
    print(f"Tempo totale di produzione: {tempo_totale:.2f} ore")
    print(f"Giorni necessari (in base alle capacità): {giorni}")


# Esecuzione del programma
if __name__ == "__main__":
    main()
