# -*- coding: utf-8 -*-
import abc
import json
import os
import threading
import uuid
import enum
from werkzeug.serving import WSGIRequestHandler

from ServiceStepAI.FlaskServiceBase.ServiceApiConfigBase import ServiceApiConfigBase


class TrainStatus(enum.Enum):
    Init = 1
    Processing = 2
    Finished = 3
    Failed = 4

def flask(host, port):
    ServiceApiConfigBase.app.register_blueprint(ServiceApiConfigBase.blue_print)
    ServiceApiConfigBase.app.run(debug=False, port=port, host=host)
class ModelBaseHandler(object):
    def __init__(self, config):

        config.set_model_handler(self)
        self._config = config
        self.realtime_predict_thread = None
        # the response use http1.1
        WSGIRequestHandler.protocol_version = "HTTP/1.1"
        # must import those 3 class after set the global values, otherwise has issue

        from ServiceStepAI.FlaskServiceBase.PredictApiBase import PredictApiBase

    def get_config(self):
        return self._config

    @abc.abstractmethod
    def predict(self, predict_request, **kwargs):
        pass

    def run(self, host="0.0.0.0", port=5000):
        realtime_predict_thread = threading.Thread(target=flask, args=(host, port,)).start()