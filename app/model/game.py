from app.model.player_local import PlayerLocal
class Game:
    def __init__(self,player:PlayerLocal,word:str,won:bool):
        self.player=player
        self.word=word
        self.won=won
    def get_game_score(self):
        score = (len(self.word) * 10) + ((9 - self.player.errors) * 5) #Formula Temporal
        return score
    