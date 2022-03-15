from abc import ABC, abstractmethod
from controller import Offer
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class Platform(ABC):
    @abstractmethod
    def get_offers(self)->[Offer]:
        pass

    @abstractmethod
    def contact(self,o:Offer) -> bool:
        pass


class Degewo(Platform):
    def get_offers(self) -> [Offer]:
        URL = 'https://www.degewo.de/wohnen-service/immobiliensuche/'
        driver = webdriver.Chrome()
        driver.get(URL)
        time.sleep(2)
        offers=[]

        while True:
            #add offers on current page
            soup = BeautifulSoup(driver.page_source,features="html.parser")
            for offer_div in soup.select("article.article-list__item"):
                new= Offer(
                    plattform="Degewo",
                    address=offer_div.select_one(".article__meta").text.replace("|", ""),
                    price=float(offer_div.select_one(".price").text.split(" ")[0].replace(".", "").replace(',','.')),
                    rooms=int(offer_div.select(".article__properties-item")[0].text.split(" ")[0]),
                    size=float(offer_div.select(".article__properties-item")[1].text.split(" ")[0].replace(',','.')),
                    url="https://immosuche.degewo.de"+offer_div.select_one("a")['href']
                )
                offers.append(new)



            #Next page, if there is a "weiter" button
            if next_button := driver.find_elements_by_css_selector(".pager__next"):
                next_button=next_button[0]
                next_button.send_keys("\n")
            else:
                break

            time.sleep(3)


        return offers

    def contact(self, o: Offer) -> bool:
        return False


slaves = [Degewo]

def get_all_new_offers()->[Offer]:
    offers=[]
    for S in slaves:
        try:
            s=S()
            new=s.get_offers()
            offers.extend(new)
        except Exception as e:
            print("Error while getting new offers from ",S)
            print(e)
    return offers
