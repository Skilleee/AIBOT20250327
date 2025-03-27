import logging

import requests

# Konfigurera loggning
logging.basicConfig(filename="api_wrapper.log", level=logging.INFO)


def make_api_request(url, params=None, headers=None):
    """
    Gör ett API-anrop och returnerar svaret.
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        logging.info("✅ API-anrop lyckades.")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Fel vid API-anrop: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    url = "https://api.example.com/data"
    response = make_api_request(url)
    print("📢 API-respons:", response)
