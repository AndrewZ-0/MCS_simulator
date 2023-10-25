import container
import random
import json

settings = json.load(open("settings.json","r"))
lines = json.load(open("lines.json","r"))

#these are things that move around the rooms, like the player
class Entity():
    def __init__(self,name,abs_x,abs_y,location):
        self._name = name
        self._abs_x = abs_x
        self._abs_y = abs_y
        self._location = location # which location, as in which room/field etc
        # GUI logic for instantiating sprite here since all entities have sprites

    def getName(self):
        return self._name

    def getabs_x(self):
        return self._abs_x

    def getabs_y(self):
        return self._abs_y

    def getLocation(self):
        return self._location

    def getType(self):
        return self._type

class Wall(Entity):
    def __init__(self,name,abs_x,abs_y,location):
        super().__init__(name,abs_x,abs_y,location)
        self._type = "wall"

class Interactable(Entity):
    def __init__(self,name,abs_x,abs_y,location):
        super().__init__(name,abs_x,abs_y,location)
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
    def __init__(self,name,abs_x,abs_y,location, open, connects, motion):
        super().__init__(name, abs_x, abs_y, location)
        self.__open = open
        self.__connects = connects
        self.__motion = motion

        self._type = "door"

    def isOpen(self):
        return self.__open

    def open(self):
        self.__open = True

    def close(self):
        self.__open = False

class GivesBuffs(Interactable):
    def __init__(self,name,abs_x,abs_y,location,buffs):
        super().__init__(name,abs_x,abs_y,location)
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
    def __init__(self,name,abs_x,abs_y,location,buffs):
        super().__init__(name,abs_x,abs_y,location,buffs)

        self._type = "furniture"
class Dynamic(GivesBuffs):
    def __init__(self,name,abs_x,abs_y,location,buffs):
        super().__init__(name,abs_x,abs_y,location,buffs)
        self.__moved = False
        # GUI logic for instantiating nametag here

    def getMoved(self):
        return self.__moved

    def saveLocation(self):
        self.__moved = False

    def randomisexposition(self,min,max):
        self._abs_x = random.randint(min,max)

    def randomiseyposition(self,min,max):
        self._abs_y = random.randint(min,max)

    def changeLocation(self,newlocation):
        self._location = newlocation
        self.__moved = True

class Item(Dynamic):
    def __init__(self,name,abs_x,abs_y,location,buffs):
        super().__init__(name,abs_x,abs_y,location,buffs)

        self._type = "item"

class Consumable(Item):
    def __init__(self,name,abs_x,abs_y,location,buffs):
        super().__init__(name,abs_x,abs_y,location,buffs)

class Key(Item):
    def __init__(self,name,abs_x,abs_y,location,buffs):
        super().__init__(name, abs_x, abs_y, location, buffs)

class Bag(Item):
    def __init__(self,name,abs_x,abs_y,location,buffs):
        super().__init__(name, abs_x, abs_y, location, buffs)

class Human(Dynamic):
    def __init__(self,name,abs_x,abs_y,location,buffs,sanity,subjects,mood):
        super().__init__(name,abs_x,abs_y,location,buffs)
        self._sanity = sanity
        self._subjects = subjects
        self.__defaultMood = mood
        self._inventory = []
        self._moods = {} # formatted as {entity(instance):mood(integer),entity:mood etc

    def gainSanity(self,sanity):
        self._sanity += sanity

    def loseSanity(self,sanity):
        self._sanity -= sanity

    def meet(self,entity):
        self._moods[entity] = self.__defaultMood + random.randint(-settings["maximum displacement for default mood"],settings["maximum displacement for default mood"])

    def met(self,entity):
        if entity in self._moods.keys():
            return True
        else:
            return False

    def getMood(self,entity):
        return self._moods[entity]

    def speak(self,speach):
        if self._location.loaded():
            speach = random.choice(lines[speach])
            # GUI code for creating speach bubble

class Student(Human):
    def __init__(self,name,abs_x,abs_y,location,buffs,sanity,subjects,mood,humanities,sciences,otherPeople,popCulture,gaming,sports):
        super().__init__(name,abs_x,abs_y,location,buffs,sanity,subjects,mood)
        self.__humanitiesEnjoyment = self.__humanitiesFluency = humanities
        self.__sciencesEnjoyment = self.__sciencesFluency = sciences
        self.__otherPeopleEnjoyment = otherPeople
        self.__popCultureEnjoyment = self.__popCultureFluency = popCulture
        self.__gamingEnjoyment = self.__gamingFluency = gaming
        self.__sportsEnjoyment = self.__sportsFluency = sports

        self.__enjoyment = {"humanities":humanities,"sciences":sciences,"otherPeople":otherPeople,"popCulture":popCulture,"gaming":gaming,"sports":sports}
        self.__fluency = self.__enjoyment.copy()
        del self.__fluency["otherPeople"] # the other people fluency will be the sum of all the moods the player has to other people, so is not stored in the dictionary

        self._type = "student"

    def getFluency(self,topic):
        if topic == "otherPeople":
            return sum(self._moods.values())
        else:
            return self.__fluency[topic]

    def getEnjoyment(self,topic):
        return self.__enjoyment[topic]

    def converse(self,student,topic):

        if not self.met(student):
            self.meet(student)

        if self.getMood(student) < settings["minimum mood to converse"]:
            self.speak("refuse to converse")
            return False
        else:
            approval = settings["fluency proportion"]*student.getFluency(topic) + (1-settings["fluency proportion"])*self.getEnjoyment(topic)
            if approval >= settings["approval displacement for positive/negative reaction"]:
                self.speak(lines["converse approve"])
            elif approval <= -settings["approval displacement for positive/negative reaction"]:
                self.speak(lines["converse disapprove"])
            else:
                self.speak(lines["converse neutral"])

            self._moods[student] += approval
            self.__enjoyment[topic] -= settings["conversation fatigue"] + settings["conversation fatigue"]/5
            for enjoyment in self.__enjoyment.values():
                enjoyment += settings["conversation fatigue"]/5

            self.gainSanity(approval)
            student.gainSanity(approval)

class Player(Student):
    def __init__(self,name,abs_x,abs_y,location,buffs,sanity,subjects,mood,humanities,sciences,otherPeople,popCulture,gaming,sports):
        super().__init__(name, abs_x, abs_y, location, buffs, sanity, subjects, mood,humanities,sciences,otherPeople,popCulture,gaming,sports)
        self.__stamina = 500

class Teacher(Human):
    def __init__(self,name,abs_x,abs_y,location,buffs,sanity,subjects,mood,attack):
        super().__init__(name,abs_x,abs_y,location,buffs,sanity,subjects,mood)
        self.__attack = attack

        self._type = "teacher"
