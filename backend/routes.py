from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from sqlalchemy import desc
from flask import request,jsonify
from .db import db
from .models import User
import re

PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$"

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

    token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": token})



@app_routes.route("/updatescore", methods=["POST"])
@jwt_required()
def update_score():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    score = data["score"]
    #print("USER ID:", user_id)
    #print("HEADERS:", request.headers)
    #print("JSON:", request.get_json(silent=True))
    
    user = User.query.get(user_id)
    if user.score is None:
        user.score = 0
        
    user.score = user.score+score
    total_score=user.score
    db.session.commit()
    return jsonify({"total_score":total_score}),200
    

@app_routes.route("/leaderboard", methods=["GET"])
@jwt_required()
def get_leaderboard():
    leaderboard=db.session.query(User).order_by(desc(User.score)).all()
    #print(leaderboard)
    leaderboard_dict = [
        {"username": u.username, "score": u.score} 
        for u in leaderboard
    ]
    return jsonify(leaderboard_dict)
