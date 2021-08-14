import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

from app.models.trigger import *

def test_pr_trigger():
    pass