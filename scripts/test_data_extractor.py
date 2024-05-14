import praw
import pandas as pd

limit_sr_posts = 10          # limit to the number of new posts in a subreddit
limit_comments = 5           # 0 is loading all the comments

#Praw Reddit instance
reddit = praw.Reddit(
    client_id="vwhAJ_NhUQ2rngo-iKiQuQ", #your praw client id
    client_secret="WLNireNYv2MSvebDyJXINnbNGkmI-Q", #your praw secret
    user_agent="Reddit-clinical Agent 1.0"
)

decaf_subreddits = ["decaf", "coffee", "CaffeineRecovery", "NoCaff", "NoCaf", "CaffeineFreeLife"]
decaf_subreddits_keywords = [
    'anxiety', 'nervous', 'panic', 'anxious', 'stress', 
    'withdrawal symptoms', 'quitting caffeine', 'limiting caffeine', 'reducing caffeine'
]

related_healthissue_sr = ["anxiety", "insomnia"]
healthissue_keywords = [
    "coffee", "decaf", "caffeine recovery", "caffeine free", 
    "caffeine withdrawal", 'quitting caffeine', 'limiting caffeine', 'reducing caffeine'
]

clinical_trials_sr = ["clinicaltrials"]
clinical_trials_keywords = [
    "coffee", "decaf", "caffeine recovery", "caffeine free", 
    "caffeine withdrawal", 'quitting caffeine', 'limiting caffeine', 'reducing caffeine']

def search_and_analyze(subreddit_list, keywords):
    results = []
    for sub in subreddit_list:
        try:
            subreddit = reddit.subreddit(sub.strip())
            for submission in subreddit.new(limit=limit_sr_posts): 
                submission.comments.replace_more(limit=limit_comments)  
                for comment in submission.comments.list():
                    if any(keyword in comment.body.lower() for keyword in keywords):
                        # Store the author's username if available, otherwise 'Deleted'
                        author_id = comment.author.name if comment.author else "Deleted"
                        # Store the comment text
                        comment_text = comment.body
                        results.append({
                            "author_id": author_id,
                            "comment": comment_text,
                            "subreddit": sub
                        })
        except Exception as e:
            print(f"An error occurred with subreddit {sub}: {e}")
    return results

# Search decaf subreddits
decaf_data = search_and_analyze(decaf_subreddits, decaf_subreddits_keywords)

# Search health issue related subreddits
health_issue_data = search_and_analyze(related_healthissue_sr, healthissue_keywords)

# Search clinical trials subreddits
clinical_trials_data = search_and_analyze(clinical_trials_sr, clinical_trials_keywords)

combined_data = decaf_data + health_issue_data + clinical_trials_data

df = pd.DataFrame(combined_data)
df.to_csv('data/test/test_data.csv', index=False)