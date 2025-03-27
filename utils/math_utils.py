import logging

import numpy as np

# Konfigurera loggning
logging.basicConfig(filename="math_utils.log", level=logging.INFO)


def moving_average(data, window_size=5):
    """
    Beräknar glidande medelvärde.
    """
    try:
        result = np.convolve(data, np.ones(window_size) / window_size, mode="valid")
        logging.info("✅ Glidande medelvärde beräknat.")
        return result
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av glidande medelvärde: {str(e)}")
        return None


def standard_deviation(data):
    """
    Beräknar standardavvikelse.
    """
    try:
        result = np.std(data)
        logging.info("✅ Standardavvikelse beräknad.")
        return result
    except Exception as e:
        logging.error(f"❌ Fel vid beräkning av standardavvikelse: {str(e)}")
        return None


# Exempelanrop
if __name__ == "__main__":
    sample_data = np.array([100, 102, 104, 98, 97, 96, 101, 105])
    ma = moving_average(sample_data)
    std_dev = standard_deviation(sample_data)
    print("📢 Glidande medelvärde:", ma)
    print("📢 Standardavvikelse:", std_dev)
