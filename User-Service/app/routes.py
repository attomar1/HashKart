from flask import request, jsonify, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required


@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user:
        return make_response("User already exists!!", 400)
    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        public_id=str(uuid.uuid4()),
        email=data["email"],
        name=data["name"],
        password=hashed_password,
    )
    db.session.add(new_user)
    db.session.commit()

    response = jsonify({"message": "New user created!"})
    return response


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    response = None
    error_response = make_response(
        "Could not verify, Incorrect username or password",
        401,
        {"WWW-Authenticate": 'Basic realm="Login required!"'},
    )
    if not email or not password:
        return error_response

    user = User.query.filter_by(email=email).first()

    if not user:
        return error_response

    if check_password_hash(user.password, password):
        token = create_access_token(identity=email)
        response = jsonify({"token": token})

    return response


@app.route("/check-admin", methods=["POST"])
@jwt_required()
def check_admin():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return make_response("Email Required!!", 400)

    user = User.query.filter_by(email=email).first()

    if not user or not user.admin:
        return jsonify({"result": False})
    return jsonify({"result": True})


@app.route("/get-user-by-email", methods=["POST"])
@jwt_required()
def get_user_by_email():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return make_response("Email Required!!", 400)

    user = User.query.filter_by(email=email).first()

    if not user:
        return make_response("User Not Found!!", 400)
    return jsonify({"id": user.id})
