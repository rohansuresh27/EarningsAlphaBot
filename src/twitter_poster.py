
import json
import time
import os
import tweepy
from typing import List, Dict

# Configure callback URL
CALLBACK_URL = f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER')}.repl.co/oauth2callback"

def setup_twitter_client() -> tweepy.Client:
    """Setup Twitter API client using Bearer token"""
    auth = tweepy.OAuthHandler(
        os.getenv('TWITTER_CONSUMER_KEY'),
        os.getenv('TWITTER_CONSUMER_SECRET')
    )
    auth.set_access_token(
        os.getenv('TWITTER_ACCESS_TOKEN'),
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
    
    client = tweepy.Client(
        consumer_key=os.getenv('TWITTER_CONSUMER_KEY'),
        consumer_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
    return client

def format_tweet(quote: Dict) -> str:
    """Format quote as tweet"""
    return f"{quote['company']} {quote['speaker']} on {quote['description']}:\n\"{quote['quote']}\"\n{quote['hashtag']}"

def post_quotes():
    """Post quotes to Twitter"""
    client = setup_twitter_client()
    
    # Read quotes from JSON file
    with open('output/FY25/Q4/HDFC Bank_Q3_quotes.json', 'r') as f:
        quotes = json.load(f)
    
    for quote in quotes:
        try:
            tweet = format_tweet(quote)
            client.create_tweet(text=tweet)
            print(f"Posted tweet: {tweet[:50]}...")
            time.sleep(120)  # Wait 2 minutes between tweets
        except Exception as e:
            print(f"Error posting tweet: {str(e)}")

def setup_oauth2_client():
    """Setup OAuth2 Twitter client"""
    oauth2_handler = tweepy.OAuth2UserHandler(
        client_id=os.getenv('TWITTER_CONSUMER_KEY'),
        client_secret=os.getenv('TWITTER_CONSUMER_SECRET'),
        redirect_uri=CALLBACK_URL,
        scope=["tweet.read", "tweet.write", "users.read"]
    )
    return oauth2_handler

def test_twitter_connection():
    """Test Twitter API connection"""
    try:
        client = setup_twitter_client()
        client.get_me()
        print("Twitter API connection successful!")
        return True
    except Exception as e:
        print(f"Twitter API connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    if test_twitter_connection():
        post_quotes()
