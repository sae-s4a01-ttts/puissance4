from grid import Grid
import copy

def parse_coldec(coldec):
    prefix_dec = int(coldec[:2])
    suffix_dec = int(coldec[-1])

    return (prefix_dec, suffix_dec)

def coldec_to_colbin(coldec):
    (prefix_dec, suffix_dec) = parse_coldec(coldec)

    if (prefix_dec, suffix_dec) == (0, 0): return ""

    prefix_bin = bin(prefix_dec)[2:]
    len_prefix_bin = len(prefix_bin)
    col_complement = (suffix_dec - len_prefix_bin)

    colbin = col_complement * '0' + prefix_bin

    return colbin

def colbin_to_coldec(colbin):
    return str(int(colbin, 2)).zfill(2) + str(len(colbin)) if colbin != "" else "000"

def binary_complement(binary_string):
    ones_complement = ""

    for bit in binary_string:
        if bit == '0': ones_complement += '1'
        elif bit == '1': ones_complement += '0'
    
    return ones_complement

def consecutive_vertical_ones(colbin:str) -> int:
    current_ones:int = 0

    for bit in colbin:
        if bit == '1': current_ones += 1
        else: return current_ones

    return current_ones

def eval_vertical_score(colsbin:list[str], column:int) -> int:
    """
    Fonction qui permet de calculer le score vertical d'une fonction.
    @params colsbin est une liste de hashcode de colonne
    @params column est la colonne de colsbin dont on veut calculer le score,
    @return le score vertical de la colonne
    """

    # Calcul le score en hauteur d'une colonne
    height_score:int
    # Calcul le score d'un enchainement d'un même pion
    sequence_score:int
    # Calcul du score final en ajoutant $height_score avec $sequence_score
    calculated_score:int

    # Colonne dont on veut calculer le score en bianire
    active_colbin:str = colsbin[column]

    # Permet de lire le hashcode de la colonne active et d'en tirer sa valeur et sa hauteur
    (prefix_coldec , suffix_coldec) = parse_coldec(colbin_to_coldec(active_colbin))

    # Permet de connaitre le nombre de pion d'une même valeur qui se suivent
    ones_sequence:int = consecutive_vertical_ones(active_colbin)

    height_score = 18.00 - suffix_coldec ** 1.70
    
    height_score = 0.00 if ( prefix_coldec < 2.00 ** (suffix_coldec - 1.00)) or \
                           ( suffix_coldec > 2.00 and suffix_coldec - 2.00 > ones_sequence ) \
                        else height_score
    
    height_score += 4.00 if suffix_coldec < 1.00 else 0.00 

    sequence_score = 0.00 if height_score < 1.00 \
                          else 4.00 ** ( ones_sequence + 1.00 )

    calculated_score = height_score + sequence_score

    return calculated_score

def eval_positive_diagonal_score(colsbin:list[str], column:int) -> int:
    
    sequence_score:int
    calculated_score:int

    range_column:int = len(colsbin)
    height_column:int = len(colsbin[column])

    prev_counter_ones:int = 0
    next_counter_ones:int = 0
    counter_holes:int = 1
    prev_hole:bool = False
    next_hole:bool = False

    ones_sequence:int = 0

    prev_height_column_tmp:int = height_column
    next_height_column_tmp:int = height_column

    for col in range(column - 1, -1, -1):

        colbin_tmp = colsbin[col][::-1]
        height_colbin_tmp = len(colbin_tmp)
        prev_height_column_tmp = prev_height_column_tmp - 1

        if prev_height_column_tmp > -1 and prev_height_column_tmp < height_colbin_tmp:
            if colbin_tmp[prev_height_column_tmp] == '1':
                prev_counter_ones += 1
                ones_sequence += 1 if not prev_hole else 0
            else:
                break
        elif prev_height_column_tmp > -1:
            prev_hole = True
            counter_holes += 1

    for col in range(column + 1, range_column):

        colbin_tmp = colsbin[col][::-1]
        height_colbin_tmp = len(colbin_tmp)
        next_height_column_tmp = next_height_column_tmp + 1

        if next_height_column_tmp < 6 and next_height_column_tmp < height_colbin_tmp:
            if colbin_tmp[next_height_column_tmp] == '1':
                next_counter_ones += 1
                ones_sequence += 1 if not next_hole else 0
            else:
                break
        elif next_height_column_tmp < 6:
            next_hole = True
            counter_holes += 1

    counter_ones:int = prev_counter_ones + next_counter_ones

    ones_unsequenced: int = ones_sequence - counter_ones

    sequence_score = 4.00 ** (ones_sequence + 1.00) + 2.00 ** (ones_unsequenced + 1.00) + counter_holes * 2

    calculated_score = sequence_score if counter_ones + counter_holes > 3 else 0.00
    
    return calculated_score


