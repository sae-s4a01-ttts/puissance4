class Joueur:

    __nom = ""

    def __init__(self, nom):
        self.setNom(nom)
    
    def setNom(self, nom:str):
        """ @param nom la nouvelle valeur de self.__nom """
        if self.__isValid(nom) : self.__nom = nom
        else: raise ValueError("Le nom du joueur n'est pas valide")

    def getNom(self) -> str:
        """ @return le nom du joueur """
        return self.__nom
    
    def __isValid(self, nom:str) -> bool:
        return nom != None and nom != ""