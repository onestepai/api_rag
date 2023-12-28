import json
from urllib import response

from src.config.ServiceApiConfig import ServiceApiConfig
from src.utils.apis import apis_info
import openai
import logging


class GPTChatBot():
    def __init__(self):
        if 'zh_cn' == ServiceApiConfig.prompt_language:
            self.final_response_prompt = "请帮我直接回复下面的提问：{}，你需要从以下我们内部信息解析，" \
                                         "帮我回答这个提问并组织答案返回:{}，表达和数据表现形式要求考虑最方便h5移动端用户观看(比如markdown富文本形式表达)，并详尽清晰。"
            self.api_select_prompt = "以下是我们的API列表：{},以下是客户的提问是：{}。请判断能否根据用户的提问内容调用我们的API回答用户提问。如果不能用我们提供的API完成需求，则只回答“unsupported”。" \
                                     "如果可以用我们提供的API完成需求，则只返回API的名称及参数，只用json表示。" \
                                     "返回API的json以apis的列表列出api的名字和所需要的调用参数"
        elif 'en_us' == ServiceApiConfig.prompt_language:
            self.final_response_prompt = "Please help me directly reply to the following question: {}, you need to analyze the information below I provide" \
                                         ", help me answer this question and organize the answer to return: {}, the expression and data presentation" \
                                         "form should be considered the most convenient for h5 mobile users to view (such as Markdown rich text format)," \
                                         " detailed and clear."
            self.api_select_prompt = "The following is my API list: {}, the following is the customer's question: {}. Please determine whether you can call my API with user's question content to answer" \
                                     " user questions. If the requirements cannot be fulfilled using the APIs I provide, just answer \"unsupported\". If the requirements can be fulfilled " \
                                     " using the API I provide, only the name and parameters of the API will be returned, expressed only in json. " \
                                     "The json returned by the API lists which anme is 'apis', and the element of API lists contains the name of the api and the required call parameters "
        # try:
        #     self.memory = [] if r.get(user_id) is None else json.loads(r.get(user_id))
        # except:
        #     self.memory =[]

    def call_llm_model(self, model_name, content):
        model = GptModel(model_name)
        response = model.search(content)
        return response


    # api结果生成类
    def final_generate(self, prompt, output_data, model_name):
        if output_data is None or len(output_data) == 0:
            if 'en_us' == ServiceApiConfig.prompt_language:
                prompt = [{"role": "user",
                           "content": "Please help to answer my question：{}".format(
                               prompt)}]
            else:
                prompt = [{"role": "user",
                           "content": "请帮助回答一下问题：{}".format(
                               prompt)}]
        else:
            prompt = [{"role": "user", "content": self.final_response_prompt.format(prompt, output_data)}]
        print('final_messages', prompt)
        answer = self.call_llm_model(model_name, prompt)
        # answer = response['choices'][0]['message']['content']
        # self.messages.append({"role":"assistant","content":answer})
        return answer

    def api_select(self, prompt, apis_info, model_name):
        prompt = [{"role": "user", "content": self.api_select_prompt.format(
            apis_info.api_descriptions, prompt)}]
        answer = self.call_llm_model(model_name, prompt)

        return answer


class GptModel():
    def __init__(self, model_name):
        if model_name == 'gpt35':
            self.model = ServiceApiConfig.gpt_3_5_model
        elif model_name == 'gpt4':
            self.model = ServiceApiConfig.gpt_4_model
        openai.api_key = ServiceApiConfig.gpt_api_key

    def search(self, content):
        return_data = ""
        try:
            for chunk in openai.ChatCompletion.create(
                    model=self.model,
                    messages=content,
                    stream=True,
                    temperature=0,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
            ):
                if hasattr(chunk.choices[0].delta, "content"):
                    return_data += chunk.choices[0].delta.content
        except Exception as e:
            return_data = "{\"error\":\"" + str(e) + "\"}"
        return return_data