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
    grille_traduite = traduction_grille(grille_actuelle.get_hashcode())
    grille_traduite[colonne_simulation].play_cell(1)

    score += algo_attaque(grille_traduite,colonne_simulation)
    return score


# Analyse les différentes possibilités de jeu pour voir si il y a un cas de victoire
# S'arrète en cas de victoire trouvée
def algo_attaque(grille, coup_simule):
    score_attaque = 0
    hauteur_colonne = (int(grille[coup_simule].get_hashcode())%10)-1

    # analyse des différentes lignes de jeu (horizontales, diagonales, verticales)
    i = 1
    while i <= 7 and score_attaque < 1000:
        if i == 1:
            score_attaque += analyse_horizontal_gauche(grille, hauteur_colonne, coup_simule)
        elif i == 2:
            score_attaque += analyse_horizontal_droit(grille, hauteur_colonne, coup_simule)
        elif i == 3:
            score_attaque += analyse_vertical_bas(grille, hauteur_colonne, coup_simule)
        elif i == 4:
            score_attaque += analyse_diag_gauche_bas(grille, hauteur_colonne, coup_simule)
        elif i == 5:
            score_attaque += analyse_diag_droit_bas(grille, hauteur_colonne, coup_simule)
        elif i == 6:
            score_attaque += analyse_diag_gauche_haut(grille, hauteur_colonne, coup_simule)
        elif i == 7:
            score_attaque += analyse_diag_droit_haut(grille, hauteur_colonne, coup_simule)
        i += 1

    # Faire un boucle avec un num qui s'incrémente
    # En fonction du num : appeler la bonne méthode d'analyse (analyse_ligne_gauche, analyse_diag_haute_gauche, ...)
    # a chaque itération vérifier qu'aucun cas de victoire n'a été trouvé, si oui stopper l'algo d'attaque

    return score_attaque


def analyse_horizontal_gauche(grille, hauteur_colonne, coup_simule):
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
    return score_alignement


def analyse_horizontal_droit(grille, hauteur_colonne, coup_simule):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and coup_simule + i <= 6 and non_bloque:
        if (grille[coup_simule+i].get_cell(hauteur_colonne).get_value() == -1):
            score_alignement += 1
        elif (grille[coup_simule+i].get_cell(hauteur_colonne).get_value() == 1):
            if (score_alignement > 100):
                score_alignement += 1000
            elif (score_alignement >= 10):
                score_alignement += 100
            else:
                score_alignement += 10
        else:
            non_bloque = False
        i+=1
    return score_alignement

def analyse_vertical_bas(grille, hauteur_colonne, coup_simule):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and hauteur_colonne - i >= 0 and non_bloque:
        if (grille[coup_simule].get_cell(hauteur_colonne-i).get_value() == 1):
            if (score_alignement > 100):
                score_alignement += 1000
            elif (score_alignement >= 10):
                score_alignement += 100
            else:
                score_alignement += 10
        else:
            non_bloque = False
        i+=1
    return score_alignement

def analyse_diag_gauche_bas(grille, hauteur_colonne, coup_simule):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and hauteur_colonne - i >= 0 and coup_simule -i >= 0 and non_bloque:
        if (grille[coup_simule-i].get_cell(hauteur_colonne-i).get_value() == -1):
            score_alignement += 1
        elif (grille[coup_simule-i].get_cell(hauteur_colonne-i).get_value() == 1):
            if (score_alignement > 100):
                score_alignement += 1000
            elif (score_alignement >= 10):
                score_alignement += 100
            else:
                score_alignement += 10
        else:
            non_bloque = False
        i+=1
    return score_alignement

def analyse_diag_droit_bas(grille, hauteur_colonne, coup_simule):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and hauteur_colonne - i >= 0 and coup_simule +i <= 6 and non_bloque:
        if (grille[coup_simule+i].get_cell(hauteur_colonne-i).get_value() == -1):
            score_alignement += 1
        elif (grille[coup_simule+i].get_cell(hauteur_colonne-i).get_value() == 1):
            if (score_alignement > 100):
                score_alignement += 1000
            elif (score_alignement >= 10):
                score_alignement += 100
            else:
                score_alignement += 10
        else:
            non_bloque = False
        i+=1
    return score_alignement

def analyse_diag_droit_haut(grille, hauteur_colonne, coup_simule):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and hauteur_colonne + i <= 5 and coup_simule + i <= 6 and non_bloque:
        if (grille[coup_simule+i].get_cell(hauteur_colonne+i).get_value() == -1):
            score_alignement += 1
        elif (grille[coup_simule+i].get_cell(hauteur_colonne+i).get_value() == 1):
            if (score_alignement > 100):
                score_alignement += 1000
            elif (score_alignement >= 10):
                score_alignement += 100
            else:
                score_alignement += 10
        else:
            non_bloque = False
        i+=1
    return score_alignement

def analyse_diag_gauche_haut(grille, hauteur_colonne, coup_simule):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and hauteur_colonne + i <= 5 and coup_simule - i >= 0 and non_bloque:
        if (grille[coup_simule-i].get_cell(hauteur_colonne+i).get_value() == -1):
            score_alignement += 1
        elif (grille[coup_simule-i].get_cell(hauteur_colonne+i).get_value() == 1):
            if (score_alignement > 100):
                score_alignement += 1000
            elif (score_alignement >= 10):
                score_alignement += 100
            else:
                score_alignement += 10
        else:
            non_bloque = False
        i+=1
    return score_alignement



# Analyse les différentes possibilités de jeu pour voir si il y a un cas de défaite
# S'arrète en cas de défaite trouvée
# def algo_defense():



########################################
#                   TESTS
########################################

grilleTest = Grid()
grilleTest.play_column(1)
grilleTest.play_column(3)
grilleTest.play_column(2)
grilleTest.play_column(3)
grilleTest.play_column(2)
grilleTest.play_column(4)
grilleTest.play_column(4)
grilleTest.play_column(5)
grilleTest.play_column(2)

# Grille actuelle
#   |   |   |   |   |   |   |
#   |   |   |   |   |   |   |
#   |   |   |   |   |   |   |
#   |   | 0 |   |   |   |   |
#   |   | 0 | 1 | 0 |   |   |
#   | 0 | 0 | 1 | 1 | 1 |   |
# 0   1   2   3   4   5   6 

# TEST TOTAL
print("colonne 0 : " , analyse_grille(grilleTest,0) == 1 , " " , analyse_grille(grilleTest,0))
print("colonne 1 : " , analyse_grille(grilleTest,1) == 3 , " " , analyse_grille(grilleTest,1))
print("colonne 2 : " , analyse_grille(grilleTest,2) == 12 , " " , analyse_grille(grilleTest,2))
print("colonne 3 : " , analyse_grille(grilleTest,3) == 119 , " " ,analyse_grille(grilleTest,3))
print("colonne 4 : " , analyse_grille(grilleTest,4) == 20, " " , analyse_grille(grilleTest,4))
print("colonne 5 : " , analyse_grille(grilleTest,5) == 26 , " " , analyse_grille(grilleTest,5))
print("colonne 6 : " , analyse_grille(grilleTest,6) == 1110 , " " , analyse_grille(grilleTest,6))

# TEST HORIZONTAL VERTICAL DIAGONAL BAS
# print("colonne 0 : " , analyse_grille(grilleTest,0) == 0 , " " , analyse_grille(grilleTest,0))
# print("colonne 1 : " , analyse_grille(grilleTest,1) == 2 , " " , analyse_grille(grilleTest,1))
# print("colonne 2 : " , analyse_grille(grilleTest,2) == 17 , " " , analyse_grille(grilleTest,2))
# print("colonne 3 : " , analyse_grille(grilleTest,3) == 126 , " " ,analyse_grille(grilleTest,3))
# print("colonne 4 : " , analyse_grille(grilleTest,4) == 36, " " , analyse_grille(grilleTest,4))
# print("colonne 5 : " , analyse_grille(grilleTest,5) == 121 , " " , analyse_grille(grilleTest,5))
# print("colonne 6 : " , analyse_grille(grilleTest,6) == 121 , " " , analyse_grille(grilleTest,6))

# TEST DIAGONALE DROITE BAS
# print("colonne 0 : " , analyse_grille(grilleTest,0) == 0 , " " , analyse_grille(grilleTest,0))
# print("colonne 1 : " , analyse_grille(grilleTest,1) == 0 , " " , analyse_grille(grilleTest,1))
# print("colonne 2 : " , analyse_grille(grilleTest,2) == 10 , " " , analyse_grille(grilleTest,2))
# print("colonne 3 : " , analyse_grille(grilleTest,3) == 10 , " " ,analyse_grille(grilleTest,3))
# print("colonne 4 : " , analyse_grille(grilleTest,4) == 11, " " , analyse_grille(grilleTest,4))
# print("colonne 5 : " , analyse_grille(grilleTest,5) == 10 , " " , analyse_grille(grilleTest,5))
# print("colonne 6 : " , analyse_grille(grilleTest,6) == 0 , " " , analyse_grille(grilleTest,6))

# TEST DIAGONALE GAUCHE BAS
# print("colonne 0 : " , analyse_grille(grilleTest,0) == 0 , " " , analyse_grille(grilleTest,0))
# print("colonne 1 : " , analyse_grille(grilleTest,1) == 1 , " " , analyse_grille(grilleTest,1))
# print("colonne 2 : " , analyse_grille(grilleTest,2) == 2 , " " , analyse_grille(grilleTest,2))
# print("colonne 3 : " , analyse_grille(grilleTest,3) == 0 , " " ,analyse_grille(grilleTest,3))
# print("colonne 4 : " , analyse_grille(grilleTest,4) == 10, " " , analyse_grille(grilleTest,4))
# print("colonne 5 : " , analyse_grille(grilleTest,5) == 0 , " " , analyse_grille(grilleTest,5))
# print("colonne 6 : " , analyse_grille(grilleTest,6) == 0 , " " , analyse_grille(grilleTest,6))

