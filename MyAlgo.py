import ast
from random import sample, random
from random import randint
import collections
import sys
sys.path.append('.')
from Distractor_Models import Distractor_Model as Distractor_Model
import os
class Distractor_Generator:
    def __init__(self,Dictionary,TopicName,DistractorNumber=4,Flag=False):
        self.__Dictionary=Dictionary
        self.__TopicName=TopicName
        self.__DistractorNumber=DistractorNumber
        self.__Flag=Flag
        self.__Distractor_Model=Distractor_Model(os.getcwd() + '/tmpFinalNoHs/my_w2v_SGFinal_epoch96.model')

    def __Initialization(self, TopicName, NumberOfQuestion, DistractorNumber=4, Entitiy=None, Flag=False):
        file = None
        Mylist = None
        Population = dict()
        Temp = None
        Temp2 = list()
        con = 1
        if (TopicName == "SW"):
            if (Entitiy != None and Flag == True):
                file = open(os.getcwd()+'/DatasetKeyword/Classes_'+self.__TopicName+'.txt')
                Mylist = file.read()
                Mylist = ast.literal_eval(Mylist)
                for Key in Entitiy:
                    Temp = Mylist.get(Key)
                    Population.update({Key + " " + con.__str__(): Temp})
                    con = con + 1
            elif (Entitiy != None):
                file = open(os.getcwd()+'/DatasetKeyword/GeneralClass_'+self.__TopicName+'.txt')
                Mylist = file.read()
                Mylist = ast.literal_eval(Mylist)
                Ent2 = Mylist.keys()
                NewEnt = list()
                for key in Entitiy:
                    tem = key.lower()
                    tem = tem.split()
                    check = False
                    for K in Ent2:
                        tem2 = K.lower()
                        for t in tem:
                            if tem2.__contains__(t):
                                check = True
                                NewEnt.append(K)
                                break
                        if check:
                            break
                    if check == False:
                        NewEnt.append("others")
                for i in range(NewEnt.__len__()):
                    Temp = Mylist.get(NewEnt[i])
                    Temp2.clear()
                    if (DistractorNumber >= Temp.__len__()):
                        print("MoreThanDistractor")
                    else:
                        for m in range(6):
                            x=sample(Temp, DistractorNumber)
                            Temp2.append(x)
                    Temp2.append(Temp.copy())
                    Population.update({Entitiy[i] + " " + con.__str__(): Temp2.copy()})
                    con = con + 1
            else:
                file = open(os.getcwd()+'/DatasetKeyword/General_'+self.__TopicName+'.txt')
                Mylist = file.read()
                Mylist = ast.literal_eval(Mylist)
                for i in range(NumberOfQuestion):
                    Temp2.clear()
                    for n in range(8):
                        Temp2.append(sample(Mylist,DistractorNumber))
                    #Not efficient Part mmkn ab2a a3adlo b3adan
                    Temp2.append(Mylist)
                    Population.update({"Question "+i.__str__(): Temp2.copy()})
        #end IF SW Topic
        elif (TopicName == "Mining"):
            if (Entitiy != None and Flag == True):
                file = open(os.getcwd()+'/DatasetKeyword/Classes_'+self.__TopicName+'.txt')
                Mylist = file.read()
                Mylist = ast.literal_eval(Mylist)
                for Key in Entitiy:
                    Temp = Mylist.get(Key)
                    Population.update({Key + " " + con.__str__(): Temp})
                    con = con + 1
            elif (Entitiy != None):
                file = open(os.getcwd()+'/DatasetKeyword/GeneralClass_'+self.__TopicName+'.txt')
                Mylist = file.read()
                Mylist = ast.literal_eval(Mylist)
                Ent2 = Mylist.keys()
                NewEnt = list()
                for key in Entitiy:
                    tem = key.lower()
                    tem = tem.split()
                    check = False
                    for K in Ent2:
                        tem2 = K.lower()
                        for t in tem:
                            if tem2.__contains__(t):
                                check = True
                                NewEnt.append(K)
                                break
                        if check:
                            break
                    if check == False:
                        NewEnt.append("others")
                for i in range(NewEnt.__len__()):
                    Temp = Mylist.get(NewEnt[i])
                    Temp2.clear()
                    if (DistractorNumber >= Temp.__len__()):
                        print("MoreThanDistractor")
                    else:
                        for m in range(6):
                            x=sample(Temp, DistractorNumber)
                            Temp2.append(x)
                    Temp2.append(Temp.copy())
                    Population.update({Entitiy[i] + " " + con.__str__(): Temp2.copy()})
                    con = con + 1
            else:
                file = open(os.getcwd()+'/DatasetKeyword/General_'+self.__TopicName+'.txt')
                Mylist = file.read()
                Mylist = ast.literal_eval(Mylist)
                for i in range(NumberOfQuestion):
                    Temp2.clear()
                    for n in range(8):
                        Temp2.append(sample(Mylist,DistractorNumber))
                    #Not efficient Part mmkn ab2a a3adlo b3adan
                    Temp2.append(Mylist)
                    Population.update({"Question "+i.__str__(): Temp2.copy()})
            #End Of Datamining Topic
        else:
            return 0
        return Population
    #Population [[]] PridicitedList [] return [[]]
    def __Compare_PridectedWord(self, Population, pridictedList):
        Temp=list()
        for Word in pridictedList:
            for smalllist in Population:
                for element in smalllist:
                    if element.__contains__(Word.__str__()):
                        if smalllist not in Temp:
                            Temp.append(smalllist)
                            break
        if(Temp.__len__()==0):
            for Word in pridictedList:
                Temp.append([Word])
        return Temp
    #pop {Key:[[]],key...} listKw[]
    def __Genatic_algorithm(self, Population :dict, listOfTargetKeywords, Contexts, counts):
        OldPopulation=Population.copy()
        Population_distance=list()
        OldPopulation_distance=list()
        # Each population key is a Population
        con=0
        Indexs=list()
        for Key in Population:
            check = False
            r=0
            Mycount = counts
            for mycount in range(Mycount):
                r=r+1
                tempIndex = list()
                #print(Population.get(Key).__len__())
                for List in Population.get(Key):
                    if check:
                        check=True
                        break
                    temp=self.__Distractor_Model.CheckAndDetermineKeyword([listOfTargetKeywords[con]])
                    temp2=self.__Distractor_Model.CheckAndDetermineKeyword(List)#[[]]
                    sumDistance=0
                    if temp2.__len__() <= self.__DistractorNumber:
                        for list2 in temp2:
                            Distance = list()
                            if temp[0][0] == 0:
                                TempPopulation=dict()
                                PridictionOutput = self.__Distractor_Model.Pridication_Context([Contexts[con]])
                                #print('pridiction ',PridictionOutput)
                                TempPopulation.update({Key: self.__Distractor_Model.CheckAndDetermineKeyword(Population.get(Key)[Population.get(Key).__len__() - 1])})
                                Reslut = self.__Compare_PridectedWord(TempPopulation.get(Key).copy(), PridictionOutput)
                                #print(Reslut)
                                rand = randint(0, Reslut.__len__() - 1)
                                for i in range(Reslut.__len__()):
                                    if i != rand:
                                        Distance.append(
                                            self.__Distractor_Model.Calculate_Distances(Reslut[rand], Reslut[i]))
                                dis = list()
                                #print(Reslut)
                                for i in range(Distance.__len__()):
                                    dis.append(Distance.index(min(Distance)))
                                    Distance[Distance.index(min(Distance))]=5
                                #print(Distance)
                                #print(dis)
                                newpop=list()
                                for K in Reslut:
                                    tem=''
                                    azon=True
                                    for N in K:
                                        if azon:
                                            azon=False
                                            tem=tem+N
                                        else:
                                            tem=tem+' '+N
                                    newpop.append(tem)
                                newpop2=list()
                                newpop2.append(newpop)
                                newpop2.append(dis)
                                newpop2.append(Population.get(Key)[Population.get(Key).__len__()-1])
                                Population.update({Key: newpop2.copy()})
                                check = True
                                break
                            else:
                                # print('temp[0] is ')
                                # print(temp[0])
                                # print('temp 2 is ')
                                # print(temp2[list2])
                                sumDistance = sumDistance + self.__Distractor_Model.Calculate_Distances(temp[0], list2)
                        OldPopulation_distance.append(sumDistance/temp2.__len__())#6
                    #fy condition na2as hana lw distractor akber mn 3adad al keywords

                #print('number of old')
                #print(OldPopulation_distance)
                #print(temp2.__len__())

                if check:
                    OldPopulation_distance.clear()
                    check=False
                    break
                tempold=OldPopulation_distance.copy()
                for i in range((round(OldPopulation_distance.__len__()/2)-1)):
                    tempIndex.append(tempold.index(min(tempold)))
                    tempold[tempold.index(min(tempold))] = 5
                #random Selection
                #print("Index is " ,tempIndex)
                for i in range(round(OldPopulation_distance.__len__()/2)-1):
                    x=randint(0,OldPopulation_distance.__len__()-1)
                    #print(x)
                    if x not in tempIndex:
                        tempIndex.append(x)
                #Cross Over
                NewPopulation=list()
                #print(Population.get(Key))
                for i in tempIndex:
                    NewPopulation.append(Population.get(Key)[i].copy())
                co=0
                #print(NewPopulation.__len__())
                #print(OldPopulation.__len__())
                while NewPopulation.__len__() < Population.get(Key).__len__()-1:
                    co=co+1
                    #print(co)
                    Male=randint(0,NewPopulation.__len__()-1)
                    Female = randint(0, NewPopulation.__len__() - 1)
                    if Male != Female:
                        NewPopulation[Male]=self.__check_Elemenets(NewPopulation[Male].copy(), temp[0].copy(), temp2.copy())
                        NewPopulation[Female]=self.__check_Elemenets(NewPopulation[Female].copy(), temp[0].copy(), temp2.copy())
                        Male = NewPopulation[Male].copy()
                        Female = NewPopulation[Female].copy()
                        half = round(Male.__len__() / 2)
                        Child = Male[:half].copy() + Female[half:].copy()
                        # print('child without mutation is ',Child)
                        Child = self.__Mutation(Child.copy(), temp2)
                        Child=self.__check_Elemenets(Child.copy(), temp[0].copy(), temp2.copy())
                        # print('child with mutation is ',Child)
                        NewPopulation.append(Child.copy())

                temp2.clear()
                #print('The New Population is ',NewPopulation)

                for Pop in NewPopulation:
                    temp2 = self.__Distractor_Model.CheckAndDetermineKeyword(Pop)
                    sumDistance = 0
                    for list2 in temp2:
                        sumDistance = sumDistance + self.__Distractor_Model.Calculate_Distances(temp[0], list2)
                    Population_distance.append(sumDistance / temp2.__len__())
                tempold.clear()
                tempold = Population_distance.copy()
                tempIndex.clear()
                for i in range((round(Population_distance.__len__() / 2))):
                    tempIndex.append(tempold.index(min(tempold)))
                    tempold[tempold.index(min(tempold))] = 5
                # random Selection
                if mycount == Mycount-1:
                    #print("Index is ", tempIndex)
                    #print("and distance is ", Population_distance)
                    NewPopulation.append(tempIndex)
                NewPopulation.append(Population.get(Key)[Population.get(Key).__len__()-1])
                Population.update({Key:NewPopulation})
                #evaluation the Populations
                #print(mycount)
                #print('evalution is ',self.evaluation_Algorithm(OldPopulation_distance,Population_distance))
                OldPopulation_distance.clear()
                Population_distance.clear()
            con=con+1
        return Population


    def __evaluation_Algorithm(self, oldPopulationDistance, NewPopulationDistance):
        #if positive then distance increase if nigative then distance decrease
        return sum(NewPopulationDistance)/NewPopulationDistance.__len__() - sum(oldPopulationDistance)/oldPopulationDistance.__len__()

