import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.db.operators.pull_request_operator import PullRequestOperator
import pytest
from app.models.pull_request import PullRequest
from app.models.user import User
from app.models.repository import Repository

@pytest.mark.asyncio
async def test_insert_pull_requests() -> None:
    prOp = PullRequestOperator()
    await prOp.insert_pull_request(PullRequest(owner=User("zxh2"), repo=Repository("test"), number=1, state="open", locked=1, created_at='2020-01-01 00:00:00'))

@pytest.mark.asyncio
async def test_query_prs_4_schedular() -> None:
    prOp = PullRequestOperator()
    result = await prOp.query_prs_4_schedular()
    assert len(result) > 0