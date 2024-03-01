from column import Column 
from grid import Grid

lvl_ia = 3

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
def analyse_grille(grille_actuelle, coups_simulation):
    score = 0 # Score initial de la grille simulée
    prochain_joueur = 1 # L'IA est toujours le joueur avec les pions 1
    grille_traduite = traduction_grille(grille_actuelle.get_hashcode())
    grille_test_victoire = Grid()
    try:
        # Simulation des différents coups avant le calcul de la grille
        for i in coups_simulation:
            grille_traduite[i].play_cell(prochain_joueur)
            # Vérifie cas de victoire : retourne + 1000 si prochain_joueur = 1 (= IA qui a joué) et -1000 sinon 
            grille_test_victoire.set_grid(grille_traduite)
            if (grille_test_victoire.maybe_its_win(i)):
                if (prochain_joueur == lvl_ia%2):
                    return 1000
                else:
                    return -1000
            prochain_joueur = (prochain_joueur + 1)%2

        score += algo_attaque(grille_traduite,coups_simulation[len(coups_simulation)-1])
        if score < 1000:
            score += algo_defense(grille_traduite)
        return score
    except:
        return -10000 # Cas ou colonne injouable car pleine


# Analyse les différentes possibilités de jeu pour voir si il y a un cas de victoire
# S'arrète en cas de victoire trouvée
def algo_attaque(grille, coup_simule):
    score_attaque = 0
    hauteur_colonne = (int(grille[coup_simule].get_hashcode())%10)-1

    # analyse des différentes lignes de jeu (horizontales, diagonales, verticales)
    i = 1
    score_ligne = 0 # Utilisé pour vérifier les score lorsqu'on joue dans le milieu d'un ligne ex : XX(0)X
    while i <= 7 and score_attaque < 1000:
        if i == 1:
            score_ligne += analyse_horizontal_gauche(grille, hauteur_colonne, coup_simule, False)
        elif i == 2:
            score_ligne += analyse_horizontal_droit(grille, hauteur_colonne, coup_simule, False)
            if score_ligne >= 120:
                score_ligne += 1000
            score_attaque += score_ligne
            score_ligne = 0
        elif i == 3:
            score_attaque += analyse_vertical_bas(grille, hauteur_colonne, coup_simule, False)
        elif i == 4:
            score_ligne += analyse_diag_gauche_bas(grille, hauteur_colonne, coup_simule, False)
        elif i == 5:
            score_ligne += analyse_diag_droit_haut(grille, hauteur_colonne, coup_simule, False)
            if score_ligne >= 120:
                score_ligne += 1000
            score_attaque += score_ligne
            score_ligne = 0
        elif i == 6:
            score_ligne += analyse_diag_gauche_haut(grille, hauteur_colonne, coup_simule, False)
        elif i == 7:
            score_ligne += analyse_diag_droit_bas(grille, hauteur_colonne, coup_simule, False)
            if score_ligne >= 120:
                score_ligne += 1000
            score_attaque += score_ligne
            score_ligne = 0
        i += 1

    return score_attaque

def algo_defense(grille):
    score_defense = 0
    c = 0
    while c < 7 and score_defense > -1000:
        hauteur_colonne_simu = int(grille[c].get_hashcode())%10
        if hauteur_colonne_simu < 6:
            # analyse de la position
            i = 1
            score_ligne = 0 # Utilisé pour vérifier les score lorsqu'on joue dans le milieu d'un ligne ex : XX(0)X
            while i <= 7 and score_defense > -1000:
                if i == 1:
                    score_ligne += analyse_horizontal_gauche(grille, hauteur_colonne_simu, c, True)
                elif i == 2:
                    score_ligne += analyse_horizontal_droit(grille, hauteur_colonne_simu, c, True)
                    if score_ligne <= -120:
                        score_ligne += -1000
                    score_defense += score_ligne
                    score_ligne = 0
                elif i == 3:
                    score_defense += analyse_vertical_bas(grille, hauteur_colonne_simu, c, True)
                elif i == 4:
                    score_ligne += analyse_diag_gauche_bas(grille, hauteur_colonne_simu, c, True)
                elif i == 5:
                    score_ligne += analyse_diag_droit_haut(grille, hauteur_colonne_simu, c, True)
                    if score_ligne <= -120:
                        score_ligne += -1000
                    score_defense += score_ligne
                    score_ligne = 0
                elif i == 6:
                    score_ligne += analyse_diag_droit_bas(grille, hauteur_colonne_simu, c, True)
                elif i == 7:
                    score_ligne += analyse_diag_gauche_haut(grille, hauteur_colonne_simu, c, True)
                    if score_ligne <= -120:
                        score_ligne += -1000
                    score_defense += score_ligne
                    score_ligne = 0
                    
                i += 1
        c += 1
    return score_defense

