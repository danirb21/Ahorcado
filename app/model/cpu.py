from app.utils.text_utils import quitar_tildes

class Cpu:
    def __init__(self,word,number_try):
        self.word=quitar_tildes(word)
        self.number_try=number_try
    