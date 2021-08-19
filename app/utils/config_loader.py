from typing import Dict
import yaml, sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

class ConfigLoader():
    
    def load_env(self) -> Dict:
        result: Dict = {}
        try:
            with open(".env.yaml") as f:
                result = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print("error with func load_env: %s" % (repr(e)))
        finally:
            return result

    def load_prediction_service_config(self) -> Dict:
        result: Dict = {}
        try:
            with open("app/prediction_service/config.yaml") as f:
                result = yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            print("error with func load_prediction_service_config: %s" % (repr(e)))
        finally:
            return result