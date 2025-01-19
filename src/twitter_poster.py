
import json
import time
import os
import tweepy
import argparse
from typing import List, Dict

# Configure callback URL
CALLBACK_URL = f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER')}.repl.co/oauth2callback"

def setup_twitter_client() -> tweepy.Client:
    """Setup Twitter API client using Bearer token"""
    # Get credentials
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    # Validate credentials
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        missing = []
        if not consumer_key: missing.append('TWITTER_CONSUMER_KEY')
        if not consumer_secret: missing.append('TWITTER_CONSUMER_SECRET')
        if not access_token: missing.append('TWITTER_ACCESS_TOKEN')
        if not access_token_secret: missing.append('TWITTER_ACCESS_TOKEN_SECRET')
        raise ValueError(f"Missing Twitter credentials: {', '.join(missing)}")
    
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    return client

def format_tweet(quote: Dict) -> str:
    """Format quote as tweet"""
    fy_q_hashtag = f"#{quote['fiscal_year']}{quote['quarter']}" if 'fiscal_year' in quote and 'quarter' in quote else ""
    return f"{quote['company']} {quote['speaker']} on {quote['description']}:\n\"{quote['quote']}\"\n{quote['hashtag']} {fy_q_hashtag}"

def post_quotes(json_path: str):
    """Post quotes to Twitter"""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")
        
    client = setup_twitter_client()
    
    # Read quotes from JSON file
    with open(json_path, 'r') as f:
        quotes = json.load(f)
    
    for quote in quotes:
        try:
            tweet = format_tweet(quote)
            client.create_tweet(text=tweet)
            print(f"Posted tweet: {tweet[:50]}...")
            time.sleep(5)  # Wait 2 minutes between tweets
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
    parser = argparse.ArgumentParser(description='Post quotes from JSON file to Twitter')
    parser.add_argument('json_path', type=str, help='Path to the JSON file containing quotes')
    args = parser.parse_args()
    
    if test_twitter_connection():
        post_quotes(args.json_path)