def eval_negative_diagonal_score(colsbin:list[str], column:int) -> int:
    
    sequence_score:int
    calculated_score:int

    range_column:int = len(colsbin)
    height_column:int = len(colsbin[column])

    prev_counter_ones:int = 0
    next_counter_ones:int = 0
    counter_holes:int = 1
    prev_hole:bool = False
    next_hole:bool = False

    ones_sequence:int = 0

    prev_height_column_tmp:int = height_column
    next_height_column_tmp:int = height_column

    for col in range(column + 1, range_column):

        colbin_tmp = colsbin[col][::-1]
        height_colbin_tmp = len(colbin_tmp)
        prev_height_column_tmp = prev_height_column_tmp - 1

        if prev_height_column_tmp > -1 and prev_height_column_tmp < height_colbin_tmp:
            if colbin_tmp[prev_height_column_tmp] == '1':
                prev_counter_ones += 1
                ones_sequence += 1 if not prev_hole else 0
            else:
                break
        elif prev_height_column_tmp > -1:
            prev_hole = True
            counter_holes += 1

    for col in range(column - 1, -1, -1): 

        colbin_tmp = colsbin[col][::-1]
        height_colbin_tmp = len(colbin_tmp)
        next_height_column_tmp = next_height_column_tmp + 1

        if next_height_column_tmp < 6 and next_height_column_tmp < height_colbin_tmp:
            if colbin_tmp[next_height_column_tmp] == '1':
                next_counter_ones += 1
                ones_sequence += 1 if not next_hole else 0
            else:
                break
        elif next_height_column_tmp < 6:
            next_hole = True
            counter_holes += 1

    counter_ones:int = prev_counter_ones + next_counter_ones

    ones_unsequenced: int = ones_sequence - counter_ones

    sequence_score = 4.00 ** (ones_sequence + 1.00) + 2.00 ** (ones_unsequenced + 1.00) + counter_holes * 2

    calculated_score = sequence_score if counter_ones + counter_holes > 3 else 0.00
    
    return calculated_score


def eval_horizontal_score(colsbin:list[str], column:int) -> int:
    """
    Fonction qui permet de calculer le score horizontal d'une fonction.
    @params colsbin est une liste de hashcode de colonne
    @params column est la colonne de colsbin dont on veut calculer le score,
    @return le score horizontal de la colonne
    """

    width_score:int
    sequence_score:int
    calculated_score:int

    range_column:int = len(colsbin)
    height_column:int = len(colsbin[column])

    prev_counter_ones:int = 0
    next_counter_ones:int = 0
    counter_holes:int = 1
    prev_hole:bool = False
    next_hole:bool = False

    ones_sequence:int = 0

    # Analyse des colonnes qui précèdent la colonne active
    for col in range(column - 1, -1, -1):
        colbin_tmp = colsbin[col][::-1]
        height_colbin_tmp = len(colbin_tmp)
        if height_column < height_colbin_tmp:
            if colbin_tmp[height_column] == '1':
                prev_counter_ones += 1
                ones_sequence += 1 if not prev_hole else 0
            else:
                break
        else:
            prev_hole = True
            counter_holes += 1

    # Analyse des colonnes qui succèdent la colonne active
    for col in range(column + 1, range_column):
        colbin_tmp = colsbin[col][::-1]
        height_colbin_tmp = len(colbin_tmp)
        if height_column < height_colbin_tmp:
            if colbin_tmp[height_column] == '1':
                next_counter_ones += 1
                ones_sequence += 1 if not next_hole else 0
            else:
                break
        else:
            next_hole = True
            counter_holes += 1
        
    width_score = range_column / (range_column ** 0.50) * range_column

    counter_ones:int = prev_counter_ones + next_counter_ones

    ones_unsequenced:int = ones_sequence - counter_ones

    sequence_score = 4.00 ** (ones_sequence + 1.00) + 2.00 ** (ones_unsequenced + 1.00) + counter_holes * 2 

    calculated_score = width_score + sequence_score if counter_ones + counter_holes > 3 else 0.00

    return calculated_score

