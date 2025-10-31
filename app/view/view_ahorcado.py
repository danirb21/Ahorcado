import tkinter as tk
import turtle as turtle

class viewAhorcado(tk.Tk):
    def __init__(self, view):
        super.__init__()
        self.title("Ahorcado")
        self.frame=tk.Frame(self,bg="lightgray", padx=10, pady=10)
        self.word_label=tk.Label(self.frame,font=("Arial",22))
        self.send_letter=tk.Button(self.frame,text="send letter")
        self.input_text=tk.Text(self.frame,)
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()

        # Turtle integrado en el canvas
        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.t = turtle.RawTurtle(self.turtle_screen)
        self.t.hideturtle()
        self.t.speed(0)
    
    def setLabelWord(self,word):
        self.word_label.config(word)
    
    
    def listenerSendLetter(self, callback):
        self.send_letter.bind(callback)
    
    def getInputText(self):
        return self.input_text.get("1.0",'end-1c')
    
    def drawAhorcado(self,errores):
        self.tur