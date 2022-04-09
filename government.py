from province import *
from population import *
import copy
from funcs import *
from PIL import Image
import random
import AI
omniscience=False
edicts=["Civilization Effort","Enslavement Effort","Liberation Effort","Assimilation Effort","Conversion Effort","Language Teaching","Ethnic Cleansing"]
class Relation:
    curid=0
    relations={}
    def __init__(self,country1,country2):
        self.country1=country1
        self.country2=country2
        self.points=[]
        self.length=0
        self.id=Relation.curid
        Government.governments[country1].relations.append(self.id)
        Government.governments[country2].relations.append(self.id)
        Relation.curid+=1
        Relation.relations[self.id]=self
class War:
    curid=0
    wars={}
    def __init__(self,side1,side2):
        self.side1=side1
        self.side2=side2
        self.points1=[]
        self.points2=[]
        self.id=War.curid
        for s in side1:
            Government.governments[s].wars.append(self.id)
            self.points1.append(0)
        for s in side2:
            Government.governments[s].wars.append(self.id)
            self.points2.append(0)
        self.occupied_territories=[]
        self.name=""
        War.curid+=1
        War.wars[self.id]=self
    def increase_points(self,country,amount):
        if country in self.side1:
            self.points1[self.side1.index(country)]+=amount
        if country in self.side2:
            self.points2[self.side2.index(country)]+=amount
    def check(self):
        dead1=True
        dead2=True
        for s in self.side1:
            if s in list(Government.governments.keys()):
                if Government.governments[s].capitulated!=True:
                    dead1=False
                    break;
            else:
                self.side1.remove(s)
        for s in self.side2:
            if s in list(Government.governments.keys()):
                if Government.governments[s].capitulated!=True:
                    dead2=False
                    break;
            else:
                self.side2.remove(s)
        if dead1==True:
            self.peace_conference(self.side2,self.side1)
        elif dead2==True:
            self.peace_conference(self.side1,self.side2)
    def peace_conference(self,winners,losers):
        occupied=[] #This is a list of all territories which have been occupied in the war. This is useful if, say, a country takes part in two different wars and has its territories split
        #between the different unrelated enemies. This list prevents one country from demanding territories occupied by a completely different country in a different war.
        demanding=[] #This is the list of countries making demands, and may be reduced in size if a country exhausts all its demands/runs out of "points"
        demandable=[] #This is the list of countries receiving demands, and may be reduced in size if a country is fully annexed or vassalised
        if winners==self.side1:
            points=self.points1
        else:
            points=self.points2
        for w in winners:
            if w in list(Government.governments.keys()):
                Government.governments[w].capitulated=False
                Government.governments[w].wars.remove(self.id)
                demanding.append([w,points[winners.index(w)]])
                if Government.governments[w].research[6]==False:
                    Government.governments[w].manpower+=Government.governments[w].soldiers
                    Government.governments[w].soldiers=0
                    for t in Government.governments[w].territories:
                        if nProvince.provinces[t].garrison>0:
                            Government.governments[w].manpower+=nProvince.provinces[t].garrison
                            nProvince.provinces[t].garrison=0
        for l in losers:
            if l in list(Government.governments.keys()):
                Government.governments[l].capitulated=False
                Government.governments[l].wars.remove(self.id)
                demandable.append(l)
                if Government.governments[l].research[6]==False:
                    Government.governments[l].manpower+=Government.governments[l].soldiers
                    Government.governments[l].soldiers=0
                    for t in Government.governments[l].territories:
                        if nProvince.provinces[t].garrison>0:
                            Government.governments[l].manpower+=nProvince.provinces[t].garrison
                            nProvince.provinces[t].garrison=0
        for o in self.occupied_territories:
            Government.governments[o[2]].take_territory(o[0],True)
            if o[2] in losers and o not in occupied:
                occupied.append(o[0])
        for d in range(len(demanding)):
            points=demanding[d][1]
            if Government.governments[demanding[d][0]].is_vassal==True:
                for d2 in range(len(demanding)):
                    if demanding[d2][0]==Government.governments[demanding[d][0]].master:
                        demanding[d2][1]+=points
                        demanding[d][1]=0
                        break;
        annexable={} #This is a dictionary holding all possible provinces each winner can annex in the peace conference
        vassalisable={} #This dictionary holds all possible countries each winner can vassalise in the peace conference
        result=[] #This is the list of all results of the peace conference.
        for d in demanding:
            annexable[d[0]]=[]
            vassalisable[d[0]]=[]
            for d2 in demandable:
                totalcost=0
                for t in Government.governments[d2].territories:
                    totalcost+=nProvince.provinces[t].building_slots
                    if d[1]>=nProvince.provinces[t].building_slots and t in occupied and Government.governments[d[0]].reachable(t)==True:
                        annexable[d[0]].append(t)
                if d[1]>=totalcost and len(Government.governments[d2].wars)<1: #This makes sure that you can't vassalise a country that is at war with a different country
                    vassalisable[d[0]].append(d2)
        while len(demanding)>0 and len(demandable)>0:
            for d in demandable:
                if len(Government.governments[d].territories)<1:
                    demandable.remove(d)
            for d in demanding:
                for a in annexable[d[0]]:
                    if d[1]<nProvince.provinces[a].building_slots or a not in occupied:
                        annexable[d[0]].remove(a)
                for v in vassalisable[d[0]]:
                    if v in demandable:
                        pass
                    else:
                        vassalisable[d[0]].remove(v)
                if len(vassalisable[d[0]])<1 and len(annexable[d[0]])<1:
                    demanding.remove(d)
            for d in demanding:
                commands=["finish"]
                if len(annexable[d[0]])>0:
                    commands.append("annex")
                if len(vassalisable[d[0]])>0:
                    commands.append("vassalise")
                state=Government.governments[d[0]].state
                if state==0:
                    print("We have won "+self.name+"! It is now time for us to make demands.")
                    for c in commands:
                        print(c)
                    done=False
                    command=""
                    while command not in commands:
                        command=input("Enter your command:")
                else:
                    if state==4 and "vassalise" in commands:
                        command="vassalise"
                    else:
                        if "annex" in commands:
                            command="annex"
                        else:
                            command="finish"
                if command=="annex":
                    if state==0:
                        choice=Government.governments[d[0]].pick_province(annexable[d[0]],True)
                    else:
                        choice=random.choice(annexable[d[0]])
                    if choice!=None:
                        Government.governments[d[0]].take_territory(choice,True)
                        result.append("The "+nProvince.provinces[choice].name+" province was ceded to "+Government.governments[d[0]].name+".")
                        demanding[demanding.index(d)][1]-=nProvince.provinces[choice].building_slots
                        if choice in occupied:
                            occupied.remove(choice)
                if command=="vassalise":
                    if state==0:
                        options={}
                        choices=vassalisable[d[0]]
                        for c in choices:
                            options[Government.governments[c].name]=c
                        done=False
                        while done==False:
                            choice=input("Enter which country you want to vassalise(enter \"show *country*\" to draw the country in relation to yours on the map, or enter cancel to cancel):")
                            for o in options:
                                if o in choice:
                                    if "show" in choice:
                                        img=Image.new("RGB",(width,height),(175,175,175))
                                        pixels=img.load()
                                        for t1 in Government.governments[d[0]].territories:
                                            for t2 in nProvince.provinces[t1].territories:
                                                pixels[t2[0],t2[1]]=Government.governments[d[0]].color
                                        for t2 in Government.governments[options[o]].territories:
                                            for t3 in nProvince.provinces[t2].territories:
                                                pixels[t3[0],t3[1]]=Government.governments[options[o]].territories
                                        img.show()
                                        del(img)
                                        del(pixels)
                                    else:
                                        done=True
                            if choice=="cancel":
                                choice=None
                                done=True
                    else:
                        choice=random.choice(vassalisable[d[0]])
                    if choice!=None:
                        if state==0:
                            choice=options[o]
                        relation=Government.get_relation(d[0],choice)
                        if relation!=None:
                            del(Relation.relations[relation])
                        obligation=Relation(d[0],choice)
                        obligation.points.append(8)
                        demandable.remove(choice)
                        totpoints=0
                        Government.governments[choice].master=d[0]
                        Government.governments[choice].is_vassal=True
                        for t in Government.governments[choice].territories:
                            if t in occupied:
                                occupied.remove(t)
                            totpoints+=nProvince.provinces[t].building_slots
                        demanding[demanding.index(d)][1]-=totpoints
                if command=="finish":
                    demanding.remove(d)
        if len(result)>0:
            print("Results of "+self.name+" peace conference:")
            for o in result:
                print(o)
        del(War.wars[self.id])
        del(self)
