from uuid import uuid4


class Product:

    def __init__(self, name, ptype, price, comments, stock):
        self.__product_id = str(uuid4())[:8]
        self.__name = name
        self.__ptype = ptype
        self.__price = price
        self.__comments = comments
        self.__stock = stock
        self.__sold = 0
        self.__status = 'Available'
        self.__user = {}

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_ptype(self):
        return self.__ptype

    def get_price(self):
        return self.__price

    def get_comments(self):
        return self.__comments

    def get_status(self):
        return self.__status

    def get_stock(self):
        return self.__stock

    def get_sold(self):
        return self.__sold

    def add_user(self, key, value):
        self.user[key] = value

    def get_user(self):
        return self.user

    def set_sold(self, sold):
        self.__sold = sold

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_name(self, name):
        self.__name = name

    def set_ptype(self, ptype):
        self.__ptype = ptype

    def set_price(self, price):
        self.__price = price

    def set_comments(self, comments):
        self.__comments = comments

    def set_stock(self, stock):
        self.__stock = stock

    def set_status(self, status):
        self.__status = status

    def add_user(self, key, value):
        self.__user[key] = value

    def get_user(self):
        return self.__user


    # def set_status(self, status):
    #     if
    #         self.__status = 'Unavailable'

    def __str__(self):
        return ''