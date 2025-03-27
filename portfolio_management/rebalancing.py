import logging
from typing import Optional, Union
import pandas as pd
from fpdf import FPDF

# Konfigurera loggning
logging.basicConfig(filename="rebalancing.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def rebalancing(portfolio: Union[pd.DataFrame, dict]) -> pd.DataFrame:
    """
    Rebalanserar portföljen till jämn vikt mellan tillgångar.
    Om indata är en dict konverteras den till DataFrame.
    Förväntar sig kolumnerna 'symbol' och 'allocation'.
    """
    try:
        if not hasattr(portfolio, "columns"):
            portfolio = pd.DataFrame(portfolio)
        if "symbol" not in portfolio.columns or "allocation" not in portfolio.columns:
            raise ValueError("Portföljen saknar nödvändiga kolumner ('symbol', 'allocation')")
        
        num_assets = len(portfolio)
        if num_assets == 0:
            raise ValueError("Portföljen är tom")
        
        target_allocation = 1.0 / num_assets
        portfolio["new_allocation"] = target_allocation
        portfolio["adjustment"] = portfolio["new_allocation"] - portfolio["allocation"]

        logger.info("✅ Portfölj rebalanserad.")
        return portfolio
    except Exception as e:
        logger.error(f"❌ Fel vid rebalansering: {str(e)}")
        if isinstance(portfolio, pd.DataFrame):
            return portfolio
        else:
            return pd.DataFrame(portfolio)

def add_rebalancing_section_to_pdf(pdf: FPDF, rebalanced_df: pd.DataFrame) -> None:
    """
    Lägger till en sektion i PDF-rapporten för att visa portföljens rebalansering.
    Förväntar sig kolumnerna 'symbol', 'allocation', 'new_allocation' och 'adjustment'.
    """
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "📊 Rebalansering av Portfölj", ln=True)
    pdf.set_font("Arial", "", 11)

    avail_width = pdf.w - pdf.l_margin - pdf.r_margin
    if rebalanced_df.empty or "symbol" not in rebalanced_df.columns:
        pdf.multi_cell(0, 8, "Ingen rebalansering kunde visas.")
        return

    for _, row in rebalanced_df.iterrows():
        symbol = row.get("symbol", "")
        old_allocation = f"{row.get('allocation', 0) * 100:.1f}%" if "allocation" in row else "-"
        new_allocation = f"{row.get('new_allocation', 0) * 100:.1f}%"
        adjustment = f"{row.get('adjustment', 0) * 100:+.1f}%" if "adjustment" in row else "–"
        pdf.multi_cell(0, 8, f"• {symbol}: {old_allocation} → {new_allocation} ({adjustment})")
    pdf.ln(5)

if __name__ == "__main__":
    portfolio = pd.DataFrame({
        "symbol": ["AAPL", "TSLA", "GOOGL", "JPM", "XOM"],
        "sector": ["Tech", "Tech", "Tech", "Finance", "Energy"],
        "allocation": [0.30, 0.25, 0.15, 0.20, 0.10],
    })

    rebalanced_portfolio = rebalancing(portfolio)
    print("📊 Rebalanserad portfölj:")
    print(rebalanced_portfolio[["symbol", "allocation", "new_allocation", "adjustment"]])
