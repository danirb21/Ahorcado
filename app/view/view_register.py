import tkinter as tk
from tkinter import messagebox


class RegisterView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro")
        self.geometry("370x300")
        self.configure(bg="lightgray")
        self.resizable(False, False)

        # ---- Título ----
        self.label_title = tk.Label(
            self,
            text="📝 Crear cuenta",
            font=("Arial", 18, "bold"),
            bg="lightgray"
        )
        self.label_title.pack(pady=20)

        frame = tk.Frame(self, bg="lightgray")
        frame.pack()

        tk.Label(frame, text="Usuario:", font=("Arial", 12), bg="lightgray").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_user = tk.Entry(frame, font=("Arial", 12))
        self.entry_user.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Contraseña:", font=("Arial", 12), bg="lightgray").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_pass1 = tk.Entry(frame, font=("Arial", 12), show="*")
        self.entry_pass1.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Repetir contraseña:", font=("Arial", 12), bg="lightgray").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_pass2 = tk.Entry(frame, font=("Arial", 12), show="*")
        self.entry_pass2.grid(row=2, column=1, pady=5)

        # ---- Botón Registrar ----
        self.btn_register = tk.Button(self, text="Registrar", font=("Arial", 12), bg="white")
        self.btn_register.pack(pady=15)

        # ---- Botón volver ----
        self.btn_back = tk.Button(self, text="Volver", font=("Arial", 11), bg="white")
        self.btn_back.pack()

    # -------- Métodos MVC --------
    def get_username(self):
        return self.entry_user.get().strip()

    def get_passwords(self):
        return self.entry_pass1.get().strip(), self.entry_pass2.get().strip()

    def listener_register(self, callback):
        self.btn_register.config(command=callback)

    def listener_back(self, callback):
        self.btn_back.config(command=callback)
        
    def _on_close(self,callback):
    
        if callable(callback):
            self.protocol("WM_DELETE_WINDOW", callback)

    def show_error(self, message):
        messagebox.showerror("Error", message)