from app.model.cpu import Cpu
from app.model.player_local import PlayerLocal
from app.view.view_ahorcado import viewAhorcado
from app.controller.game_controller import GameController
from app.model.word_provider import WordProvider
from app.view.view_configuracion import ViewConfiguracion
from app.view.view_login import LoginView
from app.view.view_register import RegisterView
from app.view.view_mode import ViewMode
def main():
    view=viewAhorcado()
    cpu=Cpu(WordProvider.getRandomWord("app/data/palabras.txt"))
    user=PlayerLocal("Pepito")
    view_conf=ViewConfiguracion()
    view_register=RegisterView()
    view_login=LoginView()
    view_mode=ViewMode()
    GameController(cpu,user,view,view_conf,view_login,view_register,view_mode)
    view_conf.mainloop()
    view.mainloop()
if __name__=="__main__":
    main()