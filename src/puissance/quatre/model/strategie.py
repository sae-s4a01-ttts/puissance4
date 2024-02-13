from column import Column 
from grid import Grid

###########################################
#                   IDEES
##########################################
# faire une liste de coups simulés dans parametres analyseGrille a la place de colonneSimulation
# permet de générer la grille simulée  
# le bot est le joueur aux pions égaux à 1
# le vrai joueur a les pions 0

# Analyser en roue (tourner dans le sens des aiguilles d'une montre en annalysant la diagonale inférieur gauche puis ligne gauche ...)
# Ne pas faire l'algo de défense si algo victoire à trouvé une victoire (score supérieur à 1000)


def traduction_grille(grille):
    grilleVide = "000000000000000000000"
    grilleDec:int = int(grille,16)
    grilleEntiere = grilleVide[0:21 - len(str(grilleDec))] + str(grilleDec)

    c1 = Column(grilleEntiere[0:3])
    c2 = Column(grilleEntiere[3:6])
    c3 = Column(grilleEntiere[6:9])
    c4 = Column(grilleEntiere[9:12])
    c5 = Column(grilleEntiere[12:15])
    c6 = Column(grilleEntiere[15:18])
    c7 = Column(grilleEntiere[18:21])

    return [c1,c2,c3,c4,c5,c6,c7]


# Simule la liste des coups pour annalyser les grilles générer et donner un score à chaque grille
def analyse_grille(grille_actuelle, colonne_simulation):
    score = 0 # Score de la grille simulée
    # Simulation du coup pour l'analyse et récupération grille actuelle
    grille_actuelle.play_column(colonne_simulation)
    grille_traduite = traduction_grille(grille_actuelle.get_hashcode())

    score += algo_attaque(grille_traduite,colonne_simulation)
    return score


# Analyse les différentes possibilités de jeu pour voir si il y a un cas de victoire
# S'arrète en cas de victoire trouvée
def algo_attaque(grille, coup_simule):
    score_attaque = 0
    hauteur_colonne = (int(grille[coup_simule].get_hashcode())%10)-1

    # analyse de la ligne de gauche
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and coup_simule - i >= 0 and non_bloque:
        if (grille[coup_simule-i].get_cell(hauteur_colonne).get_value() == -1):
            score_alignement += 1
        elif (grille[coup_simule-i].get_cell(hauteur_colonne).get_value() == 1):
            if (score_alignement > 100):
                score_alignement += 1000
            elif (score_alignement >= 10):
                score_alignement += 100
            else:
                score_alignement += 10
        else:
            non_bloque = False
        i+=1
    score_attaque += score_alignement

    return score_attaque

# Analyse les différentes possibilités de jeu pour voir si il y a un cas de défaite
# S'arrète en cas de défaite trouvée
# def algo_defense():



########################################
#                   TESTS
########################################

grille = Grid()
grille.play_column(5)
grille.play_column(3)
grille.play_column(4)
grille.play_column(4)
grille.play_column(2)
grille.play_column(3)
grille.play_column(2)
grille.play_column(6)
grille.play_column(1)

# Grille actuelle
#
#
#
#   |   | 0 | 1 | 1 |   |   |
#   | 0 | 0 | 1 | 0 | 0 | 1 |
# 0   1   2   3   4   5   6 

print("colonne 0 : " + str(analyse_grille(grille,0) == 0) + " " + str(analyse_grille(grille,0)))
print("colonne 1 : " + str(analyse_grille(grille,1) == 1) + " " + str(analyse_grille(grille,1)))
print("colonne 2 : " + str(analyse_grille(grille,2) == 2) + " " + str(analyse_grille(grille,2)))
print("colonne 3 : " + str(analyse_grille(grille,3) == 3) + " " + str(analyse_grille(grille,3)))
print("colonne 4 : " + str(analyse_grille(grille,4) == 3) + " " + str(analyse_grille(grille,4)))
print("colonne 5 : " + str(analyse_grille(grille,5) == 110) + " " + str(analyse_grille(grille,5)))
print("colonne 6 : " + str(analyse_grille(grille,6) == 111) + " " + str(analyse_grille(grille,6)))