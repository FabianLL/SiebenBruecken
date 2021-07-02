from geodist import geodist

def introduceProgram():
	return ""

def getCoordsFromUser():
	long = 0
	lat = 0
	inputCorrect = False
	while not inputCorrect:
		try:
			long = float(input("Geben Sie einen Längengrad ein: "))
			lat = float(input("Geben Sie einen Breitengrad ein: "))
			inputCorrect = True 
		except:
			print("Die Eingabe war fehlerhaft, versuchen Sie es bitte erneut.")
			inputCorrect = False
	return (long, lat)

def readBridges():
	CSV_FILEPATH = "./Zustandsnoten Fernstraßenbrücken 2020-09.csv"
	with open(file=CSV_FILEPATH, mode="r", encoding="utf-8") as bridgesFile:
		bridges = [bridge.rstrip() for bridge in bridgesFile.readlines()]
	return bridges

def getNeededHeaderIndexes(bridges):
	HEADERS = bridges[0].split("\t")

	NAME_INDEX = HEADERS.index("Bauwerksname")
	ORT_INDEX = HEADERS.index("Ort")
	ZN_INDEX = HEADERS.index("ZN")
	GML_INDEX = HEADERS.index("Google Maps Link")
	NB_INDEX = HEADERS.index("NB")
	OL_INDEX = HEADERS.index("OL")

	return [NAME_INDEX, ORT_INDEX, ZN_INDEX, GML_INDEX, NB_INDEX, OL_INDEX]

def calculateBridgeDistances(bridges, neededHeaderIndexes):
	bridgesAsDictWithDistace = []
	for bridge in bridges:
		bridgeAttributes = bridge.split("\t")

		NB = float(bridgeAttributes[neededHeaderIndexes[4]].replace(",", "."))
		OL = float(bridgeAttributes[neededHeaderIndexes[5]].replace(",", "."))
		bridgeGeoCoords = (NB, OL)

		distanceToBridge = round(geodist(userGeoCoords, bridgeGeoCoords), 2)
		distanceToBridge = str(distanceToBridge) + "km"
		
		bridgeAsDict = {
			"Rang": 0,
			"Bauwerksname": bridgeAttributes[neededHeaderIndexes[0]],
			"Ort": bridgeAttributes[neededHeaderIndexes[1]],
			"Entfernung": distanceToBridge,
			"ZN": bridgeAttributes[neededHeaderIndexes[2]],
			"Bewertung": "/",
			"Google Maps Link": bridgeAttributes[neededHeaderIndexes[3]]
		}
		bridgesAsDictWithDistace.append(bridgeAsDict)
	return bridgesAsDictWithDistace

def getSevenNearestBridgesToUserCoords(userGeoCoords, bridgesAsDictWithDistace):
	bridges = sorted(bridgesAsDictWithDistace, key=lambda bridge: bridge["Entfernung"])[:7]
	
	rang = 0
	for bridge in bridges:
		rang += 1
		bridge["Rang"] = rang
		for key in bridge:
			print(key + ": " + str(bridge[key]))
		print("\n")

if __name__ == "__main__":
	userGeoCoords = getCoordsFromUser()
	bridges = readBridges()
	headerIndexes = getNeededHeaderIndexes(bridges)
	del bridges[0]
	bridgesAsDictWithDistace = calculateBridgeDistances(bridges, headerIndexes)
	getSevenNearestBridgesToUserCoords(userGeoCoords, bridgesAsDictWithDistace)
