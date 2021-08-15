import sys, pathlib, asyncio, os
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.db.operators.pull_request_operator import PullRequestOperator
from app.models.scheduler import SchedulerModel
from typing import List
from app.models.trigger import PRSchedulerTrigger
from app.services.comments import return_pr_decision

class Scheduler():

    sched: AsyncIOScheduler

    def __init__(self) -> None:
        self.sched = AsyncIOScheduler(timezone='UTC')
        self.sched.add_job(self.job_make_decision, 'interval', id='20_seconds_job', seconds=20)
        self.sched.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
        try:
            asyncio.get_event_loop().run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass

    async def job_make_decision(self) -> None:
        try:
            # query prs
            prOp = PullRequestOperator()
            tasks: List[SchedulerModel] = await prOp.query_prScheduler_4_scheduler()

            # handle each task(schedu) and make the decision
            for task in tasks:
                return_pr_decision(PRSchedulerTrigger(installation=task.installation, pr=task.pr))
        except Exception as e:
            print("error with func job_make_decision: %s" % (repr(e)))

    

if __name__ == "__main__":
    s = Scheduler()