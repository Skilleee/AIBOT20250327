import logging
import os


def setup_logging(log_filename="trading_bot.log", log_level=logging.INFO):
    """
    Konfigurerar loggning för AI-trading boten.
    """
    try:
        # Skapa en loggmapp om den inte finns
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_filepath = os.path.join(log_dir, log_filename)

        logging.basicConfig(
            filename=log_filepath,
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logging.getLogger().addHandler(console_handler)

        logging.info("✅ Loggning initierad och konfigurerad.")
    except Exception as e:
        print(f"❌ Fel vid loggkonfiguration: {str(e)}")


def get_logger():
    """
    Returnerar en konfigurerad logger.
    """
    return logging.getLogger()


# Exempelanrop
if __name__ == "__main__":
    setup_logging()
    logger = get_logger()
    logger.info("📢 Loggningstest: Systemet körs korrekt!")
