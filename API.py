import os
import sys
from flask import Flask, request,make_response
from flask_restful  import Resource, Api
from flask_celery import make_celery
from Question import Questions as Question
from MCQ import MCQ as MCQ
from TrueAndFalse import trueFalse as TrueAndFalse
import logging
import requests
import json


#from celery.events import
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL=url,
    CELERY_RESULT_BACKEND='amqp'
)
celery = make_celery(app)

api = Api(app)
logging.basicConfig(level=logging.DEBUG)
#i = celery.control.inspect()

class GenerateQuestion(Resource):
    def post(self,QuestionType):
        Body = request.get_json()
        if "Domain" in Body and "Text" in Body and "owner" in Body:
            SendQuestions.delay(QuestionType,Body)
            return make_response("in Processing")
        else:
            return make_response("Some Attribute missed ",404)


@celery.task(name='API.SendQuestions')
def SendQuestions(QuestionType,Body):
    asyn = myAsync()
    Myobject = dict({'error': 'Something want wrong while extract the Code'})
    try:
        if "Domain" in Body and "Text" in Body:
            Result=0
            if "Diff" in Body and "Distructor" in Body:
                Result = asyn.QuestionGenrate(Body.get("Text"), Body.get("Domain"), QuestionType,Body.get("Diff"),Body.get("Distructor"))
            elif "Diff" in Body:
                Result = asyn.QuestionGenrate(Body.get("Text"), Body.get("Domain"), QuestionType,Body.get("Diff"))
            elif "Distructor" in Body:
                Result = asyn.QuestionGenrate(Body.get("Text"), Body.get("Domain"), QuestionType,DistructorNumber=Body.get("Distructor"))
            else:
                Result=asyn.QuestionGenrate(Body.get("Text"),Body.get("Domain"),QuestionType)
            if Result != 0:
                logging.debug(Result)
                if Body.get("Domain") == "PL":
                    QuestionType="Complete"

                Myobject=dict({'domain':Body.get("Domain"),'Questions':Result,'owner':Body.get("owner"),'kind':QuestionType})
        r= requests.post('https://quizly-app.herokuapp.com/instructor/AddTempQuestion',json=Myobject)
        re=0
        #print(r.text)
        if r.status_code == 201:
            re=dict({'massage':'Success'})
        else:
            re=dict({'error':'Something want wrong while extract the Code'})
        return re
    except:
        logging.error("Unexpected errorNoClass:", sys.exc_info())
        logging.error({'massage':'Something want wrong while extract the Code '})
        return sys.exc_info()[0]

class myAsync():
    def QuestionGenrate(self,content,domain,QuestionType,diff='H',DistructorNumber=4):
        try:
            Q=Question(content,domain,QuestionType)
            dic=Q.GenerateQuestions(diff,DistructorNumber)
            if dic==0:
                return 0
            dic=self.__ChangeSpacyObjectToJson(dic.copy())
            Q=self.__ChangeMyObject(dic=dic,diff=diff,Number=DistructorNumber,Q=Q)
            if Q == 0 :
                return 0
            if type(Q) ==MCQ or type(Q) ==TrueAndFalse:
                dic= Q.RunAlgorithm()
            else:
                dic = Q
            if dic ==0:
                return 0
            return dic
        except:
            print("Unexpected errorNoClass:", sys.exc_info())
            return 0
    def __ChangeSpacyObjectToJson(self,dic):
        for key in dic:
            for i in range(dic.get(key).__len__()):
                dic.get(key)[i]=str(dic.get(key)[i])
        return dic
    def __ChangeMyObject(self,dic,diff,Number,Q):
        if Q.CheckDomain():
            #mo2ktan
            if Q.QuestionType == "MCQ" and Q.Domain != "PL":
                return MCQ(Content=Q.Content,diff=diff,dic=dic,Topic=Q.Domain,NumberofDistructor=Number)
            elif Q.QuestionType == "Complete" or Q.Domain == "PL":
                return Q.ButBlankSpace(dic)
            elif Q.QuestionType == "trueorfalse":
                return TrueAndFalse(Content=Q.Content,diff=diff,dic=dic,Topic=Q.Domain)
            else:
                return 0
        else:
            return 0

api.add_resource(GenerateQuestion, '/GenerateQuestion/<string:QuestionType>',endpoint='QuestionType')  # Route_1
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)