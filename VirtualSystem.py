from entities import EntityHandler

class virtualSystem:
    def __init__(self):
        entities = {"wall":[],"door":[],"furniture":[],"item":[],"student":[],"teacher":[]} # global list of entities
        periodTypes = ["lesson"]

    def pause(self):
        EntityHandler.pauseEntities()

    def unpause(self):
        EntityHandler.unpauseEntities()