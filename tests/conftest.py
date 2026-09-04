import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

EXISTING_ACTIVITY = "Chess Club"
EXISTING_PARTICIPANT = "michael@mergington.edu"
EMPTY_ACTIVITY = "Soccer Club"
NEW_PARTICIPANT = "newstudent@mergington.edu"


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory database so tests don't leak state into each other."""
    snapshot = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(snapshot)
