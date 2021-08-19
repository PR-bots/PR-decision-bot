# predict using the trained model

import sys, pathlib
from typing import List, Dict
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

from app.models.pull_request import PullRequest
from app.models.installation import Installation
from app.prediction_service.factor_getter import FactorGetter
from app.utils.config_loader import ConfigLoader

class Predictor():

    modelSubmission = None
    modelProcess = None
    type: str

    def __init__(self, modelSubmission, modelProcess, type) -> None:
        self.modelSubmission = modelSubmission
        self.modelProcess = modelProcess
        self.type = type

    def _get_factors(self, pr: PullRequest, installation: Installation) -> Dict:
        result: Dict
        result = FactorGetter(pr, installation).query_pr_infos()
        return result

    def _factor_cut_suffix(self, s, suffixList):
        try:
            for suffix in suffixList:
                if s.endswith(suffix):
                    return s[:-len(suffix)]
            return s
        except Exception as e:
            print("error with func _factor_cut_suffix: %s" % (repr(e)))

    def predict(self, pr: PullRequest, installation: Installation) -> bool:
        try:
            # get the factors for this pr
            factorDict = self._get_factors(pr, installation)
            factorList = ConfigLoader().load_prediction_service_config()["trainer"]["factor_list"][self.type]
            X_test = [factorDict[self._factor_cut_suffix(f, ["_open", "_close"])] for f in factorList]
            if self.type == "submission":
                predictions = self.modelSubmission.predict([X_test])
            elif self.type == "process":
                predictions = self.modelSubmission.predict([X_test])

            if predictions[0] == 1:
                return True
            else:
                return False
        except Exception as e:
            print("error with func predict: %s" % (repr(e)))