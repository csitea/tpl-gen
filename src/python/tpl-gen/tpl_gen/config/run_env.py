import os


class RunEnv:
    _instance = None
    AWS_PROFILE = None
    AWS_REGION = None
    TPL_SRC = None
    CNF_SRC = None
    PROJ_PATH = None
    ORG = None
    APP = None
    ENV = None
    DATA_KEY_PATH = None
    TGT = None
    HOME = None
    SRC_EXT = None # file extension to be considered as template
    TGT_EXT = None # file extension to replace SRC_TPL after rendering
    SRC_PRF = None # prefix where to find template files
    SRC_PRF = None # replace prefix and put rendered files into another prefix

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance


    def _initialize(self):
        try:
            self.TPL_SRC = os.getenv("TPL_SRC")
            self.CNF_SRC = os.getenv("CNF_SRC")
            self.ORG = os.getenv("ORG")
            self.APP = os.getenv("APP")
            self.ENV = os.getenv("ENV")
            self.DATA_KEY_PATH = os.getenv("DATA_KEY_PATH")
            self.TGT = os.getenv("TGT")
            self.SRC_EXT = os.getenv('SRC_EXT', '.tpl')
            self.TGT_EXT = os.getenv('TGT_EXT', '')
            self.SRC_PRF = os.getenv('SRC_PRF', 'src/tpl/')
            self.TGT_PRF = os.getenv('TGT_PRF', '')

            PROJ_dir = os.path.join(__file__, "..", "..", "..", "..", "..", "..")
            self.PROJ_PATH = os.path.abspath(PROJ_dir)

            BASE_PATH = os.path.join(PROJ_dir, "..", "..")
            self.BASE_PATH = os.path.abspath(BASE_PATH)
            self.HOME = os.getenv('HOME')

        except IndexError as error:
            raise Exception("ERROR in set_vars: " + str(error)) from error

    def __call__(self):
        return self
