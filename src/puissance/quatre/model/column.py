# Importe la classe Cell depuis le module cell.py
from cell import Cell

class Column:
    # Hauteur par défaut d'une colonne
    __HEIGHT:int = 6
    
    # Attributs privés pour stocker les informations
    # de la colonne
    __column:list[Cell]
    __next_cell:int
    __hashcode:str
    
    # Constructeur de la classe Column
    def __init__(self, hashcode = '000'):
        # Si un code de hachage est fourni, génère une
        # nouvelle colonne à partir de ce code
        if hashcode != '000':
            self.generate_new_column_by_hashcode(hashcode)
        # Sinon, génère une colonne vide
        else:
            self.__generate_column()
        
    # Méthode privée pour générer une colonne vide
    def __generate_column(self) -> bool:
        # Initialise la colonne avec des cellules vides
        self.__column = [Cell() for x in range(0, self.__HEIGHT)]
        # Génère le code de hachage pour la colonne
        self.__generate_hashcode()
        # Initialise l'indice de la prochaine cellule
        # disponible
        self.__next_cell = 0
        return True
    
    # Méthode privée pour générer le code de hachage
    # de la colonne
    def __generate_hashcode(self) -> bool:
        # Récupère les valeurs des cellules de la colonne
        tmp_column:list[Cell] = [cell.get_value() for cell in self.__column]
        # Inverse l'ordre des valeurs
        tmp_column.reverse()
        
        # Supprime les valeurs par défaut (-1) de la
        # liste des valeurs
        while -1 in tmp_column:
            tmp_column.remove(-1)
        
        # Calcule le préfixe et le suffixe du code
        # de hachage
        prefix_key:int = self.__colbin_to_coldec(tmp_column) * 10 if len(tmp_column) > 0 else 0
        suffix_key:int = len(tmp_column)
        
        # Concatène le préfixe et le suffixe pour
        # former le code de hachage
        key:str = str(prefix_key + suffix_key).zfill(3)
        self.__hashcode = key
        
        return True
    
    # Méthode pour jouer une cellule dans la colonne
    def play_cell(self, player:int) -> bool:
        # Définit la valeur du joueur dans la prochaine
        # cellule disponible
        self.__column[self.__next_cell].set_value(player)
        # Incrémente l'indice de la prochaine cellule
        # disponible 
        self.__next_cell += 1
        # Génère le nouveau code de hachage après avoir
        # joué une cellule
        self.__generate_hashcode()
        return True
        
    # Méthode pour vérifier si la colonne peut être jouée
    def can_play(self) -> bool:
        # Renvoie True si la colonne n'est pas pleine,
        # False sinon
        return self.__next_cell < self.__HEIGHT
    
    # Méthode pour obtenir les cellules de la colonne
    def get_column(self) -> list[Cell]:
        # Retourne la liste des cellules de la colonne
        return self.__column
    
    # Méthode pour obtenir l'indice de la prochaine
    # cellule disponible dans la colonne
    def get_next_cell(self) -> int:
        # Retourne l'indice de la prochaine cellule
        # disponible
        return self.__next_cell
    
    # Méthode pour obtenir une cellule spécifique
    # de la colonne
    def get_cell(self, index:int) -> Cell:
        # Retourne la cellule à l'indice spécifié
        return self.__column[index]
    
    # Méthode pour obtenir le code de hachage de
    # la colonne
    def get_hashcode(self) -> str:
        # Retourne le code de hachage de la colonne
        return self.__hashcode
    
    # Méthode pour générer une nouvelle colonne à
    # partir d'un code de hachage donné
    def generate_new_column_by_hashcode(self, hashcode:str) -> bool:
        read_hashcode:int = int(hashcode)
        prefix_key:int = read_hashcode // 10
        suffix_key:int = read_hashcode % 10
        
        # Convertit le préfixe en une liste de
        # cellules binaires
        column_prefix_bin:list[Cell] = self.__dec_to_colbin(prefix_key)
        
        # Ajoute des cellules vides au début jusqu'à
        # atteindre la longueur indiquée par le suffixe
        while len(column_prefix_bin) != suffix_key:
            column_prefix_bin.append(Cell(0))
        
        # Ajoute des cellules vides à la fin jusqu'à
        # atteindre la hauteur de la colonne
        while len(column_prefix_bin) != self.__HEIGHT:
            column_prefix_bin.append(Cell())
        
        # Définit la colonne avec les cellules obtenues
        self.__column = column_prefix_bin
        self.__next_cell = suffix_key
        # Génère le code de hachage pour la nouvelle colonne
        self.__generate_hashcode()
    
    # Méthode privée pour convertir une liste de
    # cellules binaires en un nombre décimal
    def __colbin_to_coldec(self, clear_column:list[Cell]) -> int:
        # Convertit la liste de cellules en une chaîne
        # de bits
        bin_key:bin = ''.join(map(str, clear_column))
        # Convertit la chaîne de bits en un nombre décimal
        dec_key:int = int(bin_key, 2)
        return dec_key
    
    # Méthode privée pour convertir un préfixe décimal en
    # une liste de cellules binaires
    def __dec_to_colbin(self, prefix:int) -> list[Cell]:
        # Convertit le préfixe en binaire
        prefix_bin:bin = bin(prefix)
        # Crée une liste de cellules binaires à partir
        # du binaire du préfixe
        column_prefix_bin:list[Cell] = [Cell(int(x)) for x in prefix_bin[2:]]
        # Inverse l'ordre des cellules
        column_prefix_bin.reverse()
        return column_prefix_bin
