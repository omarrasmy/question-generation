import traceback

class tree:
    '''
    1- test sub tree matcher
    '''
    def testSubTreeMAtcher(self,sentence, nlp):
        try:
            # doc = nlp(test_text)
            boolean_var = self.is_sentence_has_SubTreeMatching(sentence, nlp)  # wchich found in it an aintites
            if (boolean_var == 1):
                result_list = self.return_sentence_and_its_SubTreeMAtcher(sentence, nlp)
                return result_list
            else:
                return 0
        except:
            print("An exception occurred 32")
            traceback.print_exc()

    '''
    2- return sentence that have sub tree matcher
    '''

    def break_document_into_sentences(self,doc):
        try:
            sentences = [x for x in doc.sents]
            return sentences
        except:
            print("An exception occurred 16")

    def return_sentences_with_SubTreeMAtcher(self,doc, nlp):
        try:
            substring1 = ","
            list_of_sentences_with_SubTreeMAtcher = list()
            doc = nlp(doc)
            sentences = self.break_document_into_sentences(doc)
            for sentence in sentences:
                sentence_has_SubTreeMAtcher = 0
                if (substring1 in str(sentence)):
                    list_of_sentences = str(sentence).split(",")
                    for each_sentence in list_of_sentences:
                        if (sentence_has_SubTreeMAtcher == 0):
                            doc = nlp(str(each_sentence))
                            x, y, flag = self.new_subtree_matcher(doc)
                            if ((x != '') | (y != '')):
                                sentence_has_SubTreeMAtcher = 1
                                list_of_sentences_with_SubTreeMAtcher.append(str(sentence))
                else:
                    doc = nlp(str(sentence))  # change it to each sentence if something wrong
                    x, y, flag = self.new_subtree_matcher(doc)
                    if ((x != '') | (y != '')):
                        list_of_sentences_with_SubTreeMAtcher.append(str(sentence))
            return list_of_sentences_with_SubTreeMAtcher

        except:
            print("An exception occurred 33")
            traceback.print_exc()

    '''
    3- check if the sentence has sub tree matching
    '''

    def is_sentence_has_SubTreeMatching(self,sentence, nlp):
        try:
            substring1 = ","
            sentence_has_SubTreeMAtcher = 0
            if (substring1 in str(sentence)):
                list_of_sentences = str(sentence).split(",")
                for each_sentence in list_of_sentences:
                    if (sentence_has_SubTreeMAtcher == 0):  # if it doesnt have matching yet
                        doc = nlp(str(each_sentence))
                        x, y, flag = self.new_subtree_matcher(doc)
                        if ((x != '') | (y != '')):
                            sentence_has_SubTreeMAtcher = 1
                        else:
                            return 0
                    else:
                        return 1
            else:
                doc = nlp(str(sentence))
                x, y, flag = self.new_subtree_matcher(doc)
                if ((x != '') | (y != '')):
                    return 1
                else:
                    return 0
        except:
            print("An exception occurred 34")
            traceback.print_exc()

    '''
    4- return sentence with its sub tree matchers found in it
    '''

    def return_sentence_and_its_SubTreeMAtcher(self,sentence, nlp):
        try:
            substring1 = ","
            list_sentence_and_SubTreeMAtcher_config = list()
            list_of_sub_sentence_x_y_flag = list()
            list_sentence_and_SubTreeMAtcher_config.append(sentence)
            if (substring1 in str(sentence)):
                list_of_sentences = str(sentence).split(",")
                for each_sub_sentence in list_of_sentences:
                    small_list = list()
                    doc = nlp(str(each_sub_sentence))
                    x, y, flag = self.new_subtree_matcher(doc)
                    small_list.append(x)
                    small_list.append(y)
                    small_list.append(flag)
                    small_list.append(each_sub_sentence)
                    list_of_sub_sentence_x_y_flag.append(small_list)
            else:
                small_list = list()
                doc = nlp(str(sentence))
                x, y, flag = self.new_subtree_matcher(doc)
                small_list.append(x)
                small_list.append(y)
                small_list.append(flag)
                list_of_sub_sentence_x_y_flag.append(small_list)

            list_sentence_and_SubTreeMAtcher_config.append(list_of_sub_sentence_x_y_flag)
            return list_sentence_and_SubTreeMAtcher_config
        except:
            print("An exception occurred 35")
            traceback.print_exc()

    '''
    5- new sub tree matcher
    '''

    def new_subtree_matcher(self,doc):
        try:
            subjpass = 0

            for i, tok in enumerate(doc):
                # find dependency tag that contains the text "subjpass"
                if tok.dep_.find("subjpass") == True:
                    subjpass = 1

            x = ''
            y = ''
            flag = ''
            # if subjpass == 1 then sentence is passive
            if subjpass == 1:
                flag = flag + "passive sentence"
                for i, tok in enumerate(doc):
                    if tok.dep_.find("subjpass") == True:
                        if (y == ''):
                            y = tok.text

                    if tok.dep_.endswith("obj") == True:
                        if (x == ''):
                            x = tok.text

            # if subjpass == 0 then sentence is not passive
            else:
                flag = flag + "not passive sentence"
                for i, tok in enumerate(doc):
                    if tok.dep_.endswith("subj") == True:
                        if (x == ''):
                            x = tok.text

                    if tok.dep_.endswith("obj") == True:
                        if (y == ''):
                            y = tok.text

            return x, y, flag
        except:
            print("An exception occurred 36")
            traceback.print_exc()

    '''
    6- return sub tree matcher keywords list
    '''

    def return_SubTreeMatcher_keywords_list(self,SubTreeMatcher_keywords_list):
        try:
            large_list = list()
            keywords_list = list()

            # SubTreeMatcher_keywords_list[0] #holds sentence

            for eachList in SubTreeMatcher_keywords_list[1]:
                if (eachList[0] != ''):
                    keywords_list.append(eachList[0])  # subject
                if (eachList[1] != ''):
                    keywords_list.append(eachList[1])  # object

                keywords_without_suplicates_list = self.remove_duplicates_from_lists(keywords_list)
            for each_keyword in keywords_without_suplicates_list:
                all_list = list()
                all_list.append(SubTreeMatcher_keywords_list[0])  # append sentence
                all_list.append(each_keyword)  # append keyword
                large_list.append(all_list)
            return large_list
        except:
            print("An exception occurred 37")
            traceback.print_exc()

    def remove_duplicates_from_lists(self,list_of_keywords):
        try:
            keywords_without_duplicates_list = list()
            for each_keyword in list_of_keywords:
                if each_keyword not in keywords_without_duplicates_list:
                    keywords_without_duplicates_list.append(each_keyword)
            return keywords_without_duplicates_list
        except:
            print("An exception occurred 45")
            traceback.print_exc()
