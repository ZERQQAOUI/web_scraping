import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

data = []
url = "https://pokemondb.net/pokedex/all"

# Send a request to the website
page = requests.get(url)

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(page.content, "html.parser")

table = soup.find("table", class_="data-table")
rows = table.tbody.find_all("tr")

if not os.path.exists("images"):
    os.makedirs("images")

# Loop through each row and extract the data
for row in rows:

    # Extract the Pokemon ID
    id_col = row.td.find("span", class_="infocard-cell-data")
    # Extract the Pokemon name
    name_col = row.find("a", class_="ent-name")
    
    id = id_col.text.strip()
    name = name_col.text.strip()
    data.append(f"ID: {id}, Name: {name}")
     # Extract the image URL
    img_url = row.find("img")["src"]
    
    # Download the image
    response = requests.get(img_url)
    with open(f"images/{id}_{name}.jpg", "wb") as f:
        f.write(response.content)
    
    # Print the Pokemon data
    print(f"ID: {id}, Name: {name}, Img_URL: {img_url}")
df = pd.DataFrame(data, columns=['name&ID'])
df.to_csv('donnees.csv', index=False)
