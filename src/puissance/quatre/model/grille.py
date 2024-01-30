from src.puissance.quatre.model.cellule import Cellule

class Grille:

    __longueur:int
    __hauteur:int
    __taille:int
    __grille:list[Cellule]

    def __init__(self, longueur:int = 7, hauteur:int = 6) -> None:
        self.setLongueur(longueur)
        self.setHauteur(hauteur)
        self.__genererGrille()

    def setLongueur(self, longueur:int) -> None:
        if self.__longueurIsValid(longueur): self.__longueur = longueur
        else: raise ValueError("La longueur saisie n'est pas valide")
    
    def setHauteur(self, hauteur:int) -> None:
        if self.__hauteurIsValid(hauteur): self.__hauteur = hauteur
        else: raise ValueError("La hauteur saisie n'est pas valide")

    def __setTaille(self) -> bool:
        if self.__grilleIsValid(): self.__taille = self.getLongueur() * self.getHauteur()
        else: raise ValueError("Impossible de calculer la taille de la grille")
        return True

    def __genererGrille(self) -> bool:
        if self.__grilleIsValid() and self.__setTaille():
            nombre_cellule = self.getTaille()
            self.__grille = [Cellule for x in range(0, nombre_cellule)]
            if len(self.getGrille()) == nombre_cellule: return True
        raise ValueError("Impossible de générer la grille de jeu")

    def getLongueur(self) -> int:
        return self.__longueur
    
    def getHauteur(self) -> int:
        return self.__hauteur
    
    def getTaille(self) -> int:
        return self.__taille
    
    def getGrille(self) -> list[Cellule]:
        return self.__grille

    def __longueurIsValid(self, longueur:int) -> bool:
        return longueur % 7 == 0 and longueur > 0 and longueur < 29
    
    def __hauteurIsValid(self, hauteur:int) -> bool:
        return hauteur % 6 == 0 and hauteur > 0 and hauteur < 25
    
    def __grilleIsValid(self) -> bool:
        return self.getLongueur() != None and self.getLongueur() != None
    
    def __str__(self) -> str:
        return ""