import sys, pathlib

from sqlalchemy import MetaData, Table
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.db.operators.base_operator import BaseOperator
import app.db.tables.sqlalchemy_orm as tModel
from app.models.pull_request import PullRequest
from aiomysql import Connection
from app.db.events import connect_to_db
from app.utils.global_variables import GlobalVariable
from app.models.pull_request import PullRequest
from app.models.user import User
from app.models.repository import Repository
import asyncio

class PullRequestOperator(BaseOperator):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)


    async def insert_pull_request(self, pr: PullRequest):
        try:
            async with self.connection as conn:
                async with conn.cursor() as cur:
                    await cur.execute("insert into pull_requests (owner_login, repo_name, number, state, created_at, updated_at) values (%s, %s, %s, %s, %s, %s)", (pr.owner.login, pr.repo.name, pr.number, pr.state, pr.created_at, pr.updated_at))
                    await conn.commit()
        except Exception as e:
            print("error with func insert_pull_request: %s" % (repr(e)))


if __name__ == "__main__":
    async def test_insert_pull_requests() -> None:
        await connect_to_db()
        prOp = PullRequestOperator(GlobalVariable.dbPool.acquire())
        await prOp.insert_pull_request(PullRequest(owner=User("test"), repo=Repository("test"), number=1, state="test", locked=1, created_at='2020-01-01 00:00:00', updated_at='2020-01-01 00:00:00'))

    asyncio.run(test_insert_pull_requests())