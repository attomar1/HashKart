from flask import request, jsonify, make_response
from app import app, db
from app.models import Cart, CartProduct
from flask_jwt_extended import jwt_required, get_jwt
from app.enum import CartStatus
from app.utils import *


@app.route("/add-product-cart", methods=["POST"])
@jwt_required()
def add_product_cart():
    data = request.get_json()

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not product_id or not quantity:
        return make_response("product and quantity required", 400)

    product = get_product(product_id)
    if not product:
        return make_response("Wrong product", 404)
    if quantity > product["stock"]:
        return make_response("No enough Stock", 400)
    total_price = product["price"] * quantity
    user_id = get_user(email=get_jwt().get("sub"))
    cart = Cart.query.filter_by(user_id=user_id, status=CartStatus.ACTIVE).first()
    discount_applied = False

    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    cart_product = CartProduct.query.filter_by(
        cart_id=cart.id, product_id=product_id
    ).first()

    if cart_product:
        return make_response("Product Already in the cart, Please edit it", 400)

    if quantity > app.config["THRESHOLD"]:
        total_price = total_price * app.config["PERCENTAGE"] // 100
        discount_applied = True

    cart_product = CartProduct(
        product_id=product_id, quantity=quantity, cart_id=cart.id, total=total_price
    )

    cart.total += total_price
    cart_product.discount_applied = discount_applied
    db.session.add(cart_product)
    db.session.commit()

    return jsonify({"result": "product added to cart"})


@app.route("/get-cart", methods=["GET"])
@jwt_required()
def get_cart():
    user_id = get_user(email=get_jwt().get("sub"))
    cart = Cart.query.filter_by(user_id=user_id, status=CartStatus.ACTIVE).first()
    if not cart:
        return jsonify({})

    products = []
    for cart_product in cart.products:
        product = get_product(cart_product.product_id)
        products.append(
            {
                "id": cart_product.id,
                "name": product["name"],
                "price": product["price"],
                "quantity": cart_product.quantity,
                "total": cart_product.total,
                "discount_applied": cart_product.discount_applied,
                "product_id" : cart_product.product_id
            }
        )
    coupon = get_coupon(cart.coupon_id)
    return jsonify(
        {
            "products": products,
            "total": cart.total,
            "id": cart.id,
            "status" : cart.status.value,
            "coupon": coupon['code'] if coupon else None,
            "coupon_id" : cart.coupon_id
        }
    )


@app.route("/edit-cart/<cart_id>", methods=["PUT"])
@jwt_required()
def edit_cart(cart_id):
    cart = Cart.query.filter_by(id=cart_id).first()
    if not cart:
        return make_response("User don't have a active cart", 400)
    data = request.get_json()

    cart_products = data.get("products")
    if cart_products:
        for cart_product in cart_products:
            cart_product_obj = CartProduct.query.filter_by(id =cart_product['id'] ).first()
            product = get_product(cart_product_obj.product_id)
            if not cart_product['quantity']:
                continue
            if cart_product['quantity'] > product["stock"]:
                return make_response("No enough Stock", 400)
            total_price = cart_product['quantity'] * product["price"]
            if cart_product['quantity'] > app.config["THRESHOLD"]:
                total_price = total_price * app.config["PERCENTAGE"] // 100
                cart_product_obj.discount_applied = True

            cart.total = cart.total + total_price - cart_product_obj.total
            cart_product_obj.quantity = cart_product['quantity']
            cart_product_obj.total = total_price
            db.session.commit()
    
    status = data.get("status")
    if status:
        cart.status = status
    
    total = data.get("total")
    if total:
        cart.total = total
    
    coupon_id = data.get('coupon_id')
    if coupon_id:
        cart.coupon_id = coupon_id
    
    db.session.commit()

    return jsonify({"result": "Cart updated"})


@app.route("/delete-cart/<cart_id>", methods=["DELETE"])
@jwt_required()
def delete_cart(cart_id):
    cart = Cart.query.filter_by(id=cart_id).first()
    if not cart:
        return make_response("Cart not found", 404)
    db.session.delete(cart)
    db.session.commit()
    return jsonify({"result": "Cart deleted!!"})
