from werkzeug.security import check_password_hash


def test_new_user(new_user):
    assert new_user.email == "test@test.com"
    assert check_password_hash(new_user.password, "Test@123")
    assert new_user.name == "Test"