#population [] Used To Check If Target Word Is Found in The Population Or Not if it's it change it From The OrgPopulation
    def __check_Elemenets(self, Population, TargetWord, orgPopulation):
        temp=''
        cop=0
        for i in TargetWord:
            if cop==0:
                temp=temp+i
            else:
                temp=temp+' '+i
        if temp in Population:
            #print('targ', temp)
            co=0
            while True:
                x = randint(0, orgPopulation.__len__() - 1)
                # print(x)
                # print(orgPopulation)
                element = orgPopulation[x]
                k = ''
                for i in element:
                    if (co == 0):
                        k = k + i
                        co = co + 1
                    else:
                        k = k + ' ' + i
                if k != TargetWord:
                    #print("condition al gdyd", temp, "   ", k)
                    Population.pop(Population.index(temp))
                    Population.append(k)
                    #print('popop' , Population)
                    break
        return  Population


    def __Mutation(self, Child, orgPopulation):
        mutedChild=list()
        check=True
        for word in Child:
            if word in mutedChild :
                #print('muted is ',mutedChild)
                co=0
                while True:
                    check=False
                    x=randint(0,orgPopulation.__len__()-1)
                    #print(x)
                    #print(orgPopulation)
                    element=orgPopulation[x]
                    k=''
                    #print('my element is ',element)
                    for i in element:
                        if (co == 0):
                            k=k+i
                            co=co+1
                        else:
                            k=k+' '+i
                    if k != word:
                        #print("condition al l3na",word ,"   ",k)
                        mutedChild.append(k)
                        break
            else:
                mutedChild.append(word)
        if check:
            if 0.15 > random():
                x = randint(0, orgPopulation.__len__() - 1)
                element=orgPopulation[x]
                k=''
                co=0
                for i in element:
                    if (co == 0):
                        k = k + i
                        co = co + 1
                    else:
                        k = k + ' ' + i
                if k not in mutedChild:
                    #print(k)
                    #print(mutedChild)
                    x= randint(0,mutedChild.__len__()-1)
                    mutedChild.pop(x)
                    mutedChild.append(k)
                    #print('new element i hold it is ',k)


        #print('the muttt',mutedChild)
        return mutedChild

    def RunAlgo(self):
        Temp3=list()
        Temp2=list()
        con=0
        RemoveElemenets=list()
        Entitiy = list()
        for Key in self.__Dictionary:
            x = self.__Dictionary.get(Key)
            if x.__len__() > 2:
                Entitiy.append(x[2])
            else:
                Entitiy = None
                break
        Populations = self.__Initialization(self.__TopicName, self.__Dictionary.__len__(), self.__DistractorNumber, Entitiy, self.__Flag)
        if Populations ==0:
            return 0
        #get the Keywords and context from Dicitionary
        for Key in self.__Dictionary:
            Temp3.append(self.__Dictionary.get(Key)[1].lower())
            Temp2.append(self.__Dictionary.get(Key)[0])
        Indexs = list()
        TempPopulation=dict()
        #print(Temp3)
        #print(Temp2)
        if self.__Flag == True:
            Temp = self.__Distractor_Model.CheckAndDetermineKeyword(Temp3)
            #print(Populations)
            for Key in Populations:
                Distance = list()
                TempPopulation.update({Key:self.__Distractor_Model.CheckAndDetermineKeyword(Populations.get(Key))})
                if Temp[con][0] == 0:
                    Temp[con][0]=Temp3[con]
                    PridictionOutput=self.__Distractor_Model.Pridication_Context([Temp2[con]])
                    #print('the pridicted is ',PridictionOutput)
                    #print('the keyword is ',TempPopulation.get(Key))
                    Reslut=self.__Compare_PridectedWord(TempPopulation.get(Key), PridictionOutput)
                    rand=randint(0,Reslut.__len__()-1)
                    for i in range(Reslut.__len__()):
                        if i != rand:
                            if collections.Counter(Reslut[rand]) == collections.Counter(Reslut[i]):
                                continue
                            Distance.append(self.__Distractor_Model.Calculate_Distances(Reslut[rand], Reslut[i]))

                else:
                    tempcont=0
                    for smallList in TempPopulation.get(Key):
                        if(collections.Counter(Temp[con]) == collections.Counter(smallList)):
                            RemoveElemenets.append([Key,tempcont])
                        else:
                            #print('the smallest list is ', smallList, ' and the term is ', Temp[con])
                            Distance.append(self.__Distractor_Model.Calculate_Distances(Temp[con], smallList))
                            tempcont = tempcont + 1
                dis=list()
                #print(Populations.get(Key))
                #print(Distance)
                for i in range(Distance.__len__()):
                    dis.append(Distance.index(min(Distance)))
                    Distance[Distance.index(min(Distance))]=5
