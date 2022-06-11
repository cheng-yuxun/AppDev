from uuid import uuid4

class Person:
    def __init__(self , username , password , birthdate ):
        self.__uuid = str(uuid4())[:4]
        self.__username = username
        self.__email = None
        self.__password = password
        self.__birthdate = birthdate
        self.__image = 'profile.png'


    def get_uuid(self):
        return self.__uuid

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_birthdate(self):
        return self.__birthdate

    def get_image(self):
        return self.__image


    def set_username(self , username):
        self.__username = username

    def set_email(self , email):
        self.__email = email

    def set_password(self , password):
        self.__password = password

    def set_birthdate(self , birthdate):
        self.__birthdate = birthdate

    def set_image(self, image):
        self.__image = image






class User(Person):
    def __init__(self, username , password , birthdate):
        super().__init__(username , password , birthdate )

        self.__friends = []
        self.__friendrequest = []
        self.__phonenumber = None
        self.__AboutMe = None
        self.__cc = self.creditcard()
        self.__status = 'Active'
        self.cart = {}
        self.productcart = {}
        self.history = []

    def addHistory(self,value):
        self.history.append(value)

    def gethistory(self):
        return self.history

    def addcart(self, key, value):
        self.cart[key] = value

    def getcart(self):
        return self.cart

    def addproductcart(self, a, b, c):
        self.productcart[a] = [b, c]

    def getproductcart(self):
        return self.productcart

    def get_phonenumber(self):
        return self.__phonenumber

    def get_friends(self):
        return self.__friends

    def get_friendrequest(self):
        return self.__friendrequest

    def get_AboutMe(self):
        return self.__AboutMe

    def get_creditcard(self):
        return self.__cc

    def get_status(self):
        return self.__status





    def set_phonenumber(self , phonenumber):
        self.__phonenumber = phonenumber


    def set_friends(self , friend):
        self.__friends.append(friend)

    def remove_friends(self , friend):
        self.__friends.remove(friend)

    def set_friendrequest(self , request):
        self.__friendrequest.append(request)

    def remove_friendrequest(self , request):
        self.__friendrequest.remove(request)


    def set_AboutMe(self , AboutMe):
        self.__AboutMe = AboutMe


    def set_status(self , status):
        self.__status = status

    class creditcard():
        def __init__(self):
            self.__card = None
            self.__cardno = None
            self.__expirationdate = None
            self.__ccv = None

        def set_card(self , card):
            self.__card = card

        def set_cardno(self , cardno):
            self.__cardno = cardno

        def set_expirationdate(self , expirationdate):
            self.__expirationdate = expirationdate

        def set_ccv(self , ccv):
            self.__ccv = ccv


        def get_card(self):
            return self.__card


        def get_cardno(self):
            return self.__cardno

        def reset(self):
            dict = vars(self)
            for i in dict:
                dict[i] = None





class Admin(Person):
    def __init__(self,username,password,birthdate):
        super().__init__(username , password , birthdate)
