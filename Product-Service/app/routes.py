from flask import request, jsonify, make_response
import uuid
from sqlalchemy import asc, desc
from app import app, db
from app.models import (
    Category,
    Product
)
from flask_jwt_extended import  jwt_required, get_jwt
from app.utils import check_admin
from app.enum import ProductStatus


@app.route("/categories", methods=["GET"])
@jwt_required()
def get_category():
    categories = Category.query.all()
    results = []
    for category in categories:
        results.append({"id": category.id, "name": category.name})

    return jsonify(results)


@app.route("/add-categories", methods=["POST"])
@jwt_required()
def add_category():
    if not check_admin(get_jwt().get("sub")):
        return jsonify({"message": "Admin permission required!!"})
    categories = request.get_json().get("categories")

    for category in categories:
        if Category.query.filter_by(name=category).first():
            continue
        db.session.add(Category(name=category))
        db.session.commit()

    return jsonify({"result": "Categories created"})


@app.route("/add-product", methods=["POST"])
@jwt_required()
def add_product():
    if not check_admin(get_jwt().get("sub")):
        return jsonify({"message": "Admin permission required!!"})

    products = request.get_json()
    for product in products:
        if Product.query.filter_by(name=product["name"]).first():
            continue

        new_product = Product(
            name=product["name"],
            description=product["description"],
            stock=product["stock"],
            price=product["price"],
            rating=product["rating"],
            category_id=product["category_id"],
            public_id=str(uuid.uuid4()),
        )
        db.session.add(new_product)
    db.session.commit()
    return jsonify({"result": "Product created successful"})


@app.route("/products", methods=["GET"])
@jwt_required()
def get_product():
    products = Product.query.filter_by(status=ProductStatus.ACTIVE)

    # filter
    filter_by = request.args.get("filter_by")
    search = request.args.get("search")
    if (
        filter_by
        in [
            "id",
            "name",
            "description",
            "stock",
            "price",
            "rating",
            "category",
        ]
        and search
    ):  
        if filter_by == "id":
            products = products.filter(Product.public_id == search)
        elif filter_by == "name":
            products = products.filter(Product.name.ilike(f"%{search}%"))
        elif filter_by == "description":
            products = products.filter(Product.description.ilike(f"%{search}%"))
        elif filter_by == "stock":
            products = products.filter(Product.stock == search)
        elif filter_by == "price":
            products = products.filter(Product.price == search)
        elif filter_by == "rating":
            products = products.filter(Product.rating == search)
        else:
            categories = [
                i.id
                for i in Category.query.filter(Category.name.ilike(f"%{search}%")).all()
            ]
            products = products.filter(Product.category_id.in_(categories))

    # Sorting
    sort_by = request.args.get("sort_by")
    order = request.args.get("order", "asc")
    if sort_by in [
        "name",
        "description",
        "stock",
        "price",
        "rating",
        "category",
    ] and order in ["asc", "desc"]:
        products = products.order_by(asc(sort_by) if order == "asc" else desc(sort_by))

    results = []
    for product in products:
        results.append(
            {
                "id": product.public_id,
                "name": product.name,
                "description": product.description,
                "stock": product.stock,
                "price": product.price,
                "rating": product.rating,
                "category": product.category.name,
            }
        )
    return jsonify({"result": results})


@app.route("/update-product", methods=["POST"])
@jwt_required()
def update_product():
    products = request.get_json()

    for product in products:
        product_obj = Product.query.filter_by(public_id=product['id']).first()
        if product_obj:
            product_obj.stock = product['stock']
    
    db.session.commit()
    return jsonify({"result": "Product Updated"})