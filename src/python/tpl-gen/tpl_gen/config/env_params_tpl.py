from pathlib import Path
from tpl_gen.lib.utils.env_utils import get_env_var, get_optional_env_var


class Environment:
    """
    The Environment class encapsulates several environment variables as properties.
    These variables include ORG, APP, ENV, TPL_SRC, CNF_SRC, HOME, PRODUCT_DIR, BASE_DIR, and TGT.

    Each property when accessed will fetch the corresponding environment variable using
    get_env_var or get_optional_env_var functions. The variables are not cached and will
    be fetched from the environment every time they are accessed.

    The properties PRODUCT_DIR, BASE_DIR, and TGT are optional and have default values
    when the corresponding environment variable is not set.
    """

    @property
    def ORG(self):
        """ORG: corresponds to the "ORG" environment variable."""
        return get_env_var("ORG")

    @property
    def APP(self):
        """APP: corresponds to the "APP" environment variable."""
        return get_env_var("APP")

    @property
    def ENV(self):
        """ENV: corresponds to the "ENV" environment variable."""
        return get_env_var("ENV")

    @property
    def TPL_SRC(self):
        """TPL_SRC: corresponds to the "TPL_SRC" environment variable."""
        return get_env_var("TPL_SRC")

    @property
    def CNF_SRC(self):
        """CNF_SRC: corresponds to the "CNF_SRC" environment variable."""
        return get_env_var("CNF_SRC")

    @property
    def HOME(self):
        """HOME: corresponds to the "HOME" environment variable."""
        return get_env_var("HOME")

    @property
    def PRODUCT_DIR(self):
        """PRODUCT_DIR: corresponds to the "PRODUCT_DIR" environment variable or its default value."""
        return get_optional_env_var("PRODUCT_DIR", Path.cwd().parent.parent.parent)

    @property
    def BASE_DIR(self):
        """BASE_DIR: corresponds to the "BASE_DIR" environment variable or its default value."""
        return get_optional_env_var("BASE_DIR", Path(self.PRODUCT_DIR).parent.parent)

    @property
    def TGT(self):
        """TGT: corresponds to the "TGT" environment variable or its default value."""
        return get_optional_env_var("TGT", self.CNF_SRC)
