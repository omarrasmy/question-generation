from NERModel import NERModel as NER
from Rake import rakee as rake
import traceback
from spacy.matcher import Matcher
from spacy.tokens import Span
from pattern2 import patt as pattern2
from Tree import tree as tree
import  os
class GenerateKeyword:
    def __init__(self):
        StopWordsDir = os.getcwd()+"/Complete/StopWords"
        SmartStopWordsTextName = "SmartStoplist.txt"
        self.stop_dir = os.path.join(StopWordsDir, SmartStopWordsTextName)
        self.NER=NER()
        self.pattern2=pattern2()
        self.rake=rake()
        self.tree=tree()

    def define_needed_Objects(self,Model_output_dir):
        try:
            nlp = self.NER.load_trained_model(Model_output_dir)
            matcher = self.Start_Pattern_Model(nlp)
            rake_object = self.rake.Start_Rake(self.stop_dir)
            return nlp, matcher, rake_object
        except:
            print("An exception occurred 44")
            traceback.print_exc()

    def Start_Pattern_Model(self,nlp):
        try:
            # Matcher class object
            matcher = Matcher(nlp.vocab)
            c = 0
            for pattern in self.pattern2.patterns_list:
                matcher = self.pattern2.add_pattern(matcher, pattern, self.pattern2.patterns_list_names[c])
                c = c + 1
            return matcher
        except:
            print("An exception occurred 25")
            traceback.print_exc()

    def start_by_priority(self,Model_output_dir, user_Resource):  # user_Resource --> user teaching resource

        nlp, matcher, rake_object = self.define_needed_Objects(Model_output_dir)
        doc = self.NER.test_model_after_loading(user_Resource, nlp)
        sentences = self.NER.break_document_into_sentences(doc)
        dic, approaches_list = self.Generate_Complete_Questions_By_Priority(sentences, nlp, matcher, rake_object)
        return dic, approaches_list

    def Generate_Complete_Questions_By_Priority(self,sentences, nlp, matcher, rake_object):
        try:
            all_values_list = list()

            for sentence in sentences:

                sentence_in_str_format = str(sentence)
                list1 = self.NER.test_NER_Model(sentence, nlp)
                list2 = self.pattern2.testPatterns(sentence, nlp, matcher)
                list3 = self.tree.testSubTreeMAtcher(sentence, nlp)
                list4 = self.rake.test_Rake_keyword_extraction(sentence, nlp, rake_object)

                list1_keywords = list()
                list2_keywords = list()
                list3_keywords = list()
                list4_keywords = list()

                if (list1 != 0):
                    NER_keywords_list = self.NER.return_NER_keywords_list2(list1)
                    list1_keywords = NER_keywords_list
                else:
                    list1_keywords = str(0)

                if (list1_keywords == str(0)):
                    if (list4 != 0):
                        RAKE_keywords_list = self.rake.return_RAKE_keywords_list(list4)
                        list4_keywords = RAKE_keywords_list
                    else:
                        list4_keywords = str(0)

                if ((list1_keywords == str(0)) & (list4_keywords == str(0))):
                    if (list3 != 0):
                        SubTreeMatcher_keywords_list = self.tree.return_SubTreeMatcher_keywords_list(list3)
                        list3_keywords = SubTreeMatcher_keywords_list
                    else:
                        list3_keywords = str(0)

                if ((list1_keywords == str(0)) & (list4_keywords == str(0)) & (list3_keywords == str(0))):
                    if (list2 != 0):
                        pattern_keywords_list = self.pattern2.return_patterns_keywords_list(list2)
                        list2_keywords = pattern_keywords_list
                    else:
                        list2_keywords = str(0)

                for i in list1_keywords:
                    if (i != str(0)):
                        new_list = list()
                        new_list.append(i)  # append question
                        new_list.append(0)  # append 0 --> NER approach
                        all_values_list.append(new_list)

                for i in list2_keywords:
                    if (i != str(0)):
                        new_list = list()
                        new_list.append(i)  # append question
                        new_list.append(1)  # append 1 --> patterns approach
                        all_values_list.append(new_list)

                for i in list3_keywords:
                    if (i != str(0)):
                        new_list = list()
                        new_list.append(i)  # append question
                        new_list.append(2)  # append 2 --> subtree matcher approach
                        all_values_list.append(new_list)

                for i in list4_keywords:
                    if (i != str(0)):
                        new_list = list()
                        new_list.append(i)  # append question
                        new_list.append(3)  # append 3 --> Rake approach
                        all_values_list.append(new_list)

            questions_without_duplicates = self.remove_diplicate_questions(all_values_list)

            dic = {}
            c = 0
            for each_list in questions_without_duplicates:
                dic[c] = each_list[0]
                c = c + 1

            arrporaches_list = list()
            for each_list in questions_without_duplicates:
                arrporaches_list.append(each_list[1])

            return dic, arrporaches_list
        except:
            print("An exception occurred 49")
            traceback.print_exc()

    def remove_diplicate_questions(self,all_values_list):
        try:
            questions_without_duplicates_list = list()
            keywords_list = list()
            for each_question in all_values_list:
                if each_question[0][1] not in keywords_list:
                    keywords_list.append(each_question[0][1])
                    questions_without_duplicates_list.append(each_question)
            return questions_without_duplicates_list
        except:
            print("An exception occurred 47")
            traceback.print_exc()

    def start_by_switcher(self,Model_output_dir, user_Resource):  # user_Resource --> user teaching resource
        try:
            apply_models_list = [0, 1, 2, 3]
            # LABEL=upload_Labels(dataset_and_labels_directory,Labels_file_name)
            # nlp,other_pipes,move_names,optimizer=Set_up_the_pipeline_and_entity_recognizer(model,LABEL)

            nlp, matcher, rake_object = self.define_needed_Objects(Model_output_dir)
            doc = self.NER.test_model_after_loading(user_Resource, nlp)
            sentences = self.NER.break_document_into_sentences(doc)
            dic, approaches_list = self.Generate_Complete_Questions_By_Switcher(apply_models_list, sentences, nlp, matcher,
                                                                           rake_object)
            return dic, approaches_list
        except:
            print("An exception occurred 50")
            traceback.print_exc()

    def Generate_Complete_Questions_By_Switcher(self,apply_models_list, sentences, nlp, matcher, rake_object):
        try:
            all_values_list = list()

            for sentence in sentences:

                sentence_in_str_format = str(sentence)

                switcher = {
                    0: self.NER.test_NER_Model(sentence, nlp),
                    1: self.pattern2.testPatterns(sentence, nlp, matcher),
                    2: self.tree.testSubTreeMAtcher(sentence, nlp),
                    3: self.rake.test_Rake_keyword_extraction(sentence, nlp, rake_object)
                }

                list1_keywords = list()
                list2_keywords = list()
                list3_keywords = list()
                list4_keywords = list()

                for i in apply_models_list:
                    if (i == 0):
                        list1 = switcher.get(i, "invalid model number")
                        if (list1 != 0):
                            NER_keywords_list = self.NER.return_NER_keywords_list2(list1)
                            list1_keywords = NER_keywords_list
                        else:
                            list1_keywords = str(0)

                        for i in list1_keywords:
                            if (i != str(0)):
                                new_list = list()
                                new_list.append(i)  # append question
                                new_list.append(0)  # append 0 --> NER approach
                                all_values_list.append(new_list)

                    if (i == 1):
                        list2 = switcher.get(i, "invalid model number")
                        if (list2 != 0):
                            pattern_keywords_list = self.pattern2.return_patterns_keywords_list(list2)
                            list2_keywords = pattern_keywords_list
                        else:
                            list2_keywords = str(0)

                        for i in list2_keywords:
                            if (i != str(0)):
                                new_list = list()
                                new_list.append(i)  # append question
                                new_list.append(1)  # append 1 --> patterns approach
                                all_values_list.append(new_list)

                    if (i == 2):
                        list3 = switcher.get(i, "invalid model number")
                        if (list3 != 0):
                            SubTreeMatcher_keywords_list = self.tree.return_SubTreeMatcher_keywords_list(list3)
                            list3_keywords = SubTreeMatcher_keywords_list
                        else:
                            list3_keywords = str(0)

                        for i in list3_keywords:
                            if (i != str(0)):
                                new_list = list()
                                new_list.append(i)  # append question
                                new_list.append(2)  # append 2 --> subtree matcher approach
                                all_values_list.append(new_list)

                    if (i == 3):
                        list4 = switcher.get(i, "invalid model number")
                        if (list4 != 0):
                            RAKE_keywords_list = self.rake.return_RAKE_keywords_list(list4)
                            list4_keywords = RAKE_keywords_list
                        else:
                            list4_keywords = str(0)

                    for i in list4_keywords:
                        if (i != str(0)):
                            new_list = list()
                            new_list.append(i)  # append question
                            new_list.append(3)  # append 3 --> Rake approach
                            all_values_list.append(new_list)

            questions_without_duplicates = self.remove_diplicate_questions(all_values_list)

            dic = {}
            c = 0
            for each_list in questions_without_duplicates:
                dic[c] = each_list[0]
                c = c + 1

            arrporaches_list = list()
            for each_list in questions_without_duplicates:
                arrporaches_list.append(each_list[1])

            return dic, arrporaches_list
        except:
            print("An exception occurred 48")
            traceback.print_exc()

    #test_text = "all the skills needed for the Turing Test,imitation game. reem is a good person. meshmesh is a good cat. he eats alot of dry food. GDP in developing countries such as Vietnam will continue growing at a high rate. Here is how you can keep your car and other vehicles clean. Here is how you can keep your car or other vehicles clean. Eight people, including two children, were injured in the explosion. A healthy eating pattern includes fruits, especially whole fruits. mom answers the phone, and the table is broken by marwan. today will be a good day. the garden was watered by the man. how does k-means algorithm work? and what about talking about data science. all the skills needed for the Turing Test,imitation game. alaa was fantastic in microsoft.  the environment does not change with the passage of time,but the agent's performance score does. The introduction of spreadsheets enabled business users to create simple logic on data structured in rows and columns and create their own analyses of business problems. Database administrator training is not required to create spreadsheets: They can be set up to do many things quickly and independently of information technology (IT) groups. Spreadsheets are easy to share, and end users have control over the logic involved. However, their proliferation can result in “many versions of the truth.” In other words, it can be challenging to determine if a particular user has the most relevant version of a spreadsheet, with the most current data and logic in it. Moreover, if a laptop is lost or a file becomes corrupted, the data and logic within the spreadsheet could be lost. This is an ongoing challenge because spreadsheet programs such as Microsoft Excel still run on many computers worldwide. With the proliferation of data islands (or spreadmarts), the need to centralize the data is more pressing than ever. As data needs grew, so did more scalable data warehousing solutions. supervised learning is a type of machine learning. there is a lot of supervised learning algorithms like support vector machine algorithm , knn algorithm , logistic regression , and many more. reem is a good person. meshmesh is a good cat. he eats alot of dry food. GDP in developing countries such as Vietnam will continue growing at a high rate. Here is how you can keep your car and other vehicles clean. Here is how you can keep your car or other vehicles clean. Eight people, including two children, were injured in the explosion. A healthy eating pattern includes fruits, especially whole fruits. "
#dic , approaches=I.start_by_priority(output_dir_AI_version4,test_text)
#dic , approaches=I.start_by_switcher(output_dir_AI_version4,test_text)
#print(approaches)