class Government:
    governments={}
    curid=0
    colors=[]
    victorious=False
    def vassalisation_color(color):
        col=(color[0]+random.randint(25,30),color[1]+random.randint(25,30),color[2]+random.randint(25,30))
        Government.colors.append(col)
        return col
    def largest_force(self):
        #This determines the largest force a country is capable of having. In other words, this limits a country from unfairly invading with a massive army. The limit a country can have
        #will increase by 100 soldiers per level of military technology. With "professional army" researched, this maximum will be added onto 10,000.
        max_soldiers=self.research_levels[0]*100
        if self.research[6]==True:
            max_soldiers+=10000
        if self.soldiers>max_soldiers:
            return max_soldiers
        else:
            return self.soldiers
    def reachable(self,province):
        if nProvince.provinces[province].sea!=False:
            for t in self.territories:
                if nProvince.provinces[t].true_owner==self.id and t in self.cores:
                    if (nProvince.provinces[t].sea==nProvince.provinces[province].sea) and compute_distance(nProvince.provinces[province].territories[0],nProvince.provinces[t].territories[0])<=self.naval_range:
                        return True
        for t in self.territories:
            if province in nProvince.provinces[t].neighbors and nProvince.provinces[t].true_owner==self.id and t in self.cores:
                return True
    def pick_province(self,choices,show_owners):
        #This little function basically allows a player to pick a specific territory, and be able to see it on a map.
        if self.state==0:
            options={}
            for c in choices:
                options[nProvince.provinces[c].name]=c
            for o in list(options.keys()):
                if show_owners==False:
                    print(o)
                else:
                    if nProvince.provinces[options[o]].owner!=None:
                        print(o+" - Controlled by "+Government.governments[nProvince.provinces[options[o]].owner].name)
                    else:
                        print(o)
            done=False
            while done==False:
                option=input("Enter the province you want to pick(or enter \"show *province name*\" to show it on the map, or enter \"random\" to pick a random choice):")
                for o in list(options.keys()):
                    if o in option:
                        if "show" in option:
                            self.draw_province(options[o])
                        else:
                            return options[o]
                if "random" in option:
                    return random.choice(choices)
                if "cancel" in option:
                    return None
        else:
            return random.choice(choices)
    def combat(country1,country2,naval,territory):
        #In "combat", it is determined whether an attacking country(country1) will occupy the territory it is invading(territory), or be driven back by the defending country(country2)
        #Naval is a boolean. It basically determines whether the country attacks from the sea or from neighboring land. If it attacks from the sea, due to such an attack being less
        #effective, it will have 50% less ability in fighting. However, if the attacking country has the "naval" expansion type, this penalty becomes 75%, as this country would be more
        #adept at fighting from the sea, but still slightly ineffective when having to invade from the sea.
        strength1=0
        strength2=0
        #The above 2 variables determine the relative strengths of the nations.
        sent_soldiers=Government.governments[country1].largest_force()
        strength1+=int(sent_soldiers**(1/2))
        strength2+=int((nProvince.provinces[territory].garrison)**(1/2))
        #Notice how the above strengths are square rooted and rounded. This means that a SLIGHT numerical advantage may not necessarily mean success for either side.
        if Government.governments[country1].research[6]==True:
            strength1=strength1*2
        if Government.governments[country2].research[6]==True:
            strength2=strength2*2
        #As seen above, if the fighting countries have "professional army" researched, their army strength will double.
        strength1+=Government.governments[country1].combat_bonus
        strength2+=Government.governments[country2].combat_bonus
        #As seen above, for each point of the "combat_bonus" variable, which can be increased by level of military technology or picking the "Conquest" National Focus, the country's
        #"strength" increases by 1
        if naval==True:
            if Government.governments[country1].expansion_type==0:
                strength1=int(strength1*0.75)
            else:
                strength1=strength1//2
        if strength1>=int(strength2*1.5):
            #The invading country's strength needs to be at least 50% greater than the defending country's for this to be considered a victorious invasion.
            try:
                survivors=random.randint(0,int(nProvince.provinces[territory].garrison/(strength1/strength2)))
                #Some of the garrison will inevitably survive and join up with the defending government's standing army.
            except (ValueError,ZeroDivisionError):
                survivors=0
            if survivors>nProvince.provinces[territory].garrison:
                survivors=nProvince.provinces[territory].garrison
            try:
                killed=int(((nProvince.provinces[territory].garrison-survivors)/(strength1/strength2)))
            except ZeroDivisionError:
                killed=0
            killed+=Government.governments[country2].combat_bonus
            if killed<0:
                killed=0
            #As seen above, the greater the ratio of the attacker's strength to the defender's strength, the LESS attacking soldiers will be lost.
            if survivors>0:
                Government.governments[country2].send_message("We have been successfully invaded by "+Government.governments[country1].name+"! They occupied the province of "+nProvince.provinces[territory].name+"! However, "+str(survivors)+" surviving soldiers in the garrison there have escaped and joined up with our standing army!")
                Government.governments[country2].soldiers+=survivors
                nProvince.provinces[territory].garrison=0
            if killed>sent_soldiers:
                killed=sent_soldiers
            Government.governments[country1].send_message("We have successfully invaded and occupied "+nProvince.provinces[territory].name+", previously controlled by "+Government.governments[country2].name+"! The surviving soldiers garrisoned there fled in fear of our great army! However, we unfortunately lost "+str(killed)+" troops in the struggle.")
            Government.governments[country1].soldiers-=killed
            Government.governments[country1].take_territory(territory,False)
            try:
                Government.governments[country1].research_progress[0]+=(strength1/strength2)
            except ZeroDivisionError:
                Government.governments[country1].research_progress[0]+=2
            #The combat victory gives the winning country research progress toward military technology. This leads to one conclusion - if you want to have a strong military, you need to
            #fight more battles!
        else:
            #If the invading country's strength isn't at least 50% greater, the invader loses the battle.
            try:
                ratio=strength2/strength1
            except:
                ratio=1
            survivors=random.randint(0,int(sent_soldiers/ratio))
            if survivors>sent_soldiers:
                survivors=sent_soldiers
            killed=int((nProvince.provinces[territory].garrison)/ratio)
            killed+=Government.governments[country1].combat_bonus
            if killed>nProvince.provinces[territory].garrison:
                killed=nProvince.provinces[territory].garrison
            Government.governments[country1].send_message("Our invasion of "+Government.governments[country2].name+"-controlled "+nProvince.provinces[territory].name+" was unsuccessful, and of the "+str(sent_soldiers)+" we sent, "+str(survivors)+" survived.")
            if survivors>sent_soldiers:
                survivors=sent_soldiers
            Government.governments[country1].soldiers-=sent_soldiers
            Government.governments[country1].soldiers+=survivors
            if ratio!=1:
                Government.governments[country2].research_progress[0]+=ratio
            else:
                Government.governments[country2].research_progress[0]+=0.1
            nProvince.provinces[territory].garrison-=killed
            Government.governments[country2].send_message("The province of "+nProvince.provinces[territory].name+" was invaded by "+Government.governments[country1].name+", but our garrison drove them off. Unfortunately, in the fight, we lost "+str(killed)+" soldiers from the garrison.")        
    def get_war(country1,country2):
        for w in Government.governments[country1].wars:
            if w in Government.governments[country2].wars:
                return w
        return None
    def gencol():
        col=(random.randint(100,255),random.randint(100,255),random.randint(100,255))
        while col in Government.colors:
            col=(random.randint(100,255),random.randint(100,255),random.randint(100,255))
        Government.colors.append(col)
        return col
    def collapse(self):
        if len(self.wars)<1:
            if self.id in list(Government.governments.keys()):
                print(self.name+" has collapsed!")
                for t in self.territories:
                    nProvince.provinces[t].owner=None
                    nProvince.provinces[t].true_owner=None
                    for p in nProvince.provinces[t].population:
                        population_unit.population_units[p].overlord=None
                for r in list(Relation.relations.keys()):
                    if self.id==Relation.relations[r].country1 or self.id==Relation.relations[r].country2:
                        del(Relation.relations[r])
                del(Government.governments[self.id])
                del(self)
    def get_relation_type(self,actpas,typ):
        #Pasact is an argument determining whether the Country is passive or active in this relationship(i.e. if e.g. they are the ones paying or receiving tribute etc.)
        #0 means the country is active in this diplomatic relation(e.g. the ones receiving tribute), 1 means the country is passive in this diplomatic relation(e.g. the ones giving tribute)
        output=[]
        for r in self.relations:
            if r in list(Relation.relations.keys()):
                rel=Relation.relations[r]
                if (rel.country1==self and pasact==0 and typ in rel.points) or (rel.country2==self and pasact==1 and typ in rel.points):
                    output.append(r)
            else:
                self.relations.remove(r)
        if len(output)>0:
            return output
        return None
    def get_relation(country1,country2):
        for r in list(Relation.relations.keys()):
            rel=Relation.relations[r]
            if ((rel.country1==country1 and rel.country2==country2) or (rel.country1==country2 and rel.country2==country1)):
                return r
        return None
    def accept(focus1,state2,message,rel1,rel2,cul1,cul2):
        if state2==0:
            print("A country that is "+["aiming for a cultural victory","aiming for a religious victory","aiming for a conquest victory","aiming for a scientific victory"][focus1]+" has a request.")
            response=""
            response=input(message)
            if "ye" in response:
                return True,""
            else:
                return False,""
        else:
            if focus1==2 and state2==3:
                reason="They, like us, are a nation of conquest. Therefore, they do not want to negotiate with their potential rivals for world dominance."
                return False,reason
            if focus1==1 and state2==2 and rel1!=rel2:
                reason="They are of a different religion to us, and therefore see us as heathens. They will therefore not negotiate."
                return False,reason
            if focus1==1 and state2==3 and rel1!=rel2:
                reason="They, as a nation bent on conquest, see our religious zeal as a threat to their world dominance. Therefore, they do not wish to negotiate."
                return False,reason
            if focus1==0 and state2==1 and cul1!=cul2:
                reason="They, though wanting to spread their culture like us, see us as a threat to their own culture's spread. Therefore, they do not wish to negotiate."
                return False,reason
            return True,""
    def connected_by_sea(self,province):
        #This function makes sure that it's actually possible to reach a province by sea.
        #I added this on 04/18/2020 because I found that a lot of countries invade far away from their own territories, and, despite checking whether or not they neighbor the province,
        #They still invade incorrectly from the sea(e.g. one time Rome, solely based in the Mediterranean, somehow invaded a part of Greece which was a shore of the Caspian sea.
        if nProvince.provinces[province].sea!=False:
            for t in self.territories:
                if nProvince.provinces[t].sea==nProvince.provinces[province].sea:
                    return True
        return False
    def invade(self):
        options=[]
        for d in self.discovered:
            if d not in self.territories and nProvince.provinces[d].owner!=None:
                if Government.get_war(self.id,nProvince.provinces[d].owner)!=None and Government.get_war(self.id,nProvince.provinces[d].true_owner)!=None:
                    options.append(d)
        if len(options)>0:
            if self.state!=0:
                final=[]
                for o in options:
                    if (self.is_neighbor(o)==False and self.connected_by_sea(o)==True) and random.randint(1,15)==True:
                        final.append(o)
                    elif self.is_neighbor(o)==True:
                        final.append(o)
                if len(final)>0:
                    return random.choice(final)
            else:
                print("Here are the enemy provinces we may choose to invade:")
                return self.pick_province(options,True)
        return None
    def expand(self):
        posses=[]
        for d in self.discovered:
            if d not in self.territories and nProvince.provinces[d].owner==None and self.reachable(d)==True:
                posses.append(d)
        if self.state!=0:
            options=[]
            for p in posses:
                if self.expansion_type==0:
                    if nProvince.provinces[d].sea!=False or random.randint(1,2)==1:
                        options.append(p)
                else:
                    if nProvince.provinces[d].sea==False or (random.randint(1,5)==1):
                        options.append(p)
            if len(options)>0:
                return random.choice(options)
        else:
            if len(posses)>0:
                print("Here are the territories we can expand into:")
                choice=self.pick_province(posses,False)
                return choice
    def take_territory(self,province,peacefully):
        if nProvince.provinces[province].owner==None:
            nProvince.provinces[province].true_owner=self.id
        else:
            g=nProvince.provinces[province].owner
            if peacefully==False:
                if len(self.wars)>0 and len(Government.governments[g].wars)>0:
                    wr=Government.get_war(self.id,g)
                    if wr!=None:
                        Government.governments[g].territories.remove(province)
                        if province in Government.governments[g].cores:
                            Government.governments[g].cores.remove(province)
                        if len(Government.governments[g].territories)<1:
                            Government.governments[g].capitulated=True
                            War.wars[wr].increase_points(self.id,50)
                        else:
                            War.wars[wr].increase_points(self.id,nProvince.provinces[province].building_slots)
                        if nProvince.provinces[province].true_owner!=self.id:
                            War.wars[wr].occupied_territories.append([province,self.id,g])
                        else:
                            for o in War.wars[wr].occupied_territories:
                                if o[0]==province:
                                    War.wars[wr].occupied_territories.remove(o)
            else:
                if self.edict!="":
                    nProvince.provinces[province].modifiers.append(self.edict)
                nProvince.provinces[province].true_owner=self.id
                Government.governments[g].territories.remove(province)
                if province in Government.governments[g].cores:
                    Government.governments[g].cores.remove(province)
        for p in nProvince.provinces[province].population:
            population_unit.population_units[p].overlord=self.id
        self.territories.append(province)
        nProvince.provinces[province].clear_edicts()
        nProvince.provinces[province].owner=self.id
    def population_info(self):
        w=Culture.cultures[self.culture]
        x=Religion.religions[self.religion]
        y=Language.languages[self.language]
        z=Ethnicity.ethnicities[self.ethnicity]
        return w,x,y,z
    def __init__(self):
        self.food=0
        self.money=0
        self.culture=""
        self.language=""
        self.ethnicity=""
        self.state=random.randint(1,4)
        self.religion=""
        self.id=Government.curid
        self.edict_length=0
        self.edict=""
        Government.curid+=1
        self.naval_range=0
        self.messages=[]
        self.focus=-1
        self.territories=[]
        self.soldiers=0
        self.research=[False,False,False,False,False,False,False]
        self.discovered=[]
        self.color=Government.gencol()
        self.research_levels=[0,0,0]
        self.research_progress=[0,0,0]
        self.assimilation_bonus=0
        self.combat_bonus=0
        self.expansion_type=0
        self.teaching_bonus=0
        self.name=""
        self.notifications=[]
        self.known_countries=[]
        self.relations=[]
        self.manpower=0
        self.capitulated=False
        self.wars=[]
        self.is_vassal=False
        self.master=None
        self.cores=[]
        Government.governments[self.id]=self
    def draw_country(self,country):
        img=Image.new("RGB",(width,height),(175,175,175))
        pixels=img.load()
        for t in self.territories:
            for p in nProvince.provinces[t].territories:
                pixels[p[0],p[1]]=self.color
        for t in Government.governments[country].territories:
            for p in nProvince.provinces[t].territories:
                pixels[p[0],p[1]]=Government.governments[country].color
        img.show()
    def draw_province(self,province):
        img=Image.new("RGB",(width,height),(175,175,175))
        pixels=img.load()
        for t in self.territories:
            for p in nProvince.provinces[t].territories:
                pixels[p[0],p[1]]=self.color
        if nProvince.provinces[province].owner==None:
            col=(0,0,0)
        else:
            col=Government.governments[nProvince.provinces[province].owner].color
            col=(col[0]-20,col[1]-20,col[2]-20)
        for p in nProvince.provinces[province].territories:
            pixels[p[0],p[1]]=col
        img.show()
    def draw_map(self,typ,fullworld,directory,iteration):
        img=Image.new("RGB",(width,height),(175,175,175))
        pixels=img.load()
        if omniscience==True or fullworld==True:
            places=list(nProvince.provinces.keys())
        else:
            places=self.discovered
        if typ==1:
            for p in places:
                proportion=0
                for p2 in nProvince.provinces[p].population:
                    if population_unit.population_units[p2].culture==self.culture:
                        proportion+=1
                try:
                    proportion=proportion/len(nProvince.provinces[p].population)
                except ZeroDivisionError:
                    proportion=0
                for j in nProvince.provinces[p].territories:
                    pixels[j[0],j[1]]=(int(255*proportion),0,0)
            img.show()
        if typ==2:
            if omniscience==True:
                places=list(nProvince.provinces.keys())
            else:
                places=self.discovered
            for p in places:
                proportion=0
                for p2 in nProvince.provinces[p].population:
                    if population_unit.population_units[p2].language==self.language:
                        proportion+=1
                try:
                    proportion=proportion/len(nProvince.provinces[p].population)
                except ZeroDivisionError:
                    proportion=0
                for j in nProvince.provinces[p].territories:
                    pixels[j[0],j[1]]=(int(255*proportion),0,0)
            img.show()
        if typ==3:
            for p in places:
                typ=nProvince.provinces[p].typ
                if typ==0:
                    col=(255,255,255)
                if typ==2:
                    col=(255,216,0)
                if typ==1:
                    col=(50,50,50)
                if typ==3:
                    col=(0,0,0)
                for t in nProvince.provinces[p].territories:
                    pixels[t[0],t[1]]=col
            if fullworld==True:
                img.save(directory+"/"+str(iteration)+".png")
            else:
                img.show()
        if typ==4:
            pixels=img.load()
            for p in places:
                if nProvince.provinces[p].owner!=None:
                    col=Government.governments[nProvince.provinces[p].owner].color
                    if p in Government.governments[nProvince.provinces[p].owner].cores:
                        pass
                    else:
                        col=(col[0]+50,col[1]+50,col[2]+50)
                else:
                    col=(200,200,200)
                for t in nProvince.provinces[p].territories:
                    pixels[t[0],t[1]]=col
            if fullworld==True:
                img.save(directory+"/"+str(iteration)+".png")
            else:
                img.show()
    def discover_territories(self):
        for t in self.territories:
            if t not in self.discovered:
                self.discovered.append(t)
            for n in nProvince.provinces[t].neighbors:
                if n not in self.discovered:
                    self.discovered.append(n)
            if nProvince.provinces[t].sea!=False:
                works=False
                for s in list(Seazone.seazones.keys()):
                    if t in Seazone.seazones[s].coasts:
                        c=random.choice(Seazone.seazones[s].coasts)
                        works=True
                        break;
                if works==True:
                    if compute_distance(nProvince.provinces[c].territories[0],nProvince.provinces[t].territories[0])<=self.naval_range:
                        if c not in self.discovered:
                            self.send_message("We just discovered a nearby coast!")
                            self.discovered.append(c)
        for t in self.discovered:
            if nProvince.provinces[t].owner!=None and nProvince.provinces[t].owner!=self.id:
                if nProvince.provinces[t].owner not in self.known_countries:
                    self.send_message("We have established contact with a new country. The country calls itself "+Government.governments[nProvince.provinces[t].owner].name+".")
                    self.known_countries.append(nProvince.provinces[t].owner)
    def is_neighbor(self,province):
        #This checks if the "province" Province ID neighbors the country by land. This is useful when checking if an invasion is naval or not.
        for t in self.territories:
            if province in nProvince.provinces[t].neighbors:
                return True
        return False
    def send_message(self,message):
        if message not in self.messages:
            self.messages.append(message)
    def analyse_research(self):
        gain=1
        self.research_progress[0]+=gain
        self.research_progress[1]+=gain
        self.research_progress[2]+=gain
        if self.research_progress[0]>=100:
            self.send_message("Our Military Technology has increased by a level!")
            self.research_levels[0]+=1
            self.research_progress[0]=0
            self.combat_bonus+=1
            self.naval_range+=5
        if self.research_progress[1]>=100:
            self.send_message("Our Bureaucratic Technology has increased by a level!")
            self.research_levels[1]+=1
            self.research_progress[1]=0
            self.teaching_bonus+=1
        if self.research_progress[2]>=100:
            self.send_message("Our Cultural Technology has increased by a level!")
            self.research_levels[2]+=1
            self.research_progress[2]=0
            self.assimilation_bonus+=1
    def compute_food(self):
        for s in self.territories:
            self.food+=int(len(nProvince.provinces[s].fertile)*(1+(0.1*nProvince.provinces[s].buildings[0])))
        self.food+=len(self.territories)*self.research_levels[1]
    def pick_population_unit(self):
        p1=random.choice(self.territories)
        return population_unit.population_units[random.choice(nProvince.provinces[p1].population)]
    def get_population(self):
        output=[]
        for t in self.territories:
            for p in nProvince.provinces[t].population:
                try:
                    if population_unit.population_units[p].typ!=4:
                        output.append(population_unit.population_units[p])
                except KeyError:
                    nProvince.provinces[t].population.remove(p)
        return output
    def switch_religion(self):
        if self.research[0]==False:
            self.religion=self.pick_population_unit().religion
        else:
            options={}
            choices=[]
            pops=self.get_population()
            for p in pops:
                ss=Religion.religions[p.religion].stats
                options[p.religion]=Religion.religions[p.religion].name+", STR "+str(ss[0])+", INV "+str(ss[1])+", ATR "+str(ss[2])+", zeal bonus of "+str(Religion.religions[p.religion].zeal)+"%"
                choices.append(str(p.religion))
            if len(choices)>0:
                if self.state==0:
                    for o in list(options.keys()):
                        print(str(o)+": "+options[o])
                    choice=input("Enter the corresponding number of the religion you want to switch to:")
                    while choice not in choices:
                        choice=input("Enter the corresponding number of the religion you want to switch to:")
                else:
                    choice=random.choice(choices)
                self.religion=int(choice)
            else:
                print("Relcol")
                self.collapse()
    def declare_war(country1,country2):
        Government.governments[country2].send_message("Be advised, leader, "+Government.governments[country1].name+" has declared war on us!")
        side1=[country1]
        side2=[country2]
        vassals1=Government.governments[country1].get_relation_type(0,8)
        vassals2=Government.governments[country2].get_relation_type(0,8)
        master1=Government.governments[country1].get_relation_type(1,8)
        master2=Government.governments[country2].get_relation_type(1,8)
        if vassals1!=None:
            for v in vassals1:
                side1.append(Relation.relations[v].country2)
        elif master1!=None:
            side1.append(Relation.relations[master1[0]].country1)
        if vassals2!=None:
            for v in vassals2:
                side2.append(Relation.relations[v].country2)
        elif master2!=None:
            side2.append(Relation.relations[master2[0]].country1)
        print(Government.governments[country1].name+" has declared war on "+Government.governments[country2].name+"!")
        w=War(side1,side2)
        w.name=("The "+Government.governments[country1].name+"-"+Government.governments[country2].name+" War")
    def switch_culture(self):
        if self.research[0]==False:
            self.culture=self.pick_population_unit().culture
        else:
            options={}
            choices=[]
            pops=self.get_population()
            for p in pops:
                ss=Culture.cultures[p.culture].stats
                options[p.culture]=Culture.cultures[p.culture].name+", STR "+str(ss[0])+", INV "+str(ss[1])+", ATR "+str(ss[2])
                choices.append(str(p.culture))
            if len(choices)>0:
                if self.state==0:
                    for o in list(options.keys()):
                        print(str(o)+": "+options[o])
                    choice=input("Enter the corresponding number of the culture you want to switch to:")
                    while choice not in choices:
                        choice=input("Enter the corresponding number of the culture you want to switch to:")
                else:
                    choice=random.choice(choices)
                self.culture=int(choice)
            else:
                print("Culcol")
                self.collapse()
    def switch_ethnicity(self):
        if self.research[0]==False:
            self.ethnicity=self.pick_population_unit().ethnicity
        else:
            options={}
            choices=[]
            pops=self.get_population()
            for p in pops:
                ss=Ethnicity.ethnicities[p.ethnicity].stats
                options[p.ethnicity]=Ethnicity.ethnicities[p.ethnicity].name+", STR "+str(ss[0])+", INV "+str(ss[1])+", ATR "+str(ss[2])
                choices.append(str(p.ethnicity))
            if len(choices)>0:
                if self.state==0:
                    for o in list(options.keys()):
                        print(str(o)+": "+options[o])
                    choice=input("Enter the corresponding number of the ethnicity you want to switch to:")
                    while choice not in choices:
                        choice=input("Enter the corresponding number of the ethnicity you want to switch to:")
                else:
                    choice=random.choice(choices)
                self.ethnicity=int(choice)
            else:
                print("Ethcol")
                self.collapse()
    def switch_language(self):
        if self.research[0]==False:
            self.language=self.pick_population_unit().language
        else:
            options={}
            choices=[]
            pops=self.get_population()
            for p in pops:
                ss=Language.languages[p.language].inv,Language.languages[p.language].atr
                options[p.language]=Language.languages[p.language].name+", INV "+str(ss[0])+", ATR "+str(ss[1])
                choices.append(str(p.language))
            if len(choices)>0:
                if self.state==0:
                    for o in list(options.keys()):
                        print(str(o)+": "+options[o])
                    choice=input("Enter the corresponding number of the language you want to switch to:")
                    while choice not in choices:
                        choice=input("Enter the corresponding number of the language you want to switch to:")
                else:
                    choice=random.choice(choices)
                self.ethnicity=int(choice)
            else:
                print("Lancol")
                self.collapse()
    def total_buildings(self):
        slots=0
        buildings=0
        for t in self.territories:
            slots+=nProvince.provinces[t].building_slots
            buildings+=sum(nProvince.provinces[t].buildings)
        return slots,buildings
    def collect_taxes(self):
        income=0
        for s in self.territories:
            if nProvince.provinces[s].stockpile>50000:
                nProvince.provinces[s].stockpile=50000
            income+=nProvince.provinces[s].stockpile
            nProvince.provinces[s].stockpile=0
        tributeto=self.get_relation_type(1,3)
        if tributeto!=None:
            for r in tributeto:
                gn=int(income*0.15)
                Government.governments[Relation.relations[r].country1].money+=gn
                Government.governments[Relation.relations[r].country1].send_message(self.name+", a country that gives us tribute, just gave us "+str(gn)+" currency units when collecting their taxes.")
                income=int(income*0.85)
        self.money+=income
    def sprint(self,message):
        if self.state==0:
            input(message)
    def compute_command(self):
        global omniscience
        commands=[""]
        buildables=[]
        researchables=[]
        tb=self.total_buildings()
        expandable=[]
        expansion_cost=int(((3**(len(self.territories)))//(2**self.research_levels[1]))**(1/2))
        if self.state==0:
            commands.append("statistics")
            commands.append("draw map")
            commands.append("help")
            commands.append("info")
            if len(self.messages)>0:
                commands.append("show messages")
                commands.append("clear messages")
            if len(self.relations)>0:
                commands.append("diplomacy info")
        else:
            self.messages=[]
        if self.research[1]==True and tb[0]>tb[1] and self.money>=1000:
            commands.append("build")
            buildables+=["farm","bank"]
        if self.research[2]==True and self.focus==-1:
            self.sprint("Leader of "+self.name+", it is highly advisable that you pick a national focus!")
            commands.append("pick focus")
        if self.research[0]==True:
            commands.append("collect taxes")
        if self.research[0]==False and self.money>=1000:
            researchables.append("proto-statehood")
            self.sprint("We can become a fully functioning state!")
        if self.research[0]==True and self.research[1]==False and self.money>=5000:
            researchables.append("construction")
        if self.research[0]==True and self.research[3]==False and self.money>=10000:
            researchables.append("social hierarchy")
        if self.research[3]==True and self.research[1]==True and self.research[2]!=True and self.money>=50000:
            researchables.append("national focus")
        if self.research[1]==True and self.research[4]==False and self.money>=100000:
            researchables.append("economy")
        if self.research[2]==True and self.research[5]!=True and self.money>=500000:
            researchables.append("bureaucracy")
        if self.research[5]==True and self.research[6]!=True and self.money>=1000000:
            researchables.append("professional army")
        if len(researchables)>0:
            commands.append("research")
        if self.research[5]==True and ((self.edict_length>=10 and self.edict!="") or (self.edict=="")):
            commands.append("issue edict")
        if self.research[2]==True and len(self.discovered)>len(self.territories) and self.money>=expansion_cost and len(self.wars)==0 and len(self.territories)<=len(self.cores):
            commands.append("expand")
        elif len(self.wars)>0 and self.soldiers>0 and self.capitulated==False:
            commands.append("invade")
        if self.soldiers>0 and self.money>=self.research_levels[0]:
            commands.append("distribute to garrisons")
        if "invade" in commands and "expand" in commands:
            commands.remove("expand")
        #Because countries invade too quickly and illogically, from now on, the maximum number of territories a country can have is now determined by the below set of IF statements:
        max_territories=1
        if self.research[4]==True:
            #If economy is researched, the country will now be more economically able to maintain more territories, so maximum amount of territories it has will increase.
            max_territories+=1
        if self.research[5]==True:
            #If Bureaucracy is Researched, as the name suggests, the country will be much more bureaucratically capable of managing more conquered territories, so will be able to
            #hold more.
            max_territories+=5
        if self.research[6]==True:
            #If Professional Army is Researched, Soldiers will now be able to man garrisons and so, in theory, make controlled territories a lot more stable and thus allow for more to
            #be controlled.
            max_territories+=3
        max_territories+=(self.research_levels[1]*3) #More territories can be held by the Bureaucratic Research Level Increasing.
        if len(self.territories)>max_territories and "expand" in commands:
            commands.remove("expand")
        if len(self.known_countries)>0 and self.is_vassal==False and self.research[0]==True:
            commands.append("diplomacy")
        if self.research[6]==True and self.manpower>0:
            commands.append("recruit")
        elif len(self.wars)>0 and self.manpower>0:
            commands.append("recruit")
        if self.capitulated==True:
            if self.state==0:
                print("We have capitulated, there's nothing we can do.")
            commands=[""]
        if len(commands)>1:
            done=False
            while done==False:
                if len(commands)==1:
                    done=True
                if self.state==0:
                    if len(self.messages)>0:
                        print("We have messages!")
                    command=input("Enter your command, leader of "+self.name+"(enter \"help\" to show commands):").lower()
                else:
                    if len(self.wars)>0:
                        at_war=True
                    else:
                        at_war=False
                    command=AI.make_decision(commands,self.state,at_war,self.edict_length)
                if command in commands:
                    edicts=["Civilization Effort","Enslavement Effort","Liberation Effort","Assimilation Effort","Conversion Effort","Language Teaching","Ethnic Cleansing"]
                    if command=="":
                        done=True
                    if command=="help":
                        for c in commands:
                            print(c)
                    if command=="invade":
                        result=self.invade()
                        if result!=None:
                            Government.combat(self.id,nProvince.provinces[result].owner,(not self.is_neighbor(result) and self.connected_by_sea(result)==True),result)
                            done=True
                        else:
                            self.sprint("It appears you are out of reach of any invadable provinces, because you haven't discovered them yet.")
                            commands.remove("invade")
                    if command=="build":
                        if self.state==0:
                            for b in buildables:
                                print(b)
                            choice=input("Enter what you want to build:")
                        else:
                            choice=random.choice(buildables)
                        if choice in buildables:
                            if choice=="farm":
                                indy=0
                                self.money-=1000
                            if choice=="bank":
                                indy=1
                                self.money-=1000
                            for t in self.territories:
                                if sum(nProvince.provinces[t].buildings)<nProvince.provinces[t].building_slots:
                                    nProvince.provinces[t].buildings[indy]+=1
                                    done=True
                                    break;
                    if command=="recruit":
                        #The higher your research level, the more it costs to recruit soldiers. This is supposed to simulate the idea of more developed weaponry becoming more expensive.
                        cps=(self.research_levels[0]+1)*5
                        self.sprint("We have "+str(self.manpower)+" recruitable soldiers. It costs "+str(cps)+" currency units per soldier to recruit a soldier. We have "+str(self.money)+" currency units in total.")
                        maximum=(self.money//cps)
                        #As test playthroughs have shown, the maximum wasn't entirely correct - it calculates the maximum based on JUST the amount of money a government has, NOT on
                        #the amount of money AND the amount of manpower. This means a AI country will be able to recruit a ludicrous amount. In the 2 lines of code below this is rectified.
                        if maximum>self.manpower:
                            maximum=self.manpower
                        if maximum>0:
                            if self.state==0:
                                amount=iinput("Enter how many soldiers you want to recruit(you can recruit a maximum of "+str(maximum)+" with the current funds you have):")
                                if amount>maximum:
                                    amount=maximum
                            else:
                                if len(self.wars)>0:
                                    amount=maximum
                                else:
                                    if self.state==3:
                                        amount=maximum
                                    else:
                                        amount=maximum//2
                            if amount>0:
                                self.manpower-=amount #Turns out I hadn't added this before 04/18/2020, meaning Countries would just infinitely take soldiers which is incorrect.
                                self.money-=amount*cps
                                self.soldiers+=amount
                                done=True
                        else:
                            commands.remove("recruit")
                    if command=="info":
                        if len(self.wars)>0:
                            print("We are taking part in "+str(len(self.wars))+" wars!")
                        print("We have "+str(self.money)+" currency units.")
                        print("Our Military Technology is currently at level "+str(self.research_levels[0])+", with a progress of "+str(rounded(self.research_progress[0]))+"% till the next level.")
                        print("Our Bureaucracy Technology is currently at level "+str(self.research_levels[1])+", with a progress of "+str(rounded(self.research_progress[1]))+"% till the next level.")
                        print("Our Cultural Technology is currently at level "+str(self.research_levels[2])+", with a progress of "+str(rounded(self.research_progress[2]))+"% till the next level.")
                        print("Our State Culture is the "+Culture.cultures[self.culture].name+" culture.")
                        print("Our State Religion is "+Religion.religions[self.religion].name+".")
                        print("Our Official Language is the "+Language.languages[self.language].name+" language.")
                        print("Our Accepted Ethnicity is the "+Ethnicity.ethnicities[self.ethnicity].name+" ethnicity.")
                        if self.research[5]==True:
                            print("Our Issued Edict is "+self.edict+" and has been issued  for "+str(self.edict_length)+" turns.")
                        print("We have "+str(len(self.territories))+" provinces under our administration.")
                        if self.research[6]==True or (len(self.wars)>0 and self.capitulated==False):
                            print("Our army, as it stands, has "+str(self.soldiers)+" soldiers.")
                            print("We have "+str(self.manpower)+" people we can recruit as soldiers.")
                        print("It would cost us "+str(expansion_cost)+" currency units to expand, and we cannot, currently, expand past "+str(max_territories+1)+" provinces.")
                    if command=="diplomacy":
                        choices={}
                        for c in self.known_countries:
                            if Government.get_war(self.id,c)==None:
                                choices[Government.governments[c].name]=c
                        if len(choices)>0:
                            if self.state==0:
                                for c in list(choices.keys()):
                                    print(c)
                                choice=input("Enter the country with which you want to conduct diplomacy:")
                            else:
                                choice=random.choice(list(choices.keys()))
                            if choice in list(choices.keys()):
                                choice=choices[choice]
                                gov=Government.governments[choice]
                                relation=Government.get_relation(self.id,choice)
                                if relation!=None and Government.get_war(self.id,choice)==None:
                                    options=[]
                                    if len(Relation.relations[relation].points)<1:
                                        #Relations between countries are basically set at this point. You can either declare war and basically destroy the nation, or start negotiating further.
                                        options+=["declare war"]
                                    if self.state==0:
                                        print("We have had diplomatic relations with "+gov.name+" for "+str(Relation.relations[relation].length)+" turns.")
                                    if len(Relation.relations[relation].points)>0:
                                        if self.state==0:
                                            print("We have the following points in our relations:")
                                            names=["* and # are will not declare war on each other.","* and # will come to each other's assistance if one of them is forced to fight a defensive war. This will not apply for offensive wars.","* and # will come to each other's assistance if one of them declares an offensive war. This does not apply for defensive wars.","# will pay 15% of their tax income as tribute to *.","* and # will assist each other in the case of a famine.","* has the right to annex #.","* and # will share technologies.","# will give 10% of its enlisted troops to * as a levy.","# acknowledges that it is under the overlordship of *."]
                                            for p in Relation.relations[relation].points:
                                                x=names[p]
                                                x=x.replace("*",Government.governments[Relation.relations[relation].country1].name)
                                                x=x.replace("#",Government.governments[Relation.relations[relation].country2].name)
                                                print(x)
                                        if 8 in Relation.relations[relation].points and "declare war" in options:
                                            options.remove("declare war")
                                        if 8 in Relation.relations[relation].points and self.id==Relation.relations[relation].country1:
                                            options.append("annex")
                                    if len(options)>0:
                                        if self.state==0:
                                            for o in options:
                                                print(o)
                                            option=input("Enter what new thing you want to do to the country:")
                                        else:
                                            if len(self.wars)>0 and random.randint(1,10)!=1 and "declare war" in options:
                                                options.remove("declare war")
                                            declarance=Government.accept(gov.focus,self.state,"",gov.religion,self.religion,gov.culture,self.culture)
                                            if declarance==False and "declare war" in options:
                                                option="declare war"
                                            else:
                                                option=random.choice(options)
                                        if option in options:
                                            if option=="declare war":
                                                Government.declare_war(self.id,choice)
                                            if option=="annex":
                                                self.sprint("We have annexed "+Government.governments[choice].name+"!")
                                                for t in Government.governments[choice].territories:
                                                    Government.governments[self.id].take_territory(t,True)
                                                Government.governments[choice].collapse()
                                            done=True
                                            
                                else:
                                    if Government.get_war(self.id,choice)==None:
                                        if self.id not in Government.governments[choice].known_countries:
                                            Government.governments[choice].send_message("A traveller from a previously-undiscovered land known as "+self.name+" has visited us, and showed us their location.")
                                            Government.governments[choice].known_countries.append(self.id)
                                            Government.governments[choice].discovered+=self.territories
                                        else:
                                            acceptance=Government.accept(self.focus,gov.state,self.name+" would like to establish diplomatic relations with us!",self.religion,gov.religion,self.culture,gov.religion)
                                            if acceptance[0]==True:
                                                self.sprint("We have established official diplomatic relations with "+gov.name+"!")
                                                r=Relation(self.id,choice)
                                            else:
                                                self.sprint(gov.name+" has unfortunately refused our offer for the following reason:")
                                                self.sprint(acceptance[1])
                                                if self.state==0 or self.state==3:
                                                    if self.state==0:
                                                        war=input("We can declare war on them for their refusal! Shall we?")
                                                    else:
                                                        war=random.choice(["yes","no"])
                                                else:
                                                    war="no"
                                                if "ye" in war.lower():
                                                    Government.declare_war(self.id,choice)
                                            
                                    done=True
                        else:
                            commands.remove("diplomacy")
                    if command=="issue edict":
                        if self.state==0:
                            input("Here are possible edicts we can issue:")
                            for e in edicts:
                                print(e)
                            choice=input("Enter the edict you want to issue:")
                        else:
                            choice=AI.edict_decision(self.state,self.edict)
                        if choice in edicts:
                            self.edict=choice
                            self.edict_length=0
                            for t in self.territories:
                                nProvince.provinces[t].clear_edicts()
                                nProvince.provinces[t].modifiers.append(choice)
                            done=True
                    if command=="expand":
                        result=self.expand()
                        if result!=None:
                            Government.governments[self.id].take_territory(result,True)
                            done=True
                        else:
                            commands.remove("expand")
                    if command=="draw map":
                        print("These are the maps we can draw:")
                        print("1 - Distribution of the "+Culture.cultures[self.culture].name+" Culture in the Known World")
                        print("2 - Distribution of the "+Language.languages[self.language].name+" Language in the Known World")
                        print("3 - Climate Map of the Known World")
                        print("4 - Political Map of the Known World")
                        types=[1,2,3,4]
                        try:
                            typ=int(input("Enter your choice:"))
                        except:
                            typ=0
                        if typ in types:
                            self.draw_map(typ,False,"",0)
                    if command=="research":
                        prices={"proto-statehood":1000,"construction":5000,"national focus":25000,"social hierarchy":10000,"economy":50000,"bureaucracy":100000,"professional army":500000}
                        if self.state==0:
                            input("Our choices for research:")
                            for r in researchables:
                                print(r)
                            choice=input("Enter what you want to research:")
                        else:
                            choice=random.choice(researchables)
                        if choice.lower() in researchables:
                            self.money-=prices[choice]
                            self.research[list(prices.keys()).index(choice)]=True
                            if choice=="proto-statehood":
                                options={}
                                named_options={}
                                idy=0
                                chxs=[]
                                for t in self.territories:
                                    for p in nProvince.provinces[t].population:
                                        if population_unit.population_units[p].typ not in [1,4]:
                                            f=population_unit.population_units[p].get_information()
                                            z="Culturally "+f[0]+", Ethnically "+f[3]+", "+f[2]+"-speaking Population Unit following the "+f[1]+" religion"
                                            options[z]=p
                                            chxs.append(str(idy))
                                            named_options[str(idy)]=z
                                            idy+=1
                                if self.state==0:
                                    input("We have now established a sovereign state, not just a tribal society. It is time we pick one of our Population Units as the Main one:")
                                    for o in list(named_options.keys()):
                                        print(o+" - "+named_options[o])
                                    chx=input("Enter the number of your choice:")
                                    while chx not in chxs:
                                        chx=input("Enter the number of your choice:")
                                else:
                                    chx=random.choice(chxs)
                                main_info=population_unit.population_units[options[named_options[chx]]]
                                self.culture=main_info.culture
                                self.religion=main_info.religion
                                self.language=main_info.language
                                self.ethnicity=main_info.ethnicity
                            if choice=="social hierarchy":
                                enslaved=0
                                for t in self.territories:
                                    for p in nProvince.provinces[t].population:
                                        pop=population_unit.population_units[p]
                                        if pop.ethnicity==self.ethnicity and pop.religion==self.religion and pop.language==self.language and pop.culture==self.culture:
                                            pass
                                        else:
                                            population_unit.population_units[p].typ=1
                                            enslaved+=1
                                self.sprint("We have now established our people as superior to all the rest by enslaving "+str(enslaved)+" population units! Hail "+self.name+"!")
                                self.edict="Enslavement Effort"
                            done=True
                    if command=="statistics":
                        self.show_statistics()
                    if command=="show messages":
                        input("Our messages:")
                        for i in self.messages:
                            print(i)
                        self.messages=[]
                    if command=="":
                        done=True
                    if command=="collect taxes":
                        oldmoney=self.money
                        self.collect_taxes()
                        if self.money>oldmoney:
                            self.sprint("Our tax collectors collected "+str(self.money-oldmoney)+" units of currency.")
                            done=True
                        else:
                            commands.remove("collect taxes")
                    if command=="distribute to garrisons":
                        try:
                            max_distributable=self.money//self.research_levels[0]
                            if max_distributable>self.soldiers:
                                max_distributable=self.soldiers
                        except ZeroDivisionError:
                            max_distributable=self.soldiers
                        if self.state==0:
                            amount=iinput("Enter the amount of soldiers you want to distribute to garrison in the "+str(len(self.territories))+" provinces we control(we have "+str(self.soldiers)+" soldiers):")
                        else:
                            amount=max_distributable
                        if amount>max_distributable:
                            amount=max_distributable
                        amount=(amount//len(self.territories))*len(self.territories)
                        if amount>0:
                            self.soldiers-=amount
                            self.money-=(amount*self.research_levels[0])
                            for t in self.territories:
                                nProvince.provinces[t].garrison+=amount//len(self.territories)
                            done=True
                        else:
                            commands.remove("distribute to garrisons")
                    if command=="pick focus":
                        works=[0,1,2,3]
                        if self.state==0:
                            input("Our choices of National Focus:")
                            print("0 - Cultural Focus: Aimed at Assimilating the world into our culture")
                            print("1 - Religious Focus: Aimed at Uniting the world under the one true faith")
                            print("2 - Conquest Focus: Aimed at Conquering the world")
                            print("3 - Science Focus: Aimed at Leading the world scientifically")
                            choice=input("Enter your choice(Be sure with your choice, it cannot be changed later):")
                            try:
                                choice=int(choice)
                            except:
                                choice=""
                            if choice in works:
                                if choice=="0":
                                    self.assimilation_bonus+=1
                                if choice=="1":
                                    self.teaching_bonus+=1
                                if choice=="2":
                                    self.combat_bonus+=1
                                    self.naval_range+=25
                                if choice=="3":
                                    self.teaching_bonus+=1
                                self.focus=choice
                                done=True
                        else:
                            self.focus=self.state-1
                            done=True
                if len(commands)<1:
                    done=True
                if command=="@research" and self.research[0]==True:
                    self.research=[True,True,True,True,True,True,True]
                if command=="retire":
                    self.state=self.focus+1
                    done=True
                if command=="@money":
                    self.money+=1000000
                if command=="@omniscience":
                    omniscience = not omniscience
                if command=="@domination":
                    for p in list(nProvince.provinces.keys()):
                        if p not in self.territories:
                            self.take_territory(p,True)
                if command=="@showall":
                    self.discovered=list(nProvince.provinces.keys())
    def check_characteristics(self):
        has_culture=False
        has_religion=False
        has_language=False
        has_ethnicity=False
        for t in self.territories:
            for p in nProvince.provinces[t].population:
                if has_culture==False:
                    if population_unit.population_units[p].culture==self.culture:
                        has_culture=True
                if has_religion==False:
                    if population_unit.population_units[p].religion==self.religion:
                        has_religion=True
                if has_language==False:
                    if population_unit.population_units[p].language==self.language:
                        has_language=True
                if has_ethnicity==False:
                    if population_unit.population_units[p].ethnicity==self.ethnicity:
                        has_ethnicity=True
        if len(self.get_population())>0:
            if self.research[0]==True:
                if has_culture==False:
                    self.sprint("Leader of "+self.name+"! The remaining followers of our official culture have either died out or left our lands. We need to pick a new official culture.")
                    self.switch_culture()
                if has_religion==False:
                    self.sprint("Leader of "+self.name+"! The remaining followers of our state religion have either died out or left our lands. We need to pick a new state religion.")
                    self.switch_religion()
                if has_language==False:
                    self.sprint("Leader of "+self.name+"! The remaining speakers of our official language have either died out or left our lands. We need to pick a new official language.")
                    self.switch_language()
                if has_ethnicity==False:
                    self.sprint("Leader of "+self.name+"! The remaining members of our accepted ethnic group have either died out or left our lands. We need to pick a new accepted ethnicity.")
                    self.switch_ethnicity()
        else:
            if len(self.wars)==0:
                print("Popcol")
                self.collapse()
    def show_statistics(self):
        total_population=0
        religion_breakdown={}
        culture_breakdown={}
        language_breakdown={}
        ethnic_breakdown={}
        class_breakdown={0:0,1:0,2:0,3:0}
        for t in self.territories:
            for p in nProvince.provinces[t].population:
                if population_unit.population_units[p].typ!=4:
                    data=population_unit.population_units[p].get_information()
                    if data!=None:
                        total_population+=1
                        if data[0] not in culture_breakdown:
                            culture_breakdown[data[0]]=1
                        else:
                            culture_breakdown[data[0]]+=1
                        if data[1] not in religion_breakdown:
                            religion_breakdown[data[1]]=1
                        else:
                            religion_breakdown[data[1]]+=1
                        if data[2] not in language_breakdown:
                            language_breakdown[data[2]]=1
                        else:
                            language_breakdown[data[2]]+=1
                        if data[3] not in ethnic_breakdown:
                            ethnic_breakdown[data[3]]=1
                        else:
                            ethnic_breakdown[data[3]]+=1
                        class_breakdown[population_unit.population_units[p].typ]+=1
        cul=input("Break down cultures?")
        if "ye" in cul.lower():
            for c in list(culture_breakdown.keys()):
                print("\tThe "+c+" culture is followed by "+str(culture_breakdown[c])+" population units, constituting "+rounded_division(culture_breakdown[c],total_population,True,True)+"% of our population.")
        rel=input("Break down religions?")
        if "ye" in rel.lower():
            for c in list(religion_breakdown.keys()):
                print("\t"+c+" is practiced by "+str(religion_breakdown[c])+" population units, constituting "+rounded_division(religion_breakdown[c],total_population,True,True)+"% of our population.")
        lan=input("Break down languages?")
        if "ye" in lan.lower():
            for c in list(language_breakdown.keys()):
                print("\tThe "+c+" language is spoken by "+str(language_breakdown[c])+" population units, constituting "+rounded_division(language_breakdown[c],total_population,True,True)+"% of our population.")
        eth=input("Break down ethnic groups?")
        if "ye" in eth.lower():
            for c in list(ethnic_breakdown.keys()):
                print("\tThe "+c+" people consist of "+str(ethnic_breakdown[c])+" population units, constituting "+rounded_division(ethnic_breakdown[c],total_population,True,True)+"% of our population.")
        cla=input("Break down population classifications?")
        if "ye" in cla.lower():
            nommes=["civilized","enslaved","tribal","nomadic"]
            for c in list(class_breakdown.keys()):
                print("\t"+str(class_breakdown[c])+" population units are "+nommes[c]+", constituting "+rounded_division(class_breakdown[c],total_population,True,True)+"% of our population.")
        invprov=input("Break down Population Units in individual provinces?")
        if "ye" in invprov:
            names=["Citizen","Slave","Tribesman","Nomad"]
            for t in self.territories:
                ana=input("Analyze population units in the "+nProvince.provinces[t].name+" province?")
                if "ye" in ana.lower():
                    input(nProvince.provinces[t].name+" consists of:")
                    for p in nProvince.provinces[t].population:
                        if population_unit.population_units[p].typ!=4:
                            f=population_unit.population_units[p].get_information()
                            print("\tAn ethnically "+f[3]+", culturally "+f[0]+" "+names[population_unit.population_units[p].typ]+", practicing "+f[1]+" as their faith, and speaking the "+f[2]+" language.")
    def check_survival(self):
        if len(self.wars)==0:
            self.check_characteristics()
            people=0
            for t in self.territories:
                people+=len(nProvince.provinces[t].population)
            if (people<1) or len(self.territories)<1:
                print("Surcol")
                self.collapse()
                return False
        else:
            if len(self.territories)<1:
                self.capitulated=True
    def check_victory():
        if len(list(Government.governments.keys()))<2:
            Government.victorious=True
            input(Goverment.governments[list(Government.governments.keys())[0]].name+" is the last country standing, meaning they have won the DOMINATION victory!")
        else:
            for g in list(Government.governments.keys()):
                gov=Government.governments[g]
                if gov.research_levels[0]>=200 and gov.research_levels[1]>=200 and gov.research_levels[2]>=200 and gov.focus==3:
                    input(gov.name+" has reached over 100 levels in all three technologies, meaning they have won the SCIENTIFIC victory!")
                    Government.victorious=True
                    break;
                if len(gov.territories)>len(list(nProvince.provinces.keys()))//2 and gov.focus==2:
                    input(gov.name+" controls over half of the entire world, meaning they have won the CONQUEST victory!")
                    Government.victorious=True
                    break;
                if gov.focus in [0,1]:
                    people=len(list(population_unit.population_units.keys()))
                    religioned=0
                    cultured=0
                    languaged=0
                    for p in list(population_unit.population_units.keys()):
                        pop=population_unit.population_units[p]
                        if pop.culture==gov.culture:
                            cultured+=1
                        if pop.religion==gov.religion:
                            religioned+=1
                        if pop.language==gov.language:
                            languaged+=1
                    if gov.focus==0 and (languaged/people)>0.5 and (cultured/people)>0.25:
                        input("Over half of the world speaks the "+Language.languages[gov.language].name+" language, and over a quarter of the world follow the renowned "+Culture.cultures[gov.culture].name+" culture. Both of these, respectively, are the official language and culture of "+gov.name+", meaning "+gov.name+" has won a CULTURAL victory!")
                        Government.victorious=True
                        break;
                    if gov.focus==1 and (religioned/people)>0.5:
                        input("The "+Religion.religions[gov.religion].name+" faith stands unopposed in the religious world. "+gov.name+" has succeeded in turning their faith from a tiny little cult into a mighty religion, securing a RELIGIOUS victory!")
                        Government.victorious=True
                        break;
    def analyse_territories(self):
        for t in self.territories:
            if nProvince.provinces[t].true_owner==self.id and t not in self.cores and random.randint(1,25)==1:
                self.cores.append(t)
                self.send_message("The territory of "+nProvince.provinces[t].name+" has become fully integrated into our territories!")
    def analyse(self):
        self.edict_length+=1
        self.compute_food()
        only_occupied=True
        if len(self.territories)>0:
            for t in self.territories:
                if nProvince.provinces[t].true_owner==self.id:
                    only_occupied=False
        if only_occupied==True:
            self.capitulated=True
        result=self.check_survival()
        if result!=False:
            if self.capitulated==False and len(self.territories)>0:
                share=self.food//len(self.territories)
                self.food=0
                for t in self.territories:
                    nProvince.provinces[t].foodstore+=share
                max_manpower=10000
                if self.research[6]==True:
                    max_manpower+=15000
                max_manpower+=(self.research_levels[0]*1000)
                if self.manpower>max_manpower:
                    self.manpower=max_manpower
                
                mgain=0
                for t in self.territories:
                    for p in nProvince.provinces[t].population:
                        try:
                            if population_unit.population_units[p].typ==0:
                                mgain+=10
                        except KeyError:
                            nProvince.provinces[t].population.remove(p)
                levyto=self.get_relation_type(1,7)
                if levyto!=None:
                    for r in levyto:
                        gid=Relation.relations[r].country1
                        Government.governments[gid].send_message(Government.governments[self.id]+" has, as the treaty with them demanded, given us "+str(int(mgain*0.1))+" soldiers for our army, 10% of their enlisted troops.")
                        Government.governments[gid].manpower+=int(mgain*0.1)
                        mgain=int(mgain*0.9)
                self.manpower+=mgain
                self.discover_territories()#This checks all discovered territories
            for c in self.known_countries:
                if c not in Government.governments:
                    self.known_countries.remove(c)
            for r in self.relations:
                if r not in Relation.relations.keys():
                    self.relations.remove(r)
            self.analyse_research()
            self.analyse_territories()
            self.compute_command()
            self.money+=random.randint(10,100)
