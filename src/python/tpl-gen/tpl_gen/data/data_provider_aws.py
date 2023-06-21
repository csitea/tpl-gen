import boto3
from libs.utils.console_utils import *


class DataProviderAWS:

    def __init__(self, env,conf_data):
        self.conf_data = conf_data
        self.env = env
        self.data = self.get_aws_data()


    def get_aws_data(self):

        session = boto3.Session(profile_name = self.env.AWS_PROFILE,region_name = self.env.AWS_REGION)
        self.data = self.conf_data
        aws_services = self.data['conf']['aws-services']
        # this smells - not sure whether this conf shoud be another root level,
        self.data['conf']['aws-services-data'] = {}

        for index, cservice in enumerate(aws_services):
            cservice_code = cservice['aws_service_code']
            cservice_title = cservice['title']
            print_info_heading("START ::: working on the " + cservice_title + " aws service")
            client = session.client(cservice_code)
            self.data['conf']['aws-services-data'][cservice_code] = client.meta.service_model.operation_names
            print_info_heading("STOP  ::: working on the " + cservice_title + " aws service")

        return self.data
