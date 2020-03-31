from pathlib import Path
import requests
from bs4 import BeautifulSoup

URL = 'https://www.mohfw.gov.in/'
page = requests.get(URL)


soup = BeautifulSoup(page.content, 'html.parser')
results = soup.findAll("span", {"class": "icount"})

passenger = results[0].text
active = int(results[1].text)
cured = int(results[2].text)
death = int(results[3].text)
migrated = int(results[4].text)

total = active + cured + death + migrated
ason = soup.find("div", {"class": "information_block"}).findNext('p').contents[0].text


x = '{"passenger":"' + passenger + '", "active":' + str(active) + \
    ', "cured": ' + str(cured) + ', "death": ' + \
    str(death) + ', "migrated": ' + str(migrated) + ', "total": ' + str(total) + ', "ason": "' + ason + '"}'



print(total)
print(ason)
home = str(Path.home()) + "/corona.txt"

f = open(home, "w")
f.write(x)
f.close()