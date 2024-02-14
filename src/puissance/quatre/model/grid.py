from column import Column
from cell import Cell

class Grid:

    __WIDTH:int  = 7
    
    __grid:list[Column]
    __next_player:int
    __hashcode:hex

    def __init__(self) -> None:
        self.__generate_grid()
        self.__next_player = 0

    def __generate_grid(self) -> bool:
        grid_with_columns = [Column() for x in range(0, self.__WIDTH)]
        self.__set_grid(grid_with_columns)
        self.__generate_hashcode()
        return True
    
    def __generate_hashcode(self) -> bool:
        all_column_hashcode:list = [col.get_hashcode() for col in self.__grid]
        columns_hashcode:str = ''.join(map(str, all_column_hashcode))
        dec_hashcode:int = int(columns_hashcode)
        hex_hashcode:hex = hex(dec_hashcode)
        
        self.__hashcode = hex_hashcode
        
        return True
    
    def maybe_its_win(self, last_column_played:int) -> bool:
        index_cell_played:int = self.__grid[last_column_played].get_next_cell() - 1
        last_cell_played:Cell = self.__grid[last_column_played].get_cell(index_cell_played)
        value_cell_played:int = last_cell_played.get_value()
        return self.__vertical_win(value_cell_played, last_column_played, index_cell_played) or \
               self.__horizontal_win(value_cell_played, last_column_played, index_cell_played) or \
               self.__positive_diagonal_win(value_cell_played, last_column_played, index_cell_played) or \
               self.__negative_diagonal_win(value_cell_played, last_column_played, index_cell_played)
    
    def __vertical_win(self, player:int, column:int, cell:int) -> bool:
        counter:int = 1
        for i in range(1,4):
            if cell-i >= 0:
                if self.__grid[column].get_cell(cell - i).get_value() == player: counter += 1
        return counter > 3
    
    def __horizontal_win(self, player:int, column:int, cell:int) -> bool:
        counter:int = 1
        left_side:bool = True
        right_side:bool = True
        index_column:int = 1
        while counter < 4 and (left_side or right_side):
            if left_side and column - index_column > -1:
                if self.__grid[column - index_column].get_cell(cell).get_value() == player: counter += 1
                else: left_side = False
            else: left_side = False
            if right_side and column + index_column < 7:
                if self.__grid[column + index_column].get_cell(cell).get_value() == player: counter += 1
                else: right_side = False
            else: right_side = False
            index_column += 1
        return counter > 3
    
    def __positive_diagonal_win(self, player:int, column:int, cell:int) -> bool:
        counter:int = 1
        left_side:bool = True
        right_side:bool = True
        index:int = 1
        while counter < 4 and (left_side or right_side):
            if (left_side and column - index > -1) and (cell - index > -1):
                if self.__grid[column - index].get_cell(cell - index).get_value() == player: counter += 1
                else: left_side = False
            else: left_side = False
            if (right_side and column + index < 7) and (cell + index < 6):
                if self.__grid[column + index].get_cell(cell + index).get_value() == player: counter += 1
                else: right_side = False
            else: right_side = False
            index += 1
        return counter > 3
    
    def __negative_diagonal_win(self, player:int, column:int, cell:int) -> bool:
        counter:int = 1
        left_side:bool = True
        right_side:bool = True
        index:int = 1
        while counter < 4 and (left_side or right_side):
            if (left_side and column - index > -1) and (cell + index < 6):
                if self.__grid[column - index].get_cell(cell + index).get_value() == player: counter += 1
                else: left_side = False
            else: left_side = False
            if (right_side and column + index < 7) and (cell - index > -1):
                if self.__grid[column + index].get_cell(cell - index).get_value() == player: counter += 1
                else: right_side = False
            else: right_side = False
            index += 1
        return counter > 3
    
    def play_column(self, index:int) -> bool:
        if not (index > -1 and index < 7): return False
        self.__grid[index].play_cell(self.__next_player)
        self.__next_player = (self.__next_player + 1) % 2
        self.__generate_hashcode()
        return self.maybe_its_win(index)
    
    def __set_grid(self, add_columns) -> bool:
        self.__grid = add_columns
        return True
    
    def get_grid(self) -> list[Column]:
        return self.__grid
    
    def __get_column(self, index:int) -> Column:
        return self.__grid[index]
    
    def get_hashcode(self) -> hex:
        return self.__hashcode
    
    def __str__(self) -> str:
        display_grid:str = ""
        row_in_grid:str = ""
        
        for i in range(0, 6):
            row_in_grid = "⎹ "
            for j in range(0, self.__WIDTH):
                row_in_grid += str(self.__get_column(j).get_cell(i)) + " ⎹ "
            display_grid = row_in_grid + "\n" +  display_grid
            
        display_grid += "  1   2   3   4   5   6   7"
        
        return display_grid