class Cell:

    __DEFAULT_VALUE:int = -1
    
    __value:int

    def __init__(self) -> None: 
        self.__value = self.__DEFAULT_VALUE

    def set_value(self, value:int):
        if value == 0 or value == 1 : self.__value = value
        else: raise ValueError("Cell")

    def get_value(self) -> int:
        return self.__value
    
    def is_ok(self) -> bool:
        return self.__value == self.__DEFAULT_VALUE
    
    def __to_string(self) -> str:
        match self.__value:
            case 0:
                return "X"
            case 1:
                return "O"
            case _:
                return " "

    def __str__(self) -> str:
        return self.__to_string()