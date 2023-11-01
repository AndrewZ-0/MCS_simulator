import entities

class virtualSystem:
    def __init__(self):
        entities = {"wall":[],"door":[],"furniture":[],"item":[],"student":[],"teacher":[]} # global list of entities
        periodTypes = ["lesson"]

    def pause(self):
        entities.pauseEntities()

    def unpause(self):
        entities.unpauseEntities()

    def load(self,):