class DataProviderYaml:

    def __init__(self, env,conf_data):
        self.conf_data = conf_data
        self.env = env
        self.data = self.get_yaml_data()

    def get_yaml_data(self):
        # Implement method to get data from yaml file here
        return "YAML file data"
