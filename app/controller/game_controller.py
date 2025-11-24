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
import tkinter as tk
import threading
import requests
import re
from app.view.view_register import RegisterView
from tkinter import messagebox

PASSWORD_REGEX = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$" 
#6 word, at least letter and number

API_BASE_URL="http://localhost:5000"
class GameController:
    def __init__(self,root:tk):
        #self.cpu=Cpu(WordProvider.getRandomWord("app/data/palabras.txt"))
        self.cpu=None
        self.root=root
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
        self.cpu=Cpu(WordProvider.getRandomWord("app/data/palabras.txt"))
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
            username=self.login_view.get_username()
            password=self.login_view.get_password()
            #Hacer Filtros Campo Username y password
            json={"username":username,
                "password":password}
            response=requests.post(API_BASE_URL+"/login",json=json)
            if(response.status_code!=401):
                self.login_view.destroy()
                #self.view_conf.deiconify()
                self.mode_view=ViewMode(self.root)
                self.mode_view._on_close(self.terminar_programa)
                self.mode_view.listener_modo_personalizado(self.on_button_personalizado)
                self.mode_view.listener_modo_competitivo(self.on_button_competitivo)
                self.mode_view.deiconify()
                self.jwt_token=response.json()["access_token"]
            else:
                self.login_view.show_dont_exist("El usuario o contraseña no son adecuadas")
        except Exception:
            self.login_view.show_error("Error")           
    
    def on_button_register(self):
        username=self.register_view.get_username()
        pwd,pwd1=self.register_view.get_passwords()
        
        if(pwd!=pwd1):
            self.register_view.show_passwords_equals("Las contraseñas no coinciden")  
            
        elif not username or not pwd or not pwd1:
            self.register_view.show_error("Todos los campos son obligatorios.")

        # 3. Validación de contraseña usando regex
        elif not self.validar_password(pwd1):
            self.register_view.show_error(
                "Debe tener 6+ caracteres, y debe contener al menos una letra y un digito."
            )
        else:
            try:
                response = requests.post(
                    f"{API_BASE_URL}/register",
                    json={"username": username, "password": pwd1}
                )
                if(response.status_code==409):                
                    self.register_view.show_error("Ya existe un usuario con ese nombre")
                else:
                    self.register_view.show_msg_user()
                    self.register_view.withdraw() 
                    self.login_view.deiconify()
            except Exception:
                self.register_view.show_error("Error al conectar con el servidor.")
        
    def on_back(self):
        self.register_view.withdraw() 
        self.login_view.deiconify()
    
    def on_guest(self):
        self.mode_guest=True
        self.login_view.withdraw()
        self.mode_view=ViewMode(self.root)
        self.mode_view._on_close(self.terminar_programa)
        self.mode_view.listener_modo_personalizado(self.on_button_personalizado)
        self.mode_view.listener_modo_competitivo(self.on_button_competitivo)
        self.mode_view.deiconify()

    def on_button_personalizado(self):
        self.mode_view.withdraw()
        self.view_conf=ViewConfiguracion(self.root)
        self.view_conf.listener_errores_default(self.on_default_errors_selected)
        self.view_conf.listener_confirmar(self.on_button_play)
        self.view_conf._on_close(self.terminar_programa)
        self.view_conf.deiconify()
        
    def on_button_competitivo(self):
        if(not self.mode_guest):
            self.is_compe=True
            self.view=viewAhorcado(self.root)
            self.cpu=Cpu(WordProvider.getRandomWord("app/data/palabras.txt"))
            self.cpu.number_try=10
            self.view.listener_send_Letter(self.send_letter)
            self.view._on_close(self.terminar_programa)
            self.view.set_label_word(" ".join("_" * len(self.cpu.word)))
            self.mode_view.withdraw()
            self.view.deiconify()
        else:
            self.mode_view.show_guest()
        
    def on_button_register_in_login(self):
        self.login_view.withdraw()
        self.register_view=RegisterView(self.root)
        self.register_view._on_close(self.terminar_programa)
        self.register_view.listener_register(self.on_button_register)
        self.register_view.listener_back(self.on_back)
        self.register_view.deiconify()
    def on_button_play(self):
        self.cpu=Cpu(WordProvider.getRandomWord("app/data/palabras.txt"))
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
            self.view_conf.withdraw()
            self.view=viewAhorcado(self.root)
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

        self.view.withdraw()

        # ---- MODO COMPETITIVO ----
        if self.is_compe:

            self.headers = {
                "Authorization": f"Bearer {self.jwt_token}",
                "Content-Type": "application/json"
            }

            
            self.view_resultados = CompetitiveResultView(parent=self.root)
            self.view_resultados.set_correct_word(game.word)
            self.view_resultados.set_result(game.won)
            self.view_resultados.listener_menu(self.on_btn_menu)
            self.view_resultados.listener_leaderboard(self.on_btn_leaderboards)
            self.view_resultados._on_close(self.terminar_programa)

            user = game.player
            user.score = game.get_game_score()
            
            loading = LoadingWidget(self.view_resultados,"Mostrando Resultados...")
            loading.animar()
            # ---- HILO PARA LA PETICIÓN A LA API ----
            def tarea_update_score():
                try:
                    response = requests.post(
                        API_BASE_URL + "/updatescore",
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
        self.view_resultados.withdraw()
        self.mode_view.deiconify()
    
    def on_btn_leaderboards(self):
        #print(self.view_resultados.grab_status())
        self.view_resultados.grab_release()
        self.leaderboard_view=LeaderboardView(self.root)
        #print(response.text)  
        self.leaderboard_view.listener_back(self.on_back_leaderboard)
        self.leaderboard_view._on_close(self.terminar_programa)
        self.view_resultados.withdraw()
        self.leaderboard_view.deiconify()
        
        loading=LoadingWidget(self.leaderboard_view,"Cargando")
        loading.animar()            
        def task_leaderboard():
            response=requests.get(API_BASE_URL+"/leaderboard",headers=self.headers)
            leaderboard=response.json()   
            def update_ui_leaderboard():
                loading.destroy_widget()
                self.leaderboard_view.update_table(leaderboard)      
                
            self.root.after(0,update_ui_leaderboard)  
              
        threading.Thread(target=task_leaderboard, daemon=True).start()
        
    
    def on_back_leaderboard(self):
        self.leaderboard_view.destroy()
        self.view_resultados.deiconify()
    def terminar_programa(self):
    # Destruir solo si la ventana sigue viva
       import sys
       sys.exit()
        