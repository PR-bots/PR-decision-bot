from app.models.user import User
import sys
sys.path.append('././')
from app.models.pull_request import PullRequest
from app.models.user import User
from typing import Optional

class PRComment():
    pr: PullRequest
    body: str
    sender: User

    def __init__(self, pr: PullRequest, body: str, sender: Optional[User] = None) -> None:
        self.pr = pr
        self.body = body
        self.sender = sender