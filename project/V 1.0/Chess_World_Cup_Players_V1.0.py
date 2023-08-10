import sqlite3
from re import search
from requests import get
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Chess_World_Cup_2023"
request = get(url) # from requests library

page_soup = BeautifulSoup(request.text, "html.parser") # from bs4 library
body_soup = BeautifulSoup(str(page_soup.find("body")), "html.parser")
dds_soup = body_soup.find_all("dd")

connection = sqlite3.connect("Chess_World_Cup_2023.db")

connection.execute("DROP TABLE IF EXISTS Participants;")
connection.commit()

connection.execute("""CREATE TABLE Participants(
    Name        TEXT,
    Country     TEXT,
    Rating      INTEGER
);""")
connection.commit()

for _ in dds_soup:
    _ = search(r".+?\s{4}(.+?)\s\((.+?)\).+?(\d+)", _.text) # from re library
    connection.execute(f"""INSERT INTO Participants VALUES(
        '{_.group(1)}',
        '{_.group(2)}',
        '{int(_.group(3))}'
    );""")
    connection.commit()

connection.close()
