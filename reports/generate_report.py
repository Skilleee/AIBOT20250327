import sys, os
# Lägg till projektets rotmapp i sys.path så att importer från portfolio_management och notifications fungerar
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import os
import logging
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import time
from typing import Optional

# Exempelimporter från projektet – se till att dessa moduler finns
from portfolio_management.rebalancing import add_rebalancing_section_to_pdf
from portfolio_management.portfolio_ai_analysis import generate_ai_recommendations, suggest_new_investments
from portfolio_management.portfolio_google_sheets import fetch_all_portfolios

# Konfigurera loggning
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(current_dir, "generate_report.log")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

def create_performance_chart(trade_log: pd.DataFrame, output_file: str) -> None:
    try:
        if "return" not in trade_log.columns:
            raise ValueError("Kolumnen 'return' saknas i trade_log")
        trade_log["Cumulative Returns"] = (1 + trade_log["return"]).cumprod()
        plt.figure(figsize=(10, 5))
        plt.plot(trade_log["Cumulative Returns"], label="Portfoljutveckling", color="blue")
        plt.axhline(y=1, color="gray", linestyle="--", label="Startvarde")
        plt.legend()
        plt.title("Handelsstrategins Prestanda")
        plt.xlabel("Handel")
        plt.ylabel("Avkastning")
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        logger.info("✅ Prestandadiagram genererat.")
    except Exception as e:
        logger.error(f"❌ Fel vid skapande av prestandadiagram: {str(e)}")

def add_ai_recommendations_section(pdf: FPDF) -> None:
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "AI Rekommendationer per konto", ln=True)
    pdf.set_font("DejaVu", "", 11)
    avail_width = pdf.w - pdf.l_margin - pdf.r_margin
    try:
        recommendations = generate_ai_recommendations()
        for konto, innehav in recommendations.items():
            pdf.set_font("DejaVu", "B", 12)
            pdf.cell(avail_width, 8, f"{konto}", ln=True)
            pdf.set_font("DejaVu", "", 11)
            for post in innehav:
                pdf.multi_cell(avail_width, 8, f"- {post['namn']} ({post['kategori']}, {post['värde']} kr): {post['rekommendation']}")
            pdf.ln(2)
    except Exception as e:
        pdf.set_font("DejaVu", "", 11)
        pdf.cell(avail_width, 8, f"Fel vid AI-rekommendationer: {str(e)}", ln=True)

def add_new_investment_suggestions(pdf: FPDF) -> None:
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Foreslagna nya investeringar", ln=True)
    pdf.set_font("DejaVu", "", 11)
    avail_width = pdf.w - pdf.l_margin - pdf.r_margin
    try:
        suggestions = suggest_new_investments(fetch_all_portfolios())
        for konto, forslag in suggestions.items():
            pdf.set_font("DejaVu", "B", 12)
            pdf.cell(avail_width, 8, f"{konto}", ln=True)
            pdf.set_font("DejaVu", "", 11)
            for kategori, namn in forslag:
                pdf.multi_cell(avail_width, 8, f"- {namn} - {kategori}")
            pdf.ln(2)
    except Exception as e:
        pdf.set_font("DejaVu", "", 11)
        pdf.cell(avail_width, 8, f"Fel vid nya investeringar: {str(e)}", ln=True)

def add_rebalancing_section(pdf: FPDF, rebalanced_df: pd.DataFrame) -> None:
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Rebalansering av Portfolj", ln=True)
    pdf.set_font("DejaVu", "", 11)
    avail_width = pdf.w - pdf.l_margin - pdf.r_margin
    if rebalanced_df.empty or "symbol" not in rebalanced_df.columns:
        pdf.multi_cell(avail_width, 8, "Ingen rebalansering kunde visas.")
        return
    for _, row in rebalanced_df.iterrows():
        symbol = row.get("symbol", "")
        old_allocation = f"{row.get('allocation', 0) * 100:.1f}%" if "allocation" in row else "-"
        new_allocation = f"{row.get('new_allocation', 0) * 100:.1f}%"
        adjustment = f"{row.get('adjustment', 0) * 100:+.1f}%" if "adjustment" in row else "-"
        pdf.multi_cell(avail_width, 8, f"- {symbol}: {old_allocation} -> {new_allocation} ({adjustment})")
    pdf.ln(5)

def add_sentiment_adjustment_section(pdf: FPDF, adjusted_assets: dict) -> None:
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Sentimentjusteringar", ln=True)
    pdf.set_font("DejaVu", "", 11)
    avail_width = pdf.w - pdf.l_margin - pdf.r_margin
    if not adjusted_assets:
        pdf.multi_cell(avail_width, 8, "Inga tillgångar påverkades av negativt sentiment.")
    else:
        for asset, adjustment in adjusted_assets.items():
            original = adjustment.get("original", "okänt")
            adjusted = adjustment.get("adjusted", "okänt")
            pdf.multi_cell(avail_width, 8, f"- {asset}: {original} -> {adjusted}")
    pdf.ln(4)

