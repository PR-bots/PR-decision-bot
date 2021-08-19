import re, sys, pathlib, asyncio
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
import json5 as json
from app.services.comments import return_pr_decision
from app.services.triggers import parseTriggers
from app.models.trigger import Trigger, PRTrigger
from wsgiref.simple_server import make_server
from app.prediction_service.trainer import Trainer
from app.utils.global_variables import GlobalVariable
from app.services.queries import query_app_id, query_installations
from app.services.scheduler import Scheduler

def application(environ, start_response) -> bytearray:
    start_response('200 OK', [('Content-Type', 'application/json')])
    
    request_body = environ["wsgi.input"].read(int(environ.get("CONTENT_LENGTH", 0)))
    
    json_str = request_body.decode('utf-8')
    json_str = re.sub('\'','\"', json_str)
    json_dict = json.loads(json_str)

    trigger: Trigger = parseTriggers(json_dict)

    # only when the trigger is open pull request can return the result
    if type(trigger) == PRTrigger and trigger.action == "opened":
        return_pr_decision(trigger)

    return ["success".encode('utf-8')]
 
 
if __name__ == "__main__":

    # train the prediction model
    GlobalVariable.trainer = Trainer()
    # request appId from GitHub
    GlobalVariable.appId = query_app_id()

    s = Scheduler()

    port = 4567
    httpd = make_server("0.0.0.0", port , application)
    print("serving http on port {0}...".format(str(port)))
    httpd.serve_forever()