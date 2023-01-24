from GenerateKeyword import GenerateKeyword as GenerateKeywords
import os
class Questions:
    def __init__(self,Content,Domain,QuestionType):
        self.Content=Content
        self.Domain=Domain
        self.QuestionType=QuestionType
        self.__WordGeneration = GenerateKeywords()
        self.__output_dir = os.getcwd() + "/Complete/"+Domain

    def CheckDomain(self):
        return self.Domain == "Mining" or self.Domain == "SW" or self.Domain == "PL"
    def __GenerateMyWords(self):
        if self.CheckDomain():
            dic,App = self.__WordGeneration.start_by_switcher(self.__output_dir,self.Content)
            return dic
        return 0

    def ButBlankSpace(self, dic):
        for Key in dic:
            dic.get(Key)[0] = dic.get(Key)[0].replace(dic.get(Key)[1],'---------', 1)
        return dic
    def GenerateQuestions(self,diff="h",NumberOfDistractor=4):
        dic=self.__GenerateMyWords()
        if dic ==0:
            return 0
        return dic






