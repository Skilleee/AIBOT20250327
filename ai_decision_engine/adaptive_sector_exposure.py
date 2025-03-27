import logging
import numpy as np
import pandas as pd

# Konfigurera loggning
logging.basicConfig(filename="adaptive_sector_exposure.log", level=logging.INFO)


def analyze_sector_performance(market_data):
    """
    Analyserar sektorer baserat på marknadsdata och returnerar rekommenderade sektorer.
    """
    try:
        # Grundexempel: median eller medelavkastning per sektor
        sector_performance = (
            market_data.groupby("sector")["return"].mean().sort_values(ascending=False)
        )
        top_sectors = sector_performance.head(3).index.tolist()
        bottom_sectors = sector_performance.tail(3).index.tolist()

        logging.info(
            f"✅ Bästa sektorer: {top_sectors}, Sämsta sektorer: {bottom_sectors}"
        )
        return top_sectors, bottom_sectors
    except Exception as e:
        logging.error(f"❌ Fel vid sektoranalys: {str(e)}")
        return None, None


def adjust_sector_exposure(portfolio, top_sectors, bottom_sectors):
    """
    Justerar portföljens exponering genom att öka allokeringen i de starkaste sektorerna
    och minska i de svagaste.
    """
    try:
        # Exempel: +5% om sektorn är i top 3, -5% om sektorn är i botten 3
        portfolio["adjustment"] = portfolio["sector"].apply(
            lambda x: 0.05 if x in top_sectors else (-0.05 if x in bottom_sectors else 0)
        )
        portfolio["new_allocation"] = portfolio["allocation"] + portfolio["adjustment"]

        # Säkerställ att allokeringen ligger mellan 0% och 100%
        portfolio["new_allocation"] = np.clip(portfolio["new_allocation"], 0, 1)
        logging.info("✅ Sektorexponering justerad i portföljen.")
        return portfolio
    except Exception as e:
        logging.error(f"❌ Fel vid justering av sektorexponering: {str(e)}")
        return portfolio


# ---------------- NYA FUNKTIONER: ALTERNATIVA INVESTERINGAR & SEKTORROTATION ---------------

def identify_overvalued_sectors(market_data, threshold=0.10):
    """
    Identifierar sektorer som kan vara 'övervärderade' baserat på en enkel avkastningströskel.
    Exempel: Om en sektors medelavkastning > threshold => övervärderad.
    """
    try:
        sector_performance = market_data.groupby("sector")["return"].mean()
        # Filtrera ut de som överstiger threshold
        overvalued = sector_performance[sector_performance > threshold].index.tolist()
        logging.info(f"📈 Övervärderade sektorer (return > {threshold}): {overvalued}")
        return overvalued
    except Exception as e:
        logging.error(f"❌ Fel vid identifiering av övervärderade sektorer: {str(e)}")
        return []


def rotate_to_alternatives(portfolio, overvalued_sectors):
    """
    Roterar en del av portföljen till 'alternativa investeringar' (t.ex. guld, obligationer, REITs)
    om flera sektorer är övervärderade.
    Exempel: Om övervärderade sektorer > 2 => investera 10% av portföljen i guld/obligationer.
    """
    try:
        if len(overvalued_sectors) > 2:
            # Exempel: lägg till en rad i portföljen för 'Guld' eller en fond/ETF
            alternative_asset = {
                "symbol": "GLD",           # t.ex. ETF för guld
                "sector": "Alternative",   # en egen ”sektor”
                "allocation": 0.10         # 10% i detta exempel
            }
            # Minska befintlig allokering proportionellt så summan blir 100%
            current_sum = portfolio["allocation"].sum()
            reduce_factor = (current_sum - alternative_asset["allocation"]) / current_sum
            portfolio["allocation"] = portfolio["allocation"] * reduce_factor

            # Lägg till den alternativa investeringen
            portfolio = portfolio.append(alternative_asset, ignore_index=True)
            logging.info("📌 Roterar 10% av portföljen till alternativa investeringar (Guld).")
        else:
            logging.info("📌 Inga större rotationer till alternativa investeringar just nu.")
        return portfolio
    except Exception as e:
        logging.error(f"❌ Fel vid rotation till alternativa investeringar: {str(e)}")
        return portfolio


# Exempelanrop
if __name__ == "__main__":
    # Simulerad marknadsdata
    market_data = pd.DataFrame({
        "sector": ["Tech", "Finance", "Healthcare", "Energy", "Tech", "Finance"],
        "return": [0.12, 0.05, -0.02, 0.08, 0.15, 0.02],
    })

    # Simulerad portfölj
    portfolio = pd.DataFrame({
        "symbol": ["AAPL", "JPM", "PFE", "XOM", "GOOGL"],
        "sector": ["Tech", "Finance", "Healthcare", "Energy", "Tech"],
        "allocation": [0.20, 0.15, 0.10, 0.25, 0.30],
    })

    # 1. Analysera sektorer
    top_sectors, bottom_sectors = analyze_sector_performance(market_data)
    portfolio = adjust_sector_exposure(portfolio, top_sectors, bottom_sectors)
    print("📊 Uppdaterad sektorexponering i portföljen:")
    print(portfolio)

    # 2. Identifiera övervärderade sektorer
    overvalued = identify_overvalued_sectors(market_data, threshold=0.10)

    # 3. Roterar till alternativa tillgångar om behov
    portfolio = rotate_to_alternatives(portfolio, overvalued)
    print("\n📊 Portfölj efter eventuell rotation till alternativa investeringar:")
    print(portfolio)
