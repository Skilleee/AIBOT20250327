import json
import logging
import os

from dotenv import load_dotenv

# Ladda miljövariabler
load_dotenv()

# Konfigurera loggning
logging.basicConfig(filename="config_loader.log", level=logging.INFO)


def load_config(file_path="config.json"):
    """
    Laddar inställningar från en JSON-konfigurationsfil.
    """
    try:
        with open(file_path, "r") as file:
            config = json.load(file)
            logging.info("✅ Konfigurationsfil laddad.")
            return config
    except Exception as e:
        logging.error(f"❌ Fel vid inläsning av konfigurationsfil: {str(e)}")
        return None


def get_env_variable(var_name):
    """
    Hämtar en miljövariabel.
    """
    try:
        value = os.getenv(var_name)
        if value:
            logging.info(f"✅ Miljövariabel laddad: {var_name}")
            return value
        else:
            logging.warning(f"⚠️ Miljövariabel saknas: {var_name}")
            return None
    except Exception as e:
        logging.error(f"❌ Fel vid inläsning av miljövariabel: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    config = load_config()
    api_key = get_env_variable("AVANZA_API_KEY")
    print("📢 Konfiguration:", config)
    print("📢 API-nyckel:", api_key)
