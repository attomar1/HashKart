from datetime import datetime
from sqlalchemy import Enum
from app import db
from app.enum import CartStatus
from datetime import datetime
from app.utils import UTC


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    products = db.relationship("CartProduct", backref="cart_products", lazy=True)
    user_id = db.Column(db.Integer)
    status = db.Column(Enum(CartStatus), default=CartStatus.ACTIVE)
    total = db.Column(db.Float, default=0.0)
    coupon_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=UTC))
    updated_at = db.Column(
        db.DateTime, default=datetime.now(tz=UTC), onupdate=datetime.now(tz=UTC)
    )


class CartProduct(db.Model):
    __tablename__ = "cart_product"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
    quantity = db.Column(db.Integer)
    total = db.Column(db.Integer)
    discount_applied = db.Column(db.Boolean, default=False)

