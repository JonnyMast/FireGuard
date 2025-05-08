from frcm.datamodel.model import FireRiskPrediction
import datetime


def calculate_minimum_ttf(prediction: FireRiskPrediction) -> float:
    """
    Calculate the minimum time to flashover (TTF) from a FireRiskPrediction.
    """
    return min(risk.ttf for risk in prediction.firerisks)


def normalize_max_fire_risk_value(ttf: float) -> float:
    """
    Normalize TTF to a value between 0 (high risk) and 1 (low risk).
    Assumes critical threshold is around 4.0–6.5 hours.
    """
    scaled = (ttf - 4.0) / 2.5
    return max(0, min(scaled, 1))


def timedelta_days(days: int) -> datetime.timedelta:
    """
    Utility to return a timedelta for the given number of days.
    """
    return datetime.timedelta(days=days)
