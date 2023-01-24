from rake_nltk import Rake
import operator
import RAKE
import nltk
import os
import traceback

class rakee:

    def Start_Rake(self,stop_dir):
        try:
            rake_object = RAKE.Rake(stop_dir)
            return rake_object
        except:
            print("An exception occurred 38")
            traceback.print_exc()

    '''
    2- test rake key word extraction
    '''

    def test_Rake_keyword_extraction(self,sentence, nlp, rake_object):
        try:
            boolean_var = self.is_it_has_Rake_keyword_extraction(sentence, rake_object)  # wchich found in it an aintites
            if (boolean_var == 1):  # it has
                result_list = self.return_sentence_and_its_Rake_keyword_extraction(sentence, rake_object)
                return result_list
            else:
                return 0
        except:
            print("An exception occurred 39")
            traceback.print_exc()

    '''
    3- return sentence with rake extraction only , sentences with no rake extraction wont return
    '''

    def break_document_into_sentences(self,doc):
        try:
            sentences = [x for x in doc.sents]
            return sentences
        except:
            print("An exception occurred 16")

    def return_sentences_with_Rake_keyword_extraction(self,doc, nlp, rake_object):
        try:
            list_of_sentences_with_Rake_keyword_extraction = list()
            doc = nlp(doc)
            sentences = self.break_document_into_sentences(doc)
            for sentence in sentences:
                keywords = rake_object.run(str(sentence))
                if (keywords != []):
                    if (keywords[0][1] != 0):
                        list_of_sentences_with_Rake_keyword_extraction.append(str(sentence))
            return list_of_sentences_with_Rake_keyword_extraction
        except:
            print("An exception occurred 40")
            traceback.print_exc()

    '''
    4- check if sentence has a rake extraction
    '''

    def is_it_has_Rake_keyword_extraction(self,sentence, rake_object):
        try:
            keywords = rake_object.run(str(sentence))
            if (keywords != []):
                if (keywords[0][1] != 0):
                    return 1
                else:
                    return 0
            else:
                return 0
        except:
            print("An exception occurred 41")
            traceback.print_exc()

    '''
    5- return sentence and its Rake keyword extraction found in it.
    '''

    def return_sentence_and_its_Rake_keyword_extraction(self,sentence, rake_object):
        try:
            list_sentence_and_Rake_keyword_extraction_config = list()
            list_of_highestKeyword_Score = list()
            sentence = str(sentence)
            list_sentence_and_Rake_keyword_extraction_config.append(sentence)
            keywords = rake_object.run(sentence)
            c = 3
            for each_keyword in keywords:
                if (c == 0):
                    break
                small_list = list()
                small_list.append(each_keyword[0])
                small_list.append(each_keyword[1])
                list_of_highestKeyword_Score.append(small_list)
                c = c - 1

            list_sentence_and_Rake_keyword_extraction_config.append(list_of_highestKeyword_Score)
            return list_sentence_and_Rake_keyword_extraction_config
        except:
            print("An exception occurred 42")
            traceback.print_exc()

    '''
    6- return rake keywords list
    '''

    def return_RAKE_keywords_list(self,RAKE_keywords_list):
        try:
            large_list = list()
            all_list = list()
            all_list.append(RAKE_keywords_list[0])  # append sentence
            all_list.append(RAKE_keywords_list[1][0][0])  # append keyword
            large_list.append(all_list)

            return large_list
        except:
            print("An exception occurred 43")
            traceback.print_exc()