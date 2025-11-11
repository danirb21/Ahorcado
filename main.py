from app.model.cpu import Cpu
from app.model.user import User
from app.view.view_ahorcado import viewAhorcado
from app.controller.game_controller import GameController
from app.model.word_provider import WordProvider
from app.view.view_configuracion import ViewConfiguracion
def main():
    view=viewAhorcado()
    cpu=Cpu(WordProvider.getRandomWord("app/data/palabras.txt"))
    user=User("Pepito")
    view_conf=ViewConfiguracion()
    GameController(cpu,user,view,view_conf)
    view_conf.mainloop()
    view.mainloop()
if __name__=="__main__":
    main()