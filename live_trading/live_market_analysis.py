import logging
import numpy as np
import pandas as pd

# För realtidsdata via WebSockets
import asyncio
import websockets
import json

# Konfigurera loggning
logging.basicConfig(filename="live_market_analysis.log", level=logging.INFO)


def analyze_market_conditions(data):
    """
    Analyserar marknadens tillstånd baserat på volatilitet och trender.
    """
    try:
        data["volatility"] = data["close"].pct_change().rolling(window=20).std()
        data["market_trend"] = np.where(
            data["close"].rolling(window=50).mean() > data["close"].rolling(window=200).mean(),
            "Bullish",
            "Bearish",
        )

        logging.info("✅ Marknadsanalys genomförd.")
        return data[["date", "close", "volatility", "market_trend"]]
    except Exception as e:
        logging.error(f"❌ Fel vid marknadsanalys: {str(e)}")
        return None


async def subscribe_realtime_data(symbol, on_data_callback):
    """
    Exempel på en asynkron funktion som kopplar upp till en (fiktiv) WebSocket
    och tar emot realtidsdata för en given aktiesymbol.
    
    Parametrar:
      - symbol: Vilken aktiesymbol du vill lyssna på (t.ex. "AAPL").
      - on_data_callback: En funktion som tar emot ett dict med realtidsdata.
    
    OBS! Yahoo Finance har ingen officiell gratis WebSocket-endpoint.
         Detta är en förenklad exempelimplementation. Byt ut URL
         och anpassa anropet efter den leverantör du använder (Polygon.io, AlphaVantage m.fl.).
    """
    url = "wss://fictive-stream.yourdataapi.com"  # Byt till korrekt WebSocket-URL
    try:
        async with websockets.connect(url) as ws:
            # Skicka ev. prenumerationsmeddelande
            subscribe_message = {
                "action": "subscribe",
                "symbol": symbol
            }
            await ws.send(json.dumps(subscribe_message))
            logging.info(f"🔌 WebSocket-anslutning etablerad för {symbol}")

            while True:
                # Vänta på inkommande meddelanden
                message = await ws.recv()
                data = json.loads(message)
                # Exempel: Om data är i form av { "symbol": ..., "price": ... }
                on_data_callback(data)

    except Exception as e:
        logging.error(f"❌ Fel vid realtidsprenumeration för {symbol}: {str(e)}")


def handle_realtime_update(update):
    """
    Exempel på callback-funktion som tar emot realtidsdata.
    Här kan du t.ex. uppdatera en DataFrame, köra `analyze_market_conditions()`,
    eller skicka notiser till en dashboard.
    """
    symbol = update.get("symbol", "UNKNOWN")
    price = update.get("price", None)
    if price is not None:
        logging.info(f"📡 Realtidsuppdatering för {symbol}: {price}")
    else:
        logging.warning(f"⚠️ Oväntat meddelande: {update}")


# Exempelanrop
if __name__ == "__main__":
    # 1. Existerande testkod för marknadsanalys
    df = pd.DataFrame(
        {
            "date": pd.date_range(start="2023-01-01", periods=300),
            "close": np.cumsum(np.random.randn(300) * 2 + 100),
        }
    )

    market_analysis = analyze_market_conditions(df)
    print("📢 Marknadsanalys (historisk data):")
    print(market_analysis.tail())

    # 2. Realtidsexempel (fiktivt)
    # Körs asynkront i en event loop. Avslutas med Ctrl+C i terminalen.
    async def main():
        # Lyssna på realtidsdata för en viss symbol, t.ex. "AAPL"
        await subscribe_realtime_data("AAPL", handle_realtime_update)

    # Starta event loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAvslutar realtidsprenumeration...")
