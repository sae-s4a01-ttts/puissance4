class Joueur:

    self.__nom = ""

    def __init__(self, nom):
        self.__nom = nom
    
    def setNom(self, nom:str):
        self.__nom = nom

    def getNom(self) -> str:
        return self.__nom