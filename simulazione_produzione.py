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
            capacita_massima = random.randint(30, 150)
            parametri[p] = {
                "tempo_unitario": tempo_unitario,
                "capacita_massima": capacita_massima
            }
    
        capacita_totale_giornaliera = sum(v["capacita_massima"] for v in parametri.values())
        return parametri, capacita_totale_giornaliera

def calcola_tempo_totale(quantita, parametri):
        tempo_totale = 0
        for prodotto in quantita:
            tempo_prodotto = quantita[prodotto] * parametri[prodotto]["tempo_unitario"]
            tempo_totale += tempo_prodotto
        return round(tempo_totale, 2)

def main():
          print("=== SIMULAZIONE PROCESSO PRODUTTIVO ARREDIDESIGN S.r.l. ===\n")

          # Generazione dati casuali
          quantita = genera_quantita_prodotti()
          parametri, capacita_totale = genera_parametri_produttivi()

          print("Quantità da produrre:")
          for p, q in quantita.items():
              print(f"  {p}: {q} unità")

          print("\nParametri di produzione:")
          for p, v in parametri.items():
              print(f"  {p} -> Tempo/unità: {v['tempo_unitario']}h, Capacità max/giorno: {v['capacita_massima']} unità")

          print(f"\nCapacità produttiva complessiva giornaliera: {capacita_totale} unità/giorno")

          # Calcolo tempo totale
          tempo_totale = calcola_tempo_totale(quantita, parametri)
          print(f"\nTempo totale di produzione: {tempo_totale} ore")

# Esecuzione del programma
if __name__ == "__main__":
                main()

