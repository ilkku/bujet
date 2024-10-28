import json
from datetime import datetime

BUDJETTI_TIEDOSTO = "budjetit.json"

def tallenna_budjetit(budjetit):
    """Tallentaa budjetit JSON-tiedostoon."""
    try:
        with open(BUDJETTI_TIEDOSTO, "w") as f:
            json.dump(budjetit, f, indent=4)
        print("Budjetit tallennettu onnistuneesti.")
    except IOError:
        print("Tallennus epäonnistui.")

def lataa_budjetit():
    """Lataa budjetit JSON-tiedostosta."""
    try:
        with open(BUDJETTI_TIEDOSTO, "r") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return {}

def luo_uusi_budjetti():
    """Luo uuden budjetin kysymällä käyttäjältä budjettikohteet ja summat."""
    budjetti = {}
    print("Syötä budjetoidut summat seuraaville kuluille:")
    for kohde in ["Vuokra", "Vakuutukset", "Kouluruokailu", "Sähkö", "Liikkuminen"]:
        while True:
            try:
                summa = float(input(f"{kohde}: "))
                budjetti[kohde] = summa
                break
            except ValueError:
                print("Syötä kelvollinen numero.")
    while True:
        lisaa = input("\nHaluatko lisätä uuden budjettikohteen? (k/e): ").lower()
        if lisaa == 'k':
            uusi_kohde = input("Anna uuden budjettikohteen nimi: ")
            while True:
                try:
                    uusi_summa = float(input(f"Anna summa kohteelle {uusi_kohde}: "))
                    budjetti[uusi_kohde] = uusi_summa
                    break
                except ValueError:
                    print("Syötä kelvollinen numero.")
        elif lisaa == 'e':
            break
        else:
            print("Syötä 'k' lisätäksesi kohteen tai 'e' lopettaaksesi.")
    return budjetti

def kopioi_budjetti(budjetit, kuukausi):
    """Kopioi annetun kuukauden budjetin uudelle kuukaudelle."""
    uusi_kuukausi = input("Anna uuden kuukauden nimi (esim. 2023-04): ")
    if kuukausi in budjetit:
        budjetit[uusi_kuukausi] = budjetit[kuukausi].copy()
        print(f"Budjetti kuukaudelle {kuukausi} kopioitu kuukaudelle {uusi_kuukausi}.")
    else:
        print(f"Kuukauden {kuukausi} budjettia ei löydy.")
    return budjetit

def nayta_kaikki_budjetit(budjetit):
    """Näyttää kaikki tallennetut kuukausittaiset budjetit."""
    for kuukausi, budjetti in budjetit.items():
        print(f"\nBudjetti kuukaudelle {kuukausi}:")
        for kohde, summa in budjetti.items():
            print(f"  {kohde}: {summa:.2f} €")

budjetit = lataa_budjetit()

while True:
    print("\nValitse toiminto:")
    print("1. Luo uusi kuukausibudjetti")
    print("2. Kopioi budjetti seuraavalle kuukaudelle")
    print("3. Näytä kaikki budjetit")
    print("4. Lopeta")

    valinta = input("Valintasi: ")
    
    if valinta == "1":
        nykyinen_kuukausi = datetime.now().strftime("%Y-%m")
        budjetit[nykyinen_kuukausi] = luo_uusi_budjetti()
        tallenna_budjetit(budjetit)

    elif valinta == "2":
        nayta_kaikki_budjetit(budjetit)
        kuukausi = input("\nSyötä kopioitavan budjetin kuukausi (esim. 2023-03): ")
        budjetit = kopioi_budjetti(budjetit, kuukausi)
        tallenna_budjetit(budjetit)

    elif valinta == "3":
        nayta_kaikki_budjetit(budjetit)

    elif valinta == "4":
        print("Ohjelma lopetettu.")
        break

    else:
        print("Virheellinen valinta. Yritä uudelleen.")
