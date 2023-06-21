from .data_provider_type import DataProviderType
from .data_provider_aws import DataProviderAWS
from .data_provider_yaml import DataProviderYaml
from libs.utils.console_utils import *


class GenericDataService:

    def __init__(self,env,conf_data,data_provider_type):
        self.data_provider_type = data_provider_type
        self.conf_data = conf_data
        self.env = env
        self.data = self.get_data()

    def get_data(self):
        if self.data_provider_type == DataProviderType.yaml_file:
            return DataProviderYaml(self.env,self.conf_data).get_yaml_data()
        elif self.data_provider_type == DataProviderType.aws:
            return DataProviderAWS(self.env,self.conf_data).get_aws_data()
        else:
            raise ValueError("Invalid data provider type")

