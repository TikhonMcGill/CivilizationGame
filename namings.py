import random
vowels=["a","e","i","o","u"] #Vowels
consonants=["b","c","d","f","g","h","j","k","l","m","n","p","r","s","t","v"] #Most used consonants
rconsonants=["q","x","y","w","z"] #Consonants that will be used more rarely so that generated words don't sound as unpleasant
cconsonants=["ch","kh","zh","sh","ph","sp","st","ss","ll","mm","qu","cl","kr"] #Combinations of consonants
cvowels=["ae","ea","ee","ie","ou","au"] #Combinations of vowels
words=[]
def RELU(value):
    if value<0:
        return 0
    return value
def generate_word():
    global words
    length=random.randint(3,6) #Gets length between 3 and 6
    typ=random.choice([True,False])
    output="" #The string to which letters will be added
    for x in range(length):
        #This loop will add a letter to the output, alternating between vowels and consonants
        if typ==True:
            output+=random.choice(consonants+consonants+consonants+rconsonants+cconsonants)
        else:
            output+=random.choice(vowels+vowels+vowels+vowels+cvowels)
        typ = not typ
    if output in words:
        output=generate_word()
    words.append(output)
    return output
def combine_fluently(word1,word2):
    #This function combines two words such that they sound fluent, e.g. combining the word box and cat won't give boxcat but e.g. bocat or boxat which would "sound" better
    if word2[0] in consonants and word1[-1] in consonants:
        return random.choice([word1[:-1]+word2,word1+word2[1:]])
    if word2[0] in vowels and word1[-1] in vowels:
        return random.choice([word1[:-1]+word2,word1+word2[1:]])
    return word1+word2
def adjectivize(word):
    #This function turns a word into an adjective, e.g. to use as a demonym for a country
    return combine_fluently(word,random.choice(["an","ese","i","er","ish"]))
