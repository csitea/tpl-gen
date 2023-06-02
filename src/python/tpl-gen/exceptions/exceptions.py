class StepNotDefinedInConfError(Exception):
    def __init__(self, message= "The step that you are trying to generate conf for is not defined in the configuration!!!"):
        self.message = message
        super().__init__(self.message)

