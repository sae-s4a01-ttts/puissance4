from grid import Grid
from player import Player
import copy

class Computer(Player):

    __lvl_ia = 4 

    def __init__(self, lvl_ia) -> None:
        self.__lvl_ia = lvl_ia

    def __parse_coldec(self, coldec):
        prefix_dec = int(coldec[:2])
        suffix_dec = int(coldec[-1])

        return (prefix_dec, suffix_dec)

    def __coldec_to_colbin(self, coldec):
        (prefix_dec, suffix_dec) = self.__parse_coldec(coldec)

        if (prefix_dec, suffix_dec) == (0, 0): return ""

        prefix_bin = bin(prefix_dec)[2:]
        len_prefix_bin = len(prefix_bin)
        col_complement = (suffix_dec - len_prefix_bin)

        colbin = col_complement * '0' + prefix_bin

        return colbin

    def __colbin_to_coldec(self, colbin):
        return str(int(colbin, 2)).zfill(2) + str(len(colbin)) if colbin != "" else "000"

    def __binary_complement(self, binary_string):
        ones_complement = ""

        for bit in binary_string:
            if bit == '0': ones_complement += '1'
            elif bit == '1': ones_complement += '0'
        
        return ones_complement

    def __consecutive_vertical_ones(self, colbin:str) -> int:
        current_ones:int = 0

        for bit in colbin:
            if bit == '1': current_ones += 1
            else: return current_ones

        return current_ones

    def __eval_vertical_score(self, colsbin:list[str], column:int) -> int:
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
        (prefix_coldec , suffix_coldec) = self.__parse_coldec(self.__colbin_to_coldec(active_colbin))

        # Permet de connaitre le nombre de pion d'une même valeur qui se suivent
        ones_sequence:int = self.__consecutive_vertical_ones(active_colbin)

        height_score = 18.00 - suffix_coldec ** 1.70
        
        height_score = 0.00 if ( prefix_coldec < 2.00 ** (suffix_coldec - 1.00)) or \
                            ( suffix_coldec > 2.00 and suffix_coldec - 2.00 > ones_sequence ) \
                            else height_score
        
        height_score += 4.00 if suffix_coldec < 1.00 else 0.00 

        sequence_score = 0.00 if height_score < 1.00 \
                            else 4.00 ** ( ones_sequence + 1.00 )

        calculated_score = height_score + sequence_score

        return calculated_score

    def __eval_positive_diagonal_score(self, colsbin:list[str], column:int) -> int:
        
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


    def __eval_negative_diagonal_score(self, colsbin:list[str], column:int) -> int:
        
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


    def __eval_horizontal_score(self, colsbin:list[str], column:int) -> int:
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

    def __eval_victory(self, grid) -> bool:

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
        
        def eval_positive_diagonal_victory(grid) -> bool:

            victory = False

            origin_height = 2
            origin_width  = 0

            range_sequence = [4, 5, 6, 6, 5, 4]
            irange = 0

            for dgl in range(0, 6):
                ones_sequence = 0
                colsbin = grid[origin_width : range_sequence[irange] + origin_width]
                
                next_height = origin_height
                for colbin in colsbin:
                    colbin = colbin[::-1]
                    if len(colbin) > next_height:
                        if colbin[next_height] == '1': ones_sequence += 1
                        else: ones_sequence = 0
                    else: ones_sequence = 0
                    if ones_sequence > 3:
                        victory = True
                        break

                    next_height += 1

                if victory: break

                origin_width  += 1 if origin_height < 1 else 0
                origin_height -= 1 if origin_height > 0 else 0
                irange += 1

            return victory
        
        def eval_negative_diagonal_victory(grid) -> bool:

            victory = False

            origin_height = 2
            origin_width  = 6

            range_sequence = [4, 5, 6, 6, 5, 4]
            irange = 0

            for dgl in range(5, -1, -1):
                ones_sequence = 0
                colsbin = grid[origin_width - range_sequence[irange] + 1 : origin_width + 1][::-1]
                
                next_height = origin_height
                for colbin in colsbin:
                    colbin = colbin[::-1]

                    if len(colbin) > next_height:


                        if colbin[next_height] == '1': ones_sequence += 1
                        else: ones_sequence = 0

                    else: ones_sequence = 0
                    if ones_sequence > 3:
                        victory = True
                        break

                    next_height += 1

                if victory: break

                origin_width  -= 1 if origin_height < 1 else 0
                origin_height -= 1 if origin_height > 0 else 0
                irange += 1

            return victory
                    
        
        global_victory = False

        global_victory = self.__eval_vertical_victory(grid)

        global_victory = self.__eval_horizontal_victory(grid) if not global_victory else global_victory

        global_victory = self.__eval_positive_diagonal_victory(grid) if not global_victory else global_victory

        global_victory = self.__eval_negative_diagonal_victory(grid) if not global_victory else global_victory

        return global_victory

    # Exemple d'utilisation de la fonction
    # input_string = "001011011013011000000"
    # input_string = "001011011013000011000"

    # c = separate_string(input_string)
    # c = [coldec_to_colbin(col) for col in c]
    # c = [[c[0:4], 0], [c[0:5], 1], [c[0:6], 2], [c[0:7], 3], [c[1:7], 3], [c[2:7], 3], [c[3:7], 3]]

    def __X_eval(self, c):
        c_eval = [0, 0, 0, 0, 0, 0, 0]
        grid = c[3][0]

        for col in range(0, len(c)): 
            c_eval[col] += self.__eval_vertical_score(c[col][0], c[col][1])
            c_eval[col] += self.__eval_horizontal_score(c[col][0], c[col][1])
            c_eval[col] += self.__eval_positive_diagonal_score(c[col][0], c[col][1])
            c_eval[col] += self.__eval_negative_diagonal_score(c[col][0], c[col][1])

        Xe = sum(c_eval)

        Xe += 10000.00 if self.__eval_victory(grid) else 0
        return Xe

    def __O_eval(self, c):
        c_eval = [0, 0, 0, 0, 0, 0, 0]
        grid = []

        for col in range(0, len(c)): 
            colcomp = [[self.__binary_complement(col) for col in c[col][0]], c[col][1] ]
            grid = colcomp[0] if len(colcomp[0]) == 7 else grid
            c_eval[col] += self.__eval_vertical_score(colcomp[0], colcomp[1])
            c_eval[col] += self.__eval_horizontal_score(colcomp[0], colcomp[1])
            c_eval[col] += self.__eval_positive_diagonal_score(colcomp[0], colcomp[1])
            c_eval[col] += self.__eval_negative_diagonal_score(colcomp[0], colcomp[1])

        Oe = sum(c_eval)

        Oe += 10000.00 if self.__eval_victory(grid) else 0
        return Oe

    def __separate_string(self, input_str):
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

    def __traduction_grille(self, grille):
        grilleVide = "000000000000000000000"
        grilleDec:int = int(grille,16)
        grilleEntiere = grilleVide[0:21 - len(str(grilleDec))] + str(grilleDec)

        return grilleEntiere


    # Simule la liste des coups pour annalyser les grilles générer et donner un score à chaque grille
    def __fonction_evaluation(self, grille_actuelle):
        c = self.__separate_string(self.__traduction_grille(grille_actuelle))
        c = [self.__coldec_to_colbin(col) for col in c]
        c = [[c[0:4], 0], [c[0:5], 1], [c[0:6], 2], [c[0:7], 3], [c[1:7], 3], [c[2:7], 3], [c[3:7], 3]]

        eX = self.__X_eval(c)
        eO = self.__O_eval(c)

        e = eX - eO

        return e

    # Appelle le l'algo du min max et retourne la colonne au meilleure score
    def choix_colonne(self, grille_actuelle, ordre_jeu): 

        # ordre_jeu permet de savoir si l'ia doit maximer ou minimiser son score
        # Elle minimise lorsqu'elle joue en premiere et maximise dans le cas inverse
        colonne_joue = self.__minimax(grille_actuelle, self.__lvl_ia, ordre_jeu == 0)[0]

        return colonne_joue

    # Algo du Min/Max
    def __minimax(self, grille, profondeur, joueur_maximise):

        # Retourne le score de la grille lorsqu'on arrive à une feuille de l'arbre
        if profondeur == 0 :
            return (None, self.__fonction_evaluation(grille.get_hashcode()))

        if joueur_maximise: # MAX
            meilleur_score = -100000000 # valeur de base permettant de maximiser
            colonne = 0 # colonne par défaut
            for i in range(7):
                grille_calcul = copy.deepcopy(grille) 
                grille_calcul.play_column(i) # Simulation du coup à jouer
                nouveau_score = self.__minimax(grille_calcul, profondeur - 1, False)[1]
                if nouveau_score > meilleur_score:
                    meilleur_score = nouveau_score
                    colonne = i
            return colonne, meilleur_score

        else:  # MIN
            meilleur_score = 100000000 # valeur de base permettant de maximiser
            colonne = 0 # colonne par défaut
            for i in range(7):
                grille_calcul = copy.deepcopy(grille)
                grille_calcul.play_column(i) # Simulation du coup à jouer
                nouveau_score = self.__minimax(grille_calcul, profondeur - 1, True)[1]
                if nouveau_score < meilleur_score:
                    meilleur_score = nouveau_score
                    colonne = i
            return colonne, meilleur_score

## TESTS 

# grille_test = Grid()
# grille_test.play_column(3)
# grille_test.play_column(3)
# grille_test.play_column(2)
# grille_test.play_column(3)
# grille_test.play_column(1)
# grille_test.play_column(0)

# print(choix_colonne(grille_test,0))