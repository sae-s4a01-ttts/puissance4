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
        return self.__set_grid(grid_with_columns)
    
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
    
    def get_hashcode(self) -> hex:
        return self.__hashcode
    
g = Grid()

g.play_column(1)
g.play_column(6)
g.play_column(3)

ghash = g.get_hashcode()
print(ghash)

print(sys.getsizeof(g))
print(sys.getsizeof(ghash))