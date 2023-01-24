import ast
from random import sample, random
from gensim import models
from random import randint
from gensim.models.callbacks import CallbackAny2Vec
import tempfile
from gensim.test.utils import common_corpus, common_texts, get_tmpfile
import collections
import sys
import numpy as np
import os
class EpochSaver(CallbackAny2Vec):
    '''Callback to save model after each epoch.'''
    def __init__(self, path_prefix):
        self.path_prefix = path_prefix
        self.epoch = 0
        self.list=list()
    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        if self.epoch == 0:
          np.float_(model.running_training_loss)
          self.list.append(['epoch : ', self.epoch, 'loss = ', loss])
          print(loss)
        elif loss == self.loss_previous_step:
          print('overfit')
          model.running_training_loss=0
        else:
           print(1)
           output_path = get_tmpfile('{}_epoch{}.model'.format(self.path_prefix, self.epoch))
           model.save(output_path)
           print(loss)
           self.list.append(['epoch : ', self.epoch, 'loss = ', loss-self.loss_previous_step])
        self.loss_previous_step = loss
        self.epoch += 1
        w=open('Loss.txt','a+')
        w.write(self.list.__str__())
        self.list=list()
        w.write('\n')
        w.close()

class Distractor_Model:
    def __init__(self, Model):
        self.Model=models.Word2Vec.load(Model)
        #self.Model.callbacks=()
        #self.Model.save(os.getcwd()+'\\tmpFinalNoHs\\my_w2v_SGFinal_epoch96.model')

#keyword [] , ListOfKeywords[] return number
    def __TrainModel(self):
        saver = EpochSaver("my_w2v_SGFinal")
        s = list()
        n = list()
        k = 0
        sent=open(os.getcwd()+'/Sentence.txt')
        mylist=sent.read();
        print(k)
        mylist=ast.literal_eval(mylist)
        m = models.Word2Vec(sentences=mylist, size=200, min_count=5, iter=100, sg=1, hs=0, compute_loss=True, window=5,
                            callbacks=[saver])
        con = 0
        for i, word in enumerate(m.wv.vocab):
            con = con + 1
        print(con)
        print(m.get_latest_training_loss())

    def Calculate_Distances(self,keyword,ListOfKeywords):
        Fitness=0.0
        ListDistance=list()

        for word in keyword:
#harga3            print(self.Model.wv.distances(word, other_words=ListOfKeywords))
            try:
                #print('my word is ')
                #print(word)
                #print('list word is ')
                #print(ListOfKeywords)
                ListDistance.append(self.Model.wv.distances(word, other_words=ListOfKeywords))
            except:
                print ("Unexpected error:", sys.exc_info()[0])

        for i in ListDistance:
            Fitness=Fitness+(sum(i)/i.__len__())
        return Fitness/ListDistance.__len__()
    #list []
    def CheckAndDetermineKeyword(self,ListKeywords):
        NewWords=list()
        for Word in ListKeywords:
            Word=Word.lower()
            try:
                y = Word.replace(" ", "_")
                x=self.Model.wv[y]
                NewWords.append([y])
            except:
                try:
                    y=Word.split()
                    for i in y:
                        x=self.Model.wv[i]
                    NewWords.append(y)
                except:
                    NewWords.append([0])
        return NewWords
    #return [[]]
    def Pridication_Context(self,Context):
        Temp = list()
        for c in Context:
            x=c.split()
            try:
                List=self.Model.predict_output_word(x,topn=30)
                for Word in List:
                    Temp.append(Word[0])
            except:
                print(x)
                Temp.append("algorithm")
                Temp.append("random")
                Temp.append("diagram")
                Temp.append("search")
                Temp.append("model")
        return Temp
    def similarity(self,word):
        return self.Model.wv.most_similar(word)