#                    #print(Distance)
                Distance.clear()
                Indexs.append(dis)
                #print(Indexs)
                #Indexs of [[]] each list contain the best distractor for the same index question
                con=con+1
            #Extract The Distractors and but them in the Dictionary

            conRemove=0
            Temp2.clear()
            #print(RemoveElemenets)
            con2 = 0
            for key in Populations:
                l=Populations.get(key)
                con=0
                t = list()
                t.append(Temp[con2][0])
                for i in range(Indexs[con2].__len__()):
                    #print(Temp[con2])
                    try:
                        if key in RemoveElemenets[conRemove]:
                            l.pop(RemoveElemenets[conRemove][1])
                            conRemove = conRemove + 1
                    except:
                        pass
                    t.append(l[Indexs[con2][con]])
                    con=con+1
                    if self.__DistractorNumber+1 == t.__len__():
                        break
                con2=con2+1
                if self.__DistractorNumber >= l.__len__():
                    t.append('all the Previous')
                    t.append('Non of the above')
                Temp2.append(t)
            con=0
            #print(Temp2)
            for key in self.__Dictionary:
                Temp2[con].append(self.__Dictionary.get(key)[0])
                self.__Dictionary.update({key:Temp2[con]})
                con=con+1

        else:
            con=0
            Mylist=list()
            if Populations.get(list(Populations.keys())[0]).__len__() <= 3:
                for Key in Populations:
                    if Temp3[con] in Populations.get(Key)[0]:
                        Populations.get(Key)[0].pop(Populations.get(Key)[0].index(Temp3[con]))
                    Populations.get(Key)[0].insert(0, Temp3[con])
                    Populations.get(Key)[0].append('all the Previous')
                    Populations.get(Key)[0].append('Non of the above')
                    Populations.get(Key)[0].append(Temp2[con])
                    con=con+1
                    Populations.update({Key:Populations.get(Key)[0]})

                return Populations
            if Entitiy == None:
                pop=self.__Genatic_algorithm(Populations, Temp3, Temp2, 40)
            else:
                pop = self.__Genatic_algorithm(Populations, Temp3, Temp2, 30)
            #print(pop)
            for Key in pop:
                Mylist.append([Temp3[con]])
                check=False
                for individual in pop.get(Key)[pop.get(Key).__len__()-2]:
                    if pop.get(Key).__len__() <=3:
                        if pop.get(Key)[0][individual] not in Mylist[con]:
                            Mylist[con].append(pop.get(Key)[0][individual])

                    else:
                        for L in pop.get(Key)[individual]:
                            if L not in Mylist[con]:
                                Mylist[con].append(L)
                            if Mylist[con].__len__() == self.__DistractorNumber + 1:
                                break
                        #maskt hna al list bta3t al indexs al afdal bnzba ly a5er lfa
                    if Mylist[con].__len__() == self.__DistractorNumber+1:
                        break

                con=con+1
            con=0
            for Key in self.__Dictionary:
                Mylist[con].append(self.__Dictionary.get(Key)[0])
                self.__Dictionary.update({Key:Mylist[con]})
                con=con+1

        return self.__Dictionary


