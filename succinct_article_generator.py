import random
import pandas as pd
import gensim.summarization

# Load the collected news data into a DataFrame
df = pd.read_csv('news_articles.csv')

# Group the articles by category and select up to 3 articles from each category
groups = df.groupby('category').apply(lambda x: x.sample(n=min(3, len(x)))).reset_index(drop=True)

# Shuffle the selected articles
groups = groups.sample(frac=1).reset_index(drop=True)

# Define the categories and the number of articles for each category
categories = ['Political news', 'Sports news', 'Tech news', 'Software Development News', 'Elon Musk News', 'AI news', 'Tech News', 'Gay news', 'Trump News', 'Gossip news', 'Health news', 'Science news', 'Entertainment news', 'Environmental news', 'Business news', 'Education news', 'Travel news', 'Fashion news', 'Food news', 'Cultural news', 'Lifestyle news', 'Crime news', 'Weather news', 'Religion news', 'International news']

num_articles = [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# Initialize the article list
articles = []

# Loop through the categories and select the specified number of articles for each category
for category, num in zip(categories, num_articles):
    # Select the articles for the current category
    category_articles = groups[groups['category'] == category].head(num)
    
    # Loop through the selected articles and add them to the article list
    for _, row in category_articles.iterrows():
        title = row['title']
        content = row['content']
        summary = gensim.summarization.summarize(content, ratio=0.3)  # Use TextRank algorithm for extractive summarization
        sentences = summary.split('\n')
        if len(sentences) < 4:
            continue
        article = f'<h1>{title}</h1>'
        article += f'<p>{sentences[0]}</p><p>{sentences[1]}</p><p>{sentences[2]}</p><p>{sentences[3]}</p>'
        articles.append(article)

# Shuffle the articles
random.shuffle(articles)

# Write the articles to a file
with open('generated_articles.html', 'w') as f:
    for article in articles:
        f.write(article)
