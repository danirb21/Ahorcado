import tkinter as tk
from tkinter import ttk

class CompetitiveResultView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Resultados competitivos")
        self.configure(bg="#d0d0d0")  # gris suave

        self.geometry("420x350")
        self.resizable(False, False)
        self.grab_set()

        # ----- TITULO DE RESULTADO -----
        self.result_label = tk.Label(
            self,
            font=("Arial", 22, "bold"),
            bg="#d0d0d0"
        )
        self.result_label.pack(pady=20)

        # ----- PALABRA CORRECTA -----
        self.word_label = tk.Label(
            self,
            font=("Arial", 14, "bold"),
            bg="#d0d0d0"
        )
        self.word_label.pack(pady=5)

        # ----- PUNTOS -----
        self.points_label = tk.Label(
            self,
            font=("Arial", 14),
            bg="#d0d0d0"
        )
        self.points_label.pack(pady=5)

        self.total_label = tk.Label(
            self,
            font=("Arial", 14),
            bg="#d0d0d0"
        )
        self.total_label.pack(pady=5)

        # ----- BOTONES -----
        button_frame = tk.Frame(self, bg="#d0d0d0")
        button_frame.pack(pady=30)

        self.btn_leaderboard = ttk.Button(button_frame, text="📊 Ver Leaderboard")
        self.btn_leaderboard.grid(row=0, column=0, padx=10)

        self.btn_retry = ttk.Button(button_frame, text="🔁 Jugar de nuevo")
        self.btn_retry.grid(row=0, column=1, padx=10)

        self.btn_menu = ttk.Button(button_frame, text="🏠 Menú")
        self.btn_menu.grid(row=0, column=2, padx=10)

    # ----- MÉTODOS PÚBLICOS PARA ACTUALIZAR DATOS -----
    def set_result(self, won: bool):
        """Configura el resultado de la partida (ganó/perdió)."""
        self.result_label.config(
            text="🎉 ¡HAS GANADO!" if won else "❌ HAS PERDIDO",
            fg="#008800" if won else "#cc0000"
        )

    def set_correct_word(self, word: str):
        """Muestra la palabra correcta."""
        self.word_label.config(text=f"La palabra era: {word.upper()}")

    def set_points(self, points_obtained: int, total_points: int):
        """Actualiza los puntos obtenidos y totales."""
        self.points_label.config(text=f"Puntos obtenidos: {points_obtained}")
        self.total_label.config(text=f"Puntos totales: {total_points}")
        
    def listener_menu(self, callback):
        self.btn_menu.config(command=callback)

    def listener_leaderboard(self, callback):
        self.btn_leaderboard.config(command=callback)
    def listener_retry(self, callback):
        self.btn_retry.config(command=callback) 