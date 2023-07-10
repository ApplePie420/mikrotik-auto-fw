import os
import requests
from bs4 import BeautifulSoup

URL = "https://networksdb.io/ip-addresses-of/hetzner-online-gmbh"
outputfile = URL.split("/")[-1] + ".txt"

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("div", class_="col-md-5 col-sm-5")

a = open(os.path.join("./cidr/", outputfile), "w")
for element in results:
    a.write(element.text.split("\n")[1][6:].strip() + "\n")

a.close()