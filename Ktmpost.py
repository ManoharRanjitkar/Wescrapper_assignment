import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://kathmandupost.com/"

home_response = requests.get(BASE_URL)
home_soup = BeautifulSoup(home_response.text, "html.parser")

trending_ul = home_soup.find("ul", class_="trending-topics-list")
trending_items = trending_ul.find_all("li")

article_paths = []
for item in trending_items:
    link = item.find("a")
    if link:
        article_paths.append(link["href"])

article_urls = []
for path in article_paths:
    article_urls.append(BASE_URL + path)

file_name = "Kathmandupost_articles.txt"

with open(file_name, "w", encoding="utf-8") as f:
    for url in article_urls:
        article_response = requests.get(url)
        article_soup = BeautifulSoup(article_response.text, "html.parser")

        tag_section = article_soup.find("h4", class_="title--line__red")
        tag = tag_section.find("a").get_text(
            strip=True) if tag_section else None

        title = tag_section.find_next("h1").get_text(strip=True)

        f.write("Title: " + title + "\n")
        f.write("Tag: " + str(tag) + "\n")
        f.write("URL: " + url + "\n")
        f.write("Scraped At: " + datetime.now().isoformat() + "\n")
        f.write("\n" + "." * 80 + "\n\n")

print("Data saved to", file_name)
