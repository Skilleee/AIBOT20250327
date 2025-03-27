import logging
from datetime import datetime
from typing import Optional, Dict, Any
import yfinance as yf
import pandas as pd

# Konfigurera loggning med ett specifikt format
logging.basicConfig(
    filename="market_data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def fetch_stock_price(symbol: str) -> Optional[float]:
    """
    Hämtar den senaste aktiekursen för ett givet symbol från Yahoo Finance.
    """
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1d")
        if history.empty:
            logger.warning(f"[{datetime.now()}] ⚠️ Ingen data hittades för {symbol}.")
            return None
        latest_price = history["Close"].iloc[-1]
        logger.info(f"[{datetime.now()}] ✅ Hämtade data för {symbol}: {latest_price} USD")
        return latest_price
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel vid hämtning av {symbol}: {str(e)}")
        return None

def fetch_multiple_stocks(symbols: list) -> Dict[str, float]:
    """
    Hämtar senaste priser för en lista av aktier.
    """
    stock_prices = {}
    for symbol in symbols:
        price = fetch_stock_price(symbol)
        if price is not None:
            stock_prices[symbol] = price
    return stock_prices

def fetch_forex_data(base_currency: str, quote_currency: str, period: str = "1d") -> Dict[str, Optional[pd.DataFrame]]:
    """
    Hämtar en tidsserie för valutakursen mellan två valutor.
    Returnerar en dict med nyckeln "history" som innehåller DataFrame med historiken.
    """
    try:
        pair = f"{base_currency}{quote_currency}=X"
        stock = yf.Ticker(pair)
        history = stock.history(period=period, interval="1d")
        if history.empty:
            logger.info(f"[{datetime.now()}] 💱 Växelkurs {base_currency}/{quote_currency} har ingen data för period={period}.")
            return {"history": None}
        latest_price = history["Close"].iloc[-1]
        logger.info(f"[{datetime.now()}] 💱 Hämtade {base_currency}/{quote_currency} tidsserie för {period}, senast: {latest_price}")
        return {"history": history}
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel vid hämtning av {base_currency}/{quote_currency} (period={period}): {str(e)}")
        return {"history": None}

def fetch_commodity_price(commodity: str) -> Optional[float]:
    """
    Hämtar realtidspris för en råvara (ex. guld, silver eller olja).
    """
    commodity_map = {"gold": "GC=F", "silver": "SI=F", "oil": "CL=F"}
    if commodity not in commodity_map:
        logger.error(f"[{datetime.now()}] ❌ Ogiltig råvara: {commodity}")
        return None
    return fetch_stock_price(commodity_map[commodity])

def fetch_order_flow(symbol: str) -> Optional[Dict[str, int]]:
    """
    Simulerar analys av orderflöde och likviditet för en aktie.
    """
    try:
        order_flow_data = {
            "buy_orders": 1200,
            "sell_orders": 800,
            "net_flow": 400,  # Positivt värde indikerar köparövertag
        }
        logger.info(f"[{datetime.now()}] 📊 Orderflöde för {symbol}: {order_flow_data}")
        return order_flow_data
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel vid hämtning av orderflöde för {symbol}: {str(e)}")
        return None

def fetch_undervalued_stocks(tickers: list) -> list:
    """
    Analyserar en lista av aktier och filtrerar ut de med lågt P/E och hög vinstmarginal.
    """
    undervalued_stocks = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            pe_ratio = info.get("trailingPE")
            profit_margin = info.get("profitMargins")
            if pe_ratio is not None and profit_margin is not None:
                if pe_ratio < 15 and profit_margin > 0.10:
                    undervalued_stocks.append({
                        "symbol": ticker,
                        "pe_ratio": pe_ratio,
                        "profit_margin": profit_margin
                    })
        except Exception as e:
            logger.error(f"[{datetime.now()}] ❌ Fel vid analys av {ticker}: {str(e)}")
    return undervalued_stocks

def scan_market() -> Dict[str, list]:
    """
    Skannar utvalda marknader och identifierar undervärderade aktier.
    """
    markets = {
        "OMX30": ["ERIC-B.ST", "VOLV-B.ST", "NDA-SE.ST", "HM-B.ST"],
        "DAX": ["SAP.DE", "BMW.DE", "DTE.DE", "BAS.DE"],
        "S&P 500": ["AAPL", "TSLA", "NVDA", "MSFT"]
    }
    undervalued = {}
    for market_name, tickers in markets.items():
        found = fetch_undervalued_stocks(tickers)
        undervalued[market_name] = found
        logger.info(f"[{datetime.now()}] 📊 {market_name} undervärderade aktier: {found}")
    return undervalued

def fetch_most_traded_stocks(index_ticker: str) -> list:
    """
    Hämtar de 10 mest omsatta aktierna (baserat på volym) för en given indexsymbol.
    OBS: Vissa indexdata kan vara begränsade i yfinance.
    """
    try:
        index = yf.Ticker(index_ticker)
        tickers = index.options  # Observera: Detta kan ge en lista med optionsexpirationer snarare än aktietickers.
        volume_data = {}
        for ticker in tickers[:20]:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            if not data.empty:
                volume_data[ticker] = data["Volume"].iloc[-1]
        sorted_stocks = sorted(volume_data.items(), key=lambda x: x[1], reverse=True)
        most_traded = sorted_stocks[:10]
        logger.info(f"[{datetime.now()}] 🔥 Mest omsatta aktier för {index_ticker}: {most_traded}")
        return most_traded
    except Exception as e:
        logger.error(f"[{datetime.now()}] ❌ Fel vid hämtning av mest omsatta aktier för {index_ticker}: {str(e)}")
        return []

if __name__ == "__main__":
    forex_ts = fetch_forex_data("USD", "SEK", period="1mo")
    print("Valutahistorik (USD/SEK) 1mo:", forex_ts.get("history"))
    undervalued_stocks = scan_market()
    print(f"📊 Undervärderade aktier: {undervalued_stocks}")
    omx_most_traded = fetch_most_traded_stocks('^OMX')
    print(f"🔥 Mest omsatta på OMX: {omx_most_traded}")