def analyse_horizontal_gauche(grille, hauteur_colonne, coup_simule, est_defense):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and coup_simule - i >= 0 and non_bloque:
        if est_defense:
            if (grille[coup_simule-i].get_cell(hauteur_colonne).get_value() == (lvl_ia+1)%2):
                score_alignement = evaluation_defense(score_alignement)
            else:
                non_bloque = False
        else:    
            if (grille[coup_simule-i].get_cell(hauteur_colonne).get_value() == -1):
                score_alignement += 1
            elif (grille[coup_simule-i].get_cell(hauteur_colonne).get_value() == lvl_ia%2):
                score_alignement = evaluation_attaque(score_alignement)
            else:
                non_bloque = False
        i+=1
    return score_alignement


def analyse_horizontal_droit(grille, hauteur_colonne, coup_simule, est_defense):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and coup_simule + i <= 6 and non_bloque:
        if est_defense:
            if (grille[coup_simule+i].get_cell(hauteur_colonne).get_value() == (lvl_ia+1)%2):
                score_alignement = evaluation_defense(score_alignement)
            else:
                non_bloque = False
        else:
            if (grille[coup_simule+i].get_cell(hauteur_colonne).get_value() == -1):
                score_alignement += 1
            elif (grille[coup_simule+i].get_cell(hauteur_colonne).get_value() == lvl_ia%2):
                score_alignement = evaluation_attaque(score_alignement)
            else:
                non_bloque = False
        i+=1
    return score_alignement

def analyse_vertical_bas(grille, hauteur_colonne, coup_simule, est_defense):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and hauteur_colonne - i >= 0 and non_bloque:
        if est_defense:
            if (grille[coup_simule].get_cell(hauteur_colonne-i).get_value() == (lvl_ia+1)%2):
                score_alignement = evaluation_defense(score_alignement)
            else:
                non_bloque = False
        else:
            if (grille[coup_simule].get_cell(hauteur_colonne-i).get_value() == lvl_ia%2):
                score_alignement = evaluation_attaque(score_alignement)
            else:
                non_bloque = False
        i+=1
    return score_alignement

def analyse_diag_gauche_bas(grille, hauteur_colonne, coup_simule, est_defense):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and hauteur_colonne - i >= 0 and coup_simule -i >= 0 and non_bloque:
        if est_defense:
            if (grille[coup_simule-i].get_cell(hauteur_colonne-i).get_value() == (lvl_ia+1)%2):
                score_alignement = evaluation_defense(score_alignement)
            else:
                non_bloque = False
        else:
            if (grille[coup_simule-i].get_cell(hauteur_colonne-i).get_value() == -1):
                score_alignement += 1
            elif (grille[coup_simule-i].get_cell(hauteur_colonne-i).get_value() == lvl_ia%2):
                score_alignement = evaluation_attaque(score_alignement)
            else:
                non_bloque = False
        i+=1
    return score_alignement

def analyse_diag_droit_bas(grille, hauteur_colonne, coup_simule, est_defense):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and hauteur_colonne - i >= 0 and coup_simule +i <= 6 and non_bloque:
        if est_defense:
            if (grille[coup_simule+i].get_cell(hauteur_colonne-i).get_value() == (lvl_ia+1)%2):
                score_alignement = evaluation_defense(score_alignement)
            else:
                non_bloque = False
        else:
            if (grille[coup_simule+i].get_cell(hauteur_colonne-i).get_value() == -1):
                score_alignement += 1
            elif (grille[coup_simule+i].get_cell(hauteur_colonne-i).get_value() == lvl_ia%2):
                score_alignement = evaluation_attaque(score_alignement)
            else:
                non_bloque = False
        i+=1
    return score_alignement

def analyse_diag_droit_haut(grille, hauteur_colonne, coup_simule, est_defense):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and hauteur_colonne + i <= 5 and coup_simule + i <= 6 and non_bloque:
        if est_defense:
            if (grille[coup_simule+i].get_cell(hauteur_colonne+i).get_value() == (lvl_ia+1)%2):
                score_alignement = evaluation_defense(score_alignement)
            else:
                non_bloque = False
        else:
            if (grille[coup_simule+i].get_cell(hauteur_colonne+i).get_value() == -1):
                score_alignement += 1
            elif (grille[coup_simule+i].get_cell(hauteur_colonne+i).get_value() == lvl_ia%2):
                score_alignement = evaluation_attaque(score_alignement)
            else:
                non_bloque = False
        i+=1
    return score_alignement

def analyse_diag_gauche_haut(grille, hauteur_colonne, coup_simule, est_defense):
    i = 1
    score_alignement = 0 # score permettant de vérifier alignement (ex: score > 100 = 2 jetons alignés)
    non_bloque = True
    while i < 4  and hauteur_colonne + i <= 5 and coup_simule - i >= 0 and non_bloque:
        if est_defense:
            if (grille[coup_simule-i].get_cell(hauteur_colonne+i).get_value() == (lvl_ia+1)%2): #lvl_ia permet d'alterner le "couleur" analysée en fonction de la profondeur du Min/Max
                score_alignement = evaluation_defense(score_alignement)
            else:
                non_bloque = False
        else:
            if (grille[coup_simule-i].get_cell(hauteur_colonne+i).get_value() == -1):
                score_alignement += 1
            elif (grille[coup_simule-i].get_cell(hauteur_colonne+i).get_value() == lvl_ia%2):
                score_alignement = evaluation_attaque(score_alignement)
            else:
                non_bloque = False
        i+=1
    return score_alignement

def evaluation_attaque(score_actuel):
    nouveau_score = score_actuel
    if (nouveau_score > 100):
        nouveau_score += 1000
    elif (nouveau_score >= 10):
        nouveau_score += 100
    else:
        nouveau_score += 10
    return nouveau_score

def evaluation_defense(score_actuel):
    nouveau_score = score_actuel
    if (nouveau_score < -100):
        nouveau_score -= 1000
    elif (nouveau_score <= -10):
        nouveau_score -= 100
    else:
        nouveau_score -= 10
    return nouveau_score

# Algo du Min/Max
def choix_colonne(grille_actuelle):
    colonne_joue = 0 # colonne par défaut
    score_prof_1 = -10000 if lvl_ia%2 == 1 else 10000 
    for i in range(7):
        print("IA joue ", i)
        if lvl_ia >= 2:
            score_prof_2 = -10000 if lvl_ia%2 == 0 else 10000 # Initialisation pour la première comparaison
            for j in range(7):
                print("joueur joue ", j)
                if lvl_ia >= 3:
                    score_prof_3 = -10000 if lvl_ia%2 == 1 else 10000 # Initialisation pour la première comparaison
                    for k in range(7):
                        print("IA joue ", k)
                        if lvl_ia >= 4:
                            score_prof_4 = -10000 if lvl_ia%2 == 0 else 10000 # Initialisation pour la première comparaison
                            for l in range(7):
                                # print("IA joue ", l)
                                score = analyse_grille(grille_actuelle, [i,j,k,l])
                                # print(" score = ", score)
                        else:
                            score_prof_4 = analyse_grille(grille_actuelle, [i,j,k])
                            # print(" score = ", score)
                        if lvl_ia%2 == 1:
                            if score_prof_4 > score_prof_3:
                                score_prof_3 = score_prof_4
                        else:
                            if score_prof_4 < score_prof_3:
                                score_prof_3 = score_prof_4
                else:
                    score_prof_3 = analyse_grille(grille_actuelle, [i,j])
                    # print(" score = ", score)
                if lvl_ia%2 == 1:
                    if score_prof_3 < score_prof_2:
                            score_prof_2 = score_prof_3
                else:
                    if score_prof_3 > score_prof_2:
                            score_prof_2 = score_prof_3
                    
        else:
            score_prof_2 = analyse_grille(grille_actuelle, [i])
            # print(" score = ", score)
        if lvl_ia%2 == 1:
            if score_prof_2 > score_prof_1:
                score_prof_1 = score_prof_2
                colonne_joue = i
        else:
            if score_prof_2 < score_prof_1:
                score_prof_1 = score_prof_2
                colonne_joue = i

    return colonne_joue



########################################
#                   TESTS
########################################

grilleTest = Grid()
grilleTest.play_column(4)
grilleTest.play_column(3)
grilleTest.play_column(4)
grilleTest.play_column(4)
grilleTest.play_column(4)
grilleTest.play_column(3)
grilleTest.play_column(4)
grilleTest.play_column(5)
grilleTest.play_column(4)

#   |   |   | 0 |   |   |   |
#   |   |   | 0 |   |   |   |
#   |   |   | 0 |   |   |   |
#   |   |   | 1 |   |   |   |
#   |   | 1 | 0 |   |   |   |
#   |   | 1 | 0 | 1 |   |   |
# 0   1   2   3   4   5   6 

print(choix_colonne(grilleTest))

# grilleTest.play_column(0)
# grilleTest.play_column(2)
# grilleTest.play_column(1)
# grilleTest.play_column(2)
# grilleTest.play_column(0)
# grilleTest.play_column(1)
# grilleTest.play_column(3)
# grilleTest.play_column(3)
# grilleTest.play_column(5)
# grilleTest.play_column(0)
# grilleTest.play_column(6)

