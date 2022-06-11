from uuid import uuid4
from datetime import datetime, timedelta

class Events:

    def __init__(self, name, desc, date, start_time, end_time):
        self.__uuid = str(uuid4())[:8]
        self.name = name
        self.desc = desc
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.status = 'Active'
        self.sold = 0
        self.user = {}

    def set_name(self, name):
        self.name = name

    def set_desc(self, desc):
        self.desc = desc

    def set_date(self, date):
        self.date = date

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_end_time(self, end_time):
        self.end_time = end_time

    def set_status(self, status):
        self.status =  status

    def set_sold(self, sold):
        self.sold = sold

    def get_uuid(self):
        return self.__uuid

    def get_name(self):
        return self.name

    def get_desc(self):
        return self.desc

    def get_date(self):
        return self.date

    def get_start_time(self):
        return self.start_time

    def get_end_time(self):
        return self.end_time

    def get_sold(self):
        return self.sold

    def get_timer(self):
        d_list = str(self.date).rsplit('-')
        mth = {1:'January', 2:'February', 3:'March',
         4:'April', 5:'May', 6:'June',
         7:'July', 8:'August', 9:'September',
         10:'October', 11:'November', 12:'December'}
        if int(d_list[1]) != 10:
            d_mth = int(str(d_list[1]).replace('0', ''))
        else:
            d_mth = int(str(d_list[1]))
        return f'{mth[d_mth]} {d_list[2]}, {d_list[0]} {self.start_time}' # "January 1, 2022 00:00:00"

    def add_user(self, key, value):
        self.user[key] = value

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user

    def get_oneday(self):
        current_date = datetime.now()
        d_list = str(self.date).rsplit('-')
        et_list = str(self.end_time).rsplit(':')
        end = datetime(int(d_list[0]), int(d_list[1]), int(d_list[2]),
        int(et_list[0]), int(et_list[1]), int(et_list[2]))
        if (end - current_date).days <= 0:
            return True
        else:
            return False


class Onsite(Events):
    def __init__(
            self,
            name,
            desc,
            date,
            start_time,
            end_time,
            location,
            quantity,
            price):
        super().__init__(
            name,
            desc,
            date,
            start_time,
            end_time,)
        self.category = 'Onsite'
        self.location = location
        self.quantity = quantity
        self.price = price

    def set_category(self, category):
        self.category = category

    def set_location(self, location):
        self.location = location

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_price(self, price):
        self.price = price

    def get_category(self):
        return self.category

    def get_location(self):
        return self.location

    def get_quantity(self):
        return self.quantity

    def get_price(self):
        return self.price

    def get_remainder(self):
        remainder = self.quantity - self.get_sold()
        return remainder

    def get_status(self):
        if self.get_remainder() != 0:
            current_date =  datetime.now()
            d_list = str(self.date).rsplit('-')
            st_list = str(self.start_time).rsplit(':')
            et_list = str(self.end_time).rsplit(':')
            start = datetime(int(d_list[0]), int(d_list[1]), int(d_list[2]),
            int(st_list[0]), int(st_list[1]), int(st_list[2])) # d = datetime.datetime(0, 0, 0, 0, 0, 0) -> yyyy/mm/dd hh:mm:ss format 
            end = datetime(int(d_list[0]), int(d_list[1]), int(d_list[2]),
            int(et_list[0]), int(et_list[1]), int(et_list[2]))
            if start <= current_date <= end:
                self.status = 'Ongoing'
            elif current_date > end:
                self.status = 'Expired'
        else:
            self.status = 'Full'
        return self.status

    def get_address(self):
        if self.location == 'Decathlon SGLab':
            return '230 Stadium Blvd, Singapore 397799'
        else:
            return '750A Chai Chee Rd, #01-01 ESR BizPark @Chai Chee, Singapore 469001'

class Livestream(Events):
    def __init__(self, name, desc, date, start_time, end_time, link):
        super().__init__(name, desc, date, start_time, end_time)
        self.category = "Livestream"
        self.link = link

    def set_category(self, category):
        self.category = category

    def set_link(self, link):
        self.link = link

    def get_category(self):
        return self.category

    def get_link(self):
        return self.link

    def get_status(self):
        current_date =  datetime.now()
        d_list = str(self.date).rsplit('-')
        st_list = str(self.start_time).rsplit(':')
        et_list = str(self.end_time).rsplit(':')
        start = datetime(int(d_list[0]), int(d_list[1]), int(d_list[2]),
        int(st_list[0]), int(st_list[1]), int(st_list[2])) # d = datetime.datetime(0, 0, 0, 0, 0, 0) -> yyyy/mm/dd hh:mm:ss format 
        end = datetime(int(d_list[0]), int(d_list[1]), int(d_list[2]),
        int(et_list[0]), int(et_list[1]), int(et_list[2]))
        if start <= current_date <= end:
            self.status = 'Ongoing'
        elif current_date > end:
            self.status = 'Expired'
        return self.status