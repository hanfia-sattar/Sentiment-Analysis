import praw
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob

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

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Tokenize (simple split)
    tokens = text.split()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

# Ensure NLTK resources are downloaded
def download_nltk_resources():
    nltk.download('stopwords', quiet=True)

# Download NLTK resources before using them
download_nltk_resources()

def analyze_reddit_comments(url):
    comments = get_reddit_comments(url)

    # Preprocess comments and analyze sentiment
    for comment in comments:
        comment['preprocessed_body'] = preprocess_text(comment['body'])
        comment['sentiment'] = analyze_sentiment(comment['body'])

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(comments)
    df.to_csv('reddit_comments_analyzed.csv', index=False)

    print(f"Fetched, preprocessed, and analyzed {len(comments)} comments and saved to reddit_comments_analyzed.csv")

    return df

# Example usage
if __name__ == "__main__":
    url = "https://www.reddit.com/r/languagelearning/comments/1ft2lrp/really_struggling_to_learn/"
    df = analyze_reddit_comments(url)

    # Print first 5 analyzed comments
    for _, comment in df.head().iterrows():
        print(f"Original: {comment['body'][:100]}...")  # First 100 characters
        print(f"Preprocessed: {comment['preprocessed_body'][:100]}...")
        print(f"Sentiment: {comment['sentiment']}")
        print()