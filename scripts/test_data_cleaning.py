import re
import pandas as pd

df = pd.read_csv('data/test/test_data.csv')

def clean_text(text):
    # Removing the URLs
    text = re.sub(r'http\S+', '', text)

    # Replace the newline characters with spaces
    text = re.sub(r'\n+', ' ', text)

    # Remove "u/username" from the comments
    text = re.sub(r'u/[^\s]+', '', text)

    # Convert to lowercase
    text = text.lower()  

    # Remove numbers from comments and notthe usernames
    text = re.sub(r'\d+', '', text)  

    # Remove text within double asterisks (which means removing another comment tagged in a particular comment
    text = re.sub(r'\*\*[^*]+\*\*', '', text)

    return text

# Apply the cleaning function to the 'text' column
df['comment'] = df['comment'].apply(clean_text)

# Removeing data of deleted users
df = df[df['author_id'] != 'Deleted']

df.to_csv('data/test/test_data_cleaned.csv', index=False)
