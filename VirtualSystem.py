from entities import EntityHandler

class virtualSystem:
    def __init__(self):
        self.__entities = {"wall":[],"door":[],"furniture":[],"item":[],"student":[],"teacher":[]} # global list of entities
        self.__periodTypes = ["lesson"]

    def pause(self):
        EntityHandler.pauseEntities()

    def unpause(self):
        EntityHandler.unpauseEntities()

    def instantiateWall(self,name,abs_x,abs_y,location):
        self.__entities["wall"]=EntityHandler.instantiateWall(name,abs_x,abs_y,location)