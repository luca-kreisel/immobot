from database import Offer
import database
import platforms
from time import sleep

def start():
    print("Starting ...")
    while True:
        new=platforms.get_all_new_offers()
        database.insert(new)
        database.print_all()
        sleep(90)