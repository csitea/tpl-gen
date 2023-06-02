from models.BaseModels import OAEModel, TplPathsModel


class TplGenParams:
    OAE: OAEModel
    PATHS: TplPathsModel

    def __init__(self, oae: OAEModel, paths: TplPathsModel) -> None:
        self.OAE = oae
        self.PATHS = paths
