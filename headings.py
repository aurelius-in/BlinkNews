import pandas as pd

# Load the scraped articles from the database
df = pd.read_csv('news_articles.csv')

# Remove duplicates based on the article title
df.drop_duplicates(subset=['title'], inplace=True)

# Create a dictionary to store the headings for each category
headings = {
    'Political news': [],
    'Sports news': [],
    'Tech news': [],
    'Software Development News': [],
    'Elon Musk News': [],
    'AI news': [],
    'Tech News': [],
    'Gay news': [],
    'Trump News': [],
    'Gossip news': [],
    'Health news': [],
    'Science news': [],
    'Entertainment news': [],
    'Environmental news': [],
    'Business news': [],
    'Education news': [],
    'Travel news': [],
    'Fashion news': [],
    'Food news': [],
    'Cultural news': [],
    'Lifestyle news': [],
    'Crime news': [],
    'Weather news': [],
    'Religion news': [],
    'International news': []
}

# Loop through each article and assign it to the appropriate category
for index, row in df.iterrows():
    for category in headings.keys():
        if category.lower() in row['category'].lower():
            if len(headings[category]) < 3:
                headings[category].append(row['title'])
            break

# Print the list of headings for each category
for category, articles in headings.items():
    print(f"{category}:")
    for article in articles:
        print(f"\t- {article}")
