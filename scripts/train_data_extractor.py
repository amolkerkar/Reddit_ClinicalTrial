import praw
import pandas as pd

#praw instance
user = "Reddit-clinical Agent 1.0"
reddit = praw.Reddit(
    client_id = "vwhAJ_NhUQ2rngo-iKiQuQ", #update your id
    client_secret = "WLNireNYv2MSvebDyJXINnbNGkmI-Q", #update your secret
    user_agent = user
    )

decaf_subreddits = ["decaf", "coffee", "CaffeineRecovery", "NoCaff", "NoCaf", "CaffeineFreeLife"]
keywords = ['anxiety', 'nervous', 'panic', 'anxious', 'stress', 'withdrawal symptoms']

def search_and_analyze(subreddit_list):
    results = []
    for sub in subreddit_list:
        subreddit = reddit.subreddit(sub.strip())
        for submission in subreddit.new(limit=10):  # Adjust the limit as needed for training data
            submission.comments.replace_more(limit=5)  # Adjust the limit as needed for training data
            for comment in submission.comments.list():
                if any(keyword in comment.body.lower() for keyword in keywords):
                    results.append({
                        "text": comment.body,
                    })
    return results

data = search_and_analyze(decaf_subreddits)



# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv('data/train/reddit_comments_data.csv', index=False)