# -------------------------------------------------------------------------------DataMining Test --------------------------------------------------------------------------------------------------------------#
''''
ex=dict({'question1':['A neural network is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.','neural network','unsupervised learning']
    ,'question2':['classification is a systematic grouping of observations into categories','classification','supervised learning'],
    'question3':['supervised learning is the machine learning task of learning a function that maps an input to an output based on example input-output pairs','supervised learning','supervised learning']})
print("The  Genatic ALgorithm result with specific Entity ------------------------------------------------------------------------------------------------")
result=Distractor_Generator(Dictionary=ex,TopicName='DataMining',DistractorNumber=4,Flag=True)
r=result.RunAlgo()
for key in r:
    c = 0
    a = 'a'
    s=''
    k=r.get(key)[0]
    k=k.replace("_"," ")
    for l in r.get(key):
        if c != r.get(key).__len__()-1:
            l=l.replace('_',' ')
            s=s+"  "+a +")  "+l
            a=chr(ord(a)+1)
        else:
            l=l.replace(k,"--------")
            print(l)
        c=c+1

    print(s)



ex2=dict({'question1':['A neural network is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.','neural network','unsupervised learning']
    ,'question2':['classification is a systematic grouping of observations into categories','classification','Supervised learning'],
    'question3':['supervised learning is the machine learning task of learning a function that maps an input to an output based on example input-output pairs','supervised learning','Supervised learning']})
result2=Distractor_Generator(Dictionary=ex2,TopicName='DataMining',DistractorNumber=4,Flag=False)
r2=result2.RunAlgo()
print("The  Genatic ALgorithm result with General Entity ------------------------------------------------------------------------------------------------")
for key in r2:
    c = 0
    a = 'a'
    s = ''
    k = r2.get(key)[0]
    k = k.replace("_", " ")
    for l in r2.get(key):
        if c != r2.get(key).__len__() - 1:
            l = l.replace('_', ' ')
            s = s + "  " + a + ")  " + l
            a = chr(ord(a) + 1)
        else:
            l = l.replace(k, "--------")
            print(l)
        c = c + 1

    print(s)


ex3=dict({'question1':['A neural network is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.','neural network']
    ,'question2':['classification is a systematic grouping of observations into categories','classification'],
    'question3':['supervised learning is the machine learning task of learning a function that maps an input to an output based on example input-output pairs','supervised learning']})
result3=Distractor_Generator(Dictionary=ex3,TopicName='DataMining',DistractorNumber=4,Flag=False)
r3=result3.RunAlgo()
print(r3)
print("The  Genatic ALgorithm result with No Entity ------------------------------------------------------------------------------------------------")
for key in r3:
    c = 0
    a = 'a'
    s=''
    k=r3.get(key)[0]
    k=k.replace("_"," ")
    for l in r3.get(key):
        if c != r3.get(key).__len__()-1:
            l=l.replace('_',' ')
            s=s+"  "+a +")  "+l
            a=chr(ord(a)+1)
        else:
            l=l.replace(k,"--------")
            print(l)
        c=c+1

    print(s)

ex4=dict({'question1':['A ay7aga is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.','ay7aga','unsupervised learning']
    ,'question2':['classification is a systematic grouping of ay7aga into categories','ay7aga','Supervised learning'],
    'question3':['ay7aga is the machine learning task of learning a function that maps an input to an output based on example input-output pairs','ay7aga','Supervised learning']})
result4=Distractor_Generator(Dictionary=ex4,TopicName='DataMining',DistractorNumber=4,Flag=True)
r4=result4.RunAlgo()
print("The  Genatic ALgorithm result with Entity And Pridiction of Unknown Keyword from Context ------------------------------------------------------------------------------------------------")
for key in r4:
    c = 0
    a = 'a'
    s=''
    k=r4.get(key)[0]
    k=k.replace("_"," ")
    for l in r4.get(key):
        if c != r4.get(key).__len__()-1:
            l=l.replace('_',' ')
            s=s+"  "+a +")  "+l
            a=chr(ord(a)+1)
        else:
            l=l.replace(k,"--------")
            print(l)
        c=c+1

    print(s)

ex5=dict({'question1':['A ay7aga is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.','ay7aga','unsupervised learning']
    ,'question2':['ay7aga is a systematic grouping of observations into categories','ay7aga','Supervised learning'],
    'question3':['ay7aga is the machine learning task of learning a function that maps an input to an output based on example input-output pairs','ay7aga','Supervised learning']})
result5=Distractor_Generator(Dictionary=ex5,TopicName='DataMining',DistractorNumber=4,Flag=False)
r5=result5.RunAlgo()
print("The  Genatic ALgorithm result with General Entity and Pridiction of Unknown Keyword from Context------------------------------------------------------------------------------------------------")
for key in r5:
    c = 0
    a = 'a'
    s=''
    k=r5.get(key)[0]
    k=k.replace("_"," ")
    for l in r5.get(key):
        if c != r5.get(key).__len__()-1:
            l=l.replace('_',' ')
            s=s+"  "+a +")  "+l
            a=chr(ord(a)+1)
        else:
            l=l.replace(k,"--------")
            print(l)
        c=c+1

    print(s)

ex6=dict({'question1':['A ay7aga is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.','ay7aga']
    ,'question2':['ay7aga is a systematic grouping of observations into categories','ay7aga'],
    'question3':['ay7aga is the machine learning task of learning a function that maps an input to an output based on example input-output pairs','a7aga']})
result5=Distractor_Generator(Dictionary=ex6,TopicName='DataMining',DistractorNumber=4,Flag=False)
r6=result5.RunAlgo()
print("The  Genatic ALgorithm result with No Entity and Pridiction of Unknown Keyword from Context------------------------------------------------------------------------------------------------")
for key in r6:
    c = 0
    a = 'a'
    s=''
    k=r6.get(key)[0]
    k=k.replace("_"," ")
    for l in r6.get(key):
        if c != r6.get(key).__len__()-1:
            l=l.replace('_',' ')
            s=s+"  "+a +")  "+l
            a=chr(ord(a)+1)
        else:
            l=l.replace(k,"--------")
            print(l)
        c=c+1

    print(s)


# -------------------------------------------------------------------------------SW Test --------------------------------------------------------------------------------------------------------------#


ex=dict({'question1':['package diagram shows the arrangement and organization of model elements in middle to large scale project that can be used to show both structure and dependencies between sub-systems or modules.','Package diagram','static diagrams']
    ,'question2':['requirements validation makes sure that the requirements written in software requirements specification (SRS) must be complete and consistent and are according to the customer’s needs.','Requirements validation','requirements engineering process activities'],
    'question3':['adapter pattern works as a bridge between two incompatible interfaces. This type of design pattern comes under structural pattern as this pattern combines the capability of two independent interfaces.','Adapter pattern','structural pattern']
         ,'question4':['builder pattern builds a complex object using simple objects and using a step by step approach. This type of design pattern comes under creational pattern','creational pattern','design pattern']})
print("The  Genatic ALgorithm result with specific Entity ------------------------------------------------------------------------------------------------")
result=Distractor_Generator(Dictionary=ex,TopicName='SW',DistractorNumber=4,Flag=True)
r=result.RunAlgo()
for key in r:
    c = 0
    a = 'a'
    s=''
    k=r.get(key)[0]
    k=k.replace("_"," ")
    for l in r.get(key):
        if c != r.get(key).__len__()-1:
            l=l.replace('_',' ')
            s=s+"  "+a +")  "+l
            a=chr(ord(a)+1)
        else:
            l=l.replace(k,"--------")
            print(l)
        c=c+1

    print(s)



ex2=dict({'question1':['package diagram shows the arrangement and organization of model elements in middle to large scale project that can be used to show both structure and dependencies between sub-systems or modules.','Package diagram','static diagrams']
    ,'question2':['requirements validation makes sure that the requirements written in software requirements specification (SRS) must be complete and consistent and are according to the customer’s needs.','Requirements validation','requirements engineering process activities'],
    'question3':['adapter pattern works as a bridge between two incompatible interfaces. This type of design pattern comes under structural pattern as this pattern combines the capability of two independent interfaces.','Adapter pattern','structural pattern']
         ,'question4':['builder pattern builds a complex object using simple objects and using a step by step approach. This type of design pattern comes under creational pattern','creational pattern','design pattern']})
result2=Distractor_Generator(Dictionary=ex2,TopicName='SW',DistractorNumber=4,Flag=False)
r2=result2.RunAlgo()
print("The  Genatic ALgorithm result with General Entity ------------------------------------------------------------------------------------------------")
for key in r2:
    c = 0
    a = 'a'
    s = ''
    k = r2.get(key)[0]
    k = k.replace("_", " ")
    for l in r2.get(key):
        if c != r2.get(key).__len__() - 1:
            l = l.replace('_', ' ')
            s = s + "  " + a + ")  " + l
            a = chr(ord(a) + 1)
        else:
            l = l.replace(k, "--------")
            print(l)
        c = c + 1

    print(s)


ex3=dict({'question1':['package diagram shows the arrangement and organization of model elements in middle to large scale project that can be used to show both structure and dependencies between sub-systems or modules.','Package diagram']
    ,'question2':['requirements validation makes sure that the requirements written in software requirements specification (SRS) must be complete and consistent and are according to the customer’s needs.','Requirements validation'],
    'question3':['adapter pattern works as a bridge between two incompatible interfaces. This type of design pattern comes under structural pattern as this pattern combines the capability of two independent interfaces.','Adapter pattern']
         ,'question4':['builder pattern builds a complex object using simple objects and using a step by step approach. This type of design pattern comes under creational pattern','creational pattern']})
result3=Distractor_Generator(Dictionary=ex3,TopicName='SW',DistractorNumber=4,Flag=False)
r3=result3.RunAlgo()
print(r3)
print("The  Genatic ALgorithm result with No Entity ------------------------------------------------------------------------------------------------")
for key in r3:
    c = 0
    a = 'a'
    s=''
    k=r3.get(key)[0]
    k=k.replace("_"," ")
    for l in r3.get(key):
        if c != r3.get(key).__len__()-1:
            l=l.replace('_',' ')
            s=s+"  "+a +")  "+l
            a=chr(ord(a)+1)
        else:
            l=l.replace(k,"--------")
            print(l)
        c=c+1

    print(s)

ex4=dict({'question1':['package diagram shows the arrangement and organization of ay7aga elements in middle to large scale project that can be used to show both structure and dependencies between sub-systems or modules.','ay7aga','static diagrams']
    ,'question2':['requirements validation makes sure that the requirements written in ay7aga specification (SRS) must be complete and consistent and are according to the customer’s needs.','ay7aga','requirements engineering process activities'],
    'question3':['adapter pattern works as a bridge between two incompatible ay7aga. This type of design pattern comes under structural pattern as this pattern combines the capability of two independent interfaces.','ay7aga','structural pattern']
         ,'question4':['builder pattern builds a complex object using simple objects and using a step by step approach. This type of ay7aga comes under creational pattern','ay7aga','design pattern']})
result4=Distractor_Generator(Dictionary=ex4,TopicName='SW',DistractorNumber=4,Flag=True)
r4=result4.RunAlgo()
print("The  Genatic ALgorithm result with Entity And Pridiction of Unknown Keyword from Context ------------------------------------------------------------------------------------------------")
for key in r4:
    c = 0
    a = 'a'
    s=''
    k=r4.get(key)[0]
    k=k.replace("_"," ")
    for l in r4.get(key):
        if c != r4.get(key).__len__()-1:
            l=l.replace('_',' ')
            s=s+"  "+a +")  "+l
            a=chr(ord(a)+1)
        else:
            l=l.replace(k,"--------")
            print(l)
        c=c+1

    print(s)

ex5=dict({'question1':['ay7aga shows the arrangement and organization of model elements in middle to large scale project that can be used to show both structure and dependencies between sub-systems or modules.','ay7aga','static diagrams']
    ,'question2':['requirements validation makes sure that the requirements written in ay7aga specification (SRS) must be complete and consistent and are according to the customer’s needs.','ay7aga','requirements engineering process activities'],
    'question3':['adapter pattern works as a bridge between two incompatible ay7aga. This type of design pattern comes under structural pattern as this pattern combines the capability of two independent interfaces.','ay7aga','structural pattern']
         ,'question4':['builder pattern builds a complex object using simple objects and using a step by step approach. This type of ay7aga comes under creational pattern','ay7aga','design pattern']})
result5=Distractor_Generator(Dictionary=ex5,TopicName='SW',DistractorNumber=4,Flag=False)
r5=result5.RunAlgo()
print("The  Genatic ALgorithm result with General Entity and Pridiction of Unknown Keyword from Context------------------------------------------------------------------------------------------------")
for key in r5:
    c = 0
    a = 'a'
    s=''
    k=r5.get(key)[0]
    k=k.replace("_"," ")
    for l in r5.get(key):
        if c != r5.get(key).__len__()-1:
            l=l.replace('_',' ')
            s=s+"  "+a +")  "+l
            a=chr(ord(a)+1)
        else:
            l=l.replace(k,"--------")
            print(l)
        c=c+1

    print(s)

ex6=dict({'question1':['ay7aga shows the arrangement and organization of model elements in middle to large scale project that can be used to show both structure and dependencies between sub-systems or modules.','ay7aga']
    ,'question2':['requirements validation makes sure that the requirements written in ay7aga specification (SRS) must be complete and consistent and are according to the customer’s needs.','ay7aga'],
    'question3':['adapter pattern works as a bridge between two incompatible ay7aga. This type of design pattern comes under structural pattern as this pattern combines the capability of two independent interfaces.','ay7aga']
         ,'question4':['builder pattern builds a complex object using simple objects and using a step by step approach. This type of ay7aga comes under creational pattern','ay7aga']})

print (ex6)
result5=Distractor_Generator(Dictionary=ex6,TopicName='SW',DistractorNumber=4,Flag=False)
r6=result5.RunAlgo()
print(r6)
print("The  Genatic ALgorithm result with No Entity and Pridiction of Unknown Keyword from Context------------------------------------------------------------------------------------------------")
for key in r6:
    c = 0
    a = 'a'
    s=''
    k=r6.get(key)[0]
    k=k.replace("_"," ")
    for l in r6.get(key):
        if c != r6.get(key).__len__()-1:
            l=l.replace('_',' ')
            s=s+"  "+a +")  "+l
            a=chr(ord(a)+1)
        else:
            l=l.replace(k,"--------")
            print(l)
        c=c+1

    print(s)

'''