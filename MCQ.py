import os
import ast
import sys
import logging


sys.path.append('.')
from Question import Questions as Question
from MyAlgo import Distractor_Generator as Distractor
class MCQ(Question):
    def __init__(self,Content, diff, dic, Topic, NumberofDistructor=4):
        self.diff = diff
        self.dic = dic
        self.Number = NumberofDistructor
        self.Topic = Topic
        super().__init__(Domain=Topic,Content=Content,QuestionType="MCQ")

    def __convert(self, dic):
        for key in dic:
            x = dic.get(key).pop(2)
            dic.get(key).append(x.lower())
        return dic

    def __DetermineApproach(self, dic, topic):
        file = open(os.getcwd() + '/DatasetKeyword/' + topic + '_lab.txt')
        Mylist = file.read()
        Mylist = ast.literal_eval(Mylist)
        dic1 = dict()
        dic2 = dict()
        for key in dic:
            if dic.get(key)[2] in Mylist:
                dic1[key] = dic.get(key)
            else:
                dic2[key] = dic.get(key)
        return dic1, dic2

    def __divdedDic(self, dic):
        dic1 = dict()
        dic2 = dict()
        for key in dic:
            if (dic.get(key).__len__() < 3):
                dic2[key] = dic.get(key)
            else:
                dic1[key] = dic.get(key)
        return dic1, dic2

    def __RemoveUnimportentThings(self,dic):
        for Key in dic:
            c=0
            for i in range(dic.get(Key).__len__()):
                if c == dic.get(Key).__len__()-1:
                    break
                dic.get(Key)[c]=dic.get(Key)[c].replace('_',' ')
                c=c+1
        return dic
    def __ButBlankSpace(self,dic):
        for Key in dic:
            dic.get(Key)[dic.get(Key).__len__() - 1]=dic.get(Key)[dic.get(Key).__len__()-1].lower()
            dic.get(Key)[dic.get(Key).__len__()-1]=dic.get(Key)[dic.get(Key).__len__()-1].replace(dic.get(Key)[0],'---------',1)
        return dic
    def RunAlgorithm(self,Check=True):
        dicGClass = dict()
        dicClass = dict()
        dicNoClass = dict()
        Output = dict()
        dicGClass, dicNoClass = self.__divdedDic(self.dic)
        dicGClass=self.__convert(dicGClass)
        if (self.diff.lower() == "h"):
            dicClass, dicGClass = self.__DetermineApproach(dicGClass,'Mining')
        if (len(dicClass) > 0):
            try:
                Dist = Distractor(Dictionary=dicClass, TopicName=self.Topic, DistractorNumber=self.Number, Flag=True)
                result=Dist.RunAlgo()
                for key in result:
                    Output[key] = result.get(key)
            except:
                logging.error(sys.exc_info()[0])
                return 0

        if (len(dicGClass) > 0):
            try:
                Dist = Distractor(Dictionary=dicGClass, TopicName=self.Topic, DistractorNumber=self.Number, Flag=False)
                result = Dist.RunAlgo()
                for key in result:
                    Output[key] = result.get(key)
            except:
                logging.error(sys.exc_info()[0])
                return 0
        if (len(dicNoClass) > 0):
            try:
                Dist = Distractor(Dictionary=dicNoClass, TopicName=self.Topic, DistractorNumber=self.Number, Flag=False)
                result = Dist.RunAlgo()
                for key in result:
                    Output[key] = result.get(key)
            except:
                logging.error(sys.exc_info()[0])
                return 0
        Output=self.__RemoveUnimportentThings(Output)
        if(Check):
            Output=self.__ButBlankSpace(Output)
        return Output
    ################## End OF Class ###########################


''''
ex=dict({'question1':['A neural network is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.','neural network','unsupervised learning']
    ,'question2':['classification is a systematic grouping of observations into categories','classification','Supervised learning'],
    'question3':['supervised learning is the machine learning task of learning a function that maps an input to an output based on example input-output pairs','supervised learning','Supervised learning'],
         'question4': ['A neural network is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.','neural network']
            ,'question5': ['classification is a systematic grouping of observations into categories', 'classification'],
         'question6': ['supervised learning is the machine learning task of learning a function that maps an input to an output based on example input-output pairs','supervised learning'],
         'question10': ['A neural network is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.','neural network', 'unsupervised'], 'question9': ['classification is a systematic grouping of observations into categories', 'classification','Supervised'],'question8': ['supervised learning is the machine learning task of learning a function that maps an input to an output based on example input-output pairs','supervised learning', 'Supervised']})
print("The  Genatic ALgorithm result with specific Entity ------------------------------------------------------------------------------------------------")
result=MCQ(dic=ex,Topic='DataMining',NumberofDistructor=4,diff="H")
print(len(ex))
print(result.RunAlgorithm())
'''