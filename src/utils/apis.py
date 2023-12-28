import time
import datetime
import logging

from src.config.ServiceApiConfig import ServiceApiConfig
from src.utils.swagger_reader import SwaggerReader


def time_start_end(month=1):
    t = datetime.datetime.now()
    timestamp = time.time()
    hours = month * 30 * 24
    t2 = (t - datetime.timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    ts2 = time.mktime(time.strptime(t2, '%Y-%m-%d %H:%M:%S'))
    now = (int(round(int(timestamp) * 1000)))
    before = int(str(ts2 * 1000).split(".")[0])
    return now, before


class apis_info():
    def __init__(self):

        swagger_reader = SwaggerReader()
        api_dic = swagger_reader.read()
        print(api_dic)
        if 'zh_cn' == ServiceApiConfig.prompt_language:
            prompt_means = ',含义是:'
            prompt_type = ',类型是:'
            prompt_object = '对象包含:'
            prompt_parameter = '参数包括:'
            prompt_return = '返回值参数包括:'
        elif 'en_us' == ServiceApiConfig.prompt_language:
            prompt_means = ',it means:'
            prompt_type = ',the parameter\'s type is:'
            prompt_object = 'the object includes:'
            prompt_parameter = 'the parameters includes:'
            prompt_return = 'the return includes:'

        self.api_definitions = {}
        self.api_descriptions = ''

        for key, value in api_dic.items():
            api_description = key

            api_description += prompt_means
            api_description += value['description']
            api_description += ';'
            self.api_definitions[key] = {}

            api_parameter_description = ''
            for parameter, para_value in value['parameters'].items():
                api_parameter_description += parameter
                api_parameter_description += prompt_type
                api_parameter_description += para_value['type']
                api_parameter_description += prompt_means
                api_parameter_description += para_value['description']
                if 'input_definition' in para_value:
                    api_parameter_description += prompt_object
                    for object_param, object_value in para_value['input_definition'].items():
                        api_parameter_description += object_param
                        api_parameter_description += prompt_means
                        api_parameter_description += object_value['description']
                        api_parameter_description += prompt_type
                        api_parameter_description += object_value['type']
                        api_parameter_description += ';'
                else:
                    api_parameter_description += ';'
            if len(api_parameter_description) > 0:
                api_description += prompt_parameter
                api_description += api_parameter_description
            else:
                api_description += ';'
            api_response_description = ''
            for response_para_name, response_para_value in value['output_definition'].items():
                api_response_description += response_para_name
                if 'description' in response_para_value:
                    api_response_description += prompt_means
                    api_response_description += response_para_value['description']
                    api_response_description += prompt_type
                    api_response_description += response_para_value['type']
                api_response_description += ';'
            if len(api_response_description) > 0:
                api_description += prompt_return
                api_description += api_response_description
            api_description += '。'
            self.api_descriptions += api_description
            self.api_definitions[key]['input'] = value['parameters']
            self.api_definitions[key]['input_explain'] = api_parameter_description
            self.api_definitions[key]['url'] = api_dic[key]['url']
            self.api_definitions[key]['calling_type'] = api_dic[key]['calling_type']
            self.api_definitions[key]['prefix'] = api_dic[key]['prefix']

            self.api_definitions[key]['output'] = api_dic[key]['output_definition']
            self.api_definitions[key]['output_explain'] = api_response_description


