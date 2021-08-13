import sys
sys.path.append("././")

from app.models.pull_request import PullRequest
from app.models.installation import Installation
from app.models.repository import Repository
from app.models.user import User

class Trigger():
    installation: Installation
    repo: Repository
    sender: User

    def __init__(self, installation, repo, sender) -> None:
        self.installation = installation
        self.repo = repo
        self.sender = sender


class PRTrigger(Trigger):

    pr: PullRequest
    action: str

    def __init__(self, installation, repo, sender, pr, action) -> None:
        super(PRTrigger, self).__init__(installation, repo, sender)
        self.pr = pr
        self.action = action