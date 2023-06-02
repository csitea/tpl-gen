from models.TplGenParams import TplGenParams


class TplGenStepParams(TplGenParams):
    STEP: str

    def __init__(
        self,
        org: str,
        app: str,
        env: str,
        base_dir: str,
        product_dir: str,
        output_dir: str,
        cnf_src: str,
        tpl_src: str,
        step: str,
    ) -> None:
        self.STEP = step
        super().__init__(
            org, app, env, base_dir, product_dir, output_dir, cnf_src, tpl_src
        )
