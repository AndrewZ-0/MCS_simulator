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

class LocationsHandler:
    def __init__(self):
        pass

    def getLoadedLocations(self):
        return loadedLocations

    def getLocations(self):
        return locations
