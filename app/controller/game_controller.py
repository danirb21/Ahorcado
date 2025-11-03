from app.model.cpu import Cpu
from app.model.user import User
from app.view.view_ahorcado import viewAhorcado
from app.utils.text_utils import quitar_tildes

class GameController:
    def __init__(self,cpu:Cpu,user:User,viewAhorcado:viewAhorcado):
        self.errores=0
        self.cpu=cpu
        self.user=user
        self.view=viewAhorcado
        self.view.setLabelWord(" ".join("_" * len(cpu.word)))
        self.view.listenerSendLetter(self.sendLetter)
    
    
    def sendLetter(self, event=None):
        #print(self.cpu.word)
        bol=False
        indices=[]
        if quitar_tildes(self.view.getInputText())!=self.cpu.word:    
            for i in range(len(self.cpu.word)):
                if self.cpu.word[i]==self.view.getInputText():
                    bol=True
                    indices.append(i)
            #Al saber si la letra esta o no       
            if(bol):
                nueva_palabra=self.reemplazar_caracter(self.view.getLabelWord(),indices,self.view.getInputText())                      
                self.view.setLabelWord(nueva_palabra)
                self.view.clearInputText()
                word_label=self.view.getLabelWord().replace(" ","")
                if word_label==self.cpu.word:
                    self.view.mostrar_ganado()
            else:
                if self.user.errors==9:
                    self.user.errors+=1
                    self.view.clearInputText()
                    self.view.drawAhorcado(self.user.errors)
                    self.view.mostrar_perdido(self.cpu.word)   
                else:
                    self.user.errors+=1
                    self.view.clearInputText()
                    self.view.drawAhorcado(self.user.errors)             
        else:
            self.view.setLabelWord(self.cpu.word)
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
