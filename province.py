import pickle
width,height=1357,628
snowy=111
minjungle=361
import copy
maxjungle=398
def find_province(x,y):
    for p in list(nProvince.provinces.keys()):
        if [x,y] in nProvince.provinces[p].territories:
            return p
class nProvince:
    idy=0
    provinces={}
    water=[]
    fertile=[]
    infertile=[]
    def clear_edicts(self):
        edicts=["Settlement Effort","Civilization Effort","Enslavement Effort","Liberation Effort","Assimilation Effort","Conversion Effort","Language Teaching","Ethnic Cleansing"]
        for e in edicts:
            if e in self.modifiers:
                self.modifiers.remove(e)
    def __init__(self):
        self.current_pixel=0
        self.territories=[]
        self.id=nProvince.idy
        nProvince.idy+=1
        self.neighbors=[]
        self.sea=False
        self.fertile=[]
        self.infertile=[]
        self.garrison=0
        self.modifiers=[]
        self.unrest=0
        self.age=0
        self.buildings=[0,0]
        self.owner=None
        self.true_owner=None
        self.typ=random.choice([0,1])
        self.abstract_neighbors=0
        self.stockpile=0
        self.foodstore=0
        self.name=""
        self.is_occupied=False
        self.building_slots=0
        nProvince.provinces[self.id]=self
    def get_middle(self):
        return self.territories[len(self.territories)//2]
    def iterate(self):
        self.age+=1
        food_bonus=self.buildings[0]
        interest=self.buildings[1]
        if self.typ==0:
            foodgain=len(self.fertile)
        elif self.typ==1:
            foodgain=len(self.fertile)//5
        elif self.typ==2:
            foodgain=int(len(self.fertile)*1.5)
        else:
            foodgain=0
        foodgain=int(foodgain*(1+food_bonus/100))+self.buildings[1]
        self.foodstore+=foodgain
        for pop in self.population:
            if pop in population_unit.population_units.keys():
                population_unit.population_units[pop].iterate()
            else:
                self.population.remove(pop)
        self.stockpile=int(self.stockpile*(1+interest/100))
        self.analyse()
    def analyse(self):
        if len(self.population)<1:
            if self.sea!=False:
                gain=random.randint(1,100000)
                if gain==1:
                    x=population_unit(True,self.id)
                    self.population.append(x.id)
                    x.location=self.id
    def Cellular_Automaton():
        lived=[]
        killed=[]
        for p in list(nProvince.provinces.keys()):
            living=0
            borders_permanently_fertile=False
            borders_permanently_infertile=False
            for n in nProvince.provinces[p].neighbors:
                if nProvince.provinces[n].typ==0:
                    living+=1
                if nProvince.provinces[n].typ==2:
                    borders_permanently_fertile=True
                if nProvince.provinces[n].typ==3:
                    borders_permanently_infertile=True
            if borders_permanently_fertile==True:
                lived.append(p)
            elif borders_permanently_infertile==True:
                killed.append(p)
            elif living in [2,3] and nProvince.provinces[n].typ==0:
                lived.append(p)
            elif living==3 and nProvince.provinces[n].typ==1:
                lived.append(p)
            else:
                killed.append(p)
            if len(nProvince.provinces[p].neighbors)>0:
                pass
            else:
                if p in killed:
                    killed.remove(p)
        for l in lived:
            if nProvince.provinces[l].typ!=2 and nProvince.provinces[l].typ!=3:
                nProvince.provinces[l].typ=0
        for k in killed:
            if nProvince.provinces[k].typ!=2 and nProvince.provinces[k].typ!=3:
                nProvince.provinces[k].typ=1
class Seazone:
    idy=0
    seazones={}
    def __init__(self):
        self.coasts=[]
        self.id="S"+str(Seazone.idy)
        Seazone.idy+=1
        Seazone.seazones[self.id]=self
from population import *
