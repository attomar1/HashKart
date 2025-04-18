from flask import request, jsonify, make_response
import uuid
from app import app, db
from app.models import DiscountCoupon, Transactions
from flask_jwt_extended import jwt_required, get_jwt
from app.utils import *
from app.enum import *


@app.route("/add-discount-coupons", methods=["POST"])
@jwt_required()
def add_discount_coupons():
    if not check_admin(get_jwt().get("sub")):
        return jsonify({"message": "Admin permission required!!"})
    coupons = request.get_json()

    for coupon in coupons:
        discount_coupon = DiscountCoupon.query.filter_by(code=coupon["code"]).first()
        if discount_coupon:
            continue
        discount_coupon = DiscountCoupon(
            public_id=str(uuid.uuid4()),
            code=coupon["code"],
            description=coupon["description"],
            discount=coupon["discount"],
        )
        db.session.add(discount_coupon)
        db.session.commit()

    return make_response("Coupon added", 200)


@app.route("/apply-coupon", methods=["POST"])
@jwt_required()
def apply_coupon():
    cart = get_cart()
    if not cart:
        return make_response("Cart not found", 404)
    if cart["coupon_id"]:
        return make_response("Coupon already applied", 400)

    data = request.get_json()
    coupon = data.get("coupon")
    if not coupon:
        return make_response("Coupon required", 400)

    discount_coupon = DiscountCoupon.query.filter_by(
        code=coupon, is_active=True
    ).first()
    if not discount_coupon:
        return make_response("Invalid Coupon", 400)

    update_cart(
        cart_id=cart["id"],
        payload={
            "total": cart["total"] * discount_coupon.discount // 100,
            "coupon_id": discount_coupon.id,
        },
    )
    db.session.commit()
    return make_response("Coupon Applied", 200)


@app.route("/payment", methods=["POST"])
@jwt_required()
def payment():
    cart = get_cart()
    if not cart:
        return make_response("Cart not found", 404)

    payload = []
    for cart_product in cart["products"]:
        product = get_product(product_id=cart_product['product_id'])
        if cart_product['quantity'] > product['stock']:
            return make_response(
                f"Product {cart_product.cart_product.name} is not in stock currently!!",
                400,
            )
        payload.append({
            "id" : cart_product['product_id'],
            "stock": product['stock'] - cart_product['quantity']
        })

    update_product(payload)
    update_cart(cart_id=cart['id'], payload={"status" :CartStatus.CLOSED.value})
    transaction = Transactions(cart=cart["id"])
    db.session.add(transaction)
    db.session.commit()
    return make_response(f"Payment Done!!", 200)


@app.route("/payments", methods=["GET"])
@jwt_required()
def get_payment():
    user_id = get_user(email=get_jwt().get("sub"))
    transactions = Transactions.query.all()
    result = []

    for transaction in transactions:
        result.append(
            {
                "transaction_id": transaction.id,
            }
        )

    return jsonify({"transactions": result})


@app.route("/get-coupon-by-id/<coupon_id>", methods=["GET"])
@jwt_required()
def get_coupon_by_id(coupon_id):
    coupon = DiscountCoupon.query.filter_by(id=coupon_id).first()
    if not coupon:
        return make_response("Coupon not found", 404)

    return jsonify({"id": coupon.id, "code": coupon.code})
