import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Auth
    SECRET_KEY = "thisissecret"
    # DB
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "user.db")
    # discount
    PERCENTAGE =  30
    THRESHOLD = 5
    #Admin creds
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL") or 'Admin@admin.com'
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or 'Test@123'