from werkzeug.security import check_password_hash

def test_new_discount_coupon(new_discount_coupon):
    assert new_discount_coupon.code == "TEST1"
    assert new_discount_coupon.description == "testing"


def test_new_transaction(new_transactions):
    assert new_transactions.cart == 1
