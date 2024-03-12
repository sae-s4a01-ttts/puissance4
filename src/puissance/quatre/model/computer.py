# Importation de la librairie copy pour cloner un état de grille
import copy
from grid import Grid
from player import Player

class Computer(Player):
    """Classe qui crée un ordinateur pouvant jouer au puissance
    4 en ayant la connaissance de la grille. Elle hérite de 
    Player.
    """

    # Niveau de profondeur de l'ordinateur
    __level:int

    @staticmethod
    def parse_coldec(coldec:str) -> tuple:
        """Fonction qui permet à partir d'un hashcode d'une colone 
        de connaitre la présence des pions et leur emplacement et
        la hauteur de la colonne

        Args:
            coldec (str): hashcode décimal d'une colonne

        Returns:
            tuple: constitué du code décimal de la colonne et de sa hauteur
        """
        # Récupération du code décimal de la colonne
        prefix_coldec:int = int(coldec[:2])
        # Récupération de la hauteur de la colonne
        suffix_coldec:int = int(coldec[-1])

        return (prefix_coldec, suffix_coldec)

    @staticmethod
    def coldec_to_colbin(coldec:str) -> bin:
        """Fonction qui permet de traduire une colonne avec un
        hashcode décimal en une séquence binaire

        Args:
            coldec (str): hashcode décimal d'une colonne

        Returns:
            bin: séquence binaire de la colonne
        """
        # Découpage de la partie décimal et de la hauteur du
        # hashcode de la colonne
        (prefix_coldec, suffix_coldec) = Computer.parse_coldec(coldec)

        # Cas de colonne vide, alors on renvoie un code binaire
        # vide
        if (prefix_coldec, suffix_coldec) == (0, 0) : return ''

        # Codage en binaire de la colonne
        prefix_colbin:bin   = bin(prefix_coldec)[2:]
        # Longueur de la séquence binaire
        suffix_colbin:int   = len(prefix_colbin)
        
        # Différence entre la hauteur de la colonne et la 
        # taille de la séquence binaire pour combler le manque
        # de la hauteur avec des '0'
        zero_complement:int = suffix_coldec - suffix_colbin
        colbin:bin = zero_complement * '0' + prefix_colbin

        return colbin

    @staticmethod
    def colbin_to_coldec(colbin:bin) -> str:
        """Fonction qui permet de traduire une colonne avec une
        séquence binaire en un hashcode décimal

        Args:
            colbin (bin): séquence binaire représentant la colonne

        Returns:
            str: hashcode décimal de la colonne
        """
        # Traduction de la séquence binaire en un hashcode décimal
        coldec:str = str(int(colbin, 2)).zfill(2) + str(len(colbin)) if colbin != "" else "000"
        return coldec

    @staticmethod
    def binary_complement(colbin:bin) -> bin:
        """Fonction qui permet de faire le complément à un d'une
        séquence binaire

        Args:
            colbin (bin): séquence binaire d'une colonne

        Returns:
            bin: complément à un de la colonne renseignée
        """
        # Chaine contenant la séquence binaire complémentaire
        colbin_complement:bin = ''

        # Boucle sur la séquence binaire pour en traduire sa
        # complémentarité
        for bit in colbin:
            if bit == '0': colbin_complement += '1'
            elif bit == '1': colbin_complement += '0'

        return colbin_complement

    @staticmethod
    def consecutive_vertical_ones(colbin:bin) -> int:
        """Fonction qui permet de compter le nombre de 1 qui
        sont conséqutifs dans une colonne

        Args:
            colbin (bin): séquence binaire d'une colonne

        Returns:
            int: nombre de 1 qui sont consécutifs
        """
        # Conteur de la séquence de 1 consécutifs
        ones_sequence: int = 0

        # Boucle sur la séquence binaire tant que le pion
        # à une valeur de 1
        for bit in colbin:
            if bit == '1': ones_sequence += 1
            else: return ones_sequence

        return ones_sequence

    @staticmethod
    def eval_vertical_score(colsbin:list[bin], column:int) -> int:
        """Fonction qui permet de calculer le score d'une colonne d'une 
        manière vertical.
        La fonction renvoie un score en fonction des priorités suivantes : 
            - la séquence de 1 dans le code binaire ( le nombre de 1 qui 
            vont se suivre dans la colonne )
            - la hauteur de la colonne ( selon le nombre de cellule encore 
            vide dans la colonne )
        Si le dernier pion posé n'est pas égal à 1 alors le score sera de
        0.00, également dans le cas ou un puissance 4 n'est plus possible.
        Si une colonne est vide, la fonction renvoie naturellement un score
        de 4.00

        Args:
            colsbin (list[bin]): une liste de séquence binaire de colonne
            column (int): colonne dont on veut connaitre le score

        Returns:
            int: score attribué à la colonne 
        """

        # Score en hauteur d'une colonne
        height_score:int
        # Score d'un enchainement d'un même pion
        sequence_score:int
        # Score final en ajoutant $height_score avec $sequence_score
        calculated_score:int

        # Colonne dont on veut calculer le score en bianire
        active_colbin:str = colsbin[column]

        # Permet de lire le hashcode de la colonne active et d'en tirer
        # sa valeur et sa hauteur
        (prefix_coldec , suffix_coldec) = Computer.parse_coldec(Computer.colbin_to_coldec(active_colbin))

        # Permet de connaitre le nombre de pion d'une même valeur qui se suivent
        ones_sequence:int = Computer.consecutive_vertical_ones(active_colbin)

        # Calcul du score de la hauteur de la colonne avec un score max
        # de 18.00. Plus la colonne est pleine plus le score diminue
        height_score = 18.00 - suffix_coldec ** 1.70
        
        # Si le dernier pion posé de la colonne n'est pas un 1 alors
        # le score de la hauteur est nativement à 0.00
        height_score = 0.00 if ( prefix_coldec < 2.00 ** (suffix_coldec - 1.00)) or \
                            ( suffix_coldec > 2.00 and suffix_coldec - 2.00 > ones_sequence ) \
                            else height_score
        
        # Dans le cas ou une colonne est vide alors le score est 
        # naturellement de 4.00
        height_score += 4.00 if suffix_coldec < 1.00 else 0.00 

        # Dans le cas ou il n'y existe pas de séquence de 1 sur le 
        # sommet de la colonne alors le score est de 0.00
        sequence_score = 0.00 if height_score < 1.00 \
                            else 4.00 ** ( ones_sequence + 1.00 )

        # Calcul du score en ajoutant les scores de hauteurs et de 
        # séquence de 1
        calculated_score = height_score + sequence_score

        return calculated_score

    @staticmethod
    def eval_horizontal_score(colsbin:list[bin], column:int) -> int:
        """Fonction qui permet de calculer le score d'une colonne d'une 
        manière horizontal.
        La fonction renvoie un score en fonction des priorités suivantes : 
            - la séquence de 1 dans le code binaire ( le nombre de 1 qui 
            vont se suivre sur une ligne )
            - la range d'action d'une colonne ( direction d'action sur les
            colonnes adjacentes pour faire un puissance 4 )
            - le nombre de trous étant extérieurs à la séquence de 1
        Si il n'y a plus de possibilité de faire un puissance 4 sur la 
        ligne, la fonction renvoie naturellement un score de 0.00.

        Args:
            colsbin (list[bin]): une liste de séquence binaire de colonne
            column (int): colonne dont on veut connaitre le score

        Returns:
            int: score attribué à la colonne 
        """

        # Score en dimension de range d'une colonne ( champs d'action 
        # de la colonne )
        width_score:int
        # Score d'un enchainement d'un même pion
        sequence_score:int
        # Score final en ajoutant $height_score avec $sequence_score
        calculated_score:int

        # Champs d'action de la colonne dont on veut connaitre le 
        # score
        range_column:int = len(colsbin)
        # Hauteur de la colonne dont on veut connaitre le score
        height_column:int = len(colsbin[column])

        # Compteur de 1 étant dans les colonnes qui précèdent
        # la colonne dont on veut connaitre le score
        prev_counter_ones:int = 0
        # Compteur de 1 étant dans les colonnes qui succèdent
        # la colonne dont on veut connaitre le score
        next_counter_ones:int = 0
        # Compteur du nombre de trous étant sur la ligne à évaluer
        counter_holes:int = 1
        # False si on a pas encore rencontré de tous sur les colonnes
        # qui précèdent la colonne dont on veut connaitre le score
        # True sinon
        prev_hole:bool = False
        # False si on a pas encore rencontré de tous sur les colonnes
        # qui succèdent la colonne dont on veut connaitre le score
        # True sinon
        next_hole:bool = False

        # Séquence de 1 sur une ligne
        ones_sequence:int = 0

        # Analyse des colonnes qui précèdent la colonne active
        for col in range(column - 1, -1, -1):
            # Colonne qu'on va analyser remit à l'endroit
            colbin_tmp = colsbin[col][::-1]
            # Hauteur de la colonne qu'on va analyser
            height_colbin_tmp = len(colbin_tmp)
            # Dans le cas ou la colonne est assez grande pour 
            # être testée, sinon on ajoute un trous et on
            # précise que l'on a déjà rencontré un trous
            if height_column < height_colbin_tmp:
                if colbin_tmp[height_column] == '1':
                    # Si sur la colonne analysée et sur la ligne
                    # on a un 1, alors on ajoute au nombre de 1
                    # rencontré dans les colonnes précédentes
                    prev_counter_ones += 1
                    # Dans le cas ou l'on est tombé sur un trous
                    # précedemment alors on n'ajoute pas +1
                    # au compteur de 1 consécutif
                    ones_sequence += 1 if not prev_hole else 0
                # Sinon on casse la bouble 
                else:
                    break
            else:
                prev_hole = True
                counter_holes += 1

        # Analyse des colonnes qui succèdent la colonne active
        for col in range(column + 1, range_column):
            # Colonne qu'on va analyser remit à l'endroit
            colbin_tmp = colsbin[col][::-1]
            # Hauteur de la colonne qu'on va analyser
            height_colbin_tmp = len(colbin_tmp)
            # Dans le cas ou la colonne est assez grande pour 
            # être testée, sinon on ajoute un trous et on
            # précise que l'on a déjà rencontré un trous
            if height_column < height_colbin_tmp:
                # Si sur la colonne analysée et sur la ligne
                # on a un 1, alors on ajoute au nombre de 1
                # rencontré dans les colonnes succèssivent
                if colbin_tmp[height_column] == '1':
                    next_counter_ones += 1
                    # Dans le cas ou l'on est tombé sur un trous
                    # précedemment alors on n'ajoute pas +1
                    # au compteur de 1 consécutif
                    ones_sequence += 1 if not next_hole else 0
                # Sinon on casse la bouble 
                else:
                    break
            else:
                next_hole = True
                counter_holes += 1
            
        # Calcul du score du champs d'action de la colonne dont
        # on veut connaitre le score
        # Si l'on se trouve sur la colonne du centre alors le score
        # est de 18.5... , dans le cas ou l'on se trouve sur une 
        # colonne extrémiste alors le score est de 8.00
        width_score = range_column / (range_column ** 0.50) * range_column

        # Compteur global de 1 sur la ligne 
        counter_ones:int = prev_counter_ones + next_counter_ones

        # Compteur de 1 n'étant pas dans la séquence consécutive
        ones_unsequenced:int = ones_sequence - counter_ones

        # Calcul du score de la sequence en priorisant la 
        # séquence de 1 consécutifs, on ajoutant le nombre de 
        # 1 étant sur la ligne mais pas dans la séquence
        # et le nombre de trous sur la ligne coupant la séquence
        sequence_score = 4.00 ** (ones_sequence + 1.00) + 2.00 ** (ones_unsequenced + 1.00) + counter_holes * 2 

        # Calcul du score final si il y a une possibilité de 
        # puissance 4, sinon naturellement le score sera de 
        # 0.00
        calculated_score = width_score + sequence_score if counter_ones + counter_holes > 3 else 0.00

        return calculated_score

    @staticmethod
    def eval_positive_diagonal_score(colsbin:list[bin], column:int) -> int:
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

    @staticmethod
    def eval_negative_diagonal_score(colsbin:list[bin], column:int) -> int:
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

    @staticmethod
    def eval_victory(colsbin:list[bin]) -> int:
        def eval_vertical_victory(colsbin:list[bin]) -> int:
        
            victory = 0

            for col in colsbin:
                if len(col) > 3:
                    ones_sequence = 0
                    for cel in col:
                        if cel == '1': ones_sequence += 1
                        else: ones_sequence = 0
                        if ones_sequence > 3:
                            victory += 1
                            break

            return victory
        
        def eval_horizontal_victory(colsbin:list[bin]) -> int:

            victory = 0

            for line in range(0, len(colsbin)):
                ones_sequence = 0
                for col in colsbin:
                    col = col[::-1]
                    if line < len(col):
                        if col[line] == '1': ones_sequence += 1
                        else: ones_sequence = 0
                    else: ones_sequence = 0
                    if ones_sequence > 3:
                        victory += 1
                        break
            
            return victory
        
        def eval_positive_diagonal_victory(colsbin:list[bin]) -> int:

            victory = 0

            origin_height = 2
            origin_width  = 0

            range_sequence = [4, 5, 6, 6, 5, 4]
            irange = 0

            for dgl in range(0, 6):
                ones_sequence = 0
                colsbin_range = colsbin[origin_width : range_sequence[irange] + origin_width]
                
                next_height = origin_height
                for colbin in colsbin_range:
                    colbin = colbin[::-1]
                    if len(colbin) > next_height:
                        if colbin[next_height] == '1': ones_sequence += 1
                        else: ones_sequence = 0
                    else: ones_sequence = 0
                    if ones_sequence > 3:
                        victory += 1
                        break

                    next_height += 1

                origin_width  += 1 if origin_height < 1 else 0
                origin_height -= 1 if origin_height > 0 else 0
                irange += 1

            return victory
        
        def eval_negative_diagonal_victory(colsbin:list[bin]) -> int:

            victory = 0

            origin_height = 2
            origin_width  = 6

            range_sequence = [4, 5, 6, 6, 5, 4]
            irange = 0

            for dgl in range(5, -1, -1):
                ones_sequence = 0
                colsbin_range = colsbin[origin_width - range_sequence[irange] + 1 : origin_width + 1][::-1]
                
                next_height = origin_height
                for colbin in colsbin_range:
                    colbin = colbin[::-1]

                    if len(colbin) > next_height:


                        if colbin[next_height] == '1': ones_sequence += 1
                        else: ones_sequence = 0

                    else: ones_sequence = 0
                    if ones_sequence > 3:
                        victory += 1
                        break

                    next_height += 1

                origin_width  -= 1 if origin_height < 1 else 0
                origin_height -= 1 if origin_height > 0 else 0
                irange += 1

            return victory
                    
        global_victory:int = 0

        global_victory += eval_vertical_victory(colsbin)

        global_victory += eval_horizontal_victory(colsbin) 

        global_victory += eval_positive_diagonal_victory(colsbin) 

        global_victory += eval_negative_diagonal_victory(colsbin)

        return global_victory

    @staticmethod
    def eval_player_x(colsbin:list[bin]) -> int:
        cols_score:list[int] = [0] * 7
        gridbin:list[bin] = colsbin[3][0] 
        
        for col in range(0, len(colsbin)): 
            cols_score[col] += Computer.eval_vertical_score(colsbin[col][0], colsbin[col][1])
            cols_score[col] += Computer.eval_horizontal_score(colsbin[col][0], colsbin[col][1])
            cols_score[col] += Computer.eval_positive_diagonal_score(colsbin[col][0], colsbin[col][1])
            cols_score[col] += Computer.eval_negative_diagonal_score(colsbin[col][0], colsbin[col][1])

        score_x:int = sum(cols_score)

        score_x = 10000.00 * Computer.eval_victory(gridbin) + score_x

        return score_x

    @staticmethod
    def eval_player_o(colsbin:list[bin]) -> int:
        cols_score:list[int] = [0] * 7
        gridbin:list[bin] = []

        for col in range(0, len(colsbin)): 
            colbin_complement = [[Computer.binary_complement(col) for col in colsbin[col][0]], colsbin[col][1] ]
            gridbin = colbin_complement[0] if len(colbin_complement[0]) == 7 else gridbin
            cols_score[col] += Computer.eval_vertical_score(colbin_complement[0], colbin_complement[1])
            cols_score[col] += Computer.eval_horizontal_score(colbin_complement[0], colbin_complement[1])
            cols_score[col] += Computer.eval_positive_diagonal_score(colbin_complement[0], colbin_complement[1])
            cols_score[col] += Computer.eval_negative_diagonal_score(colbin_complement[0], colbin_complement[1])

        score_o:int = sum(cols_score)

        score_o = 10000.00 * Computer.eval_victory(gridbin) + score_o

        return score_o

    def __init__(self, name:str, level:int) -> None:
        super().__init__(name)
        self.__level = level

    def play_column(self, grid:Grid, play_order:int) -> int:
        
        column_played, value_column = \
            self.__min_max(grid, self.__level, play_order == 0)

        return column_played

    def __min_max(self, grid:Grid, depth:int, maximizing_player:bool) -> tuple:

        colsdec = grid.read_column_hashcode()
        colsbin = [Computer.coldec_to_colbin(coldec) for coldec in colsdec]
        
        possibles_wins = self.__terminal_eval(colsbin)
        win_condition = possibles_wins > 0

        if depth == 0 or win_condition:
            return (None, self.__evaluation(colsbin))

        if maximizing_player:
            value = float("-inf")
            column = 0
            for i in range(7):
                grid_calcul = copy.deepcopy(grid)
                if grid_calcul.can_play_column(i):
                    grid_calcul.play_column(i)
                    new_score = self.__min_max(grid_calcul, depth - 1, False)[1]
                    if new_score > value:
                        value = new_score
                        column = i
            return column, value

        else:
            value = float("inf")
            column = 0
            for i in range(7):
                grid_calcul = copy.deepcopy(grid)
                if grid_calcul.can_play_column(i):
                    grid_calcul.play_column(i)
                    new_score = self.__min_max(grid_calcul, depth - 1, True)[1]
                    if new_score < value:
                        value = new_score
                        column = i
            return column, value
        
    def __evaluation(self, colsbin:list[bin]) -> int:

        colsbin_range = [
            [colsbin[0:4], 0],
            [colsbin[0:5], 1],
            [colsbin[0:6], 2],
            [colsbin[0:7], 3],
            [colsbin[1:7], 3],
            [colsbin[2:7], 3],
            [colsbin[3:7], 3]
        ]

        eval_x_player:int = Computer.eval_player_x(colsbin_range)
        eval_o_player:int = Computer.eval_player_o(colsbin_range)

        eval_players:int = eval_x_player - eval_o_player

        return eval_players

    def __terminal_eval(self, colsbin:list[bin]) -> list[int]:

        x_colsbin = colsbin
        o_colsbin = [Computer.binary_complement(colbin) for colbin in colsbin]

        counter_win = Computer.eval_victory(x_colsbin) + Computer.eval_victory(o_colsbin)

        return counter_win