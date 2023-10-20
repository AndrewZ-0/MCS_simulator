class Container():

    def __init__(self):

        #Array containing item instances
        self.__inventory = []

    def seeInventory(self):
        pass
        # GUI logic for seeing inventory here, pass is a placeholder

    #This checks whether a type of item, such as a stapler, is in the inventory and returns the specific item instance
    def hasType(self,item):
        for i in self.__inventory:
            if i.getName() == item:
                return i
        return False

    #This checks whether a specific item, like a specific stapler, is in the inventory
    def has(self,item):
        if any(i == item for i in self.__inventory):
            return True
        else:
            return False

    def lose(self,item):
        self.__inventory.remove(item)

    def gain(self,item):
        self.__inventory.append(item)

    def drop(self,item):
        self.lose(item)
        # logic to have it enter the location though I need to see how Andrew's structured his code to do this

    def pickUp(self,item):
        self.gain(item)
        # logic to have it leave the location though I need to see how Andrew's structured his code to do this

    # This returns the raw array
    def getInventory(self):
        return self.__inventory

    # checks if inventory is empty
    def isEmpty(self):
        if not self.__inventory:
            return True
        else:
            return False
