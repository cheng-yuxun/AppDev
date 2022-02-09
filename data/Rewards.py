from data.Parent import *
from uuid import uuid4
class Rewards(Parent):

    def __init__(self,name,points,category,redemption,code,date_start,date_expire,description,picture):
        super().__init__(name,date_start,date_expire)
        self.__uuid = str(uuid4())[:4]
        self.__points = points
        self.__category = category
        self.__redemption = redemption
        self.__code = code
        self.__status = "Available"
        self.__description = description
        self.__picture = picture

    def set_picture(self,picture):
        self.__picture = picture

    def set_description(self,description):
        self.__description = description

    def set_points(self,points):
        self.__points = points

    def set_category(self,category):
        self.__category = category

    def set_redemption(self,redemption):
        self.__redemption = redemption

    def set_code(self,code):
        self.__code = code

    def set_status(self, status):
        self.__status = status

    def get_picture(self):
        return self.__picture

    def get_points(self):
        return self.__points

    def get_description(self):
        return self.__description

    def get_category(self):
        return self.__category

    def get_redemption(self):
        return self.__redemption

    def get_code(self):
        return self.__code

    def get_uuid(self):
        return self.__uuid

    def get_status(self):
        return self.__status

class History:
    def __init__(self,description, expiryDate):
        self.__description = description
        self.__expiryDate = expiryDate

    def set_description(self,description):
        self.__description  = description

    def get_description(self):
        return  self.__description

    def set_expiryDate(self,expiryDate):
        self.__expiryDate = expiryDate

    def get_expiryDate(self):
        return self.__expiryDate