def eval_victory(grid) -> bool:

    def eval_vertical_victory(grid) -> bool:
        
        victory = False

        for col in grid:
            if len(col) > 3:
                ones_sequence = 0
                for cel in col:
                    if cel == '1': ones_sequence += 1
                    else: ones_sequence = 0
                    if ones_sequence > 3:
                        victory = True
                        break
            if victory: break

        return victory
    
    def eval_horizontal_victory(grid) -> bool:

        victory = False

        for line in range(0, len(grid)):
            ones_sequence = 0
            for col in grid:
                col = col[::-1]
                if line < len(col):
                    if col[line] == '1': ones_sequence += 1
                    else: ones_sequence = 0
                else: ones_sequence = 0
                if ones_sequence > 3:
                    victory = True
                    break
            if victory: break
        
        return victory
                
    
    global_victory = False

    global_victory = eval_vertical_victory(grid)

    global_victory = eval_horizontal_victory(grid) if not global_victory else global_victory

    # global_victory = eval_positive_diagonal_victory(grid) if not global_victory else global_victory

    # global_victory = eval_negative_diagonal_victory(grid) if not global_victory else global_victory

    return global_victory


def separate_string(input_str):
    # Initialisation du tableau pour stocker les morceaux
    separated_strings = []
    
    # Vérification si la longueur de la chaîne est divisible par 3
    if len(input_str) % 3 == 0:
        # Boucle pour parcourir la chaîne de caractères
        for i in range(0, len(input_str), 3):
            # Ajout du morceau de 3 caractères au tableau
            separated_strings.append(input_str[i:i+3])
    else:
        # Si la longueur n'est pas divisible par 3, ajouter des caractères
        # pour que la dernière partie soit de longueur 3
        input_str += ' ' * (3 - (len(input_str) % 3))
        
        # Boucle pour parcourir la chaîne de caractères
        for i in range(0, len(input_str), 3):
            # Ajout du morceau de 3 caractères au tableau
            separated_strings.append(input_str[i:i+3])
    
    return separated_strings

# Exemple d'utilisation de la fonction
# input_string = "001011011013011000000"
input_string = "001011011013000011000"

c = separate_string(input_string)
c = [coldec_to_colbin(col) for col in c]
c = [[c[0:4], 0], [c[0:5], 1], [c[0:6], 2], [c[0:7], 3], [c[1:7], 3], [c[2:7], 3], [c[3:7], 3]]

def X_eval(c):
    c_eval = [0, 0, 0, 0, 0, 0, 0]
    grid = c[3][0]

    for col in range(0, len(c)): 
        c_eval[col] += eval_vertical_score(c[col][0], c[col][1])
        c_eval[col] += eval_horizontal_score(c[col][0], c[col][1])
        c_eval[col] += eval_positive_diagonal_score(c[col][0], c[col][1])
        c_eval[col] += eval_negative_diagonal_score(c[col][0], c[col][1])

    Xe = sum(c_eval)

    Xe += 10000.00 if eval_victory(grid) else 0
    return Xe

