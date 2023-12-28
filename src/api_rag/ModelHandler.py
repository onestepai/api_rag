# -*- coding: utf-8 -*-
import time
import json
from ServiceStepAI.ModelBase.ModelBaseHandler import ModelBaseHandler
from ServiceOneStepCore.Utilities.LoggerHelper import LoggerHelper
from src.api_rag.api_rag_model import APIRAGModel


# from src.utils.swagger_reader import SwaggerReader


class ModelHandler(ModelBaseHandler):
    V1 = "v1"

    def __init__(self, config):
        ModelBaseHandler.__init__(self, config)
        self._version = ModelHandler.V1
        self.create_model()


    def create_model(self):
        if self._version == ModelHandler.V1:
            self._predictor = APIRAGModel()

    def predict(self, request, **kwargs):
        # try:
        LoggerHelper().log_info(u"Request: " + str(request))
        contents = request["request"]["content"]
        data = json.loads(contents)
        if "clean_context" in list(data.keys()):
            final_result = "Reset successfully."
        else:
            text = data["utterance"]
            model_name = data["model_name"]
            LoggerHelper().log_info(u"date_text_content: " + str(text))
            final_result = self._predictor.predict(text,model_name)
        response_predict = self.create_predict_response(request,final_result)
        if response_predict is not None:
            return response_predict


    def create_predict_response(self, request, predict_sent):
        response = {
            'requestId': request['requestId'] if 'requestId' in request else '',
            'timestamp': time.time(),
            'response': predict_sent
        }
        return {
            'requestId': request['requestId'] if 'requestId' in request else '',
            'timestamp': time.time(),
            'responseResult': {
                'result': 'success',
                'content': json.dumps(response, ensure_ascii=False)
            }
        }
