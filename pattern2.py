from spacy.matcher import Matcher
from spacy.tokens import Span
#from spacy import displacy
import pandas as pd
import traceback
import re



class patt:
    def __init__(self):
        pd.set_option('display.max_colwidth', 200)
        # define the pattern
        pattern1 = [{'DEP': 'amod', 'OP': "?"},  # adjectival modifier
                    {'POS': 'NOUN'},
                    {'LOWER': 'such'},
                    {'LOWER': 'as'},
                    {'POS': 'PROPN'}]

        # define the pattern
        pattern2 = [{'DEP': 'amod', 'OP': "?"},
                    {'POS': 'NOUN'},
                    {'LOWER': 'and', 'OP': "?"},
                    {'LOWER': 'or', 'OP': "?"},
                    {'LOWER': 'other'},
                    {'POS': 'NOUN'}]

        # define the pattern
        pattern3 = [{'DEP': 'nummod', 'OP': "?"},  # numeric modifier
                    {'DEP': 'amod', 'OP': "?"},  # adjectival modifier
                    {'POS': 'NOUN'},
                    {'IS_PUNCT': True},
                    {'LOWER': 'including'},
                    {'DEP': 'nummod', 'OP': "?"},
                    {'DEP': 'amod', 'OP': "?"},
                    {'POS': 'NOUN'}]

        # define the pattern
        pattern4 = [{'DEP': 'nummod', 'OP': "?"},
                    {'DEP': 'amod', 'OP': "?"},
                    {'POS': 'NOUN'},
                    {'IS_PUNCT': True},
                    {'LOWER': 'especially'},
                    {'DEP': 'nummod', 'OP': "?"},
                    {'DEP': 'amod', 'OP': "?"},
                    {'POS': 'NOUN'}]

        self.patterns_list = list()
        self.patterns_list.append(pattern1)
        self.patterns_list.append(pattern2)
        self.patterns_list.append(pattern3)
        self.patterns_list.append(pattern4)

        self.patterns_list_names = list()
        self.patterns_list_names = ["pattern1", "pattern2", "pattern3", "pattern4"]

    '''
    1 -start pattern model
    '''

    def Start_Pattern_Model(self,nlp):
        try:
            # Matcher class object
            matcher = Matcher(nlp.vocab)
            c = 0
            for pattern in self.patterns_list:
                matcher = self.add_pattern(matcher, pattern, self.patterns_list_names[c])
                c = c + 1
            return matcher
        except:
            print("An exception occurred 25")
            traceback.print_exc()

    '''
    2- add new pattern # pattern have to be defined first before passing it to the function
    '''

    def add_pattern(self,matcher, pattern, pattern_name):
        try:
            matcher.add(pattern_name, None, pattern)
            return matcher
        except:
            print("An exception occurred 26")
            traceback.print_exc()

    '''
    3- test pattern
    '''

    def testPatterns(self,sentence, nlp, matcher):
        try:
            boolean_var = self.is_sentence_has_patterns_matched(sentence, nlp, matcher)  # wchich found in it an aintites
            if (boolean_var == 1):  # it has
                result_list = self.return_sentence_and_its_patterns(sentence, nlp, matcher)
                return result_list
            else:
                return 0
        except:
            print("An exception occurred 27")
            traceback.print_exc()

    '''
    4- return sentences with patterns
    '''

    def break_document_into_sentences(self,doc):
        try:
            sentences = [x for x in doc.sents]
            return sentences
        except:
            print("An exception occurred 16")

    def return_sentences_with_patterns(self,doc, matcher):
        try:
            list_of_sentences_with_patterns = list()
            doc = nlp(doc)
            sentences = self.break_document_into_sentences(doc)
            # print(sentences)
            for sentence in sentences:
                doc = nlp(str(sentence))
                matches = matcher(doc)
                if (matches != []):
                    list_of_sentences_with_patterns.append(sentence[0:-1])
            return list_of_sentences_with_patterns
        except:
            print("An exception occurred 28")
            traceback.print_exc()

    '''
    5- check if the sentence has patterns matched with it 
    '''

    def is_sentence_has_patterns_matched(self,sentence, nlp, matcher):
        try:
            doc = nlp(str(sentence))
            matches = matcher(doc)
            if (matches != []):
                return 1
        except:
            print("An exception occurred 29")
            traceback.print_exc()

    '''
    6- return sentence with its patterns 
    '''

    def return_sentence_and_its_patterns(self,sentence, nlp, matcher):
        try:
            doc = nlp(str(sentence))
            matches = matcher(doc)
            list_sentence_and_pattern_config = list()
            list_of_matchesID_patternID_span_start_end = list()
            list_sentence_and_pattern_config.append(str(sentence))
            for match_id, start, end in matches:
                small_list = list()
                string_id = nlp.vocab.strings[match_id]  # Get string representation
                span = doc[start:end]  # The matched span
                small_list.append(match_id)
                small_list.append(string_id)
                small_list.append(start)
                small_list.append(end)
                small_list.append(span.text)

                list_of_matchesID_patternID_span_start_end.append(small_list)
            list_sentence_and_pattern_config.append(list_of_matchesID_patternID_span_start_end)
            return list_sentence_and_pattern_config
        except:
            print("An exception occurred 30")
            traceback.print_exc()

    '''
    7- return patterns keywords list 
    '''

    def return_patterns_keywords_list(self,patterns_list):
        try:
            keywords_list = list()
            large_list = list()
            # patterns_list[0] #holds sentence
            for eachList in patterns_list[1]:
                text = eachList[4]
                if (eachList[1] == 'pattern_1'):
                    list_of_keywords = text.split("such as")
                    for i in list_of_keywords:
                        keywords_list.append(i)

                if (eachList[1] == 'pattern_2'):
                    if ("and other" in text):
                        list_of_keywords = text.split("such as")
                        for i in list_of_keywords:
                            keywords_list.append(i)

                    if ("or other" in text):
                        list_of_keywords = text.split("or other")
                        for i in list_of_keywords:
                            keywords_list.append(i)

                if (eachList[1] == 'pattern_3'):
                    list_of_keywords = text.split("including")
                    for i in list_of_keywords:
                        keywords_list.append(i)

                if (eachList[1] == 'pattern_4'):
                    list_of_keywords = text.split("especially")
                    for i in list_of_keywords:
                        keywords_list.append(i)

            clean_keywords_list = self.clean_list(
                keywords_list)  # return no duplicates in data , and remove special characters

            for each_keyword in clean_keywords_list:
                all_list = list()
                all_list.append(patterns_list[0])  # add sentence
                all_list.append(each_keyword)  # add key word  to be replaced with a blank space
                large_list.append(all_list)

            return large_list
        except:
            print("An exception occurred 31")
            traceback.print_exc()

    def clean_list(self,list_of_patterns_keywords):
        try:
            clean_list = list()
            for each_keyword in list_of_patterns_keywords:
                # to remove special characters
                each_keyword = re.sub('[^\w\s-]', '', each_keyword).strip()
                each_keyword = each_keyword.encode('ascii', 'ignore').decode('ascii')
                if each_keyword not in clean_list:
                    clean_list.append(each_keyword)
            # print(clean_list)
            return clean_list
        except:
            print("An exception occurred 46")
            traceback.print_exc()
