import json
import logging

# Konfigurera loggning
logging.basicConfig(filename="file_utils.log", level=logging.INFO)


def save_to_json(data, file_path):
    """
    Sparar data till en JSON-fil.
    """
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        logging.info("✅ Data sparad till JSON.")
    except Exception as e:
        logging.error(f"❌ Fel vid sparande av JSON: {str(e)}")


def load_from_json(file_path):
    """
    Laddar data från en JSON-fil.
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        logging.info("✅ Data laddad från JSON.")
        return data
    except Exception as e:
        logging.error(f"❌ Fel vid inläsning av JSON: {str(e)}")
        return None


def save_to_csv(data, file_path):
    """
    Sparar data till en CSV-fil.
    """
    try:
        data.to_csv(file_path, index=False)
        logging.info("✅ Data sparad till CSV.")
    except Exception as e:
        logging.error(f"❌ Fel vid sparande av CSV: {str(e)}")


# Exempelanrop
if __name__ == "__main__":
    sample_data = {"name": "Tesla", "price": 900}
    save_to_json(sample_data, "sample.json")
    loaded_data = load_from_json("sample.json")
    print("📢 JSON Data:", loaded_data)
