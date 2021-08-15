import sys, pathlib, asyncio
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.db.operators.base_operator import BaseOperator
import app.db.tables.sqlalchemy_orm as tModel
from app.models.pull_request import PullRequest
from app.models.scheduler import PRScheduler
from app.models.user import User
from app.models.repository import Repository
from app.models.installation import Installation
from sqlalchemy import insert, text
from app.utils.config_loader import ConfigLoader
from typing import List

class PullRequestOperator(BaseOperator):
    def __init__(self) -> None:
        super().__init__()


    async def insert_pull_request(self, pr: PullRequest, installation: Installation) -> None:

        try:
            async with self.engine.connect() as connection:
                q = """
                    select id 
                    from pull_requests 
                    where owner_login=:owner_login and repo_name=:repo_name and number=:number;
                """ 
                query_result = await connection.execute(text(q), {'owner_login': pr.owner.login, 'repo_name': pr.repo.name, 'number': pr.number})
                if query_result.rowcount == 0:
                    q = """
                        insert into pull_requests (
                            owner_login, repo_name, number, state, created_at, locked, last_comment_at, installation_id
                        ) values (:owner_login, :repo_name, :number, :state, :created_at, :locked, :last_comment_at, :installation_id);
                    """
                    await connection.execute(text(q), {
                        "owner_login": pr.owner.login, 
                        "repo_name": pr.repo.name, 
                        "number": pr.number, 
                        "state": pr.state, 
                        "created_at": pr.created_at, 
                        "locked": pr.locked, 
                        "last_comment_at": pr.last_comment_at, 
                        "installation_id": installation.id
                    })
                else:
                    q = """
                        update pull_requests set
                        state=:state,
                        locked=:locked,
                        installation_id=:installation_id
                        where owner_login=:owner_login and repo_name=:repo_name and number=:number;
                    """
                    await connection.execute(text(q), {
                        "state": pr.state,
                        "locked": pr.locked, 
                        "installation_id": installation.id,
                        "owner_login": pr.owner.login, 
                        "repo_name": pr.repo.name, 
                        "number": pr.number
                    })
                await connection.commit()
        except Exception as e:
            print("error with func insert_pull_request: %s" % (repr(e)))


    async def update_pull_request(self, pr: PullRequest) -> None:
        try:
            pass
        except Exception as e:
            print("error with func update_pull_request: %s" % (repr(e)))

    
    async def query_prScheduler_4_scheduler(self) -> List[PRScheduler]:
        try:
            result: List[PRScheduler] = []
            env = ConfigLoader().load_env()
            async with self.engine.connect() as connection:
                q = """
                    select pr.id, pr.owner_login, pr.repo_name, pr.number, pr.installation_id
                    from pull_requests pr
                    where state='open' and locked=0 and
                    (last_comment_at is null or 
                    last_comment_at < TIMESTAMPADD(HOUR, -%s, UTC_TIMESTAMP()))
                    order by last_comment_at asc
                """ 
                query_result = await connection.execute(text(q % env["SCHEDULER"]["CYCLE_HOUR"]))
                for row in query_result:
                    pr = PRScheduler(installation=Installation(id=row['installation_id']), pr=PullRequest(owner=User(login=row['owner_login']), repo=Repository(name=row['repo_name']), number=row['number'], id=row['id']))
                    result.append(pr)
                return result
        except Exception as e:
            print("error with func query_prScheduler_4_scheduler: %s" % (repr(e)))


if __name__ == "__main__":

    async def test_insert_pull_requests() -> None:
        prOp = PullRequestOperator()
        await prOp.query_prScheduler_4_scheduler()
        # await prOp.insert_pull_request(PullRequest(owner=User("test2"), repo=Repository("test"), number=1, state="open", locked=1, created_at='2020-01-01 00:00:00'), installation=Installation(id=1))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_insert_pull_requests())