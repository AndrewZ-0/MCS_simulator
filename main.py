from VirtualSystem import virtualSystem
from locations import LocationsHandler
import json

locationsHandler = LocationsHandler
system = virtualSystem()

loadedLocations = locationsHandler.getLoadedLocations()

# load CS building (potentially only building in early game
with json.load(open("mcs_map.json"))["locations"]["collin sanders"] as csBuilding:
    for location in csBuilding.items():
        system.instantiateLocation(location[0],location[1][2],location[1][3],location[1][4],location[1][5],location[1][6],location[1][7])

