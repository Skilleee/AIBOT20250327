import logging
 from datetime import datetime
 import json
 import requests
 
 from portfolio_management.portfolio_ai_analysis import generate_ai_recommendations, suggest_new_investments
 from portfolio_management.portfolio_ai_analysis import (
     generate_ai_recommendations,
     suggest_new_investments,
 )
 from portfolio_management.portfolio_google_sheets import fetch_all_portfolios
 from config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
 
 @@ -30,135 +33,6 @@
         logging.error(f"❌ Fel vid skickning av Telegram-meddelande: {str(e)}")
         return None
 
 def send_daily_market_report(market_data):
     """
     Skickar en sammanfattning av marknadsrapporten via Telegram.
     """
     try:
         message = (
             "*Daglig marknadsrapport:*\n"
             f"- S&P 500: {market_data.get('sp500', 'N/A')}%\n"
             f"- Nasdaq: {market_data.get('nasdaq', 'N/A')}%\n"
             f"- Tech-sektorn: {market_data.get('tech_sector', 'N/A')}%\n"
             f"- Sentiment: {market_data.get('sentiment', 'N/A')}\n"
         )
         send_telegram_message(message)
     except Exception as e:
         logging.error(f"❌ Fel vid marknadsrapport: {str(e)}")
 
 def send_risk_alert(risk_level):
     """
     Skickar en riskvarning om risknivån är hög.
     """
     try:
         if risk_level > 0.05:
             message = f"⚠️ *Hög volatilitet upptäckt!* Risknivå: *{risk_level:.2%}*. Överväg att minska exponering."
             send_telegram_message(message)
     except Exception as e:
         logging.error(f"❌ Fel vid riskvarning: {str(e)}")
 
 def send_portfolio_update(portfolio_data):
     """
     Skickar en uppdatering av portföljen via Telegram.
     """
     try:
         message = "*Portföljuppdatering:*\n"
         for stock, change in portfolio_data.items():
             message += f"- {stock}: {change:.2%}\n"
         send_telegram_message(message)
     except Exception as e:
         logging.error(f"❌ Fel vid portföljnotis: {str(e)}")
 
 def send_macro_event_alert(event):
     """
     Skickar en makrohändelse-notis via Telegram.
     """
     try:
         message = f"*Makrohändelse:* {event}"
         send_telegram_message(message)
     except Exception as e:
         logging.error(f"❌ Fel vid makronotis: {str(e)}")
 
 def send_rl_backtest_summary(reward, final_value):
     """
     Skickar en sammanfattning av RL-agentens backtest via Telegram.
     """
     try:
         message = (
             "*RL-agentens backtest:*\n"
             f"- Total reward: {reward:.2f}\n"
             f"- Slutligt portföljvärde: {final_value:,.2f} SEK"
         )
         send_telegram_message(message)
     except Exception as e:
         logging.error(f"❌ Fel vid backtest-sammanfattning: {str(e)}")
 
 def send_ai_recommendations():
     """
     Hämtar AI-rekommendationer och nya investeringsförslag, formaterar dem med tydliga rubriker
     och punktlistor, och skickar dem via Telegram.
     """
     try:
         recommendations = generate_ai_recommendations()
         new_suggestions = suggest_new_investments(fetch_all_portfolios())
         message = "*AI Rekommendationer per konto:*\n"
         
         for konto, innehav in recommendations.items():
             message += f"\n*{konto}:*\n"
             if isinstance(innehav, list):
                 for post in innehav:
                     if isinstance(post, dict):
                         try:
                             namn = post.get("namn", "Okänt")
                             kategori = post.get("kategori", "Okänt")
                             värde = post.get("värde", "N/A")
                             valuta = post.get("valuta", "")
                             rek = post.get("rekommendation", "")
                             motivering = post.get("motivering", "")
                             riktkurs_3m = post.get("riktkurs_3m", "N/A")
                             riktkurs_6m = post.get("riktkurs_6m", "N/A")
                             riktkurs_12m = post.get("riktkurs_12m", "N/A")
                             pe_ratio = post.get("pe_ratio", "N/A")
                             rsi = post.get("rsi", "N/A")
                             riskbedomning = post.get("riskbedomning", "N/A")
                             historisk_prestanda = post.get("historisk_prestanda", "N/A")
                             
                             message += (
                                 f"• `{namn}` ({kategori}, {värde} {valuta}): *{rek}*\n"
                                 f"   _{motivering}_\n"
                                 f"   Riktkurser: 3 mån: {riktkurs_3m}, 6 mån: {riktkurs_6m}, 12 mån: {riktkurs_12m}\n"
                                 f"   PE-tal: {pe_ratio}, RSI: {rsi}, Risk: {riskbedomning}\n"
                                 f"   Historisk: {historisk_prestanda}\n"
                                 f"   [Visa historik](https://example.com/historik/{namn}) | [Mer info](https://example.com/info/{namn})\n\n"
                             )
                         except Exception as e:
                             message += f"• Fel vid läsning av rekommendation: {post} ({str(e)})\n"
                     else:
                         message += f"• {post}\n"
             elif isinstance(innehav, str):
                 message += f"• {innehav}\n"
             else:
                 message += f"• {str(innehav)}\n"
                 
         message += "\n*Föreslagna nya investeringar:*\n"
         for konto, forslag in new_suggestions.items():
             message += f"\n*{konto}:*\n"
             if isinstance(forslag, list):
                 for kategori, namn in forslag:
                     message += f"• `{namn}` – {kategori}\n"
             else:
                 message += f"• {forslag}\n"
         
         # Exempel på inline-knapp för att öppna en dashboard
         reply_markup = {
             "inline_keyboard": [
                 [{"text": "Öppna Dashboard", "url": "https://example.com/dashboard"}]
             ]
         }
         send_telegram_message(message, reply_markup=reply_markup)
     except Exception as e:
         logging.error(f"❌ Fel vid AI-rekommendationer: {str(e)}")
 
 def send_pdf_report_to_telegram(file_path):
     """
     Skickar en PDF-rapport som bilaga via Telegram.
 @@ -196,6 +70,110 @@
         logging.error(f"❌ Fel vid skickning av diagram: {str(e)}")
         return False
 
 def send_full_daily_report(market_data, risk_level, macro_event):
     """
     Skickar ett samlat dagligt meddelande med:
       - Marknadsrapport
       - Riskvarning
       - Portföljöversikt (per konto)
       - AI-rekommendationer
       - Nya investeringsförslag
     """
     try:
         # 1) Daglig marknadsrapport
         market_summary = (
             "*Daglig marknadsrapport:*\n"
             f"- S&P 500: {market_data.get('sp500', 'N/A')}%\n"
             f"- Nasdaq: {market_data.get('nasdaq', 'N/A')}%\n"
             f"- Tech-sektorn: {market_data.get('tech_sector', 'N/A')}%\n"
             f"- Sentiment: {market_data.get('sentiment', 'N/A')}\n"
         )
 
         # 2) Riskvarning
         risk_msg = ""
         if risk_level > 0.05:
             risk_msg = (
                 f"\n⚠️ *Hög volatilitet upptäckt!* "
                 f"Risknivå: *{risk_level:.2%}*. Överväg att minska exponering.\n"
             )
 
         # 3) Hämta AI-rekommendationer & nya investeringsförslag
         recommendations = generate_ai_recommendations()
         portfolios = fetch_all_portfolios()
         new_suggestions = suggest_new_investments(portfolios)
 
         # 4) Sammanfatta portföljvärden per konto + AI-rekommendationer
         portfolio_msg = "*Portföljöversikt & Rekommendationer*\n"
         for account, recs in recommendations.items():
             # Beräkna totalvärde
             total_konto = 0
             for r in recs:
                 val = r.get("total_värde", 0)
                 if isinstance(val, (int, float)):
                     total_konto += val
 
             portfolio_msg += f"\n*{account}*\n"
             portfolio_msg += f"Totalt värde (estimerat): {total_konto:,.2f} SEK\n"
             for r in recs:
                 namn = r.get("namn", "Okänt")
                 antal = r.get("antal", 0)
                 pris = r.get("pris", "N/A")
                 valuta = r.get("valuta", "")
                 total_värde = r.get("total_värde", 0)
                 rek = r.get("rekommendation", "")
                 motiv = r.get("motivering", "")
                 portfolio_msg += (
                     f"• `{namn}`: {antal} st à {pris} {valuta} "
                     f"(~{total_värde:,.2f} {valuta})\n"
                     f"   Rek: *{rek}* – _{motiv}_\n"
                 )
             portfolio_msg += "\n"
 
         # 5) Föreslagna nya investeringar
         invest_msg = "*Föreslagna nya investeringar:*\n"
         for account, forslag in new_suggestions.items():
             invest_msg += f"\n*{account}:*\n"
             if isinstance(forslag, list) and len(forslag) > 0:
                 for kategori, namn in forslag:
                     invest_msg += f"• `{namn}` – {kategori}\n"
             else:
                 invest_msg += "• (Inga förslag)\n"
 
         # 6) Makrohändelse
         macro_msg = f"\n*Makrohändelse:* {macro_event}\n"
 
         # 7) Slå ihop all text till ett meddelande
         full_message = (
             f"{market_summary}"
             f"{risk_msg}"
             f"{portfolio_msg}"
             f"{invest_msg}"
             f"{macro_msg}"
         )
 
         # 8) Lägg till inline-knapp (exempel: Dashboard)
         reply_markup = {
             "inline_keyboard": [
                 [{"text": "Öppna Dashboard", "url": "https://example.com/dashboard"}]
             ]
         }
 
         send_telegram_message(full_message, reply_markup=reply_markup)
     except Exception as e:
         logging.error(f"❌ Fel vid skapande av full daily report: {str(e)}")
 
 # Nedan är de gamla funktionerna om du fortfarande vill använda dem separat
 def send_daily_market_report(market_data):
     ...
 def send_risk_alert(risk_level):
     ...
 def send_portfolio_update(portfolio_data):
     ...
 def send_macro_event_alert(event):
     ...
 def send_rl_backtest_summary(reward, final_value):
     ...
 
 if __name__ == "__main__":
     # Exempeldata för testkörning
     market_data = {
 @@ -205,17 +183,12 @@
         "sentiment": "Positiv",
     }
     risk_level = 0.06
     portfolio_data = {"Tesla": -0.05, "Apple": 0.02, "Amazon": 0.03}
     macro_event = "Fed höjde räntan med 0.25%."
     
     send_daily_market_report(market_data)
     send_risk_alert(risk_level)
     send_portfolio_update(portfolio_data)
     send_macro_event_alert(macro_event)
     send_ai_recommendations()
     send_rl_backtest_summary(12543.21, 108769.56)
     
     # Dynamiskt filnamn baserat på dagens datum (t.ex. reports/daily_report_2025-03-29.pdf)
 
     # Anropa vår nya funktion
     send_full_daily_report(market_data, risk_level, macro_event)
 
     # Skicka PDF om du vill
     today = datetime.today().strftime("%Y-%m-%d")
     file_path = f"reports/daily_report_{today}.pdf"
     send_pdf_report_to_telegram(file_path)
