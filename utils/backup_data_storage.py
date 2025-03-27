import logging
import os
import shutil
from datetime import datetime

# Konfigurera loggning
logging.basicConfig(filename="backup_data_storage.log", level=logging.INFO)


def create_backup(source_folder="data", backup_folder="backups"):
    """
    Skapar en säkerhetskopia av analysdata, strategier och transaktionsloggar.
    """
    try:
        if not os.path.exists(source_folder):
            logging.warning(
                f"⚠️ Källmappen {source_folder} finns inte. Ingen backup skapad."
            )
            return False

        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = os.path.join(backup_folder, f"backup_{timestamp}")
        shutil.copytree(source_folder, backup_path)

        logging.info(f"✅ Backup skapad: {backup_path}")
        return True
    except Exception as e:
        logging.error(f"❌ Fel vid backup: {str(e)}")
        return False


def schedule_backup(interval=86400):
    """
    Schemalägger en automatisk backup varje dag.
    """
    import time

    logging.info("🚀 Startar schemalagd backup...")
    while True:
        create_backup()
        time.sleep(interval)


# Exempelanrop
if __name__ == "__main__":
    create_backup()
    print("📂 Säkerhetskopia skapad!")
