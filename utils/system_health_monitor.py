import logging
import time

import psutil

# Konfigurera loggning
logging.basicConfig(filename="system_health_monitor.log", level=logging.INFO)


def check_cpu_usage(threshold=80):
    """
    Kontrollerar CPU-användning och varnar om den överstiger tröskeln.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > threshold:
        logging.warning(f"⚠️ Hög CPU-användning: {cpu_usage}%")
    else:
        logging.info(f"✅ CPU-användning: {cpu_usage}%")
    return cpu_usage


def check_memory_usage(threshold=80):
    """
    Kontrollerar RAM-användning och varnar om den överstiger tröskeln.
    """
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    if memory_usage > threshold:
        logging.warning(f"⚠️ Hög minnesanvändning: {memory_usage}%")
    else:
        logging.info(f"✅ Minnesanvändning: {memory_usage}%")
    return memory_usage


def check_disk_usage(threshold=90):
    """
    Kontrollerar diskens utrymme och varnar om det blir för fullt.
    """
    disk = psutil.disk_usage("/")
    disk_usage = disk.percent
    if disk_usage > threshold:
        logging.warning(f"⚠️ Hög diskanvändning: {disk_usage}%")
    else:
        logging.info(f"✅ Diskanvändning: {disk_usage}%")
    return disk_usage


def monitor_system(interval=60):
    """
    Övervakar systemets hälsa och loggar varningar vid höga resursnivåer.
    """
    while True:
        logging.info("🔍 Systemövervakning pågår...")
        check_cpu_usage()
        check_memory_usage()
        check_disk_usage()
        time.sleep(interval)


# Exempelanrop
if __name__ == "__main__":
    logging.info("🚀 Startar systemövervakning...")
    monitor_system()
