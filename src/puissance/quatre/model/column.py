from cell import Cell

class Column:
    
    __HEIGHT:int = 6
    
    __column:list[Cell]
    __next_cell:int
    __hashcode:str
    
    def __init__(self, hashcode = '000'):
        if hashcode != '000': self.generate_new_column_by_hashcode(hashcode)
        else: self.__generate_column()
        
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
    
    def get_next_cell(self) -> int:
        return self.__next_cell
    
    def get_cell(self, index:int) -> Cell:
        return self.__column[index]
    
    def get_hashcode(self) -> str:
        return self.__hashcode
    
    def generate_new_column_by_hashcode(self, hashcode:str) -> bool:
        read_hashcode:int = int(hashcode)
        prefix_key:int = read_hashcode // 10
        suffix_key:int = read_hashcode % 10
        column_prefix_bin:list[Cell] = self.__dec_to_colbin(prefix_key)
        while len(column_prefix_bin) != suffix_key: column_prefix_bin.append(Cell(0))
        while len(column_prefix_bin) != self.__HEIGHT: column_prefix_bin.append(Cell())
        self.__column = column_prefix_bin
        self.__next_cell = suffix_key
        self.__generate_hashcode()
    
    def __colbin_to_coldec(self, clear_column:list[Cell]) -> int:
        bin_key:bin = ''.join(map(str, clear_column))
        dec_key:int = int(bin_key, 2)
        return dec_key
    
    def __dec_to_colbin(self, prefix:int) -> list[Cell]:
        prefix_bin:bin = bin(prefix)
        column_prefix_bin:list[Cell] = [Cell(int(x)) for x in prefix_bin[2:]]
        column_prefix_bin.reverse()
        return column_prefix_bin
