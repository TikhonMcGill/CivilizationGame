import random
def make_decision(commands,ai,at_war,edict_length):
    if at_war==True:
        if ai==1:
            if "recruit" in commands and random.randint(1,2)==1:
                return "recruit"
            if "invade" in commands and random.randint(1,2)==1:
                return "invade"
            if "distribute to garrisons" in commands and random.randint(1,2)==1:
                return "distribute to garrisons"
            return ""
        if ai==2:
            if "recruit" in commands and random.randint(1,2)==1:
                return "recruit"
            if "invade" in commands and random.randint(1,3)<=2:
                return "invade"
            if "distribute to garrisons" in commands and random.randint(1,3)==1:
                return "distribute to garrisons"
            return ""
        if ai==3:
            if "recruit" in commands and random.randint(1,2)==1:
                return "recruit"
            if "invade" in commands and random.randint(1,5)<=4:
                return "invade"
            if "distribute to garrisons" in commands and random.randint(1,5)==1:
                return "distribute to garrisons"
            return ""
        if ai==4:
            if "recruit" in commands and random.randint(1,2)==1:
                return "recruit"
            if "invade" in commands and random.randint(1,5)==1:
                return "invade"
            if "distribute to garrisons" in commands and random.randint(1,5)<=4:
                return "distribute to garrisons"
            return ""
    else:
        if "pick focus" in commands:
            return "pick focus"
        if "research" in commands:
            return "research"
        if "issue edict" in commands and random.randint(1,1000//(edict_length+1))==1:
            return "issue edict"
        if "collect taxes" in commands and random.randint(1,10)==1:
            return "collect taxes"
        if "diplomacy" in commands and ((ai==3 and random.randint(1,5)==1) or (ai!=3 and random.randint(1,10)==1)):
            return "diplomacy"
        if ai==1:
            if "recruit" in commands and random.randint(1,10)==1:
                return "recruit"
            if "distribute to garrisons" in commands and random.randint(1,5)==1:
                return "distribute to garrisons"
            if "expand" in commands and "build" in commands:
                return random.choice(["expand","build"])
            elif "build" in commands:
                return "build"
            elif "expand" in commands:
                return "expand"
            else:
                return random.choice(commands)
        if ai==2:
            if "recruit" in commands and random.randint(1,100)<=15:
                return "recruit"
            if "distribute to garrisons" in commands and random.randint(1,100)<=15:
                return "distribute to garrisons"
            if "expand" in commands and "build" in commands:
                return random.choice(["build","expand","expand","expand"])
            elif "build" in commands:
                return "build"
            elif "expand" in commands:
                return "expand"
            else:
                return random.choice(commands)
        if ai==3:
            if "recruit" in commands and random.randint(1,4)==1:
                return "recruit"
            if "distribute to garrisons" in commands and random.randint(1,20)==1:
                return "distribute to garrisons"
            if "expand" in commands and "build" in commands:
                return random.choice(["expand","expand","expand","expand","expand","expand","expand","expand","expand","build"])
            elif "build" in commands:
                return "build"
            elif "expand" in commands:
                return "expand"
            else:
                return random.choice(commands)
        if ai==4:
            if "recruit" in commands and random.randint(1,10)==1:
                return "recruit"
            if "distribute to garrisons" in commands and random.randint(1,5)==1:
                return "distribute to garrisons"
            if "expand" in commands and "build" in commands:
                return random.choice(["expand","build","build","build","build","build","build","build","build","build"])
            elif "build" in commands:
                return "build"
            elif "expand" in commands:
                return "expand"
            else:
                return random.choice(commands)
    return ""
def edict_decision(ai,current_edict):
    possible_edicts=["Civilization Effort","Enslavement Effort","Liberation Effort","Assimilation Effort","Conversion Effort","Language Teaching","Ethnic Cleansing"]
    if current_edict!="":
        possible_edicts.remove(current_edict)
    options=[]
    if ai==1:
        priorities=["Language Teaching","Assimilation Effort","Conversion Effort","Civilization Effort","Liberation Effort","Enslavement Effort","Ethnic Cleansing"]
    if ai==2:
        priorities=["Conversion Effort","Language Teaching","Assimilation Effort","Civilization Effort","Enslavement Effort","Liberation Effort","Ethnic Cleansing"]
    if ai==3:
        priorities=["Ethnic Cleansing","Enslavement Effort","Language Teaching","Assimilation Effort","Conversion Effort","Liberation Effort","Civilization Effort"]
    if ai==4:
        priorities=["Civilization Effort","Liberation Effort","Language Teaching","Assimilation Effort","Conversion Effort","Enslavement Effort","Ethnic Cleansing"]
    options+=[priorities[0]]*7
    options+=[priorities[1]]*6
    options+=[priorities[2]]*5
    options+=[priorities[3]]*4
    options+=[priorities[4]]*3
    options+=[priorities[5]]*2
    options+=[priorities[6]]
    return random.choice(options)
