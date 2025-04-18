from app.models import *
from werkzeug.security import generate_password_hash
import pytest
import uuid

## Model Fixtures
@pytest.fixture(scope="session")
def new_category():
    category = Category(name="Sports")
    return category


@pytest.fixture(scope="session")
def new_product():
    product = Product(
        public_id=str(uuid.uuid4()),
        name="Cricket Bat",
        description="Cricket",
        stock=100,
        price=9000.99,
        rating=4,
        category_id=1,
    )
    return product


# Functional fixture
@pytest.fixture(scope="session")
def test_client():
    from app import app as flask_app

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
