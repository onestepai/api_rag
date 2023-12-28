# coding: UTF-8

from ServiceStepAI.FlaskServiceBase.ServiceApiConfigBase import ServiceApiConfigBase
from flask_restplus import fields

from src.config.DockerConfig import DockerConfig


class ServiceApiConfig(ServiceApiConfigBase):
    def __init__(self):
        ServiceApiConfigBase.__init__(self,
                                      url_prefix=DockerConfig.URL_PREFIX + DockerConfig.API_VERSION,

                                      version=DockerConfig.API_VERSION,
                                      title=DockerConfig.API_TITLE,
                                      description=DockerConfig.API_DESCRIPTION,
                                      gpt_api_key= DockerConfig.GPT_API_KEY,
                                      gpt_4_model= DockerConfig.GPT_API_VERSION_4,
                                      gpt_3_5_model=DockerConfig.GPT_API_VERSION_35,
                                      prompt_language=DockerConfig.PROMPT_LANGUAGE
                                      )
        self.__set_predict_request()
        self.__set_predict_response()

    def __set_predict_request(self):
        request = ServiceApiConfigBase.api.model('PredictRequest.extractResult', {
            'utterance': fields.String(description='content'),
            'model_name': fields.String(description='model name'),
            'language': fields.String(description='language')
        })
        predict_request = ServiceApiConfigBase.api.model('PredictRequest', {
            'requestId': fields.String(description='request id'),
            'request': fields.Nested(request, description='request'),
            'timestamp': fields.Integer(description='calling timestamp')
        })
        ServiceApiConfigBase.predict_request = predict_request

    def __set_predict_response(self):
        response_result = ServiceApiConfigBase.api.model('PredictResponse.responseResult', {
            'result': fields.String(description='result'),
            'content': fields.String(description='content')
        })
        predict_response = ServiceApiConfigBase.api.model('PredictResponse', {
            'requestId': fields.String(description='request id'),
            'responseResult': fields.Nested(response_result, description='responseResult'),
            'timestamp': fields.Integer(description='calling timestamp')
        })
        ServiceApiConfigBase.predict_response = predict_response

