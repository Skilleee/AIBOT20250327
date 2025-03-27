import logging
from datetime import datetime
import requests
from textblob import TextBlob

# Konfigurera loggning
logging.basicConfig(filename="news_analysis.log", level=logging.INFO)

# API-konfiguration
NEWS_API_URL = "https://newsapi.org/v2/everything"
API_KEY = "be05074147f44ac58df637ba3188ad99"  # Ersätt med din riktiga API-nyckel


def fetch_news(keyword, count=10):
    """
    Hämtar de senaste nyheterna relaterade till en viss aktie eller marknad.
    """
    try:
        params = {
            "q": keyword,
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": API_KEY,
        }
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        articles = [article["title"] for article in data.get("articles", [])[:count]]
        logging.info(
            f"[{datetime.now()}] ✅ Hämtade {len(articles)} nyhetsartiklar för {keyword}"
        )
        return articles
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid hämtning av nyheter för {keyword}: {str(e)}"
        )
        return []


def analyze_news_sentiment(news_articles):
    """
    Analyserar sentimentet i nyhetsrubriker med hjälp av TextBlob.
    Returnerar en dict med sentiment och genomsnittlig polaritet.
    """
    if not news_articles:
        return {"sentiment": "neutral", "polarity": 0.0}

    total_polarity = sum(
        TextBlob(article).sentiment.polarity for article in news_articles
    ) / len(news_articles)

    sentiment = (
        "positivt" if total_polarity > 0
        else "negativt" if total_polarity < 0
        else "neutral"
    )

    logging.info(
        f"[{datetime.now()}] 📊 Sentimentanalys: {sentiment} (Polarity: {total_polarity})"
    )

    return {"sentiment": sentiment, "polarity": total_polarity}


def fetch_and_analyze_news(keyword):
    """
    Hämtar nyhetsartiklar och analyserar sentiment.
    Returnerar en dict med sentiment, polaritet och antal källor.
    """
    try:
        news_articles = fetch_news(keyword)
        sentiment_result = analyze_news_sentiment(news_articles)

        result = {
            "sentiment": sentiment_result.get("sentiment", "neutral"),
            "polarity": sentiment_result.get("polarity", 0.0),
            "source_count": len(news_articles)
        }

        return result

    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel i fetch_and_analyze_news({keyword}): {str(e)}"
        )
        return {
            "sentiment": "neutral",
            "polarity": 0.0,
            "source_count": 0,
            "error": str(e)
        }


def get_recent_headlines(limit=10):
    """
    Returnerar de senaste nyhetsrubrikerna för allmänt börsrelaterade nyheter.
    Kan användas för generell sentimentanalys.
    """
    try:
        params = {
            "q": "stock market",
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": API_KEY,
        }
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        headlines = [article["title"] for article in data.get("articles", [])[:limit]]
        logging.info(
            f"[{datetime.now()}] ✅ Hämtade {len(headlines)} rubriker (get_recent_headlines)"
        )
        return headlines
    except Exception as e:
        logging.error(
            f"[{datetime.now()}] ❌ Fel vid get_recent_headlines: {str(e)}"
        )
        return []


# Exempelanrop
if __name__ == "__main__":
    stock_news_sentiment = fetch_and_analyze_news("AAPL")
    print(f"📰 Sentiment för AAPL-nyheter: {stock_news_sentiment}")

    print("📋 Senaste börsnyheter:")
    for headline in get_recent_headlines(limit=5):
        print("•", headline)
