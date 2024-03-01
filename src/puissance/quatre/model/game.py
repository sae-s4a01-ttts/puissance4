from grid import Grid
from player import Player
from random import randint
import computer

class Game:
    
    __in_game:bool
    __grid:Grid
    __players:dict = {"1": None, "2": None}
    
    def __init__(self) -> None:
        self.__in_game = True
        self.__grid = Grid()
        pass
    
    def main(self) -> None:
        self.__solo_game()
        while self.__in_game:
            self.__display_grid()
            if not self.__play() == None: self.__in_game = False
        self.__display_grid()
        print("partie finie")
       
    def __solo_game(self) -> None:
        player_order:str = self.__define_player_order()
        new_player:Player = self.__define_new_player()
        self.__players[player_order] = new_player

        if player_order == "1": self.__players["2"] = Player("IA")
        else: self.__players["1"] = Player("IA")
        
    def __define_player_order(self) -> str:
        player_order:str = str(input("Vous voulez être le joueur 1 ou 2 ? : "))
        return player_order
         
    def __define_new_player(self) -> Player:
        player_name:str = str(input("Choisir un nom de joueur : "))
        new_player:Player = Player(player_name)
        return new_player
    
    def __play(self) -> int:
        play_placement:int = int(input("Placer votre pion : "))
        if self.__grid.play_column(play_placement - 1): return 0
        
        # Placement aléatoire de l'ordinateur
        if self.__grid.play_column(computer.choix_colonne(self.__grid)): return 1
        
    def __display_grid(self) -> None:
        print(str(self.__grid))
    
if __name__ == "__main__":
    game = Game()
    game.main()