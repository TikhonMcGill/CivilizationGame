import pickle
import copy
import random
from PIL import Image
import os
from province import nProvince, Seazone
from population import *
nProvince.provinces={}
from namings import *
from province import *
def lines(file):
    f=open(file)
    data=f.readlines()
    f.close()
    for i in range(len(data)):
        data[i]=data[i].replace("\n","")
    return data
#This first part of code is responsible for loading up map files, and assigning the right type to each province and populating the world with Population Units
Seazone.seazones=pickle.load(open("assets/map/seazones.map","rb"))
oceans=pickle.load(open("assets/map/oceans.map","rb"))
provinces=pickle.load(open("assets/map/nprovinces.map","rb"))
pids=[]
nProvince.water = oceans
nProvince.fertile=[]
nProvince.infertile=[]
neighbor1=0
neighbor2=0
for p in list(provinces.keys()):
    pids.append(p)
    provinces[p].fertile=[]
    provinces[p].infertile=[]
    provinces[p].current_pixel=0
    provinces[p].typ=random.choice([0,0,0,0,0,0,1,1,1,1,1,1,2,3])
    provinces[p].population=[]
    provinces[p].age=0
    provinces[p].abstract_neighbors=0
    provinces[p].owner=None
    provinces[p].true_owner=None
    provinces[p].unrest=0
    provinces[p].modifiers=[]
    provinces[p].buildings=[0,0]
    provinces[p].garrison=0
    provinces[p].stockpile=0
    provinces[p].foodstore=0
    provinces[p].name=generate_word().capitalize()
    provinces[p].building_slots=int(len(provinces[p].territories)**(1/2))
    if [7,109] in provinces[p].territories:
        neighbor1=p
    if [1160,73] in provinces[p].territories:
        neighbor2=p
print(neighbor1)
print(neighbor2)
nProvince.provinces=provinces
nProvince.provinces[neighbor1].neighbors.append(neighbor2)
nProvince.provinces[neighbor2].neighbors.append(neighbor1)
for p in list(nProvince.provinces.keys()):
    for d in range(random.randint(1,len(nProvince.provinces[p].territories)//10+2)):
        x=population_unit(True,p)
    for n in nProvince.provinces[p].neighbors:
        if nProvince.provinces[n].typ==3 and random.randint(1,50)==1:
            nProvince.provinces[p].typ=3
    if nProvince.provinces[p].typ==3:
        nProvince.provinces[p].building_slots=nProvince.provinces[p].building_slots*2
#This part of the code is the actual game
def list_to_int(listy):
    z=listy.split(",")
    output=[]
    for i in z:
        output.append(int(i))
    return output
def create_custom_population_unit(place,stats1,stats2,stats3,stats4,name1,name2,name3,name4):
    stats1=list_to_int(stats1)
    stats2=list_to_int(stats2)
    stats3=list_to_int(stats3)
    stats4=list_to_int(stats4)
    w,x,y,z=Culture(),Religion(),Ethnicity(),Language()
    w.stats=stats1
    x.stats=stats2
    y.stats=stats3
    z.atr,z.inv=stats4[0],stats4[1]
    w.name=name1
    x.name=name2
    y.name=name3
    z.name=name4
    p=population_unit(False,place)
    p.culture=w.id
    p.religion=x.id
    p.ethnicity=y.id
    p.language=z.id
    return p
f=random.choice(list(population_unit.population_units.keys()))
itera=0
playlist=copy.copy(pids)
playlist_index=0
random.shuffle(playlist)
players=int(input("Enter number of players:"))
for d in range(players):
    g=Government()
    g.name=input("Enter the name of your country:")
    try:
        coords=int(input("Enter Starting X-Coordinate:")),int(input("Enter starting Y-Coordinate:"))
        p=find_province(coords[0],coords[1])
    except:
        p=random.choice(pids)
    nProvince.provinces[p].name=g.name
    g.take_territory(p,True)
    z=create_custom_population_unit(p,"5,5,5","5,5,5","5,5,5","5,5",input("Enter name of your Culture:"),input("Enter name of your Religion:"),input("Enter name of your Ethnicity:"),input("Enter name of your Language:"))
    z.typ=0
    g.culture=z.culture
    g.religion=z.religion
    g.ethnicity=z.ethnicity
    g.state=0
    g.language=z.language
    print("0 - Maritime: More easily discoverable coasts")
    print("1 - Land: Cheaper to expand, but difficult to discover other shores")
    cx=[0,1]
    try:
        choice=int(input("Enter which expansion type your government needs(from the ones above):"))
    except:
        choice=2
    if choice in cx:
        g.expansion_type=choice
    else:
        g.expansion_type=random.choice(cx)
    if g.expansion_type==1:
        g.naval_range=-10
if len(os.listdir("assets/custom"))>0:
    cust=input("Add custom nations?")
    if "ye" in cust:
        for o in os.listdir("assets/custom"):
            data=lines("assets/custom/"+o)
            try:
                place=find_province(int(data[1].split(",")[0]),int(data[1].split(",")[1]))
            except:
                place=random.choice(pids)
            col=(int(data[2].split(",")[0]),int(data[2].split(",")[1]),int(data[2].split(",")[2]))
            name1=data[3]
            name2=data[4]
            name3=data[5]
            name4=data[6]
            try:
                exptyp=int(data[7])
            except:
                exptype=random.randint(0,1)
            z=create_custom_population_unit(place,"5,5,5","5,5,5","5,5,5","5,5",name1,name2,name3,name4)
            z.typ=0
            g=Government()
            g.name=data[0]
            g.culture=z.culture
            g.religion=z.religion
            g.ethnicity=z.ethnicity
            g.language=z.language
            g.color=col
            g.take_territory(place,True)
            g.cores.append(place)
            g.expansion_type=exptyp
            nProvince.provinces[place].name=g.name
            nProvince.provinces[place].typ=random.choice([0,2,2,2])
            print(data[0]+" loaded!")
            pla=input("Play as?")
            if "ye" in pla:
                g.state=0
            else:
                g.state=random.randint(1,4)
fold=input("Enter folder name:")
os.mkdir(fold)
iteration=0
def draw_map(typ):
    img=Image.new("RGB",(width,height),(175,175,175))
    pixels=img.load()
    if typ==0:
        for t in list(nProvince.provinces.keys()):
            if nProvince.provinces[t].owner==None:
                col=(200,200,200)
            else:
                col=Government.governments[nProvince.provinces[t].owner].color
            for t2 in nProvince.provinces[t].territories:
                pixels[t2[0],t2[1]]=col
    img.save(fold+"/"+str(iteration)+".png")
while Government.victorious==False: #As seen in the conditions for this loop, the game will continue for up to 1000 turns if more than one country still remains.
    for p in list(nProvince.provinces.keys()):
        nProvince.provinces[p].iterate()
    for w in list(War.wars.keys()):
        War.wars[w].check()
    for g in list(Government.governments.keys()):
        if g in list(Government.governments.keys()):
            Government.governments[g].analyse()
    if iteration%100==0 and iteration!=0:
        nProvince.Cellular_Automaton() #Every 100 turns, the Provinces go through their cellular automaton.
    draw_map(0)
    iteration+=1
    if iteration%10==0 and iteration!=0:
        Government.check_victory()
#This part of the code is analysis of a country
