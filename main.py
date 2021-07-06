from geodist import geodist


# beschreibt dem Benutzer was das Programm macht
def einfuehrung():
    # alle Saetze die ausgegeben werden sollen
    saetze = [
        "Dieses Programm ermittelt zu einem Geokoordinatenpaar innerhalb",
        "Deutschlands (z.B. 51.447918, 7.270694) die sieben nächstliegenden",
        "Fernstraßenbrücken und gibt ihre Position, ihren Zustand und einen",
        "Link auf eine Onlinekarte aus.",
    ]
    # fuegt alle Saetze mit einem Zeilenumruch zusammen
    print("\n".join(saetze), "\n")


# nimmt das Koordinatenpaar vom Benutzer entgegen
def koordinatenEingabe():
    laengengrad = 0
    breitengrad = 0
    # Kontrollvariable zur Ueberpruefung der Eingabe
    eingabeRichtig = False
    while not eingabeRichtig:
        # Versuch die Eingabe in das richtige Format zu bringen
        try:
            laengengrad = float(input("Geben Sie einen Längengrad ein: "))
            breitengrad = float(input("Geben Sie einen Breitengrad ein: "))
            eingabeRichtig = True
        except:
            print("Die Eingabe war fehlerhaft, versuchen Sie es nochmal.")
            eingabeRichtig = False
    # gibt einen Tuple mit den Koordinaten zurueck
    return (laengengrad, breitengrad)


# liest alle Bruecken aus der CSV Datei
def brueckenEinlesen():
    dateipfad = "./Zustandsnoten Fernstraßenbrücken 2020-09.csv"
    with open(file=dateipfad, mode="r", encoding="utf-8") as datei:
        # alle Bruecken, in einer Liste, ohne nachfolgende leerzeichen
        bruecken = [bruecke.rstrip() for bruecke in datei.readlines()]
    # Bruecken werden zurueckgegeben
    return bruecken


# gibt die entsprechenden indexe der verschiedenen Spalten aus
def spaltenIndexe(bruecken):
    # alle Spaltennamen
    kopfzeile = bruecken[0].split("\t")

    # Spalten als Zahlen (indexe)
    NAME_INDEX = kopfzeile.index("Bauwerksname")
    ORT_INDEX = kopfzeile.index("Ort")
    ZN_INDEX = kopfzeile.index("ZN")
    GML_INDEX = kopfzeile.index("Google Maps Link")
    NB_INDEX = kopfzeile.index("NB")
    OL_INDEX = kopfzeile.index("OL")

    # zurueckgeben der Spaltenindexe
    return [NAME_INDEX, ORT_INDEX, ZN_INDEX, GML_INDEX, NB_INDEX, OL_INDEX]


# berechnet alle Distanzen
def berechneDistanzen(bruecken, kopfzeilenIndexe):
    # neue Liste mit allen Bruecken, als Dict, und den Distanzen
    brueckenMitDistanz = []
    for bruecke in bruecken:
        # alle Werte einer Bruecke als Liste
        brueckenWerte = bruecke.split("\t")

        # Koordinaten haben ein Komma aber brauchen einen Punkt
        NB = float(brueckenWerte[kopfzeilenIndexe[4]].replace(",", "."))
        OL = float(brueckenWerte[kopfzeilenIndexe[5]].replace(",", "."))
        # Tuple mit Koordinaten der Bruecke
        brueckeGeokoordinaten = (NB, OL)

        # Distanz zur Bruecke von unserem eingegebenen Punkt
        # wird ebenfalls auf zwei Nachkommastellen gerundet
        distanzZurBruecke = round(
            geodist(eingegebeneKoordinaten, brueckeGeokoordinaten), 2
        )
        # "km" wird zur Distanz angehaengt
        distanzZurBruecke = str(distanzZurBruecke) + "km"

        # Werte der Bruecke in ein Dict einfuegen
        brueckeAlsDict = {
            "Rang": 0,
            "Bauwerksname": brueckenWerte[kopfzeilenIndexe[0]],
            "Ort": brueckenWerte[kopfzeilenIndexe[1]],
            "Entfernung": distanzZurBruecke,
            "ZN": brueckenWerte[kopfzeilenIndexe[2]],
            "Google Maps Link": brueckenWerte[kopfzeilenIndexe[3]],
        }
        # Dict zur Liste hinzufuegen
        brueckenMitDistanz.append(brueckeAlsDict)
    # Liste mit allen Bruecken zurueckgeben
    return brueckenMitDistanz


# gibt die sieben naechsten Bruecken zurueck
def naechstenSiebenBruecken(eingegebeneKoordinaten, brueckenMitDistanz):
    # sortieren der Liste mit den Bruecken als Dict nach dem Schluessel
    # Entfernung, absteigend, und gibt uns dann die ersten sieben Ergebnisse
    bruecken = sorted(brueckenMitDistanz, 
					key=lambda bruecke: bruecke["Entfernung"])[:7]

    # Rang definiert
    rang = 0
    for bruecke in bruecken:
        # Rang wird immer um eins erhoeht
        rang += 1
        # Rang Wert der Bruecke wird gesetzt
        bruecke["Rang"] = rang
        # ausgabe der Werte der Bruecke
        print("\n")
        for key in bruecke:
            print(key + ": " + str(bruecke[key]))


# main datei
if __name__ == "__main__":
    einfuehrung()
    eingegebeneKoordinaten = koordinatenEingabe()
    bruecken = brueckenEinlesen()
    headerIndexes = spaltenIndexe(bruecken)
    # spalten werden geloescht
    del bruecken[0]
    brueckenMitDistanz = berechneDistanzen(bruecken, headerIndexes)
    naechstenSiebenBruecken(eingegebeneKoordinaten, brueckenMitDistanz)
