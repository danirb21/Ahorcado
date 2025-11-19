import tkinter as tk
from app.controller.game_controller import GameController
def main():
    root=tk.Tk()
    root.withdraw()
    GameController(root)
if __name__=="__main__":
    main()