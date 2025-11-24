from app.model.player_local import PlayerLocal
class Game:
    def __init__(self,player:PlayerLocal,word:str,won:bool):
        self.player=player
        self.word=word
        self.won=won
    def get_game_score(self):
        scorematch = 50 if self.won else -30
        score = (len(self.word) * 10) - (self.player.errors * 5) + scorematch
        return score

    