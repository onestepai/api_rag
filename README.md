# Let Large Language Models understand your API
Large Language Models(LLMs) combined with private domain data bring huge value. There are currently many methods around how to make LLMs use private domain data more effectively. RAG's research allows LLMs to response user queris or generate reports through private domain data. These private domain data include text, databases, knowledge graphs, etc. However, these data need to be collected and organized for RAG. For situations where there is a large amount of complicated data, how RAG can provide support for LLMs more effectively is an important topic. 

Many systems provide various APIs, and some APIs can add, obtain, update or delete data(CRUD) in the service based on parameters. Some APIs can accomplish certain tasks. If the LLMs can understand the business functions and parameters of the API by themeselves, LLMs can be combined with the API to complete user queries. Swagger is a very popular library that helps developers generate API documentation and a visualization API teat tools. This project uses the large model to read the Swagger document to understand the business and parameters of the API, and automatically execute the user's query based on the understanding. It helps LLMs  implement API-based RAG. API-based Agent.

![image](https://github.com/onestepai/api_rag/assets/107015943/efa56206-6628-4587-8290-7e85e5e625db)



## How to use it
Use API RAG as following steps
- Put your swagger json files under swagger_files folder
- Update your service and swagger files' name in api_metadata.json as follow format:
```sh
  {
  "apis":[
    {
      "swagger_file":"api-reg-demo-service_v1.0.0.0.json",
      "url":"http://127.0.0.1:8080"
    }
  ]
}
```
- add your open.ai API key and select your major language(en_us or zh_cn) in swagger files. in config/DockerConfig.py
```sh
  GPT_API_KEY = MyEnvironment().get_environment_variable("OPENAPI_API_KEY", 'Your open ai key')
  PROMPT_LANGUAGE = MyEnvironment().get_environment_variable("PROMPT_LANGUAGE", "zh_cn")
```
- Use APIRAG with following code
```sh
from api_rag.api_rag_model import APIRAGModel
api_rag_model = APIRAGModel()
response = api_rag_model.predict(text,model_name)
```

## How to use it
Please try to use [API RAG DEMO](https://github.com/onestepai/api_rag_demo) as test service.

