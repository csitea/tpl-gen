class StepNotDefinedInConfError(Exception):
    def __init__(
        self,
        message="The step that you are trying to generate conf for is not defined in the configuration!!!",
    ):
        self.message = message
        super().__init__(self.message)


class MissingEnvironmentVariableError(EnvironmentError):
    """Exception raised when a required environment variable is missing.

    Attributes:
        variable_name -- name of the missing environment variable
        message -- explanation of the error
    """

    def __init__(self, variable_name, message="Environment variable is missing"):
        self.variable_name = variable_name
        self.message = message + ": " + variable_name
        super().__init__(self.message)
