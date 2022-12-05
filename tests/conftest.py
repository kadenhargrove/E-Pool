import pytest

from init import create_app
from models import db

@pytest.fixture
def app():
    app = create_app(db)
    yield app