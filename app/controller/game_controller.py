from app.model.cpu import Cpu
from app.model.user import User
from view.view_ahorcado import viewAhorcado

class GameController:
    def __init__(self,cpu,user,viewAhorcado):
        self.cpu=cpu
        self.user=user
        self.viewAhorcado=viewAhorcado
        