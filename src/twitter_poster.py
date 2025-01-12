
import json
import time
import os
import tweepy
from typing import List, Dict

def setup_twitter_client() -> tweepy.Client:
    """Setup Twitter API client"""
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

if __name__ == "__main__":
    post_quotes()
