from flask_restplus import Resource
from ServiceStepAI.FlaskServiceBase.ServiceApiConfigBase import ServiceApiConfigBase


@ServiceApiConfigBase.ns.route(ServiceApiConfigBase.predict_api_name)
class PredictApiBase(Resource):
    @ServiceApiConfigBase.api.doc('PredictApi')
    @ServiceApiConfigBase.api.expect(ServiceApiConfigBase.predict_request)
    @ServiceApiConfigBase.api.marshal_with(ServiceApiConfigBase.predict_response, code=201)
    def post(self):
        ServiceApiConfigBase.request_parser.parse_args()
        args = ServiceApiConfigBase.api.payload
        return ServiceApiConfigBase.model_handler.predict(args), 201
