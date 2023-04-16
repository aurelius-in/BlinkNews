import csv
import requests
from bs4 import BeautifulSoup

# define the news categories and dates to search for
categories = [
    'Political news', 'Sports news', 'Tech news', 'Software Development News', 'Elon Musk News', 'AI news', 
    'Gay news', 'Trump News', 'Gossip news', 'Health news', 'Science news', 'Entertainment news', 
    'Environmental news', 'Business news', 'Education news', 'Travel news', 'Fashion news', 'Food news', 
    'Cultural news', 'Lifestyle news', 'Crime news', 'Weather news', 'Religion news', 'International news'
]
date = '2023-04-16'  # replace with the date you want to search for

# set up a CSV file to write the scraped data to
with open('articles.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Category', 'Title', 'URL', 'Text'])

    # loop over the categories and scrape three articles for each one
    for category in categories:
        print(f"Scraping {category} articles...")
        url = f"https://www.google.com/search?q={category}&tbm=nws&lr=lang_en&hl=en&tbs=sbd:{date}&num=3"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', {'class': 'ZINbbc'})

        # loop over the scraped articles and extract the data we want to save
        for article in articles:
            try:
                title = article.find('div', {'class': 'BNeawe vvjwJb AP7Wnd'}).get_text()
                url = article.find('a')['href']
                text = article.find('div', {'class': 'BNeawe s3v9rd AP7Wnd'}).get_text()
                writer.writerow([category, title, url, text])
            except Exception as e:
                print(f"Error scraping article: {str(e)}")
                
print("Scraping complete!")
