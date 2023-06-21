import os


class RunEnv:
    _instance = None
    AWS_PROFILE = None
    AWS_REGION = None
    TPL_SRC = None
    CNF_SRC = None
    PRODUCT_DIR = None
    ORG = None
    APP = None
    ENV = None
    DATA_KEY_PATH = None
    TGT = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance


    def _initialize(self):
        try:
            self.AWS_PROFILE = os.getenv("AWS_PROFILE")
            self.AWS_REGION = os.getenv("AWS_REGION")
            self.TPL_SRC = os.getenv("TPL_SRC")
            self.CNF_SRC = os.getenv("CNF_SRC")
            self.ORG = os.getenv("ORG")
            self.APP = os.getenv("APP")
            self.ENV = os.getenv("ENV")
            self.DATA_KEY_PATH = os.getenv("DATA_KEY_PATH")
            self.TGT = os.getenv("TGT")

            product_dir = os.path.join(__file__, "..", "..", "..", "..", "..", "..")
            self.PRODUCT_DIR = os.path.abspath(product_dir)

            base_dir = os.path.join(product_dir, "..", "..")
            self.BASE_DIR = os.path.abspath(base_dir)
        except IndexError as error:
            raise Exception("ERROR in set_vars: " + str(error)) from error

    def __call__(self):
        return self




