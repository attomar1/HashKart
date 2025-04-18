from app.models import *
from werkzeug.security import generate_password_hash
import pytest
import uuid


## Model Fixtures
@pytest.fixture(scope="session")
def new_cart():
    cart = Cart(public_id=str(uuid.uuid4()), user_id=1, total=10.0)
    return cart


@pytest.fixture(scope="session")
def new_cart_product():
    cart_product = CartProduct(
        product_id="e1b49c07-210c-40ca-b47f-fd2bb2949618",
        cart_id=1,
        quantity=100,
        total=100,
    )
    return cart_product


# Functional fixture
@pytest.fixture(scope="session")
def test_client():
    from app import app as flask_app

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
