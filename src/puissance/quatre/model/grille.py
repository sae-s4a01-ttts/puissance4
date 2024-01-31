from cellule import Cellule

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
            self.__grille = [Cellule() for x in range(0, nombre_cellule)]
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
    
    def getCellule(self, index:int) -> Cellule:
        return self.getGrille()[index]
    
    def actionJoueur(self, numero_colone:int, id_joueur:int) -> None:
        if not numero_colone > 0 and not numero_colone < self.getLongueur() + 1: raise ValueError("Impossible de jouer ici")
        else:
            jeton_place:bool = False
            numero_cellule:int = 0
            etage:int = 0
            numero_colone -= 1
            while(not jeton_place):
                numero_cellule = numero_colone + etage
                if self.__joueurPeutJouer(numero_cellule): jeton_place = self.getCellule(numero_cellule).estLibre()
                else: raise ValueError("Impossible de jouer cette cellule")
                etage += self.getLongueur()

            if jeton_place: self.getCellule(numero_cellule).setValeur(id_joueur)
    
    def __joueurPeutJouer(self, numero_cellule:int) -> bool:
        return numero_cellule >= 0 and numero_cellule < self.getTaille()

    def __longueurIsValid(self, longueur:int) -> bool:
        return longueur % 7 == 0 and longueur > 0 and longueur < 29
    
    def __hauteurIsValid(self, hauteur:int) -> bool:
        return hauteur % 6 == 0 and hauteur > 0 and hauteur < 25
    
    def __grilleIsValid(self) -> bool:
        return self.getLongueur() != None and self.getLongueur() != None
    
    def __str__(self) -> str:
        resultat:str = ""
        ligne:str = "|  "

        for i in range(0, self.getTaille()):
            ligne += str(self.getCellule(i)) + "  |  "

            if (i + 1) % 7 == 0:
                resultat = ligne + "\n" + resultat
                ligne = "|  "

        for x in range(1, self.getLongueur() + 1):
            resultat += "   " + str(x) + "  "

        return resultat

g1 = Grille()

try:
    g1.actionJoueur(1,1)
except ValueError:
    print('Erreur de placement')

try:
    g1.actionJoueur(1,2)
except ValueError:
    print('Erreur de placement')

try:
    g1.actionJoueur(1,1)
except ValueError:
    print('Erreur de placement')

try:
    g1.actionJoueur(1,2)
except ValueError:
    print('Erreur de placement')

try:
    g1.actionJoueur(1,1)
except ValueError:
    print('Erreur de placement')

try:
    g1.actionJoueur(1,2)
except ValueError:
    print('Erreur de placement')

try:
    g1.actionJoueur(2,1)
except ValueError:
    print('Erreur de placement')


print(g1)

## Puissance 4
##
##              === Menu ===
##
## 1 - Nouvelle Partie
## 2 - Options
## 3 - Crédits
## 4 - Quitter

##              === Nouvelle Partie ===
##
## Choisir un nom de joueur :

##              === Options ===
##
## 1 - Niveau de l'ia (1 à 5) : 1
## 2 - Vous êtes : Joueur 1
## [esc] - Retour

##              === Crédits ===
##
## Tom Jammes, Samuel Lacam, Tony Lapeyre, Thomas Lemaire
##
## [esc] - retour