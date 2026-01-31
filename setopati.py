import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

BASE_URL = 'https://en.setopati.com/'

response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'html.parser')

breaking_news = soup.find('section', class_='jeg_post_title')
breaking_articles = []
if breaking_news:
    main = breaking_news.find('a')
    if main and main.get('href'):
        breaking_articles.append(main)
    more = soup.find('section', class_='more-breaking-news')
    if more:
        breaking_articles.extend(more.find_all('a'))

special_section = soup.find('section', class_='samachar-section')
special_articles = []
if special_section:
    special_articles.extend(special_section.find_all('a', href=True))

all_articles = breaking_articles + special_articles
trending_urls = []

for a in all_articles[:15]:
    href = a.get('href')
    if href and 'javascript' not in href and '#' not in href and 'category' not in href and 'author' not in href:
        if href.startswith('/'):
            href = BASE_URL.rstrip('/') + href
        elif 'http' not in href:
            href = BASE_URL + href
        if 'setopati.com' in href and '/view/' not in href and href not in trending_urls:
            trending_urls.append(href)

trending_urls = trending_urls[:10]

articles_data = []
for url in trending_urls:
    resp = requests.get(url)
    art_soup = BeautifulSoup(resp.text, 'html.parser')

    title_tag = art_soup.find('h1') or art_soup.find(
        'h2') or art_soup.find('div', class_='main-title')
    title = title_tag.get_text(strip=True) if title_tag else "Title not found"

    content_div = art_soup.find('article') or art_soup.find(
        'div', class_='post-content') or art_soup.find('div', class_='article-content')
    content = ""
    if content_div:
        paragraphs = content_div.find_all('p')
        content = "\n".join(p.get_text(strip=True) for p in paragraphs)
    else:
        main_content = art_soup.find('div', id='content')
        if main_content:
            paragraphs = main_content.find_all('p')
            content = "\n".join(p.get_text(strip=True)
                                for p in paragraphs[:10])

    if len(content) > 500:
        content = content[:500] + "..."

    articles_data.append({
        'title': title,
        'content': content,
        'url': url,
        'scraped_at': datetime.now().isoformat()
    })

filename = "setopati.txt"
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(articles_data, f, indent=4, ensure_ascii=False)

print(f"Saved {len(articles_data)} articles to {filename}")
