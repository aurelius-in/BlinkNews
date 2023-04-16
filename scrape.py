import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

# list of news categories
categories = ['Political news', 'Sports news', 'Tech news', 'Software Development News', 
              'Elon Musk News', 'AI news', 'Gay news', 'Trump News', 'Gossip news', 'Health news', 
              'Science news', 'Entertainment news', 'Environmental news', 'Business news', 
              'Education news', 'Travel news', 'Fashion news', 'Food news', 'Cultural news', 
              'Lifestyle news', 'Crime news', 'Weather news', 'Religion news', 'International news']

# specify the date
year = 2023
month = 4
day = 16

# convert the date to a datetime object
date = datetime(year, month, day)

# specify the number of articles to scrape per category
articles_per_category = 3

# create a SQLite database and a table for storing the articles
conn = sqlite3.connect('news_articles.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS articles
             (category text, title text, content text, url text, date text)''')

# scrape the internet for articles in the specified categories
for category in categories:
    print(f"Scraping {category} articles...")
    article_count = 0
    page = 1
    
    while article_count < articles_per_category:
        # specify the URL to scrape
        url = f"https://www.example.com/{category}/{year}/{month}/{day}/page{page}/"
        
        # make a request to the URL and parse the HTML content
        try:
            response = requests.get(url, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}. Skipping...")
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # find all article links on the page
        links = soup.find_all('a', class_='article-link')
        
        for link in links:
            article_url = link['href']
            article_title = link.text.strip()
            
            # make a request to the article URL and parse the HTML content
            try:
                response = requests.get(article_url, timeout=5)
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}. Skipping...")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # find the article content on the page
            article_content = soup.find('div', class_='article-content')
            
            # check if the article date is on or after the specified date
            article_date = soup.find('div', class_='article-date')
            article_date = datetime.strptime(article_date.text.strip(), '%Y-%m-%d')
            if article_date < date:
                print(f"{article_title} is older than {date}. Skipping...")
                continue
            
            # insert the article into the database
            c.execute("INSERT INTO articles VALUES (?, ?, ?, ?, ?)", 
                      (category, article_title, article_content.text.strip(), article_url, article_date))
            
            article_count += 1
            
            if article_count >= articles_per_category:
                break
        
        page += 1
        
conn.commit()
conn.close()

print("Scraping complete.")
