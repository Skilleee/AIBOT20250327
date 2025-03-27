from transformers import pipeline

def sentiment_analysis(texts: list) -> list:
    sentiment_classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    results = sentiment_classifier(texts)
    return results
