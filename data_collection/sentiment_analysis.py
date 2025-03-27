import logging
from datetime import datetime

import requests
from textblob import TextBlob

# För BERT-liknande sentimentanalys
from transformers import pipeline
import torch

# Konfigurera loggning
logging.basicConfig(filename="sentiment_analysis.log", level=logging.INFO)

# API-konfiguration för Twitter, Reddit eller nyhetskällor (valfri expansion)
TWITTER_API_URL = "https://api.twitter.com/2/tweets/search/recent"
REDDIT_API_URL = "https://www.reddit.com/r/stocks/new.json"
NEWS_API_URL = "https://newsapi.org/v2/everything"

# Initiera en pipeline för sentimentanalys (ex. 'distilbert-base-uncased-finetuned-sst-2-english')
transformer_sentiment = pipeline("sentiment-analysis")

def fetch_tweets(keyword, count=10):
    """
    Hämtar de senaste tweets relaterade till en viss aktie eller marknad.
    """
    try:
        headers = {
            "Authorization": "Bearer YOUR_TWITTER_BEARER_TOKEN"
        }  # Ersätt med giltig API-nyckel
        params = {"query": keyword, "max_results": count, "tweet.fields": "text"}
        response = requests.get(TWITTER_API_URL, headers=headers, params=params)
        data = response.json()
        tweets = [tweet["text"] for tweet in data.get("data", [])]
        logging.info(
            f"[{datetime.now()}] ✅ Hämtade {len(tweets)} tweets för {keyword}"
        )
        return tweets
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av tweets för {keyword}: {str(e)}"
        )
        return []

def fetch_reddit_posts(subreddit="stocks", count=10):
    """
    Hämtar de senaste inläggen från Reddit inom en viss subreddit.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(REDDIT_API_URL, headers=headers)
        data = response.json()
        posts = [
            post["data"]["title"]
            for post in data.get("data", {}).get("children", [])[:count]
        ]
        logging.info(
            f"[{datetime.now()}] ✅ Hämtade {len(posts)} Reddit-inlägg från {subreddit}"
        )
        return posts
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av Reddit-inlägg: {str(e)}"
        )
        return []

# ----------- TEXTBLOB-SENTIMENT (original) -----------
def analyze_sentiment_textblob(texts):
    """
    Använder TextBlob för att analysera sentiment i textdata.
    Returnerar en sträng: 'positivt', 'negativt' eller 'neutral'.
    """
    if not texts:
        return "neutral"

    total_polarity = sum(TextBlob(text).sentiment.polarity for text in texts) / len(texts)
    if total_polarity > 0:
        sentiment = "positivt"
    elif total_polarity < 0:
        sentiment = "negativt"
    else:
        sentiment = "neutral"

    logging.info(
        f"[{datetime.now()}] 📊 (TextBlob) Sentimentanalys: {sentiment} (Polarity: {total_polarity})"
    )
    return sentiment

# ----------- TRANSFORMER-SENTIMENT -----------
def analyze_sentiment_transformer(texts):
    """
    Använder en Hugging Face Transformers-model (ex. BERT/DistilBERT) 
    för att analysera sentiment i textdata.
    Returnerar en sträng: 'positivt', 'negativt' eller 'neutral'.
    """
    if not texts:
        return "neutral"

    results = transformer_sentiment(texts)
    total_score = 0.0
    for r in results:
        label = r["label"]
        score = r["score"]
        if label == "POSITIVE":
            total_score += score
        elif label == "NEGATIVE":
            total_score -= score

    avg_score = total_score / len(results)

    if avg_score > 0.05:
        sentiment = "positivt"
    elif avg_score < -0.05:
        sentiment = "negativt"
    else:
        sentiment = "neutral"

    logging.info(
        f"[{datetime.now()}] 📊 (Transformer) Sentimentanalys: {sentiment} (Score: {avg_score})"
    )
    return sentiment

def fetch_and_analyze_sentiment(keyword, method="transformer"):
    """
    Hämtar tweets och Reddit-inlägg för en aktie och analyserar sentimentet.
    Parametern 'method' kan vara 'textblob' eller 'transformer'.
    """
    tweets = fetch_tweets(keyword)
    reddit_posts = fetch_reddit_posts()
    all_texts = tweets + reddit_posts

    if method == "textblob":
        sentiment = analyze_sentiment_textblob(all_texts)
    else:
        sentiment = analyze_sentiment_transformer(all_texts)

    return sentiment

# ----------- Lägg till en default-funktion -----------
def analyze_sentiment(texts):
    """
    Default-funktion som matchar test_main.py.
    Använder i detta exempel Transformers.
    Returnerar en dict med nyckeln 'sentiment'.
    """
    raw_sentiment = analyze_sentiment_transformer(texts)  # 'positivt', 'negativt' eller 'neutral'
    return {"sentiment": raw_sentiment}


# Exempelanrop
if __name__ == "__main__":
    stock_sentiment = fetch_and_analyze_sentiment("AAPL", method="transformer")
    print(f"📢 Sentiment (Transformer) för AAPL: {stock_sentiment}")

    stock_sentiment_tb = fetch_and_analyze_sentiment("AAPL", method="textblob")
    print(f"📢 Sentiment (TextBlob) för AAPL: {stock_sentiment_tb}")
