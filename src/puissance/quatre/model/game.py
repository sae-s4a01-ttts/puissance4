from grid import Grid
from player import Player

class Game:
    
    def __init__(self) -> None:
        pass
    
    def define_player(self) -> Player:
        player_name:str = str(input("Choisir un nom de joueur : "))
        new_player = Player(player_name)
        return
    
    def play(self) -> bool:
        pass