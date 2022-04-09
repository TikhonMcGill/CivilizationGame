import random
from namings import *
import copy
def population_formula(number):
    return number*1000
def compute_distance(coord1,coord2):
    return int(((coord2[0]-coord1[0])**2+(coord2[1]-coord1[1])**2)**(1/2))
class Religion():
    religions = {}
    curid=0
    def __init__(self):
        self.stats=[random.randrange(-3,5),random.randrange(-3,5),random.randrange(-3,5)]
        self.zeal=random.randint(0,50)
        self.id=Religion.curid
        self.followers=1
        self.name=""
        Religion.curid+=1
        Religion.religions[self.id]=self                   
    def check(self):
        if self.followers<1:
            for g in list(Government.governments.keys()):
                if self.id==Government.governments[g].religion:
                    Government.governments[g].messages.append(self.name+", our faith, has perished.")
                    Government.governments[g].switch_religion()
            del(Religion.religions[self.id])
            del(self)
class Culture():
    cultures = {}
    curid=0
    def __init__(self):
        self.stats=[random.randrange(-3,5),random.randrange(-3,5),random.randrange(-3,5)]
        self.id=Culture.curid
        self.followers=1
        self.name=""
        Culture.curid+=1
        Culture.cultures[self.id]=self
    def check(self):
        if self.followers<1:
            for g in list(Government.governments.keys()):
                if self.id==Government.governments[g].culture:
                    Government.governments[g].messages.append(self.name+", our official culture, has died out.")
                    Government.governments[g].switch_culture()
            del(Culture.cultures[self.id])
            del(self)
class Ethnicity():
    ethnicities = {}
    curid=0
    def __init__(self):
        self.stats=[random.randrange(-3,5),random.randrange(-3,5),random.randrange(-3,5)]
        self.id=Ethnicity.curid
        self.members=1
        self.name=""
        Ethnicity.curid+=1
        Ethnicity.ethnicities[self.id]=self
    def check(self):
        if self.members<1:
            for g in list(Government.governments.keys()):
                if self.id==Government.governments[g].ethnicity:
                    Government.governments[g].messages.append(self.name+", our ethnic race, has died out.")
                    Government.governments[g].switch_ethnicity()
            del(Ethnicity.ethnicities[self.id])
            del(self)
class Language():
    languages={}
    curid=0
    def __init__(self):
        self.atr=random.randint(0,5)
        self.inv=random.randint(0,5)
        self.id=Language.curid
        self.speakers=1
        self.name=""
        Language.curid+=1
        Language.languages[self.id]=self
    def check(self):
        if self.speakers<1:
            for g in list(Government.governments.keys()):
                if self.id==Government.governments[g].language:
                    Government.governments[g].messages.append("The last speakers of "+self.name+", our historic language, have just died.")
                    Government.governments[g].switch_language()
            del(Language.languages[self.id])
            del(self)
def create_custom_pu(culture,religion,language,ethnicity,stats,location,typ,zeal):
    global Culture
    global Religion
    global Ethnicity
    global Language
    x=population_unit(False,location)
    x.culture=culture
    x.religion=religion
    x.zeal=RELU(zeal)
    x.language=language
    x.ethnicity=ethnicity
    Culture.cultures[culture].followers+=1
    Religion.religions[religion].followers+=1
    Ethnicity.ethnicities[ethnicity].members+=1
    Language.languages[language].speakers+=1
    x.typ=typ
    x.stats=stats
class population_unit():
    population_units={}
    curid=0
    def get_information(self):
        c=Culture.cultures[self.culture].name
        r=Religion.religions[self.religion].name
        l=Language.languages[self.language].name
        e=Ethnicity.ethnicities[self.ethnicity].name
        return c,r,l,e
    def __init__(self,create_new,loc):
        #Stats in order: Strength, Inventiveness, Attractiveness
        self.stats=[random.randint(0,5),random.randrange(0,5),random.randrange(0,5)]
        self.hp=300
        self.desire=0
        self.zeal=random.randint(0,100)
        self.age=0
        self.language_shift=0
        self.religion_shift=0
        self.culture_shift=0
        if create_new==True:
            word=generate_word()
            w,x,y,z=Culture(),Religion(),Ethnicity(),Language()
            w.name=adjectivize(word).capitalize()
            x.name=combine_fluently(word,"ism").capitalize()
            y.name=adjectivize(word).capitalize()
            z.name=adjectivize(word).capitalize()
            self.culture=w.id
            self.religion=x.id
            self.language=z.id
            self.ethnicity=y.id
        else:
            self.culture=""
            self.religion=""
            self.language=""
            self.ethnicity=""
        self.location=loc
        self.id=population_unit.curid
        nProvince.provinces[loc].population.append(self.id)
        self.typ=random.choice([2,3])
        if nProvince.provinces[loc].typ not in [0,2]:
            self.typ=3
        population_unit.curid+=1
        population_unit.population_units[self.id]=self
        self.overlord=nProvince.provinces[self.location].owner
    def analyse_movement(self):
        changed=False
        if self.typ==2 and nProvince.provinces[self.location].typ in [1,3]:
            self.typ=3
            changed=True
        if self.typ==3 and nProvince.provinces[self.location].typ in [0,2]:
            self.typ=2
            changed=True
        if (self.typ==3 or self.typ==0):
            if self.typ==3:
                goable=copy.copy(nProvince.provinces[self.location].neighbors)
            elif self.typ==0:
                try:
                    goable=copy.copy(Government.governments[self.overlord].territories)
                except:
                    self.typ=2
                    goable=[]
            if len(goable)>0:
                goto=""
                for g in goable:
                    if nProvince.provinces[g].typ==3:
                        goable.remove(g)
                    if nProvince.provinces[g].typ==2:
                        for g in goable:
                            if nProvince.provinces[g].typ==1:
                                goable.remove(g)
                            if nProvince.provinces[g].typ==0:
                                goable.remove(g)
                        break;
                if goto!="":
                    for g in goable:
                        if nProvince.provinces[g].typ==0:
                            for g in goable:
                                if nProvince.provinces[g].typ==1:
                                    goable.remove(g)
                            break;
                if len(goable)>0 and goto!="":
                    goto=random.choice(goable)
                    nProvince.provinces[self.location].population.remove(self.id)
                    self.location=goto
                    nProvince.provinces[self.location].population.append(self.id)
    def reproduce(self):
        choicez=nProvince.provinces[self.location].population
        choices=[]
        for c in choicez:
            if population_unit.population_units[c].typ==4:
                pass
            else:
                choices.append(population_unit.population_units[c])
        if len(choices)>1:
            ratings=[]
            weighed_choices={}
            for c in choices:
                rating=c.total_stats()[2]*c.hp
                ratings.append(rating)
                weighed_choices[rating]=c
            choice=weighed_choices[sorted(ratings)[-1]]
            if (choice.desire>=90 and choice.hp>75) or self.total_stats()[1]>=choice.total_stats()[1]-2:
                own_stats=self.total_stats()
                choice_stats=self.total_stats()
                if own_stats[1]>choice_stats[1]:
                    cult=self.culture
                    lang=self.language
                else:
                    cult=choice.culture
                    lang=choice.language
                if self.zeal>choice.zeal:
                    rel=self.religion
                    gzeal=self.zeal
                else:
                    rel=choice.religion
                    gzeal=choice.zeal
                ethn=random.choice([self.ethnicity,choice.ethnicity])
                statz=[random.choice([self.stats[0],choice.stats[0]]),random.choice([self.stats[1],choice.stats[1]]),random.choice([self.stats[2],choice.stats[2]])]
                if self.typ==choice.typ:
                    typy=self.typ
                elif self.typ==1 or choice.typ==1:
                    typy=1
                elif self.typ==2 and choice.typ==0:
                    typy=0
                elif self.typ==3 or choice.typ==3:
                    typy=3
                elif self.typ==0 and choice.typ!=1:
                    typy=0
                create_custom_pu(cult,rel,lang,ethn,statz,self.location,typy,gzeal-1)
                self.desire=0
                self.hp-=10
                choice.desire=0
                choice.hp-=10
        else:
            create_custom_pu(self.culture,self.religion,self.language,self.ethnicity,self.stats,self.location,self.typ,self.zeal-1)
            self.desire=0
    def travel_distance(self):
        x=self.total_stats()
        if self.hp>=100:
            if x[0]<2:
                return 0
            elif x[1]>=2:
                return int((x[0]*5+x[1]*5))+10
        return 0
    def total_stats(self):
        cultstats=Culture.cultures[self.culture].stats
        relstats=Religion.religions[self.religion].stats
        ethnstats=Ethnicity.ethnicities[self.ethnicity].stats
        invy,atry=Language.languages[self.language].inv,Language.languages[self.language].atr
        stre=self.stats[0]+cultstats[0]+relstats[0]+ethnstats[0]
        inv=self.stats[1]+cultstats[1]+relstats[1]+ethnstats[1]+invy
        atr=self.stats[2]+cultstats[2]+relstats[2]+ethnstats[2]+atry
        return [stre,inv,atr]
    def kill(self):
        if len(nProvince.provinces[self.location].infertile)>0:
            choix=random.choice(nProvince.provinces[self.location].infertile)
            nProvince.provinces[self.location].infertile.remove(choix)
            nProvince.provinces[self.location].fertile.append(choix)
        try:
            Culture.cultures[self.culture].followers-=1
            Culture.cultures[self.culture].check()
        except KeyError:
            pass
        try:
            Religion.religions[self.religion].followers-=1
            Religion.religions[self.religion].check()
        except KeyError:
            pass
        try:
            Ethnicity.ethnicities[self.ethnicity].members-=1
            Ethnicity.ethnicities[self.ethnicity].check()
        except KeyError:
            pass
        try:
            Language.languages[self.language].speakers-=1 
            Language.languages[self.language].check()
        except KeyError:
            pass
        nProvince.provinces[self.location].population.remove(self.id)
        del(population_unit.population_units[self.id])
        del(self)
    def iterate(self):
        try:
            self.overlord=nProvince.provinces[self.location].owner
            self.age+=1
            if self.hp<=0:
                self.typ=4
            if self.typ!=4:
                pu_names=["Citizen","Slave","Tribesman","Nomad"]
                stats=self.total_stats()
                desire_gain=RELU(0.1*stats[0])+0.1
                if len(nProvince.provinces[self.location].population)>=(nProvince.provinces[self.location].building_slots*2):
                    desire_gain=0
                if self.overlord!=None:
                    con_pu_info=Government.governments[self.overlord].culture,Government.governments[self.overlord].religion,Government.governments[self.overlord].language,Government.governments[self.overlord].ethnicity
                    self.desire+=desire_gain
                    if self.language_shift>=100:
                        Government.governments[self.overlord].send_message("A "+pu_names[self.typ]+" Population Unit has picked up the "+Language.languages[con_pu_info[2]].name+" language!")
                        Language.languages[self.language].speakers-=1
                        Language.languages[self.language].check()
                        self.language=con_pu_info[2]
                        Language.languages[con_pu_info[2]].speakers+=1
                        self.language_shift=0
                    if self.culture_shift>=100:
                        Government.governments[self.overlord].send_message("A "+pu_names[self.typ]+" Population Unit has converted to the "+Culture.cultures[con_pu_info[0]].name+" culture!")
                        Culture.cultures[self.culture].followers-=1
                        Culture.cultures[self.culture].check()
                        self.culture=con_pu_info[0]
                        Culture.cultures[con_pu_info[0]].followers+=1
                        self.culture_shift=0
                    if self.religion_shift>=100:
                        Government.governments[self.overlord].send_message("A "+pu_names[self.typ]+" Population Unit has converted to the "+Religion.religions[con_pu_info[1]].name+" religion!")
                        Religion.religions[self.religion].followers-=1
                        Religion.religions[self.religion].check()
                        self.religion=con_pu_info[1]
                        Religion.religions[con_pu_info[1]].followers+=1
                        self.religion_shift=0
                else:
                    self.desire+=desire_gain/2
                    if stats[1]>=3 and (nProvince.provinces[self.location].typ==2 and self.typ==2 and random.randint(1,10000)==1) or (nProvince.provinces[self.location].typ==0 and self.typ==2 and random.randint(1,100000)==1):
                        if nProvince.provinces[self.location].sea!=False:
                            etyp=random.choice([0,1])
                        else:
                            etyp=1
                        g=Government()
                        g.name=nProvince.provinces[self.location].name
                        g.take_territory(self.location,True)
                        g.culture=self.culture
                        g.language=self.language
                        g.ethnicity=self.ethnicity
                        g.religion=self.religion
                        g.cores.append(self.location)
                        self.overlord=g.id
                        Government.governments[g.id]=g
                nProvince.provinces[self.location].stockpile+=(stats[1]*self.hp)//10
                if self.typ==1:
                    self.hp-=1
                if self.hp<=75:
                    self.desire=0
                else:
                    if self.desire>=100:
                        self.desire=100
                        self.reproduce()
                    else:
                        self.analyse_movement()
                if self.age%10==0:
                    if nProvince.provinces[self.location].foodstore>0:
                        nProvince.provinces[self.location].foodstore-=1
                    else:
                        self.desire-=1
                        self.hp-=5
                        if nProvince.provinces[self.location].owner!=None:
                            Government.governments[nProvince.provinces[self.location].owner].send_message("We have population units starving in "+nProvince.provinces[self.location].name+"!")
                if self.overlord!=None:
                    if self.zeal<50:
                        self.religion_shift+=0.05
                    self.culture_shift+=0.05*Government.governments[self.overlord].assimilation_bonus
                    self.language_shift+=((0.05*Government.governments[self.overlord].teaching_bonus)+(0.025*Government.governments[self.overlord].assimilation_bonus))
                    if self.language==Government.governments[self.overlord].language:
                        self.culture_shift+=0.1*Government.governments[self.overlord].assimilation_bonus
                        self.religion_shift+=0.05
                    else:
                        self.culture_shift=0
                        self.religion_shift=0
                    if self.language==Government.governments[self.overlord].language:
                        self.language_shift=0
                    if self.culture==Government.governments[self.overlord].culture:
                        self.culture_shift=0
                    if self.religion==Government.governments[self.overlord].religion:
                        self.religion_shift=0
                    if Government.governments[self.overlord].research[4]==True:
                        nProvince.provinces[self.location].stockpile+=(stats[1]*self.hp)//10
                        if self.typ==1:
                            nProvince.provinces[self.location].stockpile+=(stats[1]*self.hp)//7
                    if self.typ==0:
                        chx=random.randint(0,2)
                        Government.governments[self.overlord].research_progress[chx]+=(0.01*stats[1])
                    if nProvince.provinces[self.location].unrest<10:
                        if "Settlement Effort" in nProvince.provinces[self.location].modifiers:
                            if stats[0]<5+Government.governments[self.overlord].combat_bonus and self.typ==3:
                                self.typ=2
                        if "Civilization Effort" in nProvince.provinces[self.location].modifiers:
                            mininv=3
                            if Government.governments[nProvince.provinces[self.location].owner].focus==4:
                                mininv=1
                            mininv-=Government.governments[self.overlord].teaching_bonus
                            if stats[1]>=mininv and self.typ==2:
                                self.typ=0
                        if "Enslavement Effort" in nProvince.provinces[self.location].modifiers:
                            if self.ethnicity!=Government.governments[nProvince.provinces[self.location].owner].ethnicity and self.typ!=1:
                                stre=stats[0]
                                if self.typ==3:
                                    stre+=1
                                govstr=((nProvince.provinces[self.location].garrison)*100)//population_formula(len(nProvince.provinces[self.location].population))+Government.governments[self.overlord].combat_bonus
                                if Government.governments[nProvince.provinces[self.location].owner].focus==3:
                                    govstr+=3
                                    stre-=1
                                if govstr>stre:
                                    self.typ=1
                        if "Liberation Effort" in nProvince.provinces[self.location].modifiers:
                            if self.hp<=100:
                                self.typ=0
                        if "Assimilation Effort" in nProvince.provinces[self.location].modifiers:
                            if self.culture!=Government.governments[self.overlord].culture:
                                mininv=3
                                if Government.governments[nProvince.provinces[self.location].owner].focus==0:
                                    mininv=1
                                mininv-=Government.governments[self.overlord].assimilation_bonus
                                if stats[1]>=mininv:
                                    self.culture_shift+=mininv+Government.governments[self.overlord].assimilation_bonus
                        if "Conversion Effort" in nProvince.provinces[self.location].modifiers:
                            if self.religion!=Government.governments[self.overlord].religion:
                                zeal=(self.zeal//2)+Religion.religions[self.religion].zeal
                                country_zeal=Religion.religions[Government.governments[self.overlord].religion].zeal
                                if Government.governments[nProvince.provinces[self.location].owner].focus==1:
                                    country_zeal+=10
                                    zeal-=10
                                if country_zeal>zeal:
                                    self.religion_shift+=(country_zeal-zeal)
                        if "Language Teaching" in nProvince.provinces[self.location].modifiers:
                            if self.language!=Government.governments[self.overlord].language:
                                mininv=4
                                if Government.governments[self.overlord].focus==0:
                                    mininv=2
                                mininv-=Government.governments[self.overlord].teaching_bonus
                                if stats[1]>=mininv:
                                    self.language_shift+=mininv
                        if "Ethnic Cleansing" in nProvince.provinces[self.location].modifiers:
                            if self.ethnicity!=Government.governments[nProvince.provinces[self.location].owner].ethnicity and self.typ!=1:
                                stre=stats[0]
                                if self.typ==3:
                                    stre+=1
                                govstr=(((nProvince.provinces[self.location].garrison)*100)//population_formula(len(nProvince.provinces[self.location].population)))+Government.governments[self.overlord].combat_bonus
                                if Government.governments[nProvince.provinces[self.location].owner].focus==3:
                                    govstr+=3
                                    stre-=1
                                govstr+=Government.governments[self.overlord].combat_bonus
                                if govstr>stre:
                                    self.hp-=((govstr-stre)*6)
                                if self.hp<=0:
                                    Government.governments[self.overlord].send_message("A Population Unit of an Inferior Race has just been killed! Hail our master race!")
                                    self.typ=4
            else:
                self.kill()
        except KeyError:
            self.kill()
from province import nProvince,Seazone
from government import *
