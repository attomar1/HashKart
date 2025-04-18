from werkzeug.security import generate_password_hash
import pytest
import uuid
from app import models

## Model Fixtures
@pytest.fixture(scope="session")
def new_user():
    user = models.User(
        public_id=str(uuid.uuid4()),
        email="test@test.com",
        password=generate_password_hash("Test@123"),
        name='Test'
    )
    return user


# Functional fixture
@pytest.fixture(scope="session")
def test_client():
    from app import app as flask_app

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
