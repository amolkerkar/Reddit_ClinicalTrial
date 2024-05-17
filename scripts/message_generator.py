import openai 
import pandas as pd
from textblob import TextBlob
import time
import logging
from openai import RateLimitError, OpenAIError
from keyfile import API_KEY

#logging for api limit tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

openai.api_key =  API_KEY 

df = pd.read_csv('output/final_potential_candidates.csv')

#analyze sentiment using TextBlob
def analyze_sentiment_textblob(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return sentiment.polarity, sentiment.subjectivity

#generate personalized message using OpenAI API with retry mechanism
def generate_personalized_message(text, sentiment_score):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a smart and empathetic salesman."},
                    {"role": "user", "content": f"Generate a personalized message for the author of the following comment asking politely if they can participate in a clinical trial, taking into account the sentiment score ({sentiment_score}):\n\n{text}\n\nPersonalized message:"}
                ],
                max_tokens=100,
                temperature=0.7,
            )
            message = response['choices'][0]['message']['content'].strip()
            return message
        except RateLimitError:
            wait_time = 60  # Wait time in seconds
            logging.warning(f"Rate limit reached. Attempt {attempt + 1}/{max_retries}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except OpenAIError as e:
            logging.error(f"An error occurred: {e}")
            return "Could not generate a personalized message due to an error."
    return "Could not generate a personalized message due to repeated rate limits."

#batch processing to solve limit issue
def process_batch(df_batch):
    df_batch.loc[:, 'personalized_message'] = df_batch.apply(
        lambda row: generate_personalized_message(row['comment'], row['sentiment_polarity']), axis=1)
    return df_batch

#Analyze sentiment
logging.info("Starting sentiment analysis using TextBlob...")
df['sentiment_polarity'], df['sentiment_subjectivity'] = zip(*df['comment'].apply(analyze_sentiment_textblob))


batch_size = 3  #rate limit was 3 so

#batch processing
results = []
for start in range(0, len(df), batch_size):
    end = start + batch_size
    df_batch = df.iloc[start:end].copy()
    processed_batch = process_batch(df_batch)
    results.append(processed_batch)
    

    logging.info(f"Processed batch {start // batch_size + 1}. Sleeping for 60 seconds to handle rate limits.")
    time.sleep(61)  # Increased sleep time for api limit

final_df = pd.concat(results)

final_df.to_csv('output/recruitment_messages.csv', index=False)
logging.info("Sentiment analysis and personalized messaging complete. Results saved to 'output/recruitment_messages.csv'.")
