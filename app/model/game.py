from user import User
class Game:
    def __init__(self,user:User,word:str,won:bool):
        self.user=user
        self.word=word
        self.won=won
    def get_game_score(self):
        score = (len(self.word) * 10) + ((9 - self.user.errors) * 5) #Formula Temporal
        return score
    