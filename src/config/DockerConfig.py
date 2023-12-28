from ServiceOneStepCore.Utilities.MyEnvironment import MyEnvironment
# http://10.168.1.20:5025/ner/noya/cn/1.0

class DockerConfig(object):
    GPT_API_KEY = MyEnvironment().get_environment_variable("OPENAPI_API_KEY", 'Your open ai key')
    API_VERSION = MyEnvironment().get_environment_variable("API_VERSION", '1.0')
    GPT_API_VERSION_35 = MyEnvironment().get_environment_variable("GPT_3.5", 'gpt-3.5-turbo-1106')
    GPT_API_VERSION_4 = MyEnvironment().get_environment_variable("GPT_4", 'gpt-4-1106-preview')
    URL_PREFIX = MyEnvironment().get_environment_variable("URL_PREFIX", '/api_rag/')
    SERVICE_PORT = MyEnvironment().get_environment_variable("PORT", '5000')
    API_TITLE = MyEnvironment().get_environment_variable("API_TITLE", 'API RAG Service')
    API_DESCRIPTION = MyEnvironment().get_environment_variable("API_DESCRIPTION", 'API RAG Service')
    PROMPT_LANGUAGE = MyEnvironment().get_environment_variable("PROMPT_LANGUAGE", "zh_cn")
