#Interface to the persistent database: should store offers: offers basic store/and search functionality and converts from/to internal offer class
from tinydb import TinyDB, Query

#storage path
db = TinyDB('db.json')

#class for internal offer: acts as information carrier that can be passed around, should contain all information related to a given offer
class Offer:
    def __init__(self, plattform ,address, price, size,rooms, url):
        #Offer information
        self.address = address #location of the flat
        self.price =  price #cost, should be Kaltmiete
        self.size = size #size in m^2
        self.rooms =rooms

        #for contacting
        self.url = url #url of the offer page
        self.plattform = plattform #where the offer is listed

        #for internal use
        self.contacted = False

    def asdict(self):
        return {'address': self.address, 'price': self.price, 'size': self.size, "url":self.url, "plattform":self.plattform, "contacted":self.contacted}


#insert list of offers
def insert(new:[Offer]):
    for offer in new:
        db.insert(offer.asdict())


def print_all():
    print(db.all())