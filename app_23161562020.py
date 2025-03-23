import requests
from bs4 import BeautifulSoup
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vazha"
)
cursor = db.cursor()
visited = set()

def dfs(url):
    if url in visited:
        print(f"Sudah dikunjungi: {url}")
        return
    print(f"Mengunjungi: {url}")
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
        paragraph = soup.find('p')
        content = paragraph.text if paragraph else "No Content"
        cursor.execute("INSERT INTO pages (url, title, content) VALUES (%s, %s, %s)", (url, title, content))
        db.commit()
        print(f"Disimpan: {url} | {title} | {content}")

        for link in soup.find_all('a', href=True):
            next_url = f"http://localhost/{link['href']}"
            print(f"Menemukan link: {next_url}") 
            dfs(next_url)

    except requests.exceptions.RequestException as e:
        print(f"Error mengambil {url}: {e}")

dfs("http://localhost/index.html")
cursor.close()
db.close()