from sqlalchemy import Enum, CheckConstraint
from app import db


class DiscountCoupon(db.Model):
    __tablename__ = "discount_coupon"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    code = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text())
    discount = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class Transactions(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    cart = db.Column(db.Integer)