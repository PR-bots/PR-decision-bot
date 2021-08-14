import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

from app.db.events import connect_to_db
from app.utils.global_variables import GlobalVariable
import pytest, aiomysql

@pytest.mark.asyncio
async def test_connect_to_db() -> None:
    await connect_to_db()
    assert type(GlobalVariable.dbPool) == aiomysql.pool.Pool