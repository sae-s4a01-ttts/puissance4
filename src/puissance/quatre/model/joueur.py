class Joueur:

    self.__nom = ""

    def __init__(self, nom):
        self.setNom(nom)
    
    def setNom(self, nom:str):
        """ @param nom la nouvelle valeur de self.__nom """
        self.__nom = nom

    def getNom(self) -> str:
        """ @return le nom du joueur """
        return self.__nom