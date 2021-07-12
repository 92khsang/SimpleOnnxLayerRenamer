class Splitter():
    def __init__(self, argd : dict):
        if not isinstance(argd, dict):
            raise TypeError("Invalid Input arguments")
        
        self.__argd = argd

    def split(self) -> dict:
        if self.__argd is None:
            return {}

        splited_items = {}
        splited_items['file'] = self.__argd['file']
        splited_items['target'] = self.__split_str(self.__argd['target'])
        splited_items['dest'] = self.__split_str(self.__argd['dest'])
        return splited_items

    def __split_str(self, src : str) -> list:
        if not isinstance(src, str):
            raise TypeError("Invalid Input arguments")
        
        if len(src) == 0:
            return []

        src_without_space = src.replace(" ", "")
        return src_without_space.split(',')