def cleanup_old_reports(folder: str = "reports", days_old: int = 14) -> None:
    cutoff = time.time() - days_old * 86400
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path) and (file.endswith(".pdf") or file.endswith(".png")):
            if os.path.getmtime(path) < cutoff:
                try:
                    os.remove(path)
                    logger.info(f"🗑️ Raderade gammal fil: {path}")
                except Exception as e:
                    logger.warning(f"⚠️ Kunde inte ta bort {path}: {str(e)}")

def generate_pdf_report(trade_log: Optional[pd.DataFrame] = None,
                        filename: Optional[str] = None,
                        rl_backtest_result: Optional[float] = None,
                        adjusted_assets: Optional[dict] = None,
                        latest_signal: Optional[dict] = None,
                        rebalanced_df: Optional[pd.DataFrame] = None) -> Optional[str]:
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        if filename is None:
            filename = os.path.join("reports", f"daily_report_{today}.pdf")

        cleanup_old_reports()

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Ange sökväg till fontfiler (i projektets rotmapp, i mappen fonts)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_dir = os.path.join(os.path.dirname(current_dir), "fonts")
        regular_font = os.path.join(font_dir, "DejaVuSans.ttf")
        bold_font = os.path.join(font_dir, "DejaVuSans-Bold.ttf")
        italic_font = os.path.join(font_dir, "DejaVuSans-Oblique.ttf")
        pdf.add_font("DejaVu", "", regular_font, uni=True)
        pdf.add_font("DejaVu", "B", bold_font, uni=True)
        pdf.add_font("DejaVu", "I", italic_font, uni=True)
        pdf.set_font("DejaVu", "", 12)

        logo_path = "logo.png"
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=10, y=8, w=30)

        pdf.set_font("DejaVu", "B", 16)
        pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin, 10, "AI Trading Report", ln=True, align="C")
        pdf.set_font("DejaVu", "", 12)
        pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin, 10, f"Dagens datum: {today}", ln=True, align="C")
        pdf.ln(10)

        if trade_log is not None and not trade_log.empty:
            pdf.set_font("DejaVu", "", 12)
            pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin, 10, f"Antal Affärer: {len(trade_log)}", ln=True)
            pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin, 10, f"Total Avkastning: {trade_log['return'].sum():.2%}", ln=True)
            pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin, 10, f"Win Rate: {(trade_log['return'] > 0).mean():.2%}", ln=True)
            chart_file = os.path.join("reports", f"performance_chart_{today}.png")
            create_performance_chart(trade_log, output_file=chart_file)
            if os.path.exists(chart_file):
                pdf.ln(10)
                pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin, 10, "Handelsstrategins Utveckling:", ln=True)
                pdf.image(chart_file, x=10, w=180)
                os.remove(chart_file)

        if rl_backtest_result:
            pdf.ln(10)
            pdf.set_font("DejaVu", "B", 12)
            pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin, 10, f"RL-agentens portfoljvärde efter backtest: {rl_backtest_result:.2f} SEK", ln=True)

        if adjusted_assets:
            pdf.ln(10)
            add_sentiment_adjustment_section(pdf, adjusted_assets)

        if latest_signal:
            pdf.ln(10)
            pdf.set_font("DejaVu", "B", 14)
            pdf.cell(pdf.w - pdf.l_margin - pdf.r_margin, 10, "Senaste Kop-/Saljsignal", ln=True)
            pdf.set_font("DejaVu", "", 11)
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin, 8, f"Datum: {latest_signal['date']}, Pris: {latest_signal['close']:.2f} SEK")
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin, 8, f"SMA 50: {latest_signal['sma_50']:.2f}, SMA 200: {latest_signal['sma_200']:.2f}")
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin, 8, f"Signal: {latest_signal['signal']}")
        
        if rebalanced_df is not None:
            pdf.ln(10)
            add_rebalancing_section(pdf, rebalanced_df)

        pdf.ln(10)
        add_ai_recommendations_section(pdf)
        pdf.ln(5)
        add_new_investment_suggestions(pdf)

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        pdf.output(filename)
        logger.info(f"✅ PDF-rapport genererad: {filename}")
        return filename

    except Exception as e:
        logger.error(f"❌ Fel vid skapande av PDF-rapport: {str(e)}")
        return None

if __name__ == "__main__":
    import pandas as pd
    trade_log = pd.DataFrame({
        "symbol": ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"],
        "entry_price": [150, 700, 250, 300, 2800],
        "exit_price": [155, 680, 270, 310, 2900],
        "return": [0.033, -0.028, 0.08, 0.033, 0.035],
        "trade_date": pd.date_range(start="2023-01-01", periods=5),
    })

    filename = generate_pdf_report(
        trade_log=trade_log,
        rl_backtest_result=108769.56,
        adjusted_assets={
            "AAPL": {"original": "buy", "adjusted": "hold"},
            "TSLA": {"original": "hold", "adjusted": "sell"},
        },
        latest_signal={
            "signal": "BUY",
            "close": 185.23,
            "sma_50": 180.52,
            "sma_200": 178.39,
            "date": "2025-03-23"
        },
        rebalanced_df=pd.DataFrame({
            "symbol": ["AAPL", "TSLA", "GOOGL"],
            "allocation": [0.3, 0.4, 0.3],
            "new_allocation": [0.333, 0.333, 0.333],
            "adjustment": [0.033, -0.067, 0.033]
        })
    )
    print(f"PDF-rapport skapad: {filename}")
