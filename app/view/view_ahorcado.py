import tkinter as tk
import turtle as turtle
from tkinter import messagebox

class viewAhorcado(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ahorcado")
        # Frame principal
        self.frame = tk.Frame(self, bg="lightgray", padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        # Label de palabra
        self.word_label = tk.Label(self.frame, font=("Arial", 22), bg="lightgray")
        self.word_label.pack(pady=10)

        # Canvas y turtle
        self.canvas = tk.Canvas(self.frame, width=400, height=300, bg="white")
        self.canvas.pack(pady=10)

        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.t = turtle.RawTurtle(self.turtle_screen)
        self.t.hideturtle()
        self.t.speed(0)

        # Frame inferior (input + botón)
        self.input_frame = tk.Frame(self.frame, bg="lightgray")
        self.input_frame.pack(side="bottom", pady=10)

        # Input a la izquierda
        self.input_text = tk.Text(self.input_frame, height=1, width=10, font=("Arial", 16))
        self.input_text.pack(side="left", padx=10)
        self.input_text.bind("<Return>", self._on_enter_pressed)

        # Botón a la derecha
        self.send_letter = tk.Button(self.input_frame, text="Enviar letra")
        self.send_letter.pack(side="right", padx=10)
    
    def setLabelWord(self,word):
        self.word_label.config(text=word)
    
    def _on_enter_pressed(self, event):
    # Ejecutar la misma función que el botón
        if hasattr(self, "_callback_send_letter"):
            self._callback_send_letter()
    # Evitar que el Enter agregue un salto de línea
        return "break"
    
    def listenerSendLetter(self, callback):
         self.send_letter.config(command=callback)
         self.input_text.bind("<Return>", callback)
    
    def getInputText(self):
        text=self.input_text.get("1.0",'end-1c')
        text=text.strip().replace(" ","")
        return text
    
    def clearInputText(self):
        self.input_text.delete("1.0", "end")
    
    def getLabelWord(self):
        return self.word_label.cget("text")
    
    def drawAhorcado(self, errors):
        self.t.pensize(2)
        self.t.speed(0)
        self.t.penup()

        if errors == 1:
            # Base
            self.t.goto(-100, -100)
            self.t.pendown()
            self.t.forward(150)
            self.t.penup()
        elif errors == 2:
            # Poste vertical
            self.t.goto(-75, -100)
            self.t.setheading(90)
            self.t.pendown()
            self.t.forward(200)
            self.t.penup()
        elif errors == 3:
            # Brazo superior
            self.t.goto(-75, 100)
            self.t.setheading(0)
            self.t.pendown()
            self.t.forward(100)
            self.t.penup()
        elif errors == 4:
            # Cuerda
            self.t.goto(25, 100)
            self.t.setheading(-90)
            self.t.pendown()
            self.t.forward(30)
            self.t.penup()
        elif errors == 5:
            # Cabeza
            self.t.goto(25, 70)
            self.t.setheading(0)
            self.t.pendown()
            self.t.circle(15)
            self.t.penup()
        elif errors == 6:
            # Cuerpo
            self.t.goto(25, 70)
            self.t.setheading(-90)
            self.t.pendown()
            self.t.forward(50)
            self.t.penup()
        elif errors == 7:
            # Brazo izquierdo
            self.t.goto(25, 50)
            self.t.setheading(210)
            self.t.pendown()
            self.t.forward(30)
            self.t.penup()
        elif errors == 8:
            # Brazo derecho
            self.t.goto(25, 50)
            self.t.setheading(-30)
            self.t.pendown()
            self.t.forward(30)
            self.t.penup()
        elif errors == 9:
            # Pierna izquierda
            self.t.goto(25, 20)
            self.t.setheading(240)
            self.t.pendown()
            self.t.forward(35)
            self.t.penup()
        elif errors == 10:
            # Pierna derecha
            self.t.goto(25, 20)
            self.t.setheading(-60)
            self.t.pendown()
            self.t.forward(35)
            self.t.penup()
            
    def mostrar_ganado(self):
        messagebox.showinfo("🎉 ¡Has ganado!", "¡Felicidades, adivinaste la palabra!")
        self.destroy()  # Cierra la ventana principal

    def mostrar_perdido(self, palabra_correcta: str):
        messagebox.showinfo("💀 Has perdido", f"La palabra era: {palabra_correcta}")
        self.destroy()