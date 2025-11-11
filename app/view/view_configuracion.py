import tkinter as tk
from tkinter import messagebox

class ViewConfiguracion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuración del Ahorcado")
        self.geometry("400x250")
        self.configure(bg="lightgray")
        # ---- Título ----
        self.label_titulo = tk.Label(
            self,
            text="🎯 Configuración del juego",
            font=("Arial", 18, "bold"),
            bg="lightgray"
        )
        self.label_titulo.pack(pady=20)

        # ---- Botón para usar errores por defecto ----
        self.btn_default = tk.Button(
            self,
            text="Usar número de errores por defecto (9)",
            font=("Arial", 12),
            bg="white",
            relief="raised"
        )
        self.btn_default.pack(pady=10)

        # ---- Zona de configuración personalizada ----
        self.frame_custom = tk.Frame(self, bg="lightgray")
        self.frame_custom.pack(pady=10)

        self.label_custom = tk.Label(
            self.frame_custom,
            text="Número de errores personalizados(<9):",
            font=("Arial", 12),
            bg="lightgray"
        )
        self.label_custom.pack(side="left", padx=5)

        self.entry_errores = tk.Entry(
            self.frame_custom,
            width=5,
            font=("Arial", 12)
        )
        self.entry_errores.pack(side="left")

        # ---- Botón confirmar ----
        self.btn_confirmar = tk.Button(
            self,
            text="Jugar",
            font=("Arial", 12),
            bg="white",
            relief="raised"
        )
        self.btn_confirmar.pack(pady=15)

    def get_numero_errores(self):
        num_error=0
        if(self.entry_errores.get()==''):
            num_error=''
        else:
            num_error=int(self.entry_errores.get().strip())        
        return num_error

    def _on_close(self,callback):
    
        if callable(callback):
            self.protocol("WM_DELETE_WINDOW", callback)
    
    def listener_errores_default(self, callback):
        """Asocia el botón de errores por defecto al controlador."""
        self.btn_default.config(command=callback)

    def listener_confirmar(self, callback):
        """Asocia el botón confirmar al controlador."""
        self.btn_confirmar.config(command=callback)

    # ---- Métodos de utilidad opcionales ----
    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)
