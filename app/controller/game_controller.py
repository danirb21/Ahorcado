from app.model.cpu import Cpu
from app.model.game import Game
from app.model.player_local import PlayerLocal
from app.view.view_ahorcado import viewAhorcado
from app.utils.text_utils import quitar_tildes
from app.view.view_configuracion import ViewConfiguracion
from app.view.view_login import LoginView
from app.view.view_mode import ViewMode
from app.view.view_leaderboard import LeaderboardView
from app.model.word_provider import WordProvider
from app.view.view_competitive_result import CompetitiveResultView
from app.view.loading_widget import LoadingWidget
from app.utils.config import load_environment_variables
from app.utils.config import get_resource_path
import tkinter as tk
import threading
import requests
import traceback
import logging
import re
import os
from app.view.view_register import RegisterView
from tkinter import messagebox
from app.utils.ui_utils import WindowPosition


PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$" 
load_environment_variables()
class GameController:
    def __init__(self,root:tk):
        #self.cpu=Cpu(WordProvider.getRandomWord("app/data/palabras.txt"))
        self.cpu=None
        self.root=root
        self.username=None
        self.mode_guest=False
        self.headers=None
        self.player_local=PlayerLocal()
        self.game=None
        self.jwt_token=None
        self.is_compe=False
        self.mode=""
        self.view=None
        #self.view.withdraw()
        #self.view_conf.withdraw()
        #self.register_view.withdraw()
        #self.view_conf.withdraw()
        #self.mode_view.withdraw()
        self.login_view=LoginView(root)
        self.login_view._on_close(self.terminar_programa)
        self.login_view.listener_login(self.on_button_login)
        self.login_view.listener_register(self.on_button_register_in_login)
        self.login_view.listener_guest(self.on_guest)
        self.login_view.mainloop()
    
    
    def on_default_errors_selected(self):
        self.view=viewAhorcado(self.root)
        self.cpu=Cpu(WordProvider.getRandomWord(get_resource_path("app/data/palabras.txt")))
        self.cpu.number_try=10
        self.view._on_close(self.terminar_programa)
        self.view.set_label_word(" ".join("_" * len(self.cpu.word)))
        self.view.listener_send_Letter(self.send_letter) 
        self.view_conf.withdraw()
        self.view.deiconify()
    
    def validar_password(self, pwd):
        return re.match(PASSWORD_REGEX, pwd) is not None
    
    def on_button_login(self):
        try:
            username = self.login_view.get_username()
            password = self.login_view.get_password()

            # Filtro de campos vacíos
            if not username or not password:
                self.login_view.show_error("Debe rellenar todos los campos.")
                return

            response = requests.post(
                os.getenv("API_BASE_URL") + "/login",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                # Login correcto → abrir ventana de modos
                self.jwt_token = response.json()["access_token"]
                self.username=username
                WindowPosition.store(self.login_view)
                self.login_view.destroy()
                self.mode_view = ViewMode(self.root)
                WindowPosition.apply(self.mode_view)
                self.mode_view._on_close(self.terminar_programa)
                self.mode_view.listener_modo_personalizado(self.on_button_personalizado)
                self.mode_view.listener_modo_competitivo(self.on_button_competitivo)
                self.mode_view.listener_back(self.on_back_mode)
                self.mode_view.deiconify()

            elif response.status_code == 401:
                self.login_view.show_dont_exist("El usuario o la contraseña no son correctas")

            elif response.status_code == 400:
                # Faltan campos
                self.login_view.show_error("Deber rellenar todos los campos")

            else:
                self.login_view.show_error("Error inesperado al iniciar sesión.")

        except Exception:
            logging.error(traceback.format_exc())
            self.login_view.show_error("Error al conectar con el servidor.")

    
    def on_button_register(self):
        username = self.register_view.get_username()
        pwd, pwd1 = self.register_view.get_passwords()

        # Contraseñas iguales
        if pwd != pwd1:
            self.register_view.show_passwords_equals("Las contraseñas no coinciden")
            return

        # Campos vacíos
        if not username or not pwd or not pwd1:
            self.register_view.show_error("Todos los campos son obligatorios.")
            return

        # Validación local
        if not self.validar_password(pwd1):
            self.register_view.show_error(
                "Debe tener 6+ caracteres, y debe contener al menos una letra y un dígito."
            )
            return

        try:
            response = requests.post(
                f"{os.getenv('API_BASE_URL')}/register",
                json={"username": username, "password": pwd1}
            )

            if response.status_code == 201:
                # Registro OK
                self.register_view.show_msg_user()
                WindowPosition.store(self.register_view)
                self.register_view.withdraw()
                WindowPosition.apply(self.login_view)
                self.login_view.deiconify()
            
            elif response.status_code == 409:
                self.register_view.show_error("Ya existe un usuario con ese nombre")

            elif response.status_code == 400:
                # Contraseña débil o faltan campos
                error = response.json().get("error", "Datos inválidos")
                self.register_view.show_error(error)

            else:
                self.register_view.show_error("Error inesperado en el registro.")

        except Exception:
            logging.error(traceback.format_exc())
            self.register_view.show_error("No se pudo conectar con el servidor.")


        
    def on_back_register(self):
        WindowPosition.store(self.register_view)
        self.register_view.withdraw() 
        WindowPosition.apply(self.login_view)
        self.login_view.deiconify()
        
    def on_back_conf(self):
        self.view_conf.withdraw()
        self.view_conf.grab_release()
        self.mode_view.deiconify()
    
    def on_back_mode(self):
        WindowPosition.store(self.mode_view)
        self.mode_view.withdraw()
        self.login_view=LoginView(self.root)           
        self.login_view._on_close(self.terminar_programa)
        self.login_view.listener_login(self.on_button_login)
        self.login_view.listener_register(self.on_button_register_in_login)
        self.login_view.listener_guest(self.on_guest)
        WindowPosition.apply(self.login_view)
        self.login_view.deiconify()
    def on_guest(self):
        self.mode_guest=True
        WindowPosition.store(self.login_view)
        self.login_view.withdraw()
        self.mode_view=ViewMode(self.root)
        self.mode_view._on_close(self.terminar_programa)
        self.mode_view.listener_modo_personalizado(self.on_button_personalizado)
        self.mode_view.listener_modo_competitivo(self.on_button_competitivo)
        self.mode_view.listener_back(self.on_back_mode)
        WindowPosition.apply(self.mode_view)
        self.mode_view.deiconify()

    def on_button_personalizado(self):
        WindowPosition.store(self.mode_view)
        self.mode_view.withdraw()
        self.view_conf=ViewConfiguracion(self.root)
        WindowPosition.apply(self.view_conf)
        self.view_conf.listener_errores_default(self.on_default_errors_selected)
        self.view_conf.listener_back(self.on_back_conf)
        self.view_conf.listener_confirmar(self.on_button_play)
        self.view_conf._on_close(self.terminar_programa)
        self.view_conf.deiconify()
        
    def on_button_competitivo(self):
        if(not self.mode_guest):
            self.is_compe=True
            self.view=viewAhorcado(self.root)
            self.cpu=Cpu(WordProvider.getRandomWord(get_resource_path("app/data/palabras.txt")))
            self.cpu.number_try=10
            self.view.listener_send_Letter(self.send_letter)
            self.view._on_close(self.terminar_programa)
            self.view.set_label_word(" ".join("_" * len(self.cpu.word)))
            WindowPosition.store(self.mode_view)
            self.mode_view.withdraw()
            WindowPosition.apply(self.view)
            self.view.deiconify()
        else:
            self.mode_view.show_guest()
        
    def on_button_register_in_login(self):
        WindowPosition.store(self.login_view)
        self.login_view.withdraw()
        self.register_view=RegisterView(self.root)
        self.register_view._on_close(self.terminar_programa)
        self.register_view.listener_register(self.on_button_register)
        self.register_view.listener_back(self.on_back_register)
        WindowPosition.apply(self.register_view)
        self.register_view.deiconify()
    def on_button_play(self):
        self.cpu=Cpu(WordProvider.getRandomWord(get_resource_path("app/data/palabras.txt")))
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
            self.is_compe=False
            WindowPosition.store(self.view_conf)
            self.view_conf.withdraw()
            self.view=viewAhorcado(self.root)
            WindowPosition.apply(self.view)
            self.view._on_close(self.terminar_programa)
            self.view.set_label_word(" ".join("_" * len(self.cpu.word)))
            self.view.listener_send_Letter(self.send_letter)
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
                    #self.view.mostrar_ganado()
                    self.player_local.errors=0
                    self.game=Game(self.player_local,self.cpu.word,True)
                    self.mostrar_resultado(self.game)
            else:
                self.player_local.errors+=1
                if self.player_local.errors==self.cpu.number_try:
                    self.view.clear_input_text()
                    self.view.draw_ahorcado(self.player_local.errors)
                    #self.view.mostrar_perdido(self.cpu.word) 
                    self.player_local.errors=0
                    self.game=Game(self.player_local,self.cpu.word,False)
                    self.mostrar_resultado(self.game)
                else:
                    self.view.clear_input_text()
                    self.view.draw_ahorcado(self.player_local.errors)         
        else:
            self.view.set_label_word(self.cpu.word)
            #self.view.mostrar_ganado()
            self.player_local.errors=0
            self.game=Game(self.player_local,self.cpu.word,True)
            self.mostrar_resultado(self.game)
            
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

  

    def mostrar_resultado(self, game: Game):
        palabra = self.cpu.word
        WindowPosition.store(self.view)
        self.view.withdraw()

        # ---- MODO COMPETITIVO ----
        if self.is_compe:

            self.headers = {
                "Authorization": f"Bearer {self.jwt_token}",
                "Content-Type": "application/json"
            }

            
            self.view_resultados = CompetitiveResultView(parent=self.root)
            WindowPosition.apply(self.view_resultados)
            self.view_resultados.set_correct_word(game.word)
            self.view_resultados.set_result(game.won)
            self.view_resultados.listener_menu(self.on_btn_menu)
            self.view_resultados.listener_leaderboard(self.on_btn_leaderboards)
            self.view_resultados._on_close(self.terminar_programa)
            self.view_resultados.listener_retry(self.on_btn_retry)

            user = game.player
            user.score = game.get_game_score()
            
            loading = LoadingWidget(self.view_resultados,"Mostrando Resultados...")
            loading.animar()
            # ---- HILO PARA LA PETICIÓN A LA API ----
            def tarea_update_score():
                try:
                    response = requests.post(
                        os.getenv("API_BASE_URL") + "/updatescore",
                        headers=self.headers,
                        json={"score": user.score}
                    )

                    data = response.json()
                    total_score = data["total_score"]

                except Exception as e:
                    total_score = None  
                    print(f"Error actualizando score: {e}")

                # Actualizar UI desde el hilo principal
                def actualizar_ui():
                    loading.destroy_widget()
                    if total_score is not None:
                        self.view_resultados.set_points(user.score, total_score)
                    else:
                        self.view_resultados.set_points(user.score, "Error")

                self.root.after(0,actualizar_ui)

            # Lanzar hilo
            threading.Thread(target=tarea_update_score, daemon=True).start()

    # ---- MODO PERSONALIZADO ----
        else:
            if game.won:
                self.view.mostrar_ganado()
            else:
                self.view.mostrar_perdido(palabra)

            self.mode_view.deiconify()

           
    def on_btn_menu(self):
        WindowPosition.store(self.view_resultados)
        self.view_resultados.withdraw()
        self.view_resultados.grab_release()
        WindowPosition.apply(self.mode_view)
        self.mode_view.deiconify()
        
    def on_btn_retry(self):
        self.is_compe=True
        self.cpu=Cpu(WordProvider.getRandomWord(get_resource_path("app/data/palabras.txt")))
        self.cpu.number_try=10
        self.view.set_label_word(" ".join("_" * len(self.cpu.word)))
        self.view.clear_ahorcado()   
        WindowPosition.store(self.view_resultados) 
        self.view_resultados.withdraw()
        self.view_resultados.grab_release()
        WindowPosition.apply(self.view)
        self.view.deiconify()    
    
    def on_btn_leaderboards(self):
        #print(self.view_resultados.grab_status())
        self.view_resultados.grab_release()
        self.leaderboard_view=LeaderboardView(self.root)
        #print(response.text)  
        self.leaderboard_view.listener_back(self.on_back_leaderboard)
        self.leaderboard_view._on_close(self.terminar_programa)
        WindowPosition.store(self.view_resultados)
        self.view_resultados.withdraw()
        WindowPosition.apply(self.leaderboard_view)
        self.leaderboard_view.deiconify()
        
        loading=LoadingWidget(self.leaderboard_view,"Cargando")
        loading.animar()            
        def task_leaderboard():
            response=requests.get(os.getenv("API_BASE_URL")+"/leaderboard",headers=self.headers)
            leaderboard=response.json()   
            def update_ui_leaderboard():
                loading.destroy_widget()
                self.leaderboard_view.update_table(leaderboard,self.username)      
                
            self.root.after(0,update_ui_leaderboard)  
              
        threading.Thread(target=task_leaderboard, daemon=True).start()
        
    
    def on_back_leaderboard(self):
        WindowPosition.store(self.leaderboard_view)
        self.leaderboard_view.destroy()
        WindowPosition.apply(self.view_resultados)
        self.view_resultados.deiconify()
    def terminar_programa(self):
    # Destruir solo si la ventana sigue viva
       import sys
       sys.exit()
        