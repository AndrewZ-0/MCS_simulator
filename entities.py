import container
import random

#these are things that move around the rooms, like the player
class Entity():
    def __init__(self,name,virtualx,virtualy,location):
        self._name = name
        self._virtualx = virtualx
        self._virtualy = virtualy
        self._location = location # which location, as in which room/field etc
        # GUI logic for instantiating sprite here since all entities have sprites

    def getName(self):
        return self._name

    def getVirtualx(self):
        return self._virtualx

    def getVirtualy(self):
        return self._virtualy

    def getLocation(self):
        return self._location

class Wall(Entity):
    def __init__(self,name,virtualx,virtualy,location):
        super().__init__(name,virtualx,virtualy,location)
        self.__type = 0

class Interactable(Entity):
    def __init__(self,name,virtualx,virtualy,location):
        super().__init__(name,virtualx,virtualy,location)
        self._actions = [] # each action is a tuple, the first element being a string (the description of the action), the second element being a tuple of functions to be performed, the third element a tuple of tuples, each of which are the parameters for the function. i.e ("action description",(print,action),(("action is performed",),(parameter1,parameter2,parameter3)))
        # GUI logic for instantiating nametag here since all interactables have name tags

    def getActions(self):
        return self._actions

    def addAction(self,action):
        self._actions.append(action)

    def removeAction(self,action):
        self._actions.remove(action)

    def anyActions(self):
        if self._actions:
            return True

    def clearActions(self):
        self._actions = []

class Door(Interactable):
    def __init__(self,name,virtualx,virtualy,location, open, connects, motion):
        super().__init__(name, virtualx, virtualy, location)
        self.__open = open
        self.__connects = connects
        self.__motion = motion

        self.__type = 1

    def isOpen(self):
        return self.__open

    def open(self):
        self.__open = True

    def close(self):
        self.__open = False

class GivesBuffs(Interactable):
    def __init__(self,name,virtualx,virtualy,location,buffs):
        super().__init__(name,virtualx,virtualy,location)
        self.__buffs = buffs

    def getBuffs(self):
        return self.__buffs

    def hasBuff(self,buff):
        return any(i == buff for i in self.__buffs)

    def addBuff(self,buff):
        self.__buffs.append(buff)

    def removeBuff(self,buff):
        self.__buffs.remove(buff)

class Furniture(GivesBuffs):
    def __init__(self,name,virtualx,virtualy,location,buffs):
        super().__init__(name,virtualx,virtualy,location,buffs)

        self.__type = 2
class Dynamic(GivesBuffs):
    def __init__(self,name,virtualx,virtualy,location,buffs):
        super().__init__(name,virtualx,virtualy,location,buffs)
        self.__moved = False
        # GUI logic for instantiating nametag here

    def getMoved(self):
        return self.__moved

    def randomisexposition(self,min,max):
        self._virtualx = random.randint(min,max)

    def randomiseyposition(self,min,max):
        self._virtualy = random.randint(min,max)

    def changeLocation(self,newlocation):
        self._location = newlocation

class Item(Dynamic):
    def __init__(self,name,virtualx,virtualy,location,buffs):
        super().__init__(name,virtualx,virtualy,location,buffs)

        self.__type = 3

class Consumable(Item):
    def __init__(self,name,virtualx,virtualy,location,buffs):
        super().__init__(name,virtualx,virtualy,location,buffs)

class Key(Item):
    def __init__(self,name,virtualx,virtualy,location,buffs):
        super().__init__(name, virtualx, virtualy, location, buffs)

class Bag(Item):
    def __init__(self,name,virtualx,virtualy,location,buffs):
        super().__init__(name, virtualx, virtualy, location, buffs)

class Human(Dynamic):
    def __init__(self,name,virtualx,virtualy,location,buffs,sanity,subjects,mood):
        super().__init__(name,virtualx,virtualy,location,buffs)
        self._sanity = sanity
        self._subjects = subjects
        self.__defaultMood = mood
        self._inventory = []
        self._moods = {} # formatted as {entity(instance):mood(integer),entity:mood etc

    def meet(self,entity):
        self._moods[entity] = self.__defaultMood + random.randint(-2,2)

class Student(Human):
    def __init__(self,name,virtualx,virtualy,location,buffs,sanity,subjects,mood,humanities,sciences,otherPeople,popCulture,gaming,sports):
        super().__init__(name,virtualx,virtualy,location,buffs,sanity,subjects,mood)
        self.__humanitiesEnjoyment = self.__humanitiesFluency = humanities
        self.__sciences = self.__sciencesFluency = sciences
        self.__otherPeople = otherPeople
        self.__popCulture = popCulture
        self.__gaming = self.__gamingFluency = gaming
        self.__sports = self.__sportsFluency = sports

        self.__type = 4

class Player(Student):
    def __init__(self,name,virtualx,virtualy,location,buffs,sanity,subjects,mood,humanities,sciences,otherPeople,popCulture,gaming,sports):
        super().__init__(name, virtualx, virtualy, location, buffs, sanity, subjects, mood,humanities,sciences,otherPeople,popCulture,gaming,sports)
        self.__stamina = 500

class Teacher(Human):
    def __init__(self,name,virtualx,virtualy,location,buffs,sanity,subjects,mood,attack):
        super().__init__(name,virtualx,virtualy,location,buffs,sanity,subjects,mood)
        self.__attack = attack

        self.__type = 5
