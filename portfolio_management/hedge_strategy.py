import logging
from typing import Union, Dict

# Konfigurera loggning
logging.basicConfig(
    filename="hedge_strategy.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def hedge_strategy(risk_level: Union[float, int, None]) -> Dict[str, Union[str, float]]:
    """
    Föreslår hedge-strategier baserat på portföljens risknivå.
    
    Parametrar:
        risk_level (float): Risknivå mellan 0.0 och 1.0

    Returnerar:
        dict: En dictionary med strategiförslag och metadata.
    """
    try:
        # Grundläggande validering
        if risk_level is None:
            logging.warning("⚠️ Ingen risknivå angiven.")
            return {"strategy": "Ingen strategi", "reason": "Risknivå saknas"}

        if not isinstance(risk_level, (float, int)):
            logging.warning("⚠️ Ogiltig datatyp för risknivå.")
            return {"strategy": "Ingen strategi", "reason": "Ogiltig datatyp"}

        if not (0.0 <= risk_level <= 1.0):
            logging.warning("⚠️ Risknivå utanför tillåtet intervall.")
            return {"strategy": "Ingen strategi", "reason": "Risknivå utanför intervall"}

        # Strategiutvärdering
        if risk_level > 0.7:
            hedge = "Öka exponering mot guld, obligationer och defensiva sektorer."
        elif risk_level < 0.3:
            hedge = "Öka aktieexponering i cykliska sektorer."
        else:
            hedge = "Behåll en neutral balans mellan aktier och säkra tillgångar."

        logging.info(f"✅ Hedge-strategi vald för risknivå {risk_level:.2f}: {hedge}")
        return {
            "strategy": hedge,
            "risk_level": round(risk_level, 2),
            "status": "ok"
        }

    except Exception as e:
        logging.error(f"❌ Fel vid analys av hedge-strategi: {str(e)}")
        return {
            "strategy": "Ingen strategi",
            "error": str(e),
            "status": "error"
        }

# Exempelanrop
if __name__ == "__main__":
    test_risks = [0.8, 0.5, 0.2, None, "high", -0.1]

    for risk in test_risks:
        result = hedge_strategy(risk)
        print(f"🛡 Risknivå: {risk} → Strategi: {result['strategy']}")
