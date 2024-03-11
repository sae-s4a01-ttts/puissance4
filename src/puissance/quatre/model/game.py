from random import randint

from grid import Grid
from player import Player
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
        level_ia = self.__set_level_ia()
        game_mode = self.__select_game_mode()

        player_order:int = 0

        if game_mode == 1: 
            self.__solo_game(level_ia)
            player_order = randint(0,1)
        else: self.__ia_game(level_ia)

        if game_mode == 1:
            if player_order == 0:
                print("Vous jouez les pions X")
            else:
                print("Vous jouez les pions O")

        while self.__in_game:
            joueur_gagnant = self.__play_mode_solo(player_order) if game_mode == 1 else self.__play_mode_ia(player_order)
            if not joueur_gagnant == None: self.__in_game = False
        
        self.__display_grid()
        print("Victoire de ", self.__players[joueur_gagnant].get_name())
       
    def __select_game_mode(self) -> None:
        game_mode = 1
        game_mode_input = input("Mode de jeu : \n(1) joueur vs ordinateur\n(2) ordinateur vs ordinateur\nVeuillez choisir un mode de jeu : ")
        if game_mode_input.isdigit():
            game_mode = int(game_mode_input)
        if game_mode > 2 or game_mode < 1:
            game_mode = 1
        return game_mode
        

    def __solo_game(self, level_ia) -> None:
        new_player:Player = self.__define_new_player()
        self.__players[0] = new_player
        self.__players[1] = Computer('iA', level_ia)
         
    def __ia_game(self, level_ia) -> None:
        self.__players[0] = Computer('iA_1', level_ia)
        self.__players[1] = Computer('iA_2', level_ia)

    def __set_level_ia(self) -> int:
        level_ia = 5
        level_ia_is_ok = False
        try_input = 1
        while not level_ia_is_ok:
            level_ia_input = input("Choisir le niveau de l'iA (1 à 5) : ")
            if level_ia_input.isdigit():
                level_ia = int(level_ia_input)
            if level_ia > 5 or level_ia < 1 or level_ia_input.isalpha():
                print('N' + 'o' * try_input + "n, veuillez rentrer un nombre entre 1 et 5")
            else:
                level_ia_is_ok = True

            try_input += 1

        print("Niveau de l'ia : " + str(level_ia))
        
        return level_ia 

    def __define_new_player(self) -> Player:
        player_name = ""
        while player_name == "":
            player_name = str(input("Choisir un nom de joueur : "))
            if player_name == "": print("Veuillez rentrer votre nom")
        new_player:Player = Player(player_name)
        return new_player
    
    def __play_mode_solo(self, ordre_jeu) -> int:
        if ordre_jeu == 0:
            if self.__play_joueur() == 0: return 0
            if self.__play_ia(self.__players[1], ordre_jeu) == 1: return 1
        else:
            if self.__play_ia(self.__players[1], ordre_jeu) == 1: return 1
            if self.__play_joueur() == 0: return 0

    def __play_mode_ia(self, ordre_jeu) -> int:
        if ordre_jeu == 0:
            if self.__play_ia(self.__players[0], 1) == 0: return 0
            if self.__play_ia(self.__players[1], 0) == 1: return 1
        else:
            if self.__play_ia(self.__players[1], 0) == 1: return 1
            if self.__play_ia(self.__players[0], 1) == 0: return 0

    def __play_joueur(self) -> int:
        self.__display_grid()

        saisie_joueur = ""
        play_placement = 0
        while play_placement < 1 or play_placement > 7:
            saisie_joueur = input("Placer votre pion : ")
            if saisie_joueur.isdigit():
                play_placement:int = int(saisie_joueur)
            if play_placement < 1 or play_placement > 7:
                print("Veuillez rentrer un nombre entre 1 et 7")
            if not self.__grid.can_play_column(play_placement - 1):
                print("Veuillez rentrer une colonne non pleine")
                play_placement = 0
            
        if self.__grid.play_column(play_placement - 1): return 0

    def __play_ia(self, player:Computer, ordre_jeu) -> int:
        self.__display_grid()

        play_ia = player.play_column(self.__grid, ordre_jeu)
        print(player.get_name() + " a joué en : " + str(play_ia + 1))
        if self.__grid.play_column(play_ia): return 1
    
        
    def __display_grid(self) -> None:
        print(str(self.__grid))
    
if __name__ == "__main__":
    game = Game()
    game.main()