# TEST HORIZONTAL GAUCHE
# print("colonne 0 : " , analyse_grille(grilleTest,0) == 0 , " " , analyse_grille(grilleTest,0))
# print("colonne 1 : " , analyse_grille(grilleTest,1) == 1 , " " , analyse_grille(grilleTest,1))
# print("colonne 2 : " , analyse_grille(grilleTest,2) == 2 , " " , analyse_grille(grilleTest,2))
# print("colonne 3 : " , analyse_grille(grilleTest,3) == 3 , " " ,analyse_grille(grilleTest,3))
# print("colonne 4 : " , analyse_grille(grilleTest,4) == 3, " " , analyse_grille(grilleTest,4))
# print("colonne 5 : " , analyse_grille(grilleTest,5) == 110 , " " , analyse_grille(grilleTest,5))
# print("colonne 6 : " , analyse_grille(grilleTest,6) == 111 , " " , analyse_grille(grilleTest,6))

# TEST HORIZONTAL DROIT
# print("colonne 0 : " , analyse_grille(grilleTest,0) == 0 , " " , analyse_grille(grilleTest,0))
# print("colonne 1 : " , analyse_grille(grilleTest,1) == 0 , " " , analyse_grille(grilleTest,1))
# print("colonne 2 : " , analyse_grille(grilleTest,2) == 3 , " " , analyse_grille(grilleTest,2))
# print("colonne 3 : " , analyse_grille(grilleTest,3) == 3 , " " ,analyse_grille(grilleTest,3))
# print("colonne 4 : " , analyse_grille(grilleTest,4) == 2, " " , analyse_grille(grilleTest,4))
# print("colonne 5 : " , analyse_grille(grilleTest,5) == 1 , " " , analyse_grille(grilleTest,5))
# print("colonne 6 : " , analyse_grille(grilleTest,6) == 0 , " " , analyse_grille(grilleTest,6))

# TEST HORIZONTAL
# print("colonne 0 : " , analyse_grille(grilleTest,0) == 0 , " " , analyse_grille(grilleTest,0))
# print("colonne 1 : " , analyse_grille(grilleTest,1) == 1 , " " , analyse_grille(grilleTest,1))
# print("colonne 2 : " , analyse_grille(grilleTest,2) == 5 , " " , analyse_grille(grilleTest,2))
# print("colonne 3 : " , analyse_grille(grilleTest,3) == 6 , " " ,analyse_grille(grilleTest,3))
# print("colonne 4 : " , analyse_grille(grilleTest,4) == 5, " " , analyse_grille(grilleTest,4))
# print("colonne 5 : " , analyse_grille(grilleTest,5) == 111 , " " , analyse_grille(grilleTest,5))
# print("colonne 6 : " , analyse_grille(grilleTest,6) == 111 , " " , analyse_grille(grilleTest,6))

# TEST VERTICAL BAS
# print("colonne 0 : " , analyse_grille(grilleTest,0) == 0 , " " , analyse_grille(grilleTest,0))
# print("colonne 1 : " , analyse_grille(grilleTest,1) == 0 , " " , analyse_grille(grilleTest,1))
# print("colonne 2 : " , analyse_grille(grilleTest,2) == 0 , " " , analyse_grille(grilleTest,2))
# print("colonne 3 : " , analyse_grille(grilleTest,3) == 110 , " " ,analyse_grille(grilleTest,3))
# print("colonne 4 : " , analyse_grille(grilleTest,4) == 10, " " , analyse_grille(grilleTest,4))
# print("colonne 5 : " , analyse_grille(grilleTest,5) == 0 , " " , analyse_grille(grilleTest,5))
# print("colonne 6 : " , analyse_grille(grilleTest,6) == 10 , " " , analyse_grille(grilleTest,6))

# TEST HORIZONTAL VERTICAL BAS
# print("colonne 0 : " , analyse_grille(grilleTest,0) == 0 , " " , analyse_grille(grilleTest,0))
# print("colonne 1 : " , analyse_grille(grilleTest,1) == 1 , " " , analyse_grille(grilleTest,1))
# print("colonne 2 : " , analyse_grille(grilleTest,2) == 5 , " " , analyse_grille(grilleTest,2))
# print("colonne 3 : " , analyse_grille(grilleTest,3) == 116 , " " ,analyse_grille(grilleTest,3))
# print("colonne 4 : " , analyse_grille(grilleTest,4) == 15, " " , analyse_grille(grilleTest,4))
# print("colonne 5 : " , analyse_grille(grilleTest,5) == 111 , " " , analyse_grille(grilleTest,5))
# print("colonne 6 : " , analyse_grille(grilleTest,6) == 121 , " " , analyse_grille(grilleTest,6))