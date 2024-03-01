class Cell:

    __DEFAULT_VALUE:int = -1
    
    __value:int

    def __init__(self, value = __DEFAULT_VALUE) -> None: 
        self.__value = value

    def set_value(self, value:int):
        if value == 0 or value == 1 : self.__value = value
        else: raise ValueError("Cell")

    def get_value(self) -> int:
        return self.__value
    
    def is_free(self) -> bool:
        return self.__value == self.__DEFAULT_VALUE
    
    def __to_string(self) -> str:
        return "X" if self.__value == 0 else "O" if self.__value == 1 else " "

    def __str__(self) -> str:
        return self.__to_string()