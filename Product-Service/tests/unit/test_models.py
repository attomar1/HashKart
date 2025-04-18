from werkzeug.security import check_password_hash


def test_new_category(new_category):
    assert new_category.name == "Sports"


def test_new_product(new_product):
    assert new_product.name == "Cricket Bat"
    assert new_product.description == "Cricket"
    assert new_product.stock == 100
    assert new_product.price == 9000.99
    assert new_product.rating == 4
    assert new_product.category_id == 1
