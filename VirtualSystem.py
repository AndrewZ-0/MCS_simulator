from entities import EntityHandler

class virtualSystem:
    def __init__(self):
        self.__entities = [] # global list of humans
        self.__periodTypes = ["lesson"]

    def pause(self):
        EntityHandler.pauseEntities()

    def unpause(self):
        EntityHandler.unpauseEntities()

    def instantiateWall(self,name,abs_x,abs_y,location):
        EntityHandler.instantiateWall(name,abs_x,abs_y,location)

    def instantiateDoor(self,name,abs_x,abs_y,orientation,status,connects,motion):
        self.__entities["door"].append(EntityHandler.instantiateDoor(name,abs_x,abs_y,orientation,status,connects,motion))


