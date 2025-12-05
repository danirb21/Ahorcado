import os
import secrets
from flask_jwt_extended import JWTManager
from flask import Flask
from dotenv import load_dotenv
load_dotenv()

jwt=JWTManager()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY"),
        DATABASE=os.path.join(app.instance_path, 'ahorcado.sqlite'),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'ahorcado.sqlite')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Inicializar base de datos
    from .db import init_db
    init_db(app)
    
    jwt.init_app(app)
    
    from .routes import app_routes
    app.register_blueprint(app_routes)
    #print("Instance path:", app.instance_path)
    return app