from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from flask_bcrypt import generate_password_hash, check_password_hash
from .db import db

class User(db.Model):
    __tablename__="user"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    username: Mapped[str]= mapped_column(String(25))
    password_hash: Mapped[str]=mapped_column(String(80))   
    score: Mapped[int]=mapped_column(nullable=True)
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password_hash!r}, score={self.score})"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)