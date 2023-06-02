class OAEModel:
    ORG: str
    APP: str
    ENV: str

    def __init__(self, org: str, app: str, env: str) -> None:
        self.ORG = org
        self.ENV = env
        self.APP = app


class PathsModel:
    PRODUCT_DIR: str
    BASE_DIR: str

    def __init__(self, product_dir: str, base_dir: str) -> None:
        self.PRODUCT_DIR = product_dir
        self.BASE_DIR = base_dir


class TplPathsModel(PathsModel):
    CNF_SRC: str
    TPL_SRC: str
    TGT: str

    def __init__(
        self, product_dir: str, base_dir: str, cnf_src: str, tpl_src: str, tgt: str
    ) -> None:
        self.CNF_SRC = cnf_src
        self.TPL_SRC = tpl_src
        self.TGT = tgt
        super().__init__(product_dir, base_dir)
