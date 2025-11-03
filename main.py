from app.model.cpu import Cpu
from app.model.user import User
from app.view.view_ahorcado import viewAhorcado
from app.controller.game_controller import GameController
from app.model.word_provider import WordProvider
def main():
    view=viewAhorcado()
    cpu=Cpu(WordProvider.getRandomWord("app/data/palabras.txt"),5)
    user=User("Pepito")
    GameController(cpu,user,view)
    view.mainloop()
if __name__=="__main__":
    main()