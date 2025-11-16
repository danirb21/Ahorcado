import tkinter as tk
from tkinter import messagebox


class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inicio de Sesión: AHORCADO")
        self.geometry("350x260")
        self.configure(bg="lightgray")
        self.resizable(False, False)

        # ---- Título ----
        self.label_title = tk.Label(
            self,
            text="🔐 Iniciar sesión",
            font=("Arial", 18, "bold"),
            bg="lightgray"
        )
        self.label_title.pack(pady=20)

        # ---- Frame para usuario/contraseña ----
        frame = tk.Frame(self, bg="lightgray")
        frame.pack()

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="lightgray").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_user = tk.Entry(frame, font=("Arial", 12))
        self.entry_user.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="lightgray").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_password = tk.Entry(frame, font=("Arial", 12), show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        # ---- Botón Login ----
        self.btn_login = tk.Button(self, text="Entrar", font=("Arial", 12), bg="white")
        self.btn_login.pack(pady=10)

        # ---- Botón Ir a Registro ----
        self.btn_register = tk.Button(self, text="Crear cuenta", font=("Arial", 11), bg="white")
        self.btn_register.pack(pady=5)

    # -------- Métodos MVC --------
    def get_username(self):
        return self.entry_user.get().strip()

    def get_password(self):
        return self.entry_password.get().strip()

    def listener_login(self, callback):
        self.btn_login.config(command=callback)

    def listener_register(self, callback):
        self.btn_register.config(command=callback)

    def show_error(self, message):
        messagebox.showerror("Error", message)
        
    def show_dont_exist(self, message):
        messagebox.showwarning("Usuario no encontrado",message)
        
    def _on_close(self,callback):   
        if callable(callback):
            self.protocol("WM_DELETE_WINDOW", callback)
