import random
class WordProvider:
    
    @staticmethod
    def getRandomWord(fich):

        with open(fich, "r", encoding="utf-8") as f:
            num_lineas = sum(1 for _ in f)

        indice = random.randrange(num_lineas)

        with open(fich, "r", encoding="utf-8") as f:
            for i, linea in enumerate(f):
                if i == indice:
                    palabra = linea.strip()
                    break
        return palabra
                    