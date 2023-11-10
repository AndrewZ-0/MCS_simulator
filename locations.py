loadedLocations = []
locations = []

class location:
    def __init__(self,name,xwidth,ywidth,floor,xposition,yposition,connects):
        self._name = name
        self._xwidth = xwidth
        self._ywidth = ywidth
        self._floor = floor
        self._xposition = xposition
        self._yposition = yposition
        self._connects = connects

        self.entities = {"wall":[], "door":[], "furniture":[], "item":[], "student":[], "teacher":[]}

    def load(self):
        for nondynamics in list(self.entities.values())[0:3]:
            for nondynamic in nondynamics:
                nondynamic.load()

        for dynamics in list(self.entities.values())[3:6]:
            for dynamic in dynamics:
                if dynamic.getmoved():
                    dynamic.randomisexposition(0,self._xwidth) # may be subject to change
                    dynamic.randomiseyposition(0,self._ywidth)
                dynamic.load()

        loadedLocations.append(self)

    def unload(self):
        for dynamics in list(self.entities.values())[2:5]:
            for dynamic in dynamics:
                dynamic.saveLocation()
        loadedLocations.remove(self)

    def enter(self,entity):
        self.entities[entity.getType()].append(entity)

    def leave(self,entity):
        self.entities[entity.getType()].remove(entity)

    def getName(self):
        return self._name

    def finaliseLocation(self):
        global locations

        for i,name in enumerate(self._connects):
            for pointer in locations:
                if pointer.getName == name:
                    self._connects[i] = pointer


class LocationsHandler:
    def __init__(self):
        pass

    def getLoadedLocations(self):
        return loadedLocations

    def getLocations(self):
        return locations

    def addLocation(self,name,xwidth,ywidth,floor,xposition,yposition,connects):
        global locations
        locations.append(location(name,xwidth,ywidth,floor,xposition,yposition,connects))

    def finaliseLocations(self):
        global locations

        for i in locations:
            i.finaliseLocation()
