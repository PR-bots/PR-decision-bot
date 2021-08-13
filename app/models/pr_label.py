from app.models.user import User
import sys
sys.path.append('././')
from app.models.pull_request import PullRequest

class PRLabel():
    pr: PullRequest
    body: str