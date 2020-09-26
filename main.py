from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4 as bs
import csv

csv_header = ['Nama Produk','Harga']

class tokped_scraper():
    def __init__(self, keyword, PATH, filtered_words=[]):
        self.PATH = PATH # Path to chromedriver.exe
        self.driver = webdriver.Chrome(PATH)
        self.keyword = keyword
        self.pagesource = ""
        self.filtered_words = filtered_words
    
    def search(self):
        self.driver.get("https://www.tokopedia.com/search?&q={}".format(self.keyword))
        self.pagesource = self.driver.page_source

    def scrape(self):
        soup = bs.BeautifulSoup(self.pagesource, "html.parser")

        for i in soup.find_all("div", class_="css-1bd8ct"):
            nama_produk = i.find_all("div", class_="css-18c4yhp")[0].get_text()
            harga = i.find_all("div", class_="css-rhd610")[0].get_text().replace('Rp', '').replace('.', '')
            
            # Filtering out the words from list filtered_words
            for i in self.filtered_words:
                if i in nama_produk:
                    print("{} is in \"{}\"".format(i,nama_produk))
                    continue

            with open("data.csv","a") as data_file:
                writer = csv.DictWriter(data_file, fieldnames=csv_header)
                writer.writerow({
                    'Nama Produk': nama_produk,
                    'Harga': harga
                    })

# Contoh / Example
cari_switch = tokped_scraper(
    "rtx 3090", 
    "C:\\Program Files (x86)\\chromedriver.exe",
    ['2060','2070','GTX','2080'])
cari_switch.search()
cari_switch.scrape()
