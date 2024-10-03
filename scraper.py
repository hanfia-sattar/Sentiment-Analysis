import praw
import pandas as pd
from praw.models import MoreComments

# Reddit API credentials
client_id = "B-NSOXqlj-yKai9wXeDArA"
client_secret = "aH3eajuJgz0KK3iY93UuScDpTxFvgQ"
user_agent = "Middle-Surprise-6939"

def get_reddit_comments(url):
    # Initialize Reddit API client
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)
    
    # Get the submission
    submission = reddit.submission(url=url)
    
    # Fetch all comments
    submission.comments.replace_more(limit=None)
    
    comments = []
    for comment in submission.comments.list():
        comments.append({
            'author': str(comment.author),
            'body': comment.body,
            'score': comment.score,
            'created_utc': comment.created_utc
        })
    
    return comments

# Usage
url = "https://www.reddit.com/r/languagelearning/comments/1ft2lrp/really_struggling_to_learn/"
comments = get_reddit_comments(url)

# Create a DataFrame and save to CSV
df = pd.DataFrame(comments)
df.to_csv('reddit_comments.csv', index=False)

print(f"Fetched {len(comments)} comments and saved to reddit_comments.csv")