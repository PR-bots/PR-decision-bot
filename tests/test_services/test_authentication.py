import sys
sys.path.append("././")

from app.services.authentication import auth

def test_auth_func() -> None:
    auth()