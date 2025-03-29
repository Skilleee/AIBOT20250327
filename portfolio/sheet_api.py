import logging

import google.auth
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

def read_portfolio_data_from_sheets(service, sheet_id, account_name):
    """
    Hämtar rådata från Google Sheets för ett visst konto (flik).
    Returnerar en lista av listor, där varje inre lista motsvarar en rad.
    Första raden är header-raden.
    """
    sheet = service.spreadsheets()
    # Justera kolumn-intervall om du har fler kolumner än H
    range_name = f"{account_name}!A1:H"
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    data = result.get("values", [])

    logger.info("Konto '%s' har %d rader i Google Sheets.", account_name, len(data))
    for row in data:
        logger.info("[DEBUG] Rå data för konto '%s': %s", account_name, ", ".join(row))

    # Returnera alla rader (inklusive header-raden)
    return data