# Grille actuelle
#   |   |   |   |   |   |   |
#   |   |   |   |   |   |   |
#   |   |   |   |   |   |   |
# 1 |   |   |   |   |   |   |
# 0 | 1 | 1 | 1 |   |   |   |
# 0 | 0 | 1 | 0 |   | 0 | 0 |
# 0   1   2   3   4   5   6 

# grilleTest.play_column(2)
# grilleTest.play_column(1)
# grilleTest.play_column(2)
# grilleTest.play_column(1)
# grilleTest.play_column(4)
# grilleTest.play_column(5)
# grilleTest.play_column(4)
# grilleTest.play_column(2)
# grilleTest.play_column(5)

#   |   |   |   |   |   |   |
#   |   |   |   |   |   |   |
#   |   |   |   |   |   |   |
#   |   | 1 |   |   |   |   |
#   | 1 | 0 |   | 0 | 0 |   |
#   | 1 | 0 |   | 0 | 1 |   |
# 0   1   2   3   4   5   6 

# 1 jeton 0 = +2 
# 2 jetons 0 = +20
# 3 jetons 0 = +200
# col 0: 9
# col 1: 9
# col 2: 9
# col 3: 11
# col 4: 10
# col 5: 8
# col 6: 6

#   |   |   |   |   |   |   |
#   |   |   |   |   |   |   |
#   |   |   |   |   |   |   |
#   |   |   |   |   |   |   |
#   |   |   |   |   |   |   |
# 0 |   |   | 1 |   |   |   |
# 0   1   2   3   4   5   6 

# 1 jeton 0 = +2 
# 2 jetons 0 = +20
# 3 jetons 0 = +200
# col 0: 9
# col 1: 18
# col 2: 18
# col 3: 24
# col 4: 19
# col 5: 17
# col 6: 15



# print("colonne 0 : " , analyse_grille(grilleTest.get_hashcode(),[0]))
# print("colonne 1 : " , analyse_grille(grilleTest.get_hashcode(),[1]))
# print("colonne 2 : " , analyse_grille(grilleTest.get_hashcode(),[2]))
# print("colonne 3 : " , analyse_grille(grilleTest.get_hashcode(),[3]))
# print("colonne 4 : " , analyse_grille(grilleTest.get_hashcode(),[4]))
# print("colonne 5 : " , analyse_grille(grilleTest.get_hashcode(),[5]))
# print("colonne 6 : " , analyse_grille(grilleTest.get_hashcode(),[6]))
# print(choix_colonne(grilleTest))

# TEST FINAL
# print("colonne 0 : " , analyse_grille(grilleTest.get_hashcode(),0) == -582 , " " , analyse_grille(grilleTest.get_hashcode(),0))
# print("colonne 1 : " , analyse_grille(grilleTest.get_hashcode(),1) == -650 , " " , analyse_grille(grilleTest.get_hashcode(),1))
# print("colonne 2 : " , analyse_grille(grilleTest.get_hashcode(),2) == -518 , " " , analyse_grille(grilleTest.get_hashcode(),2))
# print("colonne 3 : " , analyse_grille(grilleTest.get_hashcode(),3) == -517 , " " ,analyse_grille(grilleTest.get_hashcode(),3))
# print("colonne 4 : " , analyse_grille(grilleTest.get_hashcode(),4) == -673, " " , analyse_grille(grilleTest.get_hashcode(),4))
# print("colonne 5 : " , analyse_grille(grilleTest.get_hashcode(),5) == -678 , " " , analyse_grille(grilleTest.get_hashcode(),5))
# print("colonne 6 : " , analyse_grille(grilleTest.get_hashcode(),6) == -142 , " " , analyse_grille(grilleTest.get_hashcode(),6))
# print(choix_colonne(grilleTest.get_hashcode()))

# TEST TOTAL ATTAQUE
# print("colonne 0 : " , analyse_grille(grilleTest,0) == 1 , " " , analyse_grille(grilleTest,0))
# print("colonne 1 : " , analyse_grille(grilleTest,1) == 3 , " " , analyse_grille(grilleTest,1))
# print("colonne 2 : " , analyse_grille(grilleTest,2) == 12 , " " , analyse_grille(grilleTest,2))
# print("colonne 3 : " , analyse_grille(grilleTest,3) == 119 , " " ,analyse_grille(grilleTest,3))
# print("colonne 4 : " , analyse_grille(grilleTest,4) == 20, " " , analyse_grille(grilleTest,4))
# print("colonne 5 : " , analyse_grille(grilleTest,5) == 26 , " " , analyse_grille(grilleTest,5))
# print("colonne 6 : " , analyse_grille(grilleTest,6) == 1110 , " " , analyse_grille(grilleTest,6))
# print("Colonne joué : ", choix_colonne(grilleTest))

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