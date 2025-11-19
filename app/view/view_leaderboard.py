import tkinter as tk
from tkinter import ttk


class LeaderboardView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("🏆 Leaderboard - Ahorcado")
        self.geometry("400x400")
        self.configure(bg="lightgray")
        self.resizable(False, False)

        self.label_title = tk.Label(
            self,
            text="Clasificación Global",
            font=("Arial", 18, "bold"),
            bg="lightgray"
        )
        self.label_title.pack(pady=15)

        # --- Frame tabla ---
        frame_table = tk.Frame(self, bg="lightgray")
        frame_table.pack(pady=10, fill="both", expand=True)

        # --- Scrollbar ---
        scrollbar = tk.Scrollbar(frame_table)
        scrollbar.pack(side="right", fill="y")

        # --- Treeview Tabla ---
        self.table = ttk.Treeview(
            frame_table,
            columns=("username", "score"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=12
        )

        self.table.heading("username", text="Usuario")
        self.table.heading("score", text="Puntos")

        self.table.column("username", width=180, anchor="center")
        self.table.column("score", width=80, anchor="center")

        self.table.pack(fill="both", expand=True)
        scrollbar.config(command=self.table.yview)

        # --- Botón Volver ---
        self.btn_back = tk.Button(
            self,
            text="Volver al Menu",
            font=("Arial", 12),
            bg="white"
        )
        self.btn_back.pack(pady=10)

    # ---------------- Métodos MVC ---------------- #

    def update_table(self, data_list):
        """
        Rellena el leaderboard con una lista de diccionarios:
        [
          {"username": "Juan", "score": 120},
          {"username": "Ana", "score": 95},
          ...
        ]
        """
        # Limpiar tabla
        for row in self.table.get_children():
            self.table.delete(row)

        # Insertar datos
        for item in data_list:
            if(item["score"]!=None):
                self.table.insert(
                "", tk.END,
                values=(item["username"],item["score"])
            )

    def listener_back(self, callback):
        """Asocia el botón volver al controlador."""
        self.btn_back.config(command=callback)

    def _on_close(self, callback):
        """Cierra la vista y pasa control al callback."""
        if callable(callback):
            self.protocol("WM_DELETE_WINDOW", callback)
