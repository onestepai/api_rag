# -*- coding: utf-8 -*-
import abc
import logging
from flask import Flask, Blueprint
from flask_restplus import Api, fields
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class ServiceApiConfigBase(object):
    api = None
    blue_print = None
    ns = None
    request_parser = None

    predict_request = None
    predict_response = None
    predict_api_name = '/predict'
    gpt_api_key = None
    gpt_3_5_model = None
    gpt_4_model = None
    onestep_ai_logger = logging.getLogger('onestep-ai')

    prompt_language=None
    app = Flask(__name__)


    def __init__(self, url_prefix=None, version='1.0',
                 title='model service title', description='model service description',
                 gpt_api_key=None, gpt_3_5_model=None, gpt_4_model=None,prompt_language=None, **kwargs,

    ):
        ServiceApiConfigBase.gpt_api_key = gpt_api_key
        ServiceApiConfigBase.gpt_4_model = gpt_4_model
        ServiceApiConfigBase.gpt_3_5_model = gpt_3_5_model
        ServiceApiConfigBase.blue_print = Blueprint('', __name__, url_prefix=url_prefix)
        ServiceApiConfigBase.api = Api(ServiceApiConfigBase.blue_print, version=version,
                                       title=title, description=description)
        ServiceApiConfigBase.ns = ServiceApiConfigBase.api.namespace('', description='API')
        ServiceApiConfigBase.request_parser = ServiceApiConfigBase.api.parser()
        ServiceApiConfigBase.prompt_language = prompt_language
        self.__set_predict_request()
        self.__set_predict_response()


    def __set_predict_request(self):
        context_device = ServiceApiConfigBase.api.model('PredictRequest.context.device', {
            'deviceId': fields.String(description='device identifier'),
            'deviceType': fields.String(description='Android/iOS phone or tablet/ PC'),
            'capabilities': fields.List(fields.String(description='Audio, Vedio, Display, GPS, Camera...'))
        })
        context_user = ServiceApiConfigBase.api.model('PredictRequest.context.user', {
            'userId': fields.String(description='User Id')
        })
        context = ServiceApiConfigBase.api.model('PredictRequest.context', {
            'device': fields.Nested(context_device, description='source device info object'),
            'user': fields.Nested(context_user, description='User object')
        })

        nlu_request = ServiceApiConfigBase.api.model('PredictRequest', {
            'requestId': fields.String(description='request id'),
            'serviceVersion': fields.String(description='current service version'),
            'locale': fields.String(description='language locale, en-US, zh-CN'),
            'utteranceText': fields.String(description='Context  object'),
            'timestamp': fields.Integer(description='calling timestamp'),
            'context': fields.Nested(context, description='context info object')
        })
        ServiceApiConfigBase.predict_request = nlu_request

    def __set_predict_response(self):
        slot = ServiceApiConfigBase.api.model('PredictResponse.intents.slot', {
            'name': fields.String(description='slot name'),
            'value': fields.String(description='slot value'),
            'slotType': fields.String(description='ADDRESS, TIME, NAME. For context carryover'),
            'confidenceScore': fields.Float(description='confidence score for the predication'),
            'confidenceBin': fields.String(description='HIGH, LOW'),
        })

        intent = ServiceApiConfigBase.api.model('PredictResponse.intents', {
            'name': fields.String(description='intent name'),
            'applicationId': fields.String(description='application id for handle request'),
            'confidenceScore': fields.Float(description='confidence score for the predication'),
            'confidenceBin': fields.String(description='HIGH, LOW'),
            'slots': fields.List(fields.Nested(slot), description='slots')
        })

        nlu_response = ServiceApiConfigBase.api.model('PredictResponse', {
            'requestId': fields.String(description='request id'),
            'serviceVersion': fields.String(description='current service version'),
            'timestamp': fields.Integer(description='calling timestamp'),
            'intents': fields.List(fields.Nested(intent), description='predicted intents')
        })
        ServiceApiConfigBase.predict_response = nlu_response


    def set_model_handler(self, handler):
        ServiceApiConfigBase.model_handler = handler
