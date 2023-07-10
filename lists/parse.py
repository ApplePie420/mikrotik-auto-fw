import os
import requests
from bs4 import BeautifulSoup

debug_on = False

# This is the URL of company we want to parse
URL = "https://networksdb.io/ip-addresses-of/hetzner-online-gmbh"
# Get company name from the URL so we don't need to change it manually every time
outputfile = URL.split("/")[-1] + ".txt"

print("Fetching the website")

# fetch the page and find appropriate HTML elements containing our data
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("div", class_="col-md-5 col-sm-5")

print("Writing {} ranges into the file".format(len(results)))

# write the data to the file
a = open(os.path.join("./cidr/", outputfile), "w")
for element in results:
    # this is because the HTML element contains multiple data, so we need to split it
    a.write(element.text.split("\n")[1][6:].strip() + "\n")

# close the file
a.close()

print("Scraping of IPs done")

# append this company to the readme.md file
# could use a bit of rework, for example checking if it doesn't already exist, but meh fuck it. For debugging, change the debug_on flag
# to true so it actually writes to the file, since while in development, there'll be like a thousand test lines

print("Appending to readme")

readme = open("./README.md", "a")
# set some variables so "templating" is easier
# for now, these are set to be the same, in the future...
# TODO: get company name from the bs4 output
filename = outputfile
company_name = filename
linecount = len(results)
desc = "---TBA manually---"
# here is our template that we fill in with variables from above
template = "| {company_name} | `{filename}` | {linecount} | {desc} |\n".format(company_name=company_name, filename=filename, linecount=linecount, desc=desc)
# write and close the file
readme.write(template)
readme.close()

print("That is all, thank you")