class Parent:
    def __init__(self,name,date_start,date_expire):
        self.__name = name
        self.__date_start = date_start
        self.__date_expire = date_expire
    def set_name(self,name):
        self.__name  = name

    def get_name(self):
        return self.__name

    def set_date_start(self,date_start):
        self.__date_start = date_start

    def set_date_expire(self,date_expire):
        self.__date_expire = date_expire

    def get_date_start(self):
        return self.__date_start

    def get_date_expire(self):
        return self.__date_expire
