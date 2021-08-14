from typing import Dict
import yaml

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
