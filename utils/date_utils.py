import datetime
import logging

import pytz

# Konfigurera loggning
logging.basicConfig(filename="date_utils.log", level=logging.INFO)


def convert_to_utc(local_time, timezone):
    """
    Konverterar lokal tid till UTC.
    """
    try:
        local_tz = pytz.timezone(timezone)
        local_dt = local_tz.localize(local_time)
        utc_dt = local_dt.astimezone(pytz.utc)
        logging.info("✅ Tid konverterad till UTC.")
        return utc_dt
    except Exception as e:
        logging.error(f"❌ Fel vid tidskonvertering: {str(e)}")
        return None


def get_current_market_time():
    """
    Hämtar aktuell marknadstid i New York (EST).
    """
    try:
        est = pytz.timezone("America/New_York")
        market_time = datetime.datetime.now(est)
        logging.info("✅ Aktuell marknadstid hämtad.")
        return market_time
    except Exception as e:
        logging.error(f"❌ Fel vid hämtning av marknadstid: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    local_time = datetime.datetime(2023, 3, 1, 12, 0)
    utc_time = convert_to_utc(local_time, "Europe/Stockholm")
    market_time = get_current_market_time()
    print("📢 UTC-tid:", utc_time)
    print("📢 Marknadstid (EST):", market_time)
