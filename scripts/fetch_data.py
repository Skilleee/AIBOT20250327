# scripts/fetch_data.py

import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheets_client(json_keyfile_path: str):
    """
    Skapar och returnerar en gspread-klient via service account credentials.
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)
    return client

def fetch_portfolio_data(client, sheet_id: str, worksheet_name: str) -> list:
    """
    Hämtar alla rader från en viss flik (worksheet_name) i Google Sheets
    och returnerar en lista av listor (där varje inre lista är en hel rad).
    """
    try:
        sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
        rows = sheet.get_all_values()  # Hämtar ALLA celler i fliken
        logging.info(f"✅ Kalkylarket '{worksheet_name}' öppnades med Sheet ID: {sheet_id}")
        logging.info(f"✅ '{worksheet_name}' har {len(rows)} rader i Google Sheets.")
        return rows
    except Exception as e:
        logging.error(f"Kunde inte hämta data från worksheet '{worksheet_name}': {e}")
        return []

def parse_portfolio_rows(rows: list, account_name: str) -> list:
    """
    Tar in en lista av rader (från fetch_portfolio_data) och ett kontonamn.
    Returnerar en lista med dictionaries (en rad per innehav).
    
    Exempel på returdataset:
      [
        {
          "namn": "Tesla",
          "ticker": "TSLA",
          "antal": 6,
          "pris": 263.55,
          "valuta": "SEK",
          "total_värde": 1580.87,
          "typ": "Aktie",
          "kategori": "Tech",
          "konto": "Alice"
        },
        ...
      ]
    Används senare av AI-funktioner och/eller för att beräkna totalsummor.
    """
    parsed_data = []

    # Förväntad kolumnindelning (justera om ditt Google Sheet har annan ordning):
    #   0: Aktie/Fond/ETF
    #   1: Ticker
    #   2: Antal
    #   3: Kurs (SEK)
    #   4: Värde (SEK)
    #   5: Typ
    #   6: Kategori
    #   7: Konto
    #
    # Du kan anpassa index nedan efter hur ditt GSheet är upplagt.

    for i, row in enumerate(rows):
        # Hoppa över första raden om det är rubriker
        if i == 0:
            logging.info(f"[DEBUG] Hoppar över header-rad för konto '{account_name}'.")
            continue

        # Kolla att vi har minst 8 kolumner i row
        if len(row) < 8:
            logging.debug(f"[DEBUG] Raden saknar kolumner (har {len(row)}).")
            continue

        # Plocka ut råvärden
        namn = row[0].strip() if row[0] else ""
        ticker = row[1].strip() if row[1] else ""
        antal_str = row[2].strip() if row[2] else "0"
        kurs_str = row[3].strip() if row[3] else "0"
        total_str = row[4].strip() if row[4] else "0"
        typ = row[5].strip() if row[5] else ""
        kategori = row[6].strip() if row[6] else ""
        konto = row[7].strip() if row[7] else account_name  # fallback

        # Konvertera antal
        try:
            antal = float(antal_str.replace(",", "."))
        except ValueError:
            antal = 0.0

        # Konvertera kurs
        try:
            kurs = float(kurs_str.replace(",", "."))
        except ValueError:
            kurs = 0.0

        # Konvertera total_värde
        # Tar bort "kr", mellanslag och ersätter komma med punkt
        total_str = (total_str.replace("kr", "")
                                .replace(" ", "")
                                .replace(",", "."))
        try:
            total_värde = float(total_str)
        except ValueError:
            total_värde = 0.0

        item = {
            "namn": namn,
            "ticker": ticker,
            "antal": antal,
            "pris": kurs,
            "valuta": "SEK",       # Du kan hårdkoda om allt är i SEK
            "total_värde": total_värde,
            "typ": typ,
            "kategori": kategori,
            "konto": konto,
        }
        parsed_data.append(item)

    return parsed_data

def fetch_all_portfolios(json_keyfile_path: str, sheet_id: str) -> dict:
    """
    Liknande funktionen du hade i portfolio_google_sheets.py.
    Returnerar ett dict med portföljdata för dina konton.
    Exempel:
      {
        "Alice": [ {...}, {...} ],
        "Valter": [ {...}, ...],
        "Pension": [...],
        "Investeringskonto": [...]
      }
    """
    client = get_google_sheets_client(json_keyfile_path)

    accounts = ["Alice", "Valter", "Pension", "Investeringskonto"]
    portfolios = {}

    for acct in accounts:
        rows = fetch_portfolio_data(client, sheet_id, acct)
        parsed = parse_portfolio_rows(rows, acct)
        portfolios[acct] = parsed  # en lista av dictionaries

    return portfolios
