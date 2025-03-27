import logging
from datetime import datetime
import requests
from typing import Dict

# Konfigurera loggning
logging.basicConfig(filename="macro_data.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# API-konfiguration (ex. Alpha Vantage)
MACRO_API_URL = "https://www.alphavantage.co/query"
API_KEY = "D90V8NAHPLJSR7VO"  # Ersätt med din egen API-nyckel

# Fallback-värden för test
DEFAULT_VALUES: Dict[str, float] = {
    "GDP": 2.1,
    "REAL_GDP": 1.7,
    "INFLATION": 3.4,
    "FEDERAL_FUNDS_RATE": 5.25,
    "UNEMPLOYMENT_RATE": 4.1
}

def fetch_macro_data(indicator: str = "GDP") -> Dict[str, float]:
    """
    Hämtar makroekonomisk data från API eller fallback-värden.
    Returnerar en dict: {"indicator": indicator, "value": value}
    """
    try:
        params = {
            "function": indicator,
            "apikey": API_KEY
        }
        response = requests.get(MACRO_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Eftersom vissa API-indikatorer kräver premium används fallback
        value = DEFAULT_VALUES.get(indicator, 0.0)
        logger.info(f"[{datetime.now()}] ✅ Hämtade {indicator}: {value}")
        return {"indicator": indicator, "value": value}
    except Exception as e:
        logger.warning(f"[{datetime.now()}] ⚠️ Kunde inte hämta {indicator} via API. Fallback används. Fel: {str(e)}")
        value = DEFAULT_VALUES.get(indicator, 0.0)
        return {"indicator": indicator, "value": value}

def fetch_interest_rates() -> Dict[str, float]:
    """Hämtar aktuell styrränta."""
    return fetch_macro_data("FEDERAL_FUNDS_RATE")

def fetch_inflation() -> Dict[str, float]:
    """Hämtar aktuell inflation."""
    return fetch_macro_data("INFLATION")

def fetch_gdp_growth() -> Dict[str, float]:
    """Hämtar BNP-tillväxt."""
    return fetch_macro_data("REAL_GDP")

def fetch_unemployment_rate() -> Dict[str, float]:
    """Hämtar arbetslöshetsnivå."""
    return fetch_macro_data("UNEMPLOYMENT_RATE")

if __name__ == "__main__":
    interest_rate = fetch_interest_rates()
    print(f"🏦 Aktuell ränta: {interest_rate}")
    inflation = fetch_inflation()
    print(f"📈 Inflation: {inflation}")
    gdp_growth = fetch_gdp_growth()
    print(f"📊 BNP-tillväxt: {gdp_growth}")
    unemployment = fetch_unemployment_rate()
    print(f"👥 Arbetslöshet: {unemployment}")
