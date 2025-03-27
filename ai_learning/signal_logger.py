"""
signal_logger.py

Loggar realtidssignaler (köp/sälj/håll) till en CSV, så du kan analysera
eller fortsätta träna RL baserat på faktiskt utfall.
"""

import csv
import os
from datetime import datetime

def log_signal_to_csv(symbol, action, price, comment="", filename="trade_signals.csv"):
    """
    Loggar en handelssignal i en CSV-fil.
    symbol: T.ex. "EURUSD"
    action: "BUY", "SELL", "HOLD", eller liknande
    price: aktuell pris
    comment: ev. extra info
    filename: filnamn för logg
    """
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "symbol", "action", "price", "comment"])
        writer.writerow([datetime.now().isoformat(), symbol, action, price, comment])

if __name__ == "__main__":
    # Exempel
    log_signal_to_csv("USDSEK", "BUY", 10.25, "Momentum uppåt")
