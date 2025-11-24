import tkinter as tk

class LoadingWidget(tk.Frame):
    def __init__(self, parent, text):
        super().__init__(parent, bg="#5A5858")  # semitransparente
        self.text=text
        # overlay a pantalla completa
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        # cuadro centrado
        self.box = tk.Frame(self, bg="white", padx=20, pady=10)
        self.box.place(relx=0.5, rely=0.5, anchor="center")

        self.label = tk.Label(self.box, text="Cargando", font=("Arial", 14), bg="white")
        self.label.pack()

        self.anim_index = 0
        self._animando = True
        self.animar()

    def animar(self):
        if not self._animando:
            return

        puntos = "." * (self.anim_index % 4)
        self.label.config(text=self.text+puntos)
        self.anim_index += 1
        self.after(400, self.animar)

    def destroy_widget(self):
        self._animando = False
        self.grab_release()
        self.destroy()
