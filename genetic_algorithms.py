# UE IA & JEUX - L3, SU
# TP "comportement réactif"
#
# Nicolas Bredeche
# 2021-03-31

from pyroborobo import Pyroborobo, Controller, AgentObserver, WorldObserver, CircleObject, SquareObject, MovableObject
# from custom.controllers import SimpleController, HungryController
import numpy as np
import random
import math
import statistics
import paintwars_arena

rob = 0

# =-=-=-=-=-=-=-=-=-= NE RIEN MODIFIER *AVANT* CETTE LIGNE =-=-=-=-=-=-=-=-=-=

simulation_mode = 1 # Simulation mode: realtime=0, fast=1, super_fast_no_render=2 -- pendant la simulation, la touche "d" permet de passer d'un mode à l'autre.

posInit = (400,400)
param = []
evaluations = 10
bestDistance =0
bestParam=[]
bestIteration = 0
i = 0
listeDist = []
bestComportement =0
parent = False
enfant = False
scr =0

def step(robotId, sensors, position):
    mu = 1
    la = 1
    global param, bestDistance, bestParam, i, listeDist,bestComportement,parent, enfant , scr, arene
    dist=0
    # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
    # Remarques:
    # - l'évaluation est ici la distance moyenne parcourue, mais on peut en imaginer d'autres
    # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
    # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres
    # toutes les 400 itérations: le robot est remis au centre de l'arène avec une orientation aléatoire
    #for i in range(evaluations):
    if rob.iterations % 400 == 0 :
            if rob.iterations > 0:
                    #print("param parent = ", bestParam)

                    dist = math.sqrt( math.pow( posInit[0] - position[0], 2 ) + math.pow( posInit[1] - position[1], 2 ) )
                    listeDist.append(dist)
                    if i%3 == 0:
                        #print("listedist = ",listeDist)
                        sommeComportement=sum(listeDist)
                        listeDist.clear()
                        #print("somme = ",sommeComportement )
                        param = []
                        for i in range(0, 8):
                            param.append(random.randint(-1, 1))

            else: #la 1ere iteration
                param = []
                for i in range(0, 8):
                    param.append(random.randint(-1, 1))


                '''
             if rob.iterations % 800 == 0 : # comparer enf parent... SAUF LA 1ERE FOIS
                 if(bestDistance<dist):
                     param=enfant
                     bestDistance=dist
                    
            '''
            rob.controllers[robotId].set_position(posInit[0], posInit[1])
            rob.controllers[robotId].set_absolute_orientation(random.randint(0, 90))
            i=i+1

    if bestDistance<dist :
        bestDistance=dist
        bestParam=param
        bestIteration=rob.iterations
        enfant = True
        #print ("bestiteration ",bestIteration)
        print("bestdist =",bestDistance)
        paramenfant = bestParam
        print("====>PARAMS= ",bestParam)

    if (enfant == True):
        if paramenfant[0] == 0:
            paramenfant[0] = 1
        elif paramenfant[0] == 1:
            paramenfant[0] = 0
        elif paramenfant[0] == -1:
            paramenfant[0] = 0
        enfant = False
        param = paramenfant
    #print("posrinit", position)
    if rob.iterations == 0:
        arene = np.copy(arena)

    somme =scoreEnvironnement(arene,position,robotId)
    #print("somme = ",somme)


    # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
    translation = math.tanh(param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"]);
    rotation = math.tanh(param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"]["distance"] + param[7] * sensors["sensor_front_right"]["distance"]);

    scr += score(translation,rotation)
    #print("score = ",scr)
    return translation, rotation



def score(translation,rotation):
    return translation * (1-abs(rotation))


#copier l'arene avant d'utiliser la fonction
#robotId != 0
def scoreEnvironnement(arene,position, robotId, arene_x = 27, arene_y = 27):

    index_x= int(position[0]//arene_x)
    #print("inedx_x =",index_x)

    index_y= int (position[1]//arene_y)
    #print("inedx_y =",index_y)
    if index_x >26 :
        index_x= 26
    if index_y >26:
        index_y=26


    arene[index_x][index_y] = -1 * robotId
    somme = 0
    for i in range (arene_x):
        for j in range (arene_y):
            #robotId = 0 inclus
            if arene[i][j] <= 0 :
                somme += 1
    return somme



# =-=-=-=-=-=-=-=-=-= NE RIEN MODIFIER *APRES* CETTE LIGNE =-=-=-=-=-=-=-=-=-=


number_of_robots = 1  # 8 robots identiques placés dans l'arène

arena = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

offset_x = 36
offset_y = 36
edge_width = 28
edge_height = 28


class MyController(Controller):

    def __init__(self, wm):
        super().__init__(wm)

    def reset(self):
        return

    def step(self):

        sensors = {}

        sensors["sensor_left"] = {"distance": self.get_distance_at(0)}
        sensors["sensor_front_left"] = {"distance": self.get_distance_at(1)}
        sensors["sensor_front"] = {"distance": self.get_distance_at(2)}
        sensors["sensor_front_right"] = {"distance": self.get_distance_at(3)}
        sensors["sensor_right"] = {"distance": self.get_distance_at(4)}
        sensors["sensor_back_right"] = {"distance": self.get_distance_at(5)}
        sensors["sensor_back"] = {"distance": self.get_distance_at(6)}
        sensors["sensor_back_left"] = {"distance": self.get_distance_at(7)}

        translation, rotation = step(self.id, sensors, self.absolute_position)

        self.set_translation(translation)
        self.set_rotation(rotation)

    def check(self):
        # print (self.id)
        return True


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class MyAgentObserver(AgentObserver):
    def __init__(self, wm):
        super().__init__(wm)
        self.arena_size = Pyroborobo.get().arena_size

    def reset(self):
        super().reset()
        return

    def step_pre(self):
        super().step_pre()
        return

    def step_post(self):
        super().step_post()
        return


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class MyWorldObserver(WorldObserver):
    def __init__(self, world):
        super().__init__(world)
        rob = Pyroborobo.get()

    def init_pre(self):
        super().init_pre()

    def init_post(self):
        global offset_x, offset_y, edge_width, edge_height, rob

        super().init_post()

        for i in range(len(arena)):
            for j in range(len(arena[0])):
                if arena[i][j] == 1:
                    block = BlockObject()
                    block = rob.add_object(block)
                    block.soft_width = 0
                    block.soft_height = 0
                    block.solid_width = edge_width
                    block.solid_height = edge_height
                    block.set_color(164, 128, 0)
                    block.set_coordinates(offset_x + j * edge_width, offset_y + i * edge_height)
                    retValue = block.can_register()
                    # print("Register block (",block.get_id(),") :", retValue)
                    block.register()
                    block.show()

        counter = 0
        for robot in rob.controllers:
            x = 260 + counter*40
            y = 400
            robot.set_position(x, y)
            counter += 1

    def step_pre(self):
        super().step_pre()

    def step_post(self):
        super().step_post()


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class Tile(SquareObject):  # CircleObject):

    def __init__(self, id=-1, data={}):
        super().__init__(id, data)
        self.owner = "nobody"

    def step(self):
        return

    def is_walked(self, id_):
        return


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class BlockObject(SquareObject):
    def __init__(self, id=-1, data={}):
        super().__init__(id, data)

    def step(self):
        return

    def is_walked(self, id_):
        return


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def main():
    global rob

    rob = Pyroborobo.create(
        "config/paintwars.properties",
        controller_class=MyController,
        world_observer_class=MyWorldObserver,
        #        world_model_class=PyWorldModel,
        agent_observer_class=MyAgentObserver,
        object_class_dict={}
        ,override_conf_dict={"gInitialNumberOfRobots": number_of_robots, "gDisplayMode": simulation_mode}
    )

    rob.start()

    rob.update(1000000)
    rob.close()

if __name__ == "__main__":
    main()
