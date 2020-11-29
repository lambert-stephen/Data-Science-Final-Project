import requests
from bs4 import BeautifulSoup
import csv
import time

db = []
base = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

for i in range(0, 181):
    print("Processing Page", i)
    number = str(i)
    page = requests.get(base + number, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all("table")

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            if not row.has_attr('class'):
                col = row.find('td', {"class": "clamp-summary-wrap"})
                data = []

                # Get title numbered
                data.append(col.find("span", {"class": "title numbered"}).text.strip())

                # Get title
                data.append(col.find("a", {"class": "title"}).find("h3").text.strip())

                # Get platform and release date
                div = col.find("div", {"class": "clamp-details"})
                spans = div.find_all("span")
                for idx, span in enumerate(spans):
                    if idx > 0:
                        data.append(span.text.strip())

                # Get metascore
                div2 = col.find("div", {"class": "clamp-metascore"})
                data.append(div2.find("div").text.strip())

                # Get userscore
                div3 = col.find("div", {"class": "clamp-userscore"})
                data.append(div3.find("div").text.strip())

                db.append(data)

    time.sleep(3)


print(db)

# with open ("videogame_data.csv", "a+") as my_csv:
#     csvWriter = csv.writer(my_csv, delimiter=',')
#     csvWriter.writerows(db)
