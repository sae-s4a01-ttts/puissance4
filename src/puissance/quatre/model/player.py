class Player:
    # Attribut privé pour stocker le nom du joueur
    __name:str

    # Constructeur de la classe Player
    def __init__(self, name:str) -> None:
        # Initialise le nom du joueur en utilisant
        # la méthode set_name()
        self.set_name(name)

    # Méthode pour définir le nom du joueur
    def set_name(self, name:str) -> None:
        # Vérifie si le nom est valide en appelant
        # la méthode privée __is_valid()
        if self.__is_valid(name) :
            # Affecte le nom au joueur
            self.__name = name
        else:
            # Lève une exception si le nom n'est
            # pas valide
            raise ValueError("")

    # Méthode pour obtenir le nom du joueur
    def get_name(self) -> str:
        # Retourne le nom du joueur
        return self.__name

    # Méthode privée pour vérifier si un nom est valide
    def __is_valid(self, name:str) -> bool:
        # Renvoie True si le nom n'est pas vide ni None,
        # False sinon
        return name != None and name != ""
