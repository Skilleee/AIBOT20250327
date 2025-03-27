import logging

# Konfigurera loggning
logging.basicConfig(filename="error_handler.log", level=logging.INFO)


def log_error(error_message):
    """
    Loggar ett fel och returnerar ett standardiserat svar.
    """
    try:
        logging.error(f"❌ Fel: {error_message}")
        return {"status": "error", "message": error_message}
    except Exception as e:
        logging.error(f"❌ Fel vid loggning av fel: {str(e)}")
        return {"status": "error", "message": "Okänt fel"}


# Exempelanrop
if __name__ == "__main__":
    error_response = log_error("API-förfrågan misslyckades")
    print("📢 Felsvar:", error_response)
