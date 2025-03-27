import logging
import multiprocessing
import time

# Konfigurera loggning
logging.basicConfig(filename="process_manager.log", level=logging.INFO)


def worker(task_name, duration):
    """
    Simulerar en bakgrundsprocess.
    """
    try:
        logging.info(f"✅ Startar process: {task_name}")
        time.sleep(duration)
        logging.info(f"✅ Klar: {task_name}")
    except Exception as e:
        logging.error(f"❌ Fel i process {task_name}: {str(e)}")


def manage_processes(tasks, timeout=10):
    """
    Hanterar flera parallella processer och returnerar True om alla lyckas.
    """
    processes = []
    try:
        for task_name, duration in tasks:
            process = multiprocessing.Process(target=worker, args=(task_name, duration))
            process.start()
            processes.append(process)

        for process in processes:
            process.join(timeout=timeout)
            if process.is_alive():
                logging.warning("⚠️ Timeout: En process tog för lång tid och avslutas.")
                process.terminate()
                process.join()

        logging.info("✅ Alla processer klara!")
        return True

    except Exception as e:
        logging.error(f"❌ Fel vid hantering av processer: {str(e)}")
        return False


# Exempelanrop
if __name__ == "__main__":
    task_list = [("Datainsamling", 2), ("Analys", 3), ("Rapportgenerering", 1)]
    success = manage_processes(task_list)
    if success:
        print("📊 Alla processer slutförda!")
    else:
        print("❌ Något gick fel under processhantering.")
