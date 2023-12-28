import json
import requests
import logging

from src.config.ServiceApiConfig import ServiceApiConfig
from src.utils.apis import apis_info
from src.api_rag.gpt_api import GPTChatBot


class APIRAGModel(object):

    def __init__(self):
        self.apis_info = apis_info()

    def call_apis(self, answer, headers):
        results = ''
        for api in answer['apis']:
            result = self.call_api(api, headers)
            results += result
        return results

    def call_api(self, api, headers):
        url = self.apis_info.api_definitions[api['name']]['url']
        prefix = self.apis_info.api_definitions[api['name']]['prefix']
        logging.info(str(api) + "-------->" + "url" + "------>" + str(url))
        input_data = ''
        params = {}
        input_params = {}
        if 'params' in api:
            input_params = api['params']
        elif 'parameters' in api:
            input_params = api['parameters']
        for key, value in input_params.items():
            if key in self.apis_info.api_definitions[api['name']]['input']:
                if self.apis_info.api_definitions[api['name']]['input'][key]['in'] == 'header':
                    headers[key] = input_params[key].encode(encoding='utf-8')
                elif self.apis_info.api_definitions[api['name']]['input'][key]['in'] == 'body':
                    input_data = json.dumps(input_params[key])
                elif self.apis_info.api_definitions[api['name']]['input'][key]['in'] == 'query':
                    params[key] = input_params[key].encode(encoding='utf-8')
        logging.info(str(api) + "------>" + "request_data----->" + str(input_data))

        output_data = requests.request(method=self.apis_info.api_definitions[api['name']]['calling_type'].upper(),
                                       url=url + prefix, headers=headers, params=params,
                                       data=input_data.encode(encoding='utf-8')).text
        output_explain = self.apis_info.api_definitions[api['name']]['output_explain']
        logging.info(str(api) + "------>" + "output_data----->" + str(output_data))
        if ServiceApiConfig.prompt_language == 'en_us':
            return ' data is ' + str(output_data) + ' the data explanation is ' + str(output_explain)
        else:
            return '数据是' + str(output_data) + '数据的解释是' + str(output_explain)

    def predict(self, prompt, model_name=''):
        self.chatbot = GPTChatBot()
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Connection': 'keep-alive',
            'content-type': 'Application/json',
            'Accept': '*/*',
        }
        # self.headers["authorization"] = 'Bearer ' + str(token)

        api_info = self.chatbot.api_select(prompt, self.apis_info, model_name)
        logging.info("fallback----->" + str(api_info))
        api_result = None
        if '不支持' not in api_info:
            api_info = api_info.replace('`', '')
            if api_info.startswith('json'):
                api_info = api_info.strip('json')
            logging.info("API------>generate---->" + str(api_info))
            api_info_json = json.loads(api_info)
            logging.info("API------>answer---->" + str(api_info_json))

            if len(api_info_json['apis']) > 0:
                api_result = self.call_apis(api_info_json, headers)
        final_result = self.chatbot.final_generate(prompt, api_result, model_name)
        logging.info("API------>final_result---->" + str(final_result))
        return final_result

