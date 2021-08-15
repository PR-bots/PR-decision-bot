# handle triggers
from gettext import install
import sys, pathlib, asyncio
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

from app.models.trigger import *
from app.models.repository import Repository
from app.models.user import User
from app.models.installation import Installation
from app.models.pull_request import PullRequest
from app.utils.time_operator import TimeOperator
from app.db.operators.pull_request_operator import PullRequestOperator
from typing import Dict

def parseTriggers(response: Dict) -> Trigger:
    try:
        repo = Repository(name=response['repository']['name'])
        owner = User(login=response['repository']['full_name'].split("/")[0])
        sender = User(login=response['sender']['login'])
        installation = Installation(id=response['installation']['id'], app_id=None) # app_id is not in the response Dict

        if "pull_request" in response:
            # create PRTrigger
            pr = PullRequest(owner=owner, repo=repo, number=response['number'], state=response['pull_request']['state'], locked=response['pull_request']['locked'], created_at=TimeOperator().convertTZTime2TimeStamp(response['pull_request']['created_at']))

            # insert into database
            async def insert_pr(pr: PullRequest) -> None:
                prOp = PullRequestOperator()
                prs = await prOp.insert_pull_request(pr=pr, installation=installation)
                return prs
            loop = asyncio.get_event_loop()
            loop.run_until_complete(insert_pr(pr))

            prTrigger = PRTrigger(installation=installation, repo=repo, sender=sender, pr=pr, action=response['action'])
            return prTrigger
    except Exception as e:
        print("error with func parseTriggers: %s" % (repr(e)))