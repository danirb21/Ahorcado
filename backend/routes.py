from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from sqlalchemy import desc
from flask import request,jsonify
from .db import db
from .models import User
import re

PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]).{8,}$"

def validar_password(pwd):
    return re.match(PASSWORD_REGEX, pwd) is not None

app_routes=Blueprint("routes",__name__)

@app_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "El usuario ya existe"}), 409
    
    if not username or not password:
        return jsonify({"error": "Faltan campos"}), 400

    if not validar_password(password):
        return jsonify({"error": "Contraseña débil"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "El usuario ya existe"}), 409

    
    #Añadirle el ID de jwt al user
    u = User(username=username)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    
    return jsonify({"msg": "Usuario creado correctamente"}), 201


@app_routes.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Credenciales inválidas"}), 401

    token = create_access_token(identity=user.id)

    return jsonify({"access_token": token})



@app_routes.route("/updatescore", methods=["POST"])
@jwt_required()
def update_score():
    user_id = get_jwt_identity()
    data = request.get_json()
    score = data["score"]

    user = User.query.get(user_id)
    user.score += score
    db.session.add(user)
    db.session.commit()

@app_routes.route("/leaderboard", methods=["GET"])
@jwt_required()
def get_leaderboard():
    #user=User(id=1,username="Pepito",password="323",score=43,)
    leaderboard=db.session.query(User).order_by(desc(User.score)).all()
    leaderboard_dict = [
        {"id": u.id, "username": u.username, "score": u.score} 
        for u in leaderboard
    ]
    return jsonify(leaderboard_dict)
