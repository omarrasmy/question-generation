#import spacy.cli
import dic as dic
import plac
import random
import time
import spacy
#import en_core_web_lg
#import en_core_web_sm
import os
import traceback
#from __future__ import unicode_literals, print_function
from pathlib import Path
from spacy.util import minibatch, compounding
from spacy import displacy
#from google.colab import drive
from datetime import datetime
#from google.colab import files


class NERModel:
    def __init__(self):
        self.n_iter = 300
        model_training_time = 0
    def load_pretrained_model(self):
        try:
            print('s')
           # nlp = en_core_web_lg.load()
        except:
            print("An exception occurred 1")
            traceback.print_exc()

    '''
    2-upload training dataset
    '''

    def upload_corpus(self,dataset_and_labels_directory, dataset_text_name):
        try:
            # ask_for_access_to_google_drive()
            corpus = os.path.join(dataset_and_labels_directory, dataset_text_name)
            with open(corpus, 'r') as i_file:
                t_data = i_file.read()
            TRAIN_DATA = eval(t_data)
            return TRAIN_DATA
        except:
            print("An exception occurred 2")
            traceback.print_exc()

    '''
    3-upload dataset Labels
    '''

    def upload_Labels(self,dataset_and_labels_directory, labels_text_name):
        try:
            # ask_for_access_to_google_drive()
            corpus = os.path.join(dataset_and_labels_directory, labels_text_name)
            with open(corpus, 'r') as i_file:
                t_data = i_file.read()
            LABEL = t_data.split(",")
            return LABEL
        except:
            print("An exception occurred 3")
            traceback.print_exc()

    '''
    4-set pipline and entity recognizer
    '''

    def Set_up_the_pipeline_and_entity_recognizer(self,model, LABEL):
        """Set up the pipeline and entity recognizer, and train the new entity."""
        random.seed(0)
        try:
            if model is not None:
                nlp = spacy.load(model)  # load existing spaCy model
                print("Loaded model '%s'" % model)
            else:
                nlp = spacy.blank("en")  # create blank Language class
                print("Created blank 'en' model")

            # Add entity recognizer to model if it's not in the pipeline
            # nlp.create_pipe works for built-ins that are registered with spaCy

            if "ner" not in nlp.pipe_names:
                ner = nlp.create_pipe("ner")
                nlp.add_pipe(ner)
            # otherwise, get it, so we can add labels to it
            else:
                ner = nlp.get_pipe("ner")

            for en in LABEL:
                ner.add_label(en)  # add new entity label to entity recognizer

            # Adding extraneous labels shouldn't mess anything up
            # ner.add_label("VEGETABLE")
            if model is None:
                optimizer = nlp.begin_training()
            else:
                optimizer = nlp.resume_training()
            move_names = list(ner.move_names)
            # get names of other pipes to disable them during training
            pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
            other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
            return (nlp, other_pipes, move_names, optimizer)
        except:
            print("An exception occurred 4")
            traceback.print_exc()

    '''
    5- train the model
    '''

    def train_model(self,TRAIN_DATA, nlp, other_pipes, optimizer):
        start_time = datetime.now()
        try:
            training_losses = list()
            with nlp.disable_pipes(*other_pipes):  # only train NER
                sizes = compounding(1.0, 4.0, 1.001)
                # batch up the examples using spaCy's minibatch
                count = 0
                for itn in range(self.n_iter):
                    small_list = list()
                    count = count + 1
                    random.shuffle(TRAIN_DATA)
                    batches = minibatch(TRAIN_DATA, size=sizes)
                    losses = {}
                    for batch in batches:
                        texts, annotations = zip(*batch)
                        nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
                    print(count, " : ", "Losses", losses)
                    small_list.append(count)
                    small_list.append(losses)
                    training_losses.append(small_list)

            self.model_training_time = format(datetime.now() - start_time)
            print('Time elapsed (hh:mm:ss.ms) {}'.format(datetime.now() - start_time))
            return nlp, training_losses, self.model_training_time
        except:
            print("An exception occurred 5")
            traceback.print_exc()


    '''
    7- save trained model
    '''

    def save_trained_model(self,new_model_name, nlp, output_dir):
        try:
            # save model to output directory
            if output_dir is not None:
                output_dir = Path(output_dir)
                if not output_dir.exists():
                    output_dir.mkdir()
                # ------------------------------------------------------------->askfor rename model
                nlp.meta["name"] = new_model_name  # rename model
                nlp.to_disk(output_dir)
                print("Saved model to", output_dir)
                return 1  # ------------------------------------------------>change it
        except:
            print("An exception occurred 7")
            traceback.print_exc()

    '''
    8- load trained model
    '''

    def load_trained_model(self,output_dir):
        try:
            # ask_for_access_to_google_drive()
            # output_dir = Path(output_dir)
            print("Loading from", output_dir)
            nlp = spacy.load(output_dir)
            return nlp  # return loaded Mining trained model
        except:
            print("An exception occurred 8")
            traceback.print_exc()

    '''
    9- test model after loading
    '''

    def test_model_after_loading(self,user_resource, nlp):
        try:
            # test the saved model
            doc = nlp(user_resource)
            return doc
        except:
            print("An exception occurred 9")

    '''
    10- test model after training
    '''

    def test_model_after_training(self,sentence, nlp):
        try:
            doc = nlp(sentence)
            return doc
        except:
            print("An exception occurred 10")

    '''----------------------------------------------------------------'''

    '''
    11- print entities
    '''

    def print_entities(self,sentence):
        try:
            for ent in sentence.ents:
                print(sentence)
                print("Label: ", ent.label_, " Keyword: ", ent.text)
        except:
            print("An exception occurred 11")

    '''
    12- print entities
    '''

    def print_entities1(self,doc):
        try:
            sentences = [x for x in doc.sents]
            for sentence in sentences:
                print(sentence)
                for ent in sentence.ents:
                    print("Label: ", ent.label_, " Keyword: ", ent.text)
                print("")
        except:
            print("An exception occurred 12")

    '''
    13- print entities by display
    '''

    def print_entities_by_displacy(self,sentence):
        try:
            displacy.render(sentence, jupyter=True, style='ent')

        except:
            print("An exception occurred 13")

    '''
    14- print entities by display
    '''

    def print_entities_by_displacy1(self,doc):
        try:
            displacy.render(doc, jupyter=True, style='ent')
        except:
            print("An exception occurred 14")

    '''
    15- set name for the new model
    '''

    def Set_a_name_to_the_new_model(self):
        try:
            new_model_name = input("Enter A name for the new model: ")
        except:
            print("An exception occurred 15")

    '''---------------------------------------------------------------------'''
    '''
    16- segmentation
    '''

    def break_document_into_sentences(self,doc):
        try:
            sentences = [x for x in doc.sents]
            return sentences
        except:
            print("An exception occurred 16")

    '''
    17- return sentences that have entities only 
    '''

    def return_sentences_with_entities(self,doc):
        try:
            list_of_sentences_with_entities = list()
            sentences = self.break_document_into_sentences(doc)
            for sentence in sentences:
                if (sentence.ents != []):
                    list_of_sentences_with_entities.append(sentence)
            return list_of_sentences_with_entities
        except:
            print("An exception occurred 17")

    '''
    18 - check if the sentences has entities 
    '''

    def is_sentence_has_entities(self,sentence):
        try:
            if (sentence.ents != []):
                return 1
            else:
                return 0
        except:
            print("An exception occurred 18")

    '''
    19 - return sentences and its entities 
    '''

    def return_sentence_and_its_entities(self,sentence):
        try:
            list_sentence_entity_label = list()
            list_of_entities_and_its_label = list()
            list_sentence_entity_label.append(sentence)
            for ent in sentence.ents:
                small_list = list()
                small_list.append(ent.text)
                small_list.append(ent.label_)
                list_of_entities_and_its_label.append(small_list)
            list_sentence_entity_label.append(list_of_entities_and_its_label)
            return list_sentence_entity_label
        except:
            print("An exception occurred 19")

    '''
    20 - return sentences and its entities
    '''

    def return_sentence_and_its_entities1(self,sentence):
        try:

            keyword = 'NER'  # it holds the extracted keyword
            label = ''
            Name = 'NER'  # it holds the name of model

            dic[sentence] = {'Keyword': Name, 'Label': Name}

            # list_sentence_entity_label=list()
            list_of_entities_and_its_label = list()
            # list_sentence_entity_label.append(sentence)
            for ent in sentence.ents:
                small_list = list()
                small_list.append(ent.text)
                small_list.append(ent.label_)
                list_of_entities_and_its_label.append(small_list)
            # list_sentence_entity_label.append(list_of_entities_and_its_label)
            return  # list_sentence_entity_label
        except:
            print("An exception occurred 20")

    '''
    21-  test NER Model 
    '''

    def return_sentence_and_its_entities1(self,sentence):
        try:
            list_sentence_entity_label = list()
            list_of_entities_and_its_label = list()
            list_sentence_entity_label.append(sentence)
            for ent in sentence.ents:
                small_list = list()
                small_list.append(ent.text)
                small_list.append(ent.label_)
                list_of_entities_and_its_label.append(small_list)
            list_sentence_entity_label.append(list_of_entities_and_its_label)
            return list_sentence_entity_label
        except:
            print("An exception occurred 21")

    '''
    22- test NER Model 
    '''

    def test_NER_Model(self,sentence, nlp):
        try:
            boolean_var = self.is_sentence_has_entities(sentence)
            if (boolean_var == 1):
                result_list = self.return_sentence_and_its_entities(sentence)
                return result_list
            else:
                return 0
        except:
            print("An exception occurred 22")
            traceback.print_exc()

    '''
    23- return ner keywords list
    '''

    def return_NER_keywords_list2(self,NER_list):
        try:
            large_list = list()

            # NER_list[0] #holds sentence , and we dont need it
            for eachList in NER_list[1]:
                all_list = list()
                all_list.append(NER_list[0])  # append sentence
                all_list.append(eachList[0])  # append keyword
                all_list.append(eachList[1])  # append  keyword's label
                large_list.append(all_list)
                # keywords_list.append(eachList[0])
            return large_list
        except:
            print("An exception occurred 23")
            traceback.print_exc()

    '''
    24- put blank space in ner sentences
    '''

    def put_blank_Space_in_NER_Sentences(self,sentence, keyword):
        try:
            text = str(sentence)
            print(keyword)
            sentence_with_blank_Space = text.replace(keyword, " _________ ")
            return sentence_with_blank_Space
        except:
            print("An exception occurred 24")
            traceback.print_exc()