import sys, pathlib
from turtle import update

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
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

class PullRequestOperator(BaseOperator):
    def __init__(self) -> None:
        super().__init__()


    async def insert_pull_request(self, pr: PullRequest):
        def run_queries(session):
            session.execute(insert(tModel.PullRequest).values(
                owner_login = pr.owner.login,
                repo_name = pr.repo.name,
                number = pr.number,
                state = pr.state,
                locked = pr.locked,
                created_at = pr.created_at,
                updated_at = pr.updated_at
            ))
        try:
            async with AsyncSession(self.engine) as session:
                await session.run_sync(run_queries)
                await session.commit()
                print("pause")
        except Exception as e:
            print("error with func insert_pull_request: %s" % (repr(e)))


if __name__ == "__main__":

    import pymysql
    pymysql.install_as_MySQLdb() # we are using python3
    async def test_insert_pull_requests() -> None:
        # await connect_to_db()
        prOp = PullRequestOperator()
        await prOp.insert_pull_request(PullRequest(owner=User("test"), repo=Repository("test"), number=1, state="test", locked=1, created_at='2020-01-01 00:00:00', updated_at='2020-01-01 00:00:00'))

    asyncio.run(test_insert_pull_requests())