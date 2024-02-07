class Player:

    __name:str

    def __init__(self, name:str) -> None:
        self.set_name(name)
    
    def set_name(self, name:str) -> None:
        if self.__is_valid(name) : self.__name = name
        else: raise ValueError("")

    def get_name(self) -> str:
        """ @return player's name """
        return self.__name
    
    def __is_valid(self, name:str) -> bool:
        return name != None and name != ""