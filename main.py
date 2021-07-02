from geodist import geodist

def einfuehrung():
	print("")

def koordinatenEingabe():
	laengengrad = 0
	breitengrad = 0
	eingabeRichtig = False
	while not eingabeRichtig:
		try:
			laengengrad = float(input("Geben Sie einen Längengrad ein: "))
			breitengrad = float(input("Geben Sie einen Breitengrad ein: "))
			eingabeRichtig = True 
		except:
			print("Die Eingabe war fehlerhaft, versuchen Sie es bitte erneut.")
			eingabeRichtig = False
	return (laengengrad, breitengrad)

def brueckenEinlesen():
	dateipfad = "./Zustandsnoten Fernstraßenbrücken 2020-09.csv"
	with open(file=dateipfad, mode="r", encoding="utf-8") as datei:
		bruecken = [bruecke.rstrip() for bruecke in datei.readlines()]
	return bruecken

def spaltenNamen(bruecken):
	kopfzeile = bruecken[0].split("\t")

	NAME_INDEX = kopfzeile.index("Bauwerksname")
	ORT_INDEX = kopfzeile.index("Ort")
	ZN_INDEX = kopfzeile.index("ZN")
	GML_INDEX = kopfzeile.index("Google Maps Link")
	NB_INDEX = kopfzeile.index("NB")
	OL_INDEX = kopfzeile.index("OL")

	return [NAME_INDEX, ORT_INDEX, ZN_INDEX, GML_INDEX, NB_INDEX, OL_INDEX]

def berechneDistanzen(bruecken, kopfzeilenIndexe):
	brueckenMitDistanz = []
	for bruecke in bruecken:
		brueckenWerte = bruecke.split("\t")

		NB = float(brueckenWerte[kopfzeilenIndexe[4]].replace(",", "."))
		OL = float(brueckenWerte[kopfzeilenIndexe[5]].replace(",", "."))
		brueckeGeokoordinaten = (NB, OL)

		distanzZurBruecke = round(geodist(eigegebeneKoordinaten, brueckeGeokoordinaten), 2)
		distanzZurBruecke = str(distanzZurBruecke) + "km"
		
		brueckeAlsDict = {
			"Rang": 0,
			"Bauwerksname": brueckenWerte[kopfzeilenIndexe[0]],
			"Ort": brueckenWerte[kopfzeilenIndexe[1]],
			"Entfernung": distanzZurBruecke,
			"ZN": brueckenWerte[kopfzeilenIndexe[2]],
			"Google Maps Link": brueckenWerte[kopfzeilenIndexe[3]]
		}
		brueckenMitDistanz.append(brueckeAlsDict)
	return brueckenMitDistanz

def naechstenSiebenBruecken(eigegebeneKoordinaten, brueckenMitDistanz):
	bruecken = sorted(brueckenMitDistanz, key=lambda bruecke: bruecke["Entfernung"])[:7]
	
	rang = 0
	for bruecke in bruecken:
		rang += 1
		bruecke["Rang"] = rang
		for key in bruecke:
			print(key + ": " + str(bruecke[key]))
		print("\n")

if __name__ == "__main__":
	einfuehrung()
	eigegebeneKoordinaten = koordinatenEingabe()
	bruecken = brueckenEinlesen()
	headerIndexes = spaltenNamen(bruecken)
	del bruecken[0]
	brueckenMitDistanz = berechneDistanzen(bruecken, headerIndexes)
	naechstenSiebenBruecken(eigegebeneKoordinaten, brueckenMitDistanz)
