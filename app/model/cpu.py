from app.utils.text_utils import quitar_tildes

class Cpu:
    number_try=0
    def __init__(self,word):
        self.word=quitar_tildes(word).lower()
    