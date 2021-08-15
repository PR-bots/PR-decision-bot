import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from typing import Optional
from app.utils.config_loader import ConfigLoader

class BaseOperator:

    engine: Optional[AsyncEngine] = None

    def __init__(self) -> None:
        try:
            self.engine = create_async_engine(ConfigLoader().load_env()["MYSQL"]["MYSQL_CONNECTION"], echo=True)
        except Exception as e:
            print("error with initialization of BaseOperator: %s" % (repr(e)))