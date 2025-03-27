import logging
import os
import subprocess
import time

# Konfigurera loggning
logging.basicConfig(filename="fail_safe_mechanism.log", level=logging.INFO)


def restart_bot():
    """
    Startar om AI-trading boten vid oväntade krascher.
    """
    try:
        logging.warning("⚠️ Systemfel upptäckt! Försöker starta om boten...")
        os.system("python main.py &")  # Startar om boten i bakgrunden
        logging.info("✅ Boten har startats om.")
    except Exception as e:
        logging.error(f"❌ Fel vid omstart av boten: {str(e)}")


def check_system_health():
    """
    Kontrollerar om AI-boten körs och vidtar åtgärder vid avbrott.
    """
    try:
        process_name = "main.py"
        output = subprocess.getoutput(f"ps aux | grep {process_name} | grep -v grep")
        if process_name not in output:
            logging.warning("⚠️ Boten verkar ha kraschat! Startar om...")
            restart_bot()
        else:
            logging.info("✅ AI-boten är igång och fungerar som förväntat.")
    except Exception as e:
        logging.error(f"❌ Fel vid systemhälsokontroll: {str(e)}")


def monitor_bot(interval=60):
    """
    Kontinuerligt övervakar AI-boten och återställer den vid krasch.
    """
    while True:
        logging.info("🔍 Övervakar AI-trading botens status...")
        check_system_health()
        time.sleep(interval)


# Exempelanrop
if __name__ == "__main__":
    logging.info("🚀 Startar Fail-Safe Mechanism...")
    monitor_bot()
