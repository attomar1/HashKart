import json
from app.utils import get_token
import requests


def test_apply_coupon(test_client):
    token = get_token()
    payload = json.dumps({"coupon": "TEST1"})
    response = test_client.post(
        "/apply-coupon",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    if response.status_code == 404:
        assert b"Cart not found" in response.data
    elif response.status_code == 400:
        assert b"Coupon already applied" in response.data
    else:
        assert response.status_code == 200
        assert b"Coupon Applied" in response.data

    # Test for no coupon
    response = test_client.post(
        "/apply-coupon",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    if response.status_code == 404:
        assert b"Cart not found" in response.data
    else:
        assert response.status_code == 400
        assert b"Coupon already applied" in response.data or b'Coupon required' in response.data

    # Test for wrong coupon
    payload = json.dumps({"coupon": "WRONGCOUPON"})
    response = test_client.post(
        "/apply-coupon",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    if response.status_code == 404:
        assert b"Cart not found" in response.data
    else:
        assert response.status_code == 400
        assert b"Coupon already applied" in response.data or b'Invalid Coupon' in response.data

def test_payment(test_client):
    token = get_token()
    response = test_client.post(
        "/payment",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    if response.status_code == 404:
        assert b"Cart not found" in response.data
    else:
        assert response.status_code == 200
        assert b"Payment Done!!" in response.data


def test_get_payment(test_client):
    token = get_token()
    response = test_client.get(
        "payments",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200
    assert "transactions" in response.get_json().keys()


## Admin endpoints
def test_add_discount_coupons(test_client):
    token = get_token()
    payload = json.dumps(
        [
            {"code": "TEST1", "description": "test", "discount": 25},
            {"code": "TEST2", "description": "test", "discount": 30},
            {"code": "TEST3", "description": "test", "discount": 75},
        ]
    )
    response = test_client.post(
        "/add-discount-coupons",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 200
    assert b"Coupon added" in response.data
