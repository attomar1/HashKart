import json
from app.utils import get_token
import requests
from app.utils import CART_SERVICE_URL

def test_get_cart(test_client):
    token = get_token()
    response = test_client.get(
        "/get-cart", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    if response.get_json():
        assert b"total" in response.data
        assert b"id" in response.data
        assert b"coupon_id" in response.data
        assert b"products" in response.data


def test_add_product_cart(test_client):
    token = get_token()
    payload = json.dumps(
        {"product_id": "7e278b83-9332-49fb-852f-eb9d6e967bb5", "quantity": 10}
    )
    response = test_client.post(
        "/add-product-cart",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    if response.status_code == 400:
        assert b"Product Already in the cart, Please edit it" in response.data
    else:
        assert response.status_code == 200


def test_edit_cart(test_client):
    token = get_token()
    res = requests.get(
        f"{CART_SERVICE_URL}/get-cart",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    if res:
        res = res.json()
        assert "products" in res.keys()
        payload = json.dumps({"total": 10})
        response = test_client.put(
            f"/edit-cart/{res.get('id')}",
            data=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
        )

        assert response.status_code == 200


def test_delete_cart(test_client):
    token = get_token()
    res = requests.get(
        f"{CART_SERVICE_URL}/get-cart",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    if res:
        res = res.json()
        assert "id" in res.keys()
        response = test_client.delete(
            f"/delete-cart/{res.get('id')}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
