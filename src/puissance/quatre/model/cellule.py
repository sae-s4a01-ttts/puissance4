class Cellule:

    __valeur:int

    def __init__(self) -> None: 
        self.__valeur = 0

    def setValeur(self, valeur:int):
        if valeur > 0 and valeur < 3: self.__valeur = valeur
        else: raise ValueError("Impossible d'assigner cette valeur à cette cellule")

    def getValeur(self) -> int:
        return self.__valeur
    
    def estLibre(self) -> bool:
        return self.getValeur() == 0
    
    def __toString(self) -> str:
        match self.getValeur():
            case 1:
                return "X"
            case 2:
                return "O"
            case _:
                return " "

    def __str__(self) -> str:
        return self.__toString()