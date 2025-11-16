from app.model.cpu import Cpu
from app.model.player_local import PlayerLocal
from app.view.view_ahorcado import viewAhorcado
from app.utils.text_utils import quitar_tildes
from app.view.view_configuracion import ViewConfiguracion
from app.view.view_login import LoginView
from app.view.view_mode import ViewMode
import requests
from app.view.view_register import RegisterView
from tkinter import messagebox

API_BASE_URL="http://localhost:5000"
class GameController:
    def __init__(self,cpu:Cpu,player_local:PlayerLocal,view_ahorcado:viewAhorcado, view_configuracion:ViewConfiguracion, view_login: LoginView, view_register: RegisterView, view_mode:ViewMode):
        self.cpu=cpu
        self.player_local=player_local
        self.view=view_ahorcado
        self.view_conf=view_configuracion
        self.login_view=view_login
        self.register_view=view_register
        self.mode_view=view_mode
        self.view.withdraw()
        self.view_conf.withdraw()
        self.register_view.withdraw()
        self.view_conf.withdraw()
        self.view_conf.listener_errores_default(self.on_default_errors_selected)
        self.view_conf.listener_confirmar(self.on_button_play)
        self.view_conf._on_close(self.terminar_programa)
        self.login_view._on_close(self.terminar_programa)
        self.register_view._on_close(self.terminar_programa)
        self.view._on_close(self.terminar_programa)
        self.view.set_label_word(" ".join("_" * len(cpu.word)))
        self.view.listener_send_Letter(self.send_letter)
        self.login_view.listener_login(self.on_button_login)
        self.register_view.listener_register(self.on_button_register)
        self.login_view.listener_register(self.on_button_register_in_login)
    
    
    def on_default_errors_selected(self):
        self.cpu.number_try=10
        self.view_conf.destroy()
        self.view.deiconify()
    
    def on_button_login(self):
        try:
            username=self.login_view.get_username()
            password=self.login_view.get_password()
            #Hacer Filtros Campo Username y password
            json={"username":username,
                "password":password}
            requests.post(API_BASE_URL+"/login",json=json)
            if(requests.status_codes!=401):
                self.login_view.destroy()
                self.view_conf.deiconify()
            else:
                self.login_view.show_dont_exist("El usuario o contraseña no son adecuadas")
        except Exception:
            self.login_view.show_error("Error")           
    
    def on_button_register(self):
        username=self.register_view.get_username()
        passwords=self.register_view.get_passwords()
        #Filtro passwords
        
    def on_button_register_in_login(self):
        self.login_view.withdraw()
        self.register_view.deiconify()
    def on_button_play(self):
        bol=True
        try:
            if self.view_conf.get_numero_errores()<10 and self.view_conf.get_numero_errores()>0:
                self.cpu.number_try=self.view_conf.get_numero_errores()
                    
            else:
                bol=False
                raise ValueError("El numero es menor que 0 o mayor que 10")
        except (ValueError,TypeError):
            try:
                if self.view_conf.get_numero_errores()!='':
                    bol=False
                    messagebox.showerror(
                    "Error de entrada",
                    "Por favor, introduce un número entero válido."
                    )  
                else:
                    self.cpu.number_try=10
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
                self.player_local.errors+=1
                if self.player_local.errors==self.cpu.number_try:
                    self.view.clear_input_text()
                    self.view.draw_ahorcado(self.player_local.errors)
                    self.view.mostrar_perdido(self.cpu.word)   
                else:
                    self.view.clear_input_text()
                    self.view.draw_ahorcado(self.player_local.errors)             
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
        