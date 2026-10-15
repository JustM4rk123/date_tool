"""Date parsing, validation, and interactive selection helpers."""

import re
from collections.abc import Callable
from datetime import date
from typing import TypeVar

import holidays
import questionary
from dateutil.relativedelta import relativedelta

T = TypeVar("T")


class CalendarDate:
    """A calendar date parsed from a YYYY-MM-DD string."""

    def __init__(self, date_string: str):
        if matches := re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", date_string):
            self.tuple = tuple(map(int, matches.groups()))
            self.date = date(*self.tuple)
        else:
            raise ValueError

    def __str__(self) -> str:
        return f"{self.date}"


class BirthDate(CalendarDate):
    """A calendar date of birth with the person's calculated age."""

    def __init__(self, date_string: str):
        super().__init__(date_string)
        today = date.today()
        if today < self.date:
            raise ValueError
        self.age = relativedelta(today, self.date)


HOLIDAY_COUNTRIES = {
    "Italy": "IT",
    "United States": "US",
    "United Kingdom": "GB",
    "Canada": "CA",
    "Australia": "AU",
    "Germany": "DE",
    "France": "FR",
    "Spain": "ES",
    "Japan": "JP",
    "South Korea": "KR",
    "China": "CN",
    "Russia": "RU",
}


def is_business_day(date_obj: date, nationality: str) -> bool:
    """Return whether a date is a weekday that is not a national holiday."""
    return not (
        date_obj.weekday() > 4 or date_obj in holidays.country_holidays(nationality)
    )


def validate_input(func: Callable[[], T], error_str: str) -> T:
    """Call a function until it returns a value without raising ValueError."""
    while True:
        try:
            value = func()
        except ValueError:
            print(error_str)
        else:
            return value


def validate_positve(n: int) -> int:
    """Return a positive integer or raise ValueError."""
    if n <= 0:
        raise ValueError
    return n


def get_operator() -> str:
    """Prompt the user to choose addition or subtraction."""
    return questionary.select(
        "Do you want to add or subtract? ", choices=["Add", "Subtract"]
    ).ask()


def get_nationality() -> str:
    """Prompt the user to choose a country and return its ISO code."""
    nationality = questionary.select(
        "Pick your nationality: ", choices=[country for country in HOLIDAY_COUNTRIES]
    ).ask()
    return HOLIDAY_COUNTRIES[nationality]