def O_eval(c):
    c_eval = [0, 0, 0, 0, 0, 0, 0]
    grid = []

    for col in range(0, len(c)): 
        colcomp = [[binary_complement(col) for col in c[col][0]], c[col][1] ]
        grid = colcomp[0] if len(colcomp[0]) == 7 else grid
        c_eval[col] += eval_vertical_score(colcomp[0], colcomp[1])
        c_eval[col] += eval_horizontal_score(colcomp[0], colcomp[1])
        c_eval[col] += eval_positive_diagonal_score(colcomp[0], colcomp[1])
        c_eval[col] += eval_negative_diagonal_score(colcomp[0], colcomp[1])

    Oe = sum(c_eval)

    Oe += 10000.00 if eval_victory(grid) else 0
    return Oe

def separate_string(input_str):
    # Initialisation du tableau pour stocker les morceaux
    separated_strings = []
    
    # Vérification si la longueur de la chaîne est divisible par 3
    if len(input_str) % 3 == 0:
        # Boucle pour parcourir la chaîne de caractères
        for i in range(0, len(input_str), 3):
            # Ajout du morceau de 3 caractères au tableau
            separated_strings.append(input_str[i:i+3])
    else:
        # Si la longueur n'est pas divisible par 3, ajouter des caractères
        # pour que la dernière partie soit de longueur 3
        input_str += ' ' * (3 - (len(input_str) % 3))
        
        # Boucle pour parcourir la chaîne de caractères
        for i in range(0, len(input_str), 3):
            # Ajout du morceau de 3 caractères au tableau
            separated_strings.append(input_str[i:i+3])
    
    return separated_strings

def traduction_grille(grille):
    grilleVide = "000000000000000000000"
    grilleDec:int = int(grille,16)
    grilleEntiere = grilleVide[0:21 - len(str(grilleDec))] + str(grilleDec)

    return grilleEntiere


# Simule la liste des coups pour annalyser les grilles générer et donner un score à chaque grille
def fonction_evaluation(grille_actuelle):
    c = separate_string(grille_actuelle)
    c = [[c[0:4], 0], [c[0:5], 1], [c[0:6], 2], [c[0:7], 3], [c[1:7], 3], [c[2:7], 3], [c[3:7], 3]]

    eX = X_eval(c)
    eO = O_eval(c)

    e = sum(eX) - sum(eO)

    return e

# Algo du Min/Max
def choix_colonne(grille_actuelle, ordre_jeu):
    colonne_joue = 0 # colonne par défaut
    score_prof_0 = -10000 if ordre_jeu == 0 else 10000
    for i in range(7):
        print("IA joue ", i)
        if lvl_ia >= 2:
            score_prof_1 = -10000 if ordre_jeu == 1 else 10000
            for j in range(7):
                grille_calcul = copy.deepcopy(grille_actuelle) # Copy l'état de la grille sans copier sa référence

                print("Joueur joue ", j)
                try:
                    grille_calcul.play_column(i)
                    grille_calcul.play_column(j)
                    
                    score_prof_2 = fonction_evaluation(traduction_grille(grille_calcul.get_hashcode()))
                    print(" score prof 2 = ", score_prof_2)
                    if ordre_jeu == 1:
                        if score_prof_2 > score_prof_1:
                            score_prof_1 = score_prof_2
                    else:
                        if score_prof_2 < score_prof_1:
                            score_prof_1 = score_prof_2
                except:
                    None
        else:
            grille_calcul = copy.deepcopy(grille_actuelle) # Copy l'état de la grille sans copier sa référence

            try:
                grille_calcul.play_column(i)
                
                score_prof_1 = fonction_evaluation(traduction_grille(grille_calcul.get_hashcode()))
            except:
                None
        print(" score prof 1 = ", score_prof_1)
        if ordre_jeu == 0:
            if score_prof_1 > score_prof_0:
                score_prof_0 = score_prof_1
                colonne_joue = i
        else:
            if score_prof_1 < score_prof_0:
                score_prof_0 = score_prof_1
                colonne_joue = i

    return colonne_joue

## TESTS 

lvl_ia = 1

# grille_test = Grid()
# grille_test.play_column(3)
# grille_test.play_column(3)
# grille_test.play_column(2)
# grille_test.play_column(3)
# grille_test.play_column(1)
# grille_test.play_column(0)

# print(choix_colonne(grille_test,0))