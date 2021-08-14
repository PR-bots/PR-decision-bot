import aiomysql
from typing import Optional

class GlobalVariable():

    dbPool: Optional[aiomysql.pool.Pool] = None