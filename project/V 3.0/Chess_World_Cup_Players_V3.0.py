# import libraries
import re
import sqlite3
import requests
from bs4 import BeautifulSoup


# First Step: Make a request to Wikipedia
while True:
    try:
        url = "https://en.wikipedia.org/wiki/Chess_World_Cup_2023"
        request = requests.get(url)
        break
    
    except request.exceptions.ConnectionError:
        print("This is you connection problem. Ckeck it and press Enter to try again")
        uresponse = input("Type 'exit' if you want to exit the programm: ")
        if uresponse.lower() == "exit":
            exit()
    
    except Exception as error:
        print(f"Something went wrong:{error}\nYou can report it: mohammadsijani.contact@gmail.com")
        exit()


# Second Step: Scrape data and store them in a list
page_soup = BeautifulSoup(request.text, "html.parser")
body_soup = BeautifulSoup(str(page_soup.find("body")), "html.parser")
dds_soup = body_soup.find_all("dd")

participants = list()
for dd in dds_soup:
    dd = re.search(r".+?\s{4}(.+?)\s\((.+?)\).+?(\d+)", dd.text)
    participants.append([dd.group(1), dd.group(2), int(dd.group(3))])


# Third Step: Store data in a ".db" file
print("Data was collected! Press Enter to store them...")

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


# Fourth Step: Print data for user

print("Data was stored in Chess_World_Cup_2023.db!\n Hope you enjoyed my programm")