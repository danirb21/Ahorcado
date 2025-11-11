from app.model.cpu import Cpu
from app.model.user import User
from app.view.view_ahorcado import viewAhorcado
from app.utils.text_utils import quitar_tildes
from app.view.view_configuracion import ViewConfiguracion
from tkinter import messagebox

class GameController:
    def __init__(self,cpu:Cpu,user:User,view_ahorcado:viewAhorcado, view_configuracion:ViewConfiguracion):
        self.errores=0
        self.cpu=cpu
        self.user=user
        self.view=view_ahorcado
        self.view_conf=view_configuracion
        self.view_conf.listener_errores_default(self.on_default_errors_selected)
        self.view_conf.listener_confirmar(self.on_button_play)
        self.view_conf._on_close(self.terminar_programa)
        self.view._on_close(self.terminar_programa)
        self.view.withdraw()
        self.view.set_label_word(" ".join("_" * len(cpu.word)))
        self.view.listener_send_Letter(self.send_letter)
    
    
    def on_default_errors_selected(self):
        self.cpu.number_try=9
        self.view_conf.destroy()
        self.view.deiconify()
    
    def on_button_play(self):
        bol=True
        try:
            if self.view_conf.get_numero_errores()<9 and self.view_conf.get_numero_errores()>0:
                self.cpu.number_try=self.view_conf.get_numero_errores()
                    
            else:
                bol=False
                raise ValueError("El numero es menor que 0 o mayor que 9")
        except (ValueError,TypeError):
            try:
                if self.view_conf.get_numero_errores()!='':
                    bol=False
                    messagebox.showerror(
                    "Error de entrada",
                    "Por favor, introduce un número entero válido."
                    )  
                else:
                    self.cpu.number_try=9  
            except ValueError:
                bol=False
                messagebox.showerror(
                    "Error de entrada",
                    "Por favor, introduce un número entero válido."
                )  
        if(bol): 
            self.view_conf.destroy()
            self.view.deiconify()
            
    def send_letter(self, event=None):
        #print(self.cpu.word)
        bol=False
        indices=[]
        if quitar_tildes(self.view.get_input_text())!=self.cpu.word:    
            for i in range(len(self.cpu.word)):
                if self.cpu.word[i]==self.view.get_input_text():
                    bol=True
                    indices.append(i)
            #Al saber si la letra esta o no       
            if(bol):
                nueva_palabra=self.reemplazar_caracter(self.view.get_label_word(),indices,self.view.get_input_text())                      
                self.view.set_label_word(nueva_palabra)
                self.view.clear_input_text()
                word_label=self.view.get_label_word().replace(" ","")
                if word_label==self.cpu.word:
                    self.view.mostrar_ganado()
            else:
                if self.user.errors==self.cpu.number_try:
                    self.user.errors+=1
                    self.view.clear_input_text()
                    self.view.draw_ahorcado(self.user.errors)
                    self.view.mostrar_perdido(self.cpu.word)   
                else:
                    self.user.errors+=1
                    self.view.clear_input_text()
                    self.view.draw_ahorcado(self.user.errors)             
        else:
            self.view.set_label_word(self.cpu.word)
            self.view.mostrar_ganado()
            
    def reemplazar_caracter(self, palabra, indices, letra):
    # Quitar espacios y convertir a lista
        chars = palabra.replace(" ", "")
        chars = list(chars)
    # Reemplazar la letra correcta
        for i in range(0,len(indices)):
             if 0 <= indices[i] < len(chars):
                chars[indices[i]] = letra                       
    # Volver a unir con espacios
        return " ".join(chars)

    def terminar_programa(self):
    # Destruir solo si la ventana sigue viva
       if hasattr(self, 'view'):
            self.view.destroy()
       import sys
       sys.exit()
        