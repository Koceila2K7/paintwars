# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Prénom Nom: Nabil KERDOUCHE 
#  Prénom Nom: Koceila KIRECHE
import math
import random
import time

def get_team_name(t):
    return "K_N_"+str(t)  # à compléter (comme vous voulez)


i = 0
translation = 1
rotation = 0

nb_rotations = 0;
nb_step = 0;
old_rotation = -1

collerAuMur = False;
angleDroit = 0
maxStep = 20;
offsetStep = 10;
debut  = True;
direction = 1;
def step(robotId, sensors):
    global i, translation, rotation, nb_step, old_rotation, nb_rotations, angleDroit, maxStep, offsetStep, debut, direction

    # -----------------  comportement de base + pour suiveur ! -----------------
    translation = 1
    rotation = 0

    # comportement de base  0,1
    if (robotId <= -1):  # la base
        if sensors["sensor_front"]["distance"] < 1:
            rotation = 0.75 * random.choice([-1, 1])  #
        elif sensors["sensor_front_left"]["distance"] < 1:
            rotation = 0.75
        elif sensors["sensor_front_right"]["distance"] < 1:
            rotation = -0.75  # 1 - sensors["sensor_front_right"]["distance"]
        
        #si bloqué de l'avant fait marche arrière
        if ( (sensors["sensor_front"]["distance"] < 0.5 
        or sensors["sensor_front_left"]["distance"] < 0.5 
        or sensors["sensor_front_right"]["distance"] < 0.5
        or sensors["sensor_left"]["distance"] < 0.5
        or sensors["sensor_right"]["distance"] < 0.5) 

        and sensors["sensor_back"]["distance"] > 1):
            translation = -1 #marche arrière
            rotation = 0.75 * random.choice([-1, 1])


    # les suiveurs de robots  2,3,4
    if (robotId >= 0 and robotId <= 6):  # suiveur robot
        
        if (sensors["sensor_front"]["distance"] < 1 and (not sensors["sensor_front"]["isRobot"] or sensors["sensor_front"]["isSameTeam"])):
            rotation = 0.75 * random.choice([-1, 1])  #
        elif (sensors["sensor_front_left"]["distance"] < 1 and (not sensors["sensor_front"]["isRobot"] or sensors["sensor_front"]["isSameTeam"])):
            rotation = 0.75
        elif (sensors["sensor_front_right"]["distance"] < 1 and (not sensors["sensor_front"]["isRobot"] or sensors["sensor_front"]["isSameTeam"])):
            rotation = -0.75  # 1 - sensors["sensor_front_right"]["distance"]
        
        # -----------------  comportement suiveur robots -----------------
        if (sensors["sensor_front"]["isRobot"] == True or sensors["sensor_front_right"]["isRobot"] == True or
                sensors["sensor_front_left"]["isRobot"] == True):
            if (sensors["sensor_front"]["distance"] < 1 and sensors["sensor_front"]["isSameTeam"] == False):
                rotation = 0
            if (sensors["sensor_front_right"]["distance"] < 1 and sensors["sensor_front_right"]["isSameTeam"] == False):
                rotation = 0.5   #1 - sensors["sensor_front_right"]["distance"]
            if (sensors["sensor_front_left"]["distance"] < 1 and sensors["sensor_front_left"]["isSameTeam"] == False):
                rotation = -0.5
        

    # les suiveurs de murs  5
    if(robotId >6 ): # la base
        
        if sensors["sensor_front"]["distance"] < 1:
            rotation = 0.75 * random.choice([-1 , 1])#
        elif sensors["sensor_front_left"]["distance"] < 1:
            rotation = 0.75
        elif sensors["sensor_front_right"]["distance"] < 1:
            rotation = -0.75#1 - sensors["sensor_front_right"]["distance"]
        
        #-----------------  comportement suiveur mur -----------------
        if(sensors["sensor_front"]["distance"] < 1):
            if(sensors["sensor_front"]["isRobot"]==False): #mur
                rotation = 1 - sensors["sensor_front"]["distance"]
            else:
                translation = 1
                rotation = 0.75 * random.choice([-1 , 1]) #rotation = -1 * sensors["sensor_front"]["distance"]

        elif(sensors["sensor_front_right"]["distance"] < 1):
            if(sensors["sensor_front_right"]["isRobot"]==False): #mur
                rotation = 2 * sensors["sensor_front_right"]["distance"] - 1
            else: #robot
                translation = 1
                rotation = -1

        elif(sensors["sensor_front_left"]["distance"] < 1):
            if(sensors["sensor_front_left"]["isRobot"]==False): #mur
                rotation = 1 - 2 * sensors["sensor_front_left"]["distance"]
            else:
                translation = 1
                rotation = 1
    
		## comportement suivre le mur apres un angle a revoir ...
		##
		##
		##
        

    #algo génetic  6,7
    if robotId >= 50: #exclu
        #param obtenu avec genetic_algorithms
        param = [1, 1, 1, 1, 1, -1, -1, 1]
        translation = math.tanh( param[0] + param[1] * sensors["sensor_front_left"]["distance"] + param[2] * sensors["sensor_front"]["distance"] + param[3] * sensors["sensor_front_right"]["distance"]);
        rotation = math.tanh(param[4] + param[5] * sensors["sensor_front_left"]["distance"] + param[6] * sensors["sensor_front"][ "distance"] + param[7] * sensors["sensor_front_right"]["distance"]);
    i += 1

    #Tester parcours fleurs;
    #pour du moment que une rotation à -1 veut dire une rotation à 45° 
    #donc pour faire une rotation il faut faire deux rotation;
 
    if robotId == 7:
        nb_step = nb_step + 1;
        if(debut):
            if(nb_step > 10 *maxStep):
                nb_step = 0;
                debut = False;
            if(sensors["sensor_left"]["distance"] > 0.5): # Pas d'obstacle a gauche
                if(sensors["sensor_back_left"]["distance"] < 1  and  sensors["sensor_back_left"]["isRobot"]==False): # mur juste derriere a gauche
                    translation = 1
                    rotation = -1 #1 - 2 * sensors["sensor_front_left"]["distance"]
            if(sensors["sensor_right"]["distance"] > 0.5): # Pas d'obstacle a droite
                if(sensors["sensor_back_right"]["distance"] < 1  and  sensors["sensor_back_right"]["isRobot"]==False): # mur juste derriere a droite
                    translation = 1
                    rotation = 1 #1 - 2 * sensors["sensor_front_left"]["distance"]  
        else:
            translation = 1;
            rotation = 0;
            if sensors["sensor_front"]["distance"] < 1:
                rotation = 0.75 * random.choice([-1, 1])  #
            elif sensors["sensor_front_left"]["distance"] < 1:
                 rotation = 0.75
            elif sensors["sensor_front_right"]["distance"] < 1:
                rotation = -0.75
            else:
                if(angleDroit>0 and angleDroit<3):
                    nb_step = 0;
                    rotation =  direction;
                    angleDroit = angleDroit +1

                if(angleDroit == 3):
                    angleDroit = 0;
                    nb_step=0;
                    
                if(nb_step > maxStep):
                    nb_rotations = nb_rotations +1;
                    maxStep = maxStep + offsetStep;
                    if(maxStep > maxStep + 5*offsetStep):
                        maxStep = offsetStep;
                    nb_step = 0
                    if (nb_rotations > 4):
                        direction = random.choice([1,-1]);
                        rotation =  direction * 1/6
                        angleDroit = 1
                        nb_rotations = 0;
                        
                    else:
                        rotation = direction
                        angleDroit = 1;
        
        if(robotId>-1):
            if(sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False):
                translation = 1;
                rotation = 0
            if(sensors["sensor_front_left"]["isRobot"] == True and sensors["sensor_front_left"]["isSameTeam"] == False):
                translation = 1;
                rotation = -1
            if(sensors["sensor_front_right"]["isRobot"] == True and sensors["sensor_front_right"]["isSameTeam"] == False):
                translation = 1;
                rotation = 1
        
        if sensors["sensor_front"]["isRobot"] == True and sensors["sensor_front"]["isSameTeam"] == False:
            translation = 0# exemple de détection d'un robot de l'équipe adversaire (ne sert à rien)
            rotation = 0

    return translation, rotation 



