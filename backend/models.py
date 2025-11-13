from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__="user"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    username: Mapped[str]= mapped_column(String(25))
    password: Mapped[str]=mapped_column(String(28))   
    score: Mapped[int]
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password={self.fullname!r}, score={self.score})"

class Game(Base):
    __tablename__="game"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True)
    word:Mapped[str]=mapped_column(String(24))
    won:Mapped[bool]=mapped_column(Boolean)
    user_id:Mapped[int]=mapped_column(ForeignKey("USER.id"))
    user:Mapped["User"]=relationship()
    
    def __repr__(self) -> str:
        return f"Game(id={self.id!r}, word={self.word!r}, won={self.won!r}, user={self.user.id})"