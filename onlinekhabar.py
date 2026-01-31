import requests
from bs4 import BeautifulSoup
from datetime import datetime

RSS_URL = "https://onlinekhabar.com/rss"   # replace with the site’s RSS feed

response = requests.get(RSS_URL)
soup = BeautifulSoup(response.content, "xml")

items = soup.find_all("item")

file_name = "Onlinekhabar_articles.txt"

with open(file_name, "w", encoding="utf-8") as f:
    for item in items[:5]:   # limit to 5 articles
        title = item.title.get_text(strip=True)
        link = item.link.get_text(strip=True)
        pub_date = item.pubDate.get_text(strip=True)

        f.write("Title: " + title + "\n")
        f.write("URL: " + link + "\n")
        f.write("Published: " + pub_date + "\n")
        f.write("Scraped At: " + datetime.now().isoformat() + "\n")
        f.write("\n" + "." * 80 + "\n\n")

print("Data saved to", file_name)
