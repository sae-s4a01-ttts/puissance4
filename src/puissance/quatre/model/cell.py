class Cell:
    # Valeur par défaut pour une cellule non attribuée
    __DEFAULT_VALUE:int = -1
    
    # Attribut privé pour stocker la valeur de la cellule
    __value:int

    # Constructeur de la classe Cell
    def __init__(self, value = __DEFAULT_VALUE) -> None: 
        # Initialise la valeur de la cellule
        self.__value = value

    # Méthode pour définir la valeur de la cellule
    def set_value(self, value:int):
        # Vérifie si la valeur est valide (0 ou 1)
        if value == 0 or value == 1 :
            # Affecte la valeur à la cellule
            self.__value = value
        else:
            # Lève une exception si la valeur n'est 
            # pas valide
            raise ValueError("Cell")  

    # Méthode pour obtenir la valeur de la cellule
    def get_value(self) -> int:
        # Retourne la valeur de la cellule
        return self.__value

    # Méthode pour vérifier si la cellule est libre 
    # (non attribuée)
    def is_free(self) -> bool:
        # Retourne True si la cellule est libre,
        # False sinon
        return self.__value == self.__DEFAULT_VALUE  

    # Méthode privée pour convertir la valeur de la cellule 
    # en chaîne de caractères
    def __to_string(self) -> str:
        # Renvoie "X" pour joueur X, "O" pour joueur O,
        # et " " pour une cellule libre
        return "X" if self.__value == 0 else "O" if self.__value == 1 else " "  

    # Méthode spéciale pour représenter la cellule sous
    # forme de chaîne de caractères
    def __str__(self) -> str:
        # Renvoie la représentation de la cellule en
        # tant que chaîne de caractères
        return self.__to_string()
