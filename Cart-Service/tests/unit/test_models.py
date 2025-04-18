def test_new_cart(new_cart):
    assert new_cart.user_id == 1
    assert new_cart.total == 10.0


def test_new_cart_product(new_cart_product):
    assert new_cart_product.product_id == "e1b49c07-210c-40ca-b47f-fd2bb2949618"
    assert new_cart_product.cart_id == 1
    assert new_cart_product.quantity == 100
    assert new_cart_product.total == 100
