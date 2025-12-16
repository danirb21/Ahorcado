from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    from .models import User   
    with app.app_context():
        db.create_all()
        inspector = inspect(db.engine)
        print(inspector.get_table_names()) 
        print("✔ Tablas creadas (o ya existentes).")
