import requests
from requests_toolbelt import MultipartEncoder
from ServiceStepAI.FlaskServiceBase.ServiceApiConfigBase import ServiceApiConfigBase


class HttpUtil(object):
    @staticmethod
    def post(url, http_request, **kwargs):
        try:
            headers = {"Content-Type": "application/json"}
            ServiceApiConfigBase.onestep_ai_logger.info("post to url: " + url + " with data: " + str(http_request))
            response = requests.post(url, headers=headers, json=http_request, **kwargs)
            return response.json()
        except Exception as e:
            ServiceApiConfigBase.onestep_ai_logger.error("Send to API [{0}] Exception: ".format(url))
            ServiceApiConfigBase.onestep_ai_logger.error(e)

    """
    Example:
    multipart_form_data = {
                            'file': ('filename', open('test.txt', 'rb'), 'text/plain'),
                            'name': file_name,
                            'size': str(file_size),
                            'index': str(index),
                            'total': str(total_index)
                        }
    """
    @staticmethod
    def upload_big_file(url, multipart_form_data):
        try:
            ServiceApiConfigBase.onestep_ai_logger.info("upload big file to: " + url + " with: " + str(multipart_form_data))
            m = MultipartEncoder(fields=multipart_form_data)
            headers = {"Content-Type": m.content_type}
            response = requests.post(url=url, headers=headers, data=m)
            return response.json()
        except Exception as e:
            ServiceApiConfigBase.onestep_ai_logger.error("upload file to API [{0}] Exception: ".format(url))
            ServiceApiConfigBase.onestep_ai_logger.error(e)

    @staticmethod
    def download_file_from_url(url, out_file_path):
        try:
            ServiceApiConfigBase.onestep_ai_logger.info("download file to: " + out_file_path + " from: " + url)
            r = requests.get(url)
            with open(out_file_path, 'wb') as f:
                f.write(r.content)
            return r.status_code
        except Exception as e:
            ServiceApiConfigBase.onestep_ai_logger.error("download_file_from_url [{0}] Exception: ".format(url))
            ServiceApiConfigBase.onestep_ai_logger.error(e)


    """
    Example:
    multipart_form_data = {
                           'file': ('filename', open('test.txt', 'rb'), 'text/plain'),
                           'name': file_name,
                           'size': str(file_size),
                           'index': str(index),
                           'total': str(total_index)
                       }
    http_request = {
            'itemType': type,
            'clientID': clientID,
            'clientPlatform': clientPlatform,
            'timestamp': timestamp,
            'namespace': namespace,
            'version': version
             
    """
    @staticmethod
    def upload_big_file_with_request(url, multipart_form_data, http_request):
        try:
            ServiceApiConfigBase.onestep_ai_logger.info("upload big file to: " + url + " with: " + str(multipart_form_data))
            m = MultipartEncoder(fields=multipart_form_data)
            headers = {"Content-Type": m.content_type}
            response = requests.post(url=url, headers=headers, json=http_request, data=m)
            return response.json()
        except Exception as e:
            ServiceApiConfigBase.onestep_ai_logger.error("upload file to API [{0}] Exception: ".format(url))
            ServiceApiConfigBase.onestep_ai_logger.error(e)