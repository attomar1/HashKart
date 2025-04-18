import json
from app.utils import get_token


def test_get_categorys(test_client):
    token = get_token()
    response = test_client.get(
        "/categories", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_get_product(test_client):
    token = get_token()
    response = test_client.get(
        "/products?sort_by=name&order=desc&filter_by=rating&search=4",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


## Admin EndPoints
def test_add_product(test_client):
    token = get_token()
    payload = json.dumps(
        [
            {
                "name": "Iphone 14",
                "description": "iphone",
                "stock": 50,
                "price": 100000,
                "rating": 5,
                "category_id": 1,
            },
            {
                "name": "Nike Air",
                "description": "shoes",
                "stock": 50,
                "price": 5000,
                "rating": 4,
                "category_id": 2,
            },
            {
                "name": "Gym bag",
                "description": "gym",
                "stock": 5,
                "price": 500,
                "rating": 2,
                "category_id": 3,
            },
        ]
    )
    response = test_client.post(
        "/add-product",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 200
    assert b"Product created successful" in response.data


def test_add_category(test_client):
    token = get_token()
    payload = json.dumps({"categories": ["Electronics", "Fashion", "Sports"]})
    response = test_client.post(
        "/add-categories",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 200
    assert b"Categories created" in response.data
