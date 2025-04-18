from datetime import datetime
from sqlalchemy import Enum, CheckConstraint
from app import db
from app.enum import ProductStatus
from datetime import datetime
from app.utils import UTC


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    products = db.relationship("Product", backref="category", lazy=True)


class Product(db.Model):
    __tablename__ = "product"
    __table_args__ = (
        CheckConstraint("rating >=0 AND rating <=5", name="rating_range"),
    )
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
    stock = db.Column(db.Integer, default=0)
    price = db.Column(db.Float)
    rating = db.Column(db.Integer)
    status = db.Column(Enum(ProductStatus), default=ProductStatus.ACTIVE)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    created_at = db.Column(db.DateTime, default=datetime.now(tz=UTC))
    updated_at = db.Column(
        db.DateTime, default=datetime.now(tz=UTC), onupdate=datetime.now(tz=UTC)
    )
