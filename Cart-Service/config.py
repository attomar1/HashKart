import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Auth
    SECRET_KEY = "thisissecret"
    # DB
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "cart.db")
    # discount
    PERCENTAGE =  30
    THRESHOLD = 5
    #Admin creds
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL") or 'Admin@admin.com'
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or 'Test@123'
    #Service URL
    USER_SERVICE_URL = os.environ.get("USER_SERVICE_URL") or 'http://127.0.0.1:5000'
    PRODUCT_SERVICE_URL = os.environ.get("PRODUCT_SERVICE_URL") or 'http://127.0.0.1:5001'
    CART_SERVICE_URL = os.environ.get("CART_SERVICE_URL") or 'http://127.0.0.1:5002'
    PAYMENT_SERVICE_URL = os.environ.get("PAYMENT_SERVICE_URL") or 'http://127.0.0.1:5003'

