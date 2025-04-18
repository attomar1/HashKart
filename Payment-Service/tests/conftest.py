from app.models import *
from werkzeug.security import generate_password_hash
import pytest
import uuid

## Model Fixtures
@pytest.fixture(scope="session")
def new_discount_coupon():
    discount_coupon = DiscountCoupon(
        public_id=str(uuid.uuid4()), code="TEST1", description="testing"
    )
    return discount_coupon


@pytest.fixture(scope="session")
def new_transactions():
    transaction = Transactions(cart=1)
    return transaction


# Functional fixture
@pytest.fixture(scope="session")
def test_client():
    from app import app as flask_app

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client
