from swagger_parser import SwaggerParser
import json
class SwaggerReader:
    #def __init__(self):

    def load_api(self, filename: str):
        with open(filename) as f_in:
            return json.load(f_in)
    def read(self):
        api_definition = self.load_api('api_metadata.json')
        api_dic = {}
        for api in api_definition['apis']:
            swagger_file = api['swagger_file']
            parser = SwaggerParser(swagger_path='swagger_files/' + swagger_file)

            for key, value in parser.operation.items():
                print(parser.paths[value[0]][value[1]])
                api_dic[key] = {}
                api_dic[key]['url'] = api['url']
                api_dic[key]['description'] = parser.specification['paths'][value[0]][value[1]]['summary']
                parameters = {}
                for parameter_key, parameter_value in parser.paths[value[0]][value[1]]['parameters'].items():
                    parameter_name = parameter_value['name']
                    parameters[parameter_name] = {}
                    parameters[parameter_name]['description'] = parameter_value['description']

                    if 'schema' in parameter_value:
                        request_schema_type = parameter_value['schema']

                        if '$ref' not in request_schema_type:
                            parameters[parameter_name]['type'] = request_schema_type['type']
                        else:
                            request_schema = parser.paths[value[0]][value[1]]['parameters'][parameter_name]['schema']
                            ref_path = request_schema['$ref'].split('/')
                            current_path = ''
                            for directory in ref_path:
                                if directory == '#':
                                    current_path = parser.specification
                                else:
                                    current_path = current_path[directory]
                            if current_path['type'] == 'object':
                                parameters[parameter_name]['type'] = 'object'
                                parameters[parameter_name]['input_definition'] = current_path['properties']
                    parameters[parameter_name]['in'] = parameter_value['in']
                api_dic[key]['parameters'] = parameters
                api_dic[key]['prefix'] = value[0]
                api_dic[key]['calling_type'] = value[1]
                response_schema = parser.paths[value[0]][value[1]]['responses']['200']['schema']
                if '$ref' in response_schema:
                    ref_path = response_schema['$ref'].split('/')
                    current_path = ''
                    for directory in ref_path:
                        if directory == '#':
                            current_path = parser.specification
                        else:
                            current_path = current_path[directory]
                    if current_path['type'] == 'object':
                        api_dic[key]['output_definition'] = current_path['properties']
                else:
                    api_dic[key]['output_definition'] = parser.paths[value[0]][value[1]]['responses']['200']['schema']
            print(api_dic)
        return api_dic
