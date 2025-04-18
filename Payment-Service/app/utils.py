import pytz
import requests
from app import app, models

UTC = pytz.UTC
USER_SERVICE_URL = app.config["USER_SERVICE_URL"]
PRODUCT_SERVICE_URL = app.config["PRODUCT_SERVICE_URL"]
CART_SERVICE_URL = app.config['CART_SERVICE_URL']


def get_token():
    payload = {
        "email": app.config["ADMIN_EMAIL"],
        "password": app.config["ADMIN_PASSWORD"],
    }
    response = requests.post(url=f"{USER_SERVICE_URL}/login", json=payload)
    return response.json().get("token")


def check_admin(email):
    headers={
            "Authorization": f"Bearer {get_token()}",
            "Content-Type": "application/json",
    }
    response = requests.post(
        url=f"{USER_SERVICE_URL}/check-admin", json={"email": email},
        headers=headers
    )
    if response.status_code == 400:
        return False
    return response.json().get("result")


def get_user(email):
    try:
        headers={
            "Authorization": f"Bearer {get_token()}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            url=f"{USER_SERVICE_URL}/get-user-by-email", json={"email": email},
            headers=headers
        )
        return response.json().get("id")
    except:
        return None


def get_product(product_id):
    try:
        headers={
            "Authorization": f"Bearer {get_token()}",
            "Content-Type": "application/json",
        }
        response = requests.get(
            url=f"{PRODUCT_SERVICE_URL}/products?filter_by=id&search={product_id}",
            headers=headers
        )
        return response.json().get("result")[0]
    except:
        return None


def get_cart():
    try:
        headers={
            "Authorization": f"Bearer {get_token()}",
            "Content-Type": "application/json",
        }
        response = requests.get(
            url=f"{CART_SERVICE_URL}/get-cart",
            headers=headers
        )
        return response.json()
    except:
        return None

def update_cart(cart_id, payload):
    headers={
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
    }
    response = requests.put(
        url=f"{CART_SERVICE_URL}/edit-cart/{cart_id}",
        json=payload,
        headers=headers
    )
    return response.json()

def update_product(payload):
    headers={
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        url=f"{PRODUCT_SERVICE_URL}/update-product",
        json=payload,
        headers=headers
    )
    return response.json()