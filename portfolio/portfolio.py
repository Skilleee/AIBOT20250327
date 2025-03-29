import logging
from .sheet_api import read_portfolio_data_from_sheets

logger = logging.getLogger(__name__)

def parse_portfolio_data(raw_data, account_name):
    """
    Tar in rådata (inkl. header-raden) och returnerar en lista av dictar
    med nycklar för instrument, ticker, antal, kurs, värde, typ, kategori och konto.
    """
    portfolio_data = []
    for i, row in enumerate(raw_data):
        # Hoppa över header-raden (första raden)
        if i == 0:
            logger.info("[DEBUG] Hoppar över header-rad '%s' för konto '%s'.", row, account_name)
            continue

        logger.info("[DEBUG] Parsing rad för konto '%s': %s", account_name, row)

        # Försök parsa kolumnerna enligt förväntad ordning:
        # 0: instrument_name, 1: ticker, 2: antal, 3: kurs, 4: värde, 5: typ, 6: kategori, 7: konto
        try:
            instrument_name = row[0]
            ticker = row[1]
            shares = float(row[2].replace(",", "."))  # Om du har svenska kommatecken
            price = float(row[3].replace(",", "."))
            value = float(row[4].replace(",", "."))
            instrument_type = row[5]
            category = row[6]
            account = row[7]

            portfolio_data.append({
                "instrument_name": instrument_name,
                "ticker": ticker,
                "shares": shares,
                "price": price,
                "value": value,
                "type": instrument_type,
                "category": category,
                "account": account
            })
        except (IndexError, ValueError) as e:
            logger.warning(
                "Kunde inte parsa rad för konto '%s': %s. Rad: %s",
                account_name, e, row
            )

    return portfolio_data


def read_all_portfolios(service, sheet_id, accounts):
    """
    Läser in portföljdata för en lista av konton (t.ex. ["Alice", "Valter", "Pension", ...])
    och returnerar en gemensam lista av parsed data.
    """
    all_data = []
    for account in accounts:
        raw_data = read_portfolio_data_from_sheets(service, sheet_id, account)
        parsed_data = parse_portfolio_data(raw_data, account)
        all_data.extend(parsed_data)

    return all_data


def calculate_total_portfolio_value_by_account(portfolio_data):
    """
    Summerar total portföljvolym per konto och returnerar en dict:
    {
      "Alice": <summa>,
      "Valter": <summa>,
      ...
    }
    """
    total_values_by_account = {}
    for item in portfolio_data:
        account = item["account"]
        total_values_by_account[account] = (
            total_values_by_account.get(account, 0.0) + item["value"]
        )
    return total_values_by_account
