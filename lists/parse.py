import json
import requests
from bs4 import BeautifulSoup

f = open("test.json")
ip = json.load(f)
f.close()

URL = "https://networksdb.io/ip-addresses-of/hetzner-online-gmbh"
outputfile = "hetzner.txt"

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("div", class_="col-md-5 col-sm-5")

a = open(outputfile, "w")
for element in results:
    a.write(element.text.split("\n")[1][6:].strip() + "\n")

a.close()