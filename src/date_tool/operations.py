"""Functions that calculate and format date intervals."""

from datetime import date, timedelta

import inflect
from dateutil.relativedelta import relativedelta

from .controls import CalendarDate, is_business_day

TIME_UNITS = ["year", "month", "day"]
"""Time units used by the date and age formatting functions."""


def calculate_time(start: CalendarDate, end: CalendarDate) -> tuple[int, int, int]:
    """Calculate the interval between two dates in years, months, and days."""
    if start.date < end.date:
        start, end = end, start
    difference = relativedelta(start.date, end.date)
    return difference.years, difference.months, difference.days


def calculate_date(start: CalendarDate, operator: str, unit: str, change: int) -> str:
    """Add or subtract years, months, or days from a date."""
    match unit:
        case "Years":
            delta = relativedelta(years=change)
        case "Months":
            delta = relativedelta(months=change)
        case "Days":
            delta = relativedelta(days=change)
        case _:
            raise ValueError
    if operator == "Add":
        new = start.date + delta
    elif operator == "Subtract":
        new = start.date - delta
    else:
        raise ValueError

    return f"{new.year}-{new.month}-{new.day}"


def age_format(age: relativedelta, extended: str) -> str:
    """Format an age as years only or as years, months, and days."""
    p = inflect.engine()

    match extended:
        case "Years only":
            years = age.years
            return f"{years} {p.plural('year', years)}"
        case "Years, months and days":
            parts = (age.years, age.months, age.days)
            words = [
                f"{part} {p.plural(TIME_UNITS[idx], part)}"
                for idx, part in enumerate(parts)
            ]
            return p.join(words)
        case _:
            raise ValueError


def calculate_business_days(
    start: CalendarDate, end: CalendarDate, nationality: str
) -> int:
    """Count business days after the start date through the end date."""
    if end.date < start.date:
        start, end = end, start

    difference = end.date - start.date

    business_days = 0
    for i in range(1, difference.days + 1):
        current = start.date + timedelta(days=i)
        if is_business_day(current, nationality):
            business_days += 1

    return business_days


def calculate_date_business_days(
    start: CalendarDate, operator: str, change: int, nationality: str
) -> date:
    """Add or subtract a number of business days from a date."""
    if operator == "Add":
        direction = 1
    elif operator == "Subtract":
        direction = -1
    else:
        raise ValueError

    current = start.date
    business_days = 0
    while business_days < change:
        current += timedelta(days=direction)
        if is_business_day(current, nationality):
            business_days += 1

    return current
