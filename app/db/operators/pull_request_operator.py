import sys, pathlib, asyncio
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.db.operators.base_operator import BaseOperator
import app.db.tables.sqlalchemy_orm as tModel
from app.models.pull_request import PullRequest
from app.models.pull_request import PullRequest
from app.models.user import User
from app.models.repository import Repository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, text
from app.utils.config_loader import ConfigLoader
from typing import List

class PullRequestOperator(BaseOperator):
    def __init__(self) -> None:
        super().__init__()


    '''
    check whether pr exists, if exists then update
    '''
    async def insert_pull_request(self, pr: PullRequest) -> None:
        def run_queries(session):
            session.execute(insert(tModel.PullRequest).values(
                owner_login = pr.owner.login,
                repo_name = pr.repo.name,
                installation_id = pr.installation.id,
                number = pr.number,
                state = pr.state,
                locked = pr.locked,
                created_at = pr.created_at,
                last_comment_at = pr.last_comment_at
            ))
        try:
            async with AsyncSession(self.engine) as session:
                await session.run_sync(run_queries)
                await session.commit()
        except Exception as e:
            print("error with func insert_pull_request: %s" % (repr(e)))


    async def update_pull_request(self, pr: PullRequest) -> None:
        try:
            pass
        except Exception as e:
            print("error with func update_pull_request: %s" % (repr(e)))

    
    async def query_prs_4_scheduler(self) -> List[PullRequest]:
        try:
            result: List[PullRequest] = []
            env = ConfigLoader().load_env()
            async with self.engine.connect() as connection:
                q = '''
                select pr.id, pr.owner_login, pr.repo_name, pr.number
                from pull_requests pr
                where last_comment_at < TIMESTAMPADD(HOUR, -%s, UTC_TIMESTAMP())
                order by last_comment_at asc
                ''' 
                query_result = await connection.execute(text(q % env["SCHEDULER"]["CYCLE_HOUR"]))
                for row in query_result:
                    pr = PullRequest(owner=User(login=row['owner_login']), repo=Repository(name=row['repo_name']), number=row['number'], id=row['id'])
                    result.append(pr)
                return result
        except Exception as e:
            print("error with func query_prs_4_scheduler: %s" % (repr(e)))


if __name__ == "__main__":

    async def test_insert_pull_requests() -> None:
        prOp = PullRequestOperator()
        await prOp.query_prs_4_schedular()
        # await prOp.insert_pull_request(PullRequest(owner=User("test"), repo=Repository("test"), number=1, state="open", locked=1, created_at='2020-01-01 00:00:00'))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_insert_pull_requests())