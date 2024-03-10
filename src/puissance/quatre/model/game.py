from grid import Grid
from player import Player
from random import randint
from computer import Computer

class Game:
    
    __in_game:bool
    __grid:Grid
    __players = [None, None]
    
    def __init__(self) -> None:
        self.__in_game = True
        self.__grid = Grid()
        pass
    
    def main(self) -> None:
        self.__solo_game()
        player_order:int = randint(0,1)
        if player_order == 0:
            print("Vous jouez les pions X")
        else:
            print("Vous jouez les pions O")
        while self.__in_game:
            joueur_gagnant = self.__play(player_order)
            if not joueur_gagnant == None: self.__in_game = False
        self.__display_grid()
        print("Victoire de ", self.__players[joueur_gagnant].get_name())
       
    def __solo_game(self) -> None:
        new_player:Player = self.__define_new_player()
        self.__players[0] = new_player
        lvl_ia = 0
        while lvl_ia <= 0:
            saisie_joueur = input("Choisissez le niveau de l'IA : ")
            if saisie_joueur.isdigit():
                lvl_ia:int = int(saisie_joueur) 
            if lvl_ia <= 0:
                print('Veuillez choisir un niveau supérieur à 0')
        self.__players[1] = Computer(lvl_ia)
         
    def __define_new_player(self) -> Player:
        player_name = ""
        while player_name == "":
            player_name = str(input("Choisir un nom de joueur : "))
            if player_name == "": print("Veuillez rentrer votre pseudo")
        new_player:Player = Player(player_name)
        return new_player
    
    def __play(self, ordre_jeu) -> int:
        if ordre_jeu == 0:
            if self.__play_joueur() == 0: return 0
            if self.__play_ia(ordre_jeu) == 1: return 1
        else:
            if self.__play_ia(ordre_jeu) == 1: return 1
            if self.__play_joueur() == 0: return 0

    def __play_joueur(self) -> int:
        self.__display_grid() 
        # Gestion saisie joueur
        saisie_joueur = ""
        play_placement = 0
        while play_placement < 1 or play_placement > 7:
            saisie_joueur = input("Placer votre pion : ")
            if saisie_joueur.isdigit():
                play_placement:int = int(saisie_joueur)
            if play_placement < 1 or play_placement > 7:
                print("Veuillez rentrer un nombre entre 1 et 7")
            
        if self.__grid.play_column(play_placement - 1): return 0

    def __play_ia(self, ordre_jeu) -> int:
        # Placement aléatoire de l'ordinateur
        if self.__grid.play_column(self.__players[1].choix_colonne(self.__grid, ordre_jeu)): return 1
    
        
    def __display_grid(self) -> None:
        print(str(self.__grid))
    
if __name__ == "__main__":
    game = Game()
    game.main()