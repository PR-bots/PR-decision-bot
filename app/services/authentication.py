# this is the authentication service
import sys, time
sys.path.append("././")

import yaml, jwt
from app.models.jwt_query import JWTQuery
from app.models.installation import Installation
from app.services.queries import query_access_token

ALGORITHM = "RS256"

def getToken(installation: Installation) -> str:
    result: str = None
    try: 
        with open(".env.yaml") as f:
            envConfig = yaml.load(f, Loader=yaml.FullLoader)
            if "APP_ID" not in envConfig or "PRIVATE_KEY_PATH" not in envConfig:
                raise Exception("error with configuration .env.yaml")
        
        appId: int = envConfig['APP_ID']
        private_key_path: str = envConfig['PRIVATE_KEY_PATH']

        with open(private_key_path) as f:
            private_pem = f.read()
        
        payload = {
            "iat": int(time.time()) - 60,
            "exp": int(time.time()) + (10 * 60),
            "iss": appId
        }
        encoded_jwt = jwt.encode(payload, private_pem, algorithm=ALGORITHM)
        
        # query access token of the installation
        headers = {'Authorization': 'bearer ' + encoded_jwt, "Accept": "application/vnd.github.v3+json"}
        url = "https://api.github.com/app/installations/{installation_id}/access_tokens".format(installation_id=installation.id)
        jwtQuery = JWTQuery(headers=headers, url=url)
        result = query_access_token(jwtQuery)
        
    except Exception as e:
        print(repr(e))

    finally:
        return result