"""
#essayer de suivre le mur apres un angle
        if(sensors["sensor_left"]["distance"] > 0.5): # Pas d'obstacle a gauche
            if(sensors["sensor_back_left"]["distance"] < 1  and  sensors["sensor_back_left"]["isRobot"]==False): # mur juste derriere a gauche
                translation = 1
                rotation = -1 #1 - 2 * sensors["sensor_front_left"]["distance"]
        if(sensors["sensor_right"]["distance"] > 0.5): # Pas d'obstacle a droite
            if(sensors["sensor_back_right"]["distance"] < 1  and  sensors["sensor_back_right"]["isRobot"]==False): # mur juste derriere a droite
                translation = 1
                rotation = 1 #1 - 2 * sensors["sensor_front_left"]["distance"]
	
"""


"""

    if robotId == 7:
        nb_step = nb_step+1;
        translation = 1;
        rotation = 0;

        if sensors["sensor_front_left"]["distance"] < 1 or sensors["sensor_front"]["distance"] < 1:
            rotation = 0.5
        elif sensors["sensor_front_right"]["distance"] < 1:
            rotation = -0.5
        else:
            if(debut):
                nb_step = nb_step + 1;
                if(nb_step > 3 *maxStep):
                    nb_step = 0;
                    debut = False;
            else:
                if(angleDroit>0 and angleDroit<3):
                    nb_step = 0;
                    rotation =  direction;
                    angleDroit = angleDroit +1

                if(angleDroit == 3):
                    angleDroit = 0;
                    nb_step=0;
                    
                if(nb_step > maxStep):
                    nb_rotations = nb_rotations +1;
                    maxStep = maxStep + offsetStep;
                    if(maxStep > maxStep + 5*offsetStep):
                        maxStep = offsetStep;
                    nb_step = 0
                    if (nb_rotations > 4):
                        direction == random.choice([-1,1]);
                        rotation =  direction * 1/6
                        angleDroit = 1
                        nb_rotations = 0;
                        
                    else:
                        rotation = direction
                        angleDroit = 1;
"""

"""

    if robotId == 7:
        nb_step = nb_step+1;
        translation = 1;
        rotation = 0;

        if sensors["sensor_front_left"]["distance"] < 1 or sensors["sensor_front"]["distance"] < 1:
            rotation = 0.5
        elif sensors["sensor_front_right"]["distance"] < 1:
            rotation = -0.5
        else:
            if(debut):
                nb_step = nb_step + 1;
                if(nb_step > 3 *maxStep):
                    nb_step = 0;
                    debut = False;
            else:
                if(angleDroit>0 and angleDroit<3):
                    nb_step = 0;
                    rotation =  direction;
                    angleDroit = angleDroit +1

                if(angleDroit == 3):
                    angleDroit = 0;
                    nb_step=0;
                    
                if(nb_step > maxStep):
                    nb_rotations = nb_rotations +1;
                    maxStep = maxStep + offsetStep;
                    if(maxStep > maxStep + 5*offsetStep):
                        maxStep = offsetStep;
                    nb_step = 0
                    if (nb_rotations > 4):
                        direction == random.choice([-1,1]);
                        rotation =  direction * 1/6
                        angleDroit = 1
                        nb_rotations = 0;
                        
                    else:
                        rotation = direction
                        angleDroit = 1;
   """