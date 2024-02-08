import sys

from column import Column

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
    
    def play_column(self, index:int) -> bool:
        if not (index > -1 and index < 7): return False
        self.__grid[index].play_cell(self.__next_player)
        self.__next_player = (self.__next_player + 1) % 2
        self.__generate_hashcode()
        return True
    
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