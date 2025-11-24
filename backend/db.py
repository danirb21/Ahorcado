from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
db = SQLAlchemy()

def init_db(app):
    db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
    """Inicializa la base de datos con la app."""
    db.init_app(app)
    # Si quieres crear las tablas automáticamente:
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
            print("Base de datos creada por primera vez.")
    else:
        print("✔ Base de datos ya existente, no se crea de nuevo.")
