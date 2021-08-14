import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

from app.services.authentication import auth

def test_auth_func() -> None:
    auth()