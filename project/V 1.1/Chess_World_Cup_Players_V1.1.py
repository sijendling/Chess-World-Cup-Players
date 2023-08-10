import sqlite3
from re import search
from requests import get
from bs4 import BeautifulSoup


url = "https://en.wikipedia.org/wiki/Chess_World_Cup_2023"
request = get(url) # from requests library

page_soup = BeautifulSoup(request.text, "html.parser") # from bs4 library
body_soup = BeautifulSoup(str(page_soup.find("body")), "html.parser")
dds_soup = body_soup.find_all("dd")

participants = list()
for dd in dds_soup:
    dd = search(r".+?\s{4}(.+?)\s\((.+?)\).+?(\d+)", dd.text) # from re library
    participants.append([dd.group(1), dd.group(2), int(dd.group(3))])

connection = sqlite3.connect("Chess_World_Cup_2023.db")

connection.execute("DROP TABLE IF EXISTS Participants;")
connection.commit()

connection.execute("""CREATE TABLE Participants(
    Name        TEXT,
    Country     TEXT,
    Rating      INTEGER
);""")
connection.commit()

for player in participants:
    connection.execute(f"""INSERT INTO Participants VALUES(
        '{player[0]}',
        '{player[1]}',
        '{player[2]}'
    );""") # palyer[0] => Player Name, player[1] => Player Country, player[2] => Player Rating 
    connection.commit()

connection.close()
