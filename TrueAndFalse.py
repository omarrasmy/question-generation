import random
from Question import Questions as Question
from MCQ import MCQ as MCQ

class trueFalse(Question):
    def __init__(self,Content, diff, dic, Topic, NumberofDistructor=2):
        self.diff = diff
        self.dic = dic
        self.Number = NumberofDistructor
        self.Topic = Topic
        super().__init__(Domain=Topic, Content=Content, QuestionType="MCQ")

    def __RandomDistructor(self,Questions):
        for Key in Questions:
            x=random.randint(1, 2)
            Questions.get(Key)[Questions.get(Key).__len__() - 1] = Questions.get(Key)[Questions.get(Key).__len__() - 1].lower()
            Questions.get(Key).pop(x)
        return self.__RandomQuestions(Questions)

    def __RandomQuestions(self,Questions):
        x=random.randint(10, 80)
        RandomPresnt=int((x/100)*Questions.__len__())
        #print(RandomPresnt)
        count = 0
        for Key in Questions:
            if(count < RandomPresnt):
                Questions.get(Key)[Questions.get(Key).__len__() - 1] = Questions.get(Key)[Questions.get(Key).__len__() - 1].replace(Questions.get(Key)[0], Questions.get(Key)[1], 1)
                Questions.get(Key).insert(2,"F")
            else:
                Questions.get(Key).insert(2,"T")
            count=count+1
        return Questions

    def RunAlgorithm(self):
        Dic=MCQ(Content=self.Content,diff=self.diff,dic=self.dic,Topic=self.Topic,NumberofDistructor=self.Number)
        Output=Dic.RunAlgorithm(Check=False)
        if(Output == 0):
            return 0
        return self.__RandomDistructor(Output)



'''''
sent1 = dict({0:['A neural network is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.','neural network']
     ,1:['classification is a systematic grouping of observations into categories','classification'],
     2:['supervised learning is the machine learning task of learning a function that maps an input to an output based on example input-output pairs','supervised learning']})
x=trueFalse(Content="asdasd",diff="h",dic=sent1 ,Topic='Mining',NumberofDistructor=2)
x.RunAlgorithm()


dic1 = dict({0:['second Principle of dynamic_system_development_method Empowered teams that have the authority to make decisions','dynamic_system_development_method']
     ,1:['activity diagram and implementation shows the arrangement and organization of model elements in middle to large scale project that can be used to show both structure and dependencies between sub-systems or modules','activity diagram'],
     2:['Languages that support object-oriented programming (OOP) typically use inheritance for code reuse and extensibility in the form of either classes or prototyping. Those that use classes support two main concepts','prototyping']})
y=trueFalse(Content="asdasd",diff="h",dic=sent1 ,Topic='SW',NumberofDistructor=2)
y.RunAlgorithm()

dic2 = dict({0:['bjects are accessed somewhat like variables with complex internal structure, and in many languages are effectively pointers, serving as actual references to a single instance of said object in memory within a heap or stack. They provide a layer of abstraction which can be used to separate internal from external code','abstraction']
     ,1:['encapsulation is an object oriented programming concept that binds together the data and functions that manipulate the data, and that keeps both safe from outside interference and misuse. Data encapsulation led to the important OOP concept of data hiding','encapsulation'],
     2:['object_oriented_programming uses objects, but not all of the associated techniques and structures are supported directly in languages that claim to support oop','object_oriented_programming']})
n=trueFalse(Content="asdasd",diff="h",dic=sent1 ,Topic='SW',NumberofDistructor=2)
n.RunAlgorithm()

dic3=dict({0:['A neural network is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.','neural network']
    ,1:['new word is a systematic grouping of observations into categories','new word'],
    2:['supervised learning is the new_word task of learning a function that maps an input to an output based on example input-output pairs','new_word']})
m=trueFalse(Content="asdasd",diff="h",dic=sent1 ,Topic='Mining',NumberofDistructor=2)
m.RunAlgorithm()
'''''