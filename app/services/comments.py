# the services related to labels
import sys, requests, pathlib, json
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
from app.services.authentication import getToken
from app.models.pr_comment import PRComment
from app.models.trigger import *

def return_pr_decision(prTrigger: PRTrigger) -> bool:
    try:
        token = getToken(prTrigger.installation)
        comment = PRComment(pr=prTrigger.pr, body="This is the decision from bot")
        headers = {'Authorization': 'token ' + token, 'Accept': 'application/vnd.github.v3+json'}
        url = "https://api.github.com/repos/{owner}/{repo}/issues/{pull_request_number}/comments".format(owner=comment.pr.owner.login, repo=comment.pr.repo.name, pull_request_number=comment.pr.number)
        data = {"body": comment.body}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code != 200:
            raise Exception("error with func return_pr_decision: code: %s, message: %s" % (response.status_code, json.loads(response.text)["message"]))
        print("pause")
    except Exception as e:
        print("error with func return_pr_decision: %s" % (repr(e)))


if __name__ == "__main__":
    return_pr_decision()