from app.models.jwt_query import JWTQuery
import sys, pathlib, asyncio, os
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
from apscheduler.schedulers.background import BackgroundScheduler
from app.db.operators.pull_request_operator import PullRequestOperator
from app.models.scheduler import SchedulerModel
from typing import List
from app.models.trigger import PRSchedulerTrigger
from app.services.comments import return_pr_decision_schedular
from app.services.queries import query_installations

class Scheduler():

    sched: BackgroundScheduler

    def __init__(self) -> None:
        self.sched = BackgroundScheduler()
        self.sched.add_job(self.job_make_decision, 'interval', id='1_hour_job', seconds=60*60)
        self.sched.start()
        print("the schedular is started.")

    def job_make_decision(self) -> None:
        try:
            # query prs
            prOp = PullRequestOperator()
            tasks: List[SchedulerModel] = asyncio.run(prOp.query_prScheduler_4_scheduler())

            # the installation_id may change, so we need to use bot_slug to get app_id and then get related installation_id
            installationDict = query_installations()

            # handle each task and make the decision
            for task in tasks:
                # if user remove the installation, we also need to remove it......
                asyncio.run(return_pr_decision_schedular(PRSchedulerTrigger(installation=installationDict[task.pr.owner.login], pr=task.pr)))
        except Exception as e:
            print("error with func job_make_decision: %s" % (repr(e)))