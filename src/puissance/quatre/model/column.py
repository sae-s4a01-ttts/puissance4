from cell import Cell

class Column:
    
    __HEIGHT:int = 6
    
    __column:list[Cell]
    __next_cell:int
    __hashcode:str
    
    def __init__(self):
        self.__generate_column()
        
    def __generate_column(self) -> bool:
        self.__column = [Cell() for x in range(0, self.__HEIGHT)]
        self.__generate_hashcode()
        self.__next_cell = 0
        return True
    
    def __generate_hashcode(self) -> bool:
        tmp_column:list[Cell] = [cell.get_value() for cell in self.__column]
        tmp_column.reverse()
        
        while -1 in tmp_column:
            tmp_column.remove(-1)
        
        prefix_key:int = self.__colbin_to_coldec(tmp_column) * 10 if len(tmp_column) > 0 else 0
        suffix_key:int = len(tmp_column)
        
        key:str = str(prefix_key + suffix_key).zfill(3)
        self.__hashcode = key
        
        return True
    
    def play_cell(self, player:int) -> bool:
        if not self.__can_play(): raise ValueError("")
        self.__column[self.__next_cell].set_value(player)
        self.__next_cell += 1
        self.__generate_hashcode()
        return True
        
    def __can_play(self) -> bool:
        return self.__next_cell < self.__HEIGHT
    
    def get_column(self) -> list[Cell]:
        return self.__column
    
    def get_cell(self, index:int) -> Cell:
        return self.__column[index]
    
    def get_hashcode(self) -> str:
        return self.__hashcode
    
    def __colbin_to_coldec(self, clear_column:list[Cell]) -> int:
        bin_key:bin = ''.join(map(str, clear_column))
        dec_key:int = int(bin_key, 2)
        return dec_key