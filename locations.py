class location:
    def __init__(self,name,xwidth,ywidth,floor,xposition,yposition,exits):
        self._name = name
        self._xwidth = xwidth
        self._ywidth = ywidth
        self._floor = floor
        self._xposition = xposition
        self._yposition = yposition
        self._exits = exits

        self._loaded = False

        self.entities = {"wall":[], "door":[], "furniture":[], "item":[], "student":[], "teacher":[]}

    def load(self):
        for dynamics in list(self.entities.values())[2:5]:
            for dynamic in dynamics:
                if dynamic.getmoved:
                    dynamic.randomisexposition(0,self._xwidth) # may be subject to change
                    dynamic.randomiseyposition(0,self._ywidth)
        GUIsystem.load(self) # Should be a function in GUIsystem, taking the room as an argument


    def enter(self,entity):
        self.entities[entity.getType()].append(entity)

    def leave(self,entity):
        self.entities[entity.getType()].remove(entity)
