from entities import EntityHandler
from locations import LocationsHandler
import json


class virtualSystem:
    def __init__(self):
        self.__entities = [] # global list of humans
        self.__periodTypes = ["lesson"]
        self.__entityHandler = EntityHandler()
        self.__locationHandler = LocationsHandler()

    def pause(self):
        self.__entityHandler.pauseEntities()

    def unpause(self):
        self.__entityHandler.unpauseEntities()

    def instantiateWall(self,name,abs_x,abs_y,location):
        self.__entityHandler.instantiateWall(name,abs_x,abs_y,location)

    def instantiateDoor(self,name,abs_x,abs_y,orientation,status,connects,motion):
        self.__entityHandler.instantiateDoor(name,abs_x,abs_y,orientation,status,connects,motion)

    def instantiateFurniture(self,name,abs_x,abs_y,location,buffs):
        self.__entityHandler.instantiateFurniture(name,abs_x,abs_y,location,buffs)

    def instantiateStudent(self,name,abs_x,abs_y,location,buffs,sanity,subjects,mood,humanities,sciences,otherPeople,popCulture,gaming,sports):
        self.__entities.append(self.__entityHandler.instantiateStudent(name,abs_x,abs_y,location,buffs,sanity,subjects,mood,humanities,sciences,otherPeople,popCulture,gaming,sports))

    def instantiateTeacher(self,name,abs_x,abs_y,location,buffs,sanity,subjects,mood,attack):
        self.__entities.append(self.__entityHandler.instantiateTeacher(name,abs_x,abs_y,location,buffs,sanity,subjects,mood,attack))

    def instantiateLocation(self,name,xwidth,ywidth,floor,xposition,yposition,exits):
        connects = []
        with json.load(open("mcs_map.json"))["exits"] as exitTable:
            for i in exits:
                for j in exitTable[i]["connects"].keys():
                    if j != name:
                        connects.append(j)
            self.__locationHandler.addLocation(name,xwidth,ywidth,floor,xposition,yposition,connects)


    def finaliseLocations(self):
        self.__locationHandler.finaliseLocations()

