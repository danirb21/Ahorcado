import tkinter as tk
from tkinter import messagebox
class ViewMode(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.title("Seleccionar modo de juego")
        self.geometry("400x280")
        self.configure(bg="lightgray")

        # ---- Título ----
        self.label_titulo = tk.Label(
            self,
            text="Selecciona el modo de juego",
            font=("Arial", 18, "bold"),
            bg="lightgray"
        )
        self.label_titulo.pack(pady=20)

        # ---- Texto explicativo del competitivo ----
        self.label_competitivo_info = tk.Label(
            self,
            text="Modo competitivo:\nRequiere iniciar sesión\npara guardar puntuación.",
            font=("Arial", 12),
            bg="lightgray",
            fg="black",
            justify="center"
        )
        self.label_competitivo_info.pack(pady=5)

        self.btn_competitivo = tk.Button(
            self,
            text="Modo competitivo",
            font=("Arial", 14),
            bg="white",
            relief="raised",
            width=20
        )
        self.btn_competitivo.pack(pady=10)

        # ---- Botón modo personalizado ----
        self.btn_personalizado = tk.Button(
            self,
            text="Modo personalizado",
            font=("Arial", 14),
            bg="white",
            relief="raised",
            width=20
        )
        self.btn_personalizado.pack(pady=10)

    # LISTENERS
    def listener_modo_competitivo(self, callback):
        """El controlador maneja la acción de modo competitivo."""
        self.btn_competitivo.config(command=callback)

    def listener_modo_personalizado(self, callback):
        """El controlador maneja la acción de modo personalizado."""
        self.btn_personalizado.config(command=callback)
        
    def show_guest(self):
        return messagebox.showwarning("Modo Invitado","No puedes acceder en modo Invitado al Competitivo")

    def _on_close(self,callback):   
        if callable(callback):
            self.protocol("WM_DELETE_WINDOW", callback)