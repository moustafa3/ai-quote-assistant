from app.domain.entities import QuoteItem


def calculate_subtotal(items: list[QuoteItem]) -> float:
    """
    Calculate quote subtotal before discount.
    """
    return round(sum(item.total for item in items), 2)


def calculate_discount_amount(subtotal: float, discount_rate: float) -> float:
    """
    Calculate discount amount from subtotal and discount rate.
    """
    return round(subtotal * discount_rate, 2)


def calculate_total(subtotal: float, discount_amount: float) -> float:
    """
    Calculate final draft total after discount.
    """
    return round(subtotal - discount_amount, 2)