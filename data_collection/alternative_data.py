import logging

import requests

# Konfigurera loggning
logging.basicConfig(filename="alternative_data.log", level=logging.INFO)


def fetch_google_trends(keyword):
    """
    Hämtar trenddata från Google Trends för ett specifikt sökord.
    """
    try:
        url = f"https://api.googletrends.com/trends/{keyword}"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ Google Trends-data hämtad för: {keyword}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av Google Trends-data: {str(e)}")
        return None


def fetch_twitter_sentiment(keyword):
    """
    Analyserar sentiment från Twitter-data.
    """
    try:
        url = f"https://api.twitter.com/sentiment/{keyword}"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ Twitter-sentiment analyserat för: {keyword}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av Twitter-sentiment: {str(e)}")
        return None


def fetch_satellite_data(location):
    """
    Hämtar satellitdata för att analysera ekonomiska trender.
    """
    try:
        url = f"https://api.satellitedata.com/economy/{location}"
        response = requests.get(url)
        data = response.json()
        logging.info(f"✅ Satellitdata hämtad för: {location}")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av satellitdata: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    keyword = "Tesla"
    location = "New York"

    google_trends_data = fetch_google_trends(keyword)
    twitter_sentiment_data = fetch_twitter_sentiment(keyword)
    satellite_data = fetch_satellite_data(location)

    print(f"📢 Google Trends-data:", google_trends_data)
    print(f"📢 Twitter-sentimentdata:", twitter_sentiment_data)
    print(f"📢 Satellitdata:", satellite_data)
