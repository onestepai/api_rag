import logging

from src.config.ServiceApiConfig import ServiceApiConfig

from src.config.DockerConfig import DockerConfig
from src.api_rag.ModelHandler import ModelHandler

logging.getLogger().setLevel(logging.INFO)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
  config = ServiceApiConfig()
  ModelHandler(config).run(port=int(DockerConfig.SERVICE_PORT))