"""
Utilities for performing calculation with dates

This module provides the following features:
1- Calculating time between two dates
2- Manipulating a date by adding or removing
    a certain quantity and unit of time (years, months or days)
3- Calculate age
4- Calculating business days between two dates
5- Manipulating a date by adding or removing business days
"""

import re
import sys
from datetime import date, timedelta

import holidays
import inflect
import questionary
from dateutil.relativedelta import relativedelta


class CalendarDate:
    """
    Represents a calendar date parsed from a YYYY-MM-DD string.

    :param date_string: A date in YYYY-MM-DD format.
    :type date_string: str
    :raises ValueError: If the date string does not match the expected
        format or contains an invalid date.
    :ivar tuple: The date represented as a (year, month, day) tuple.
    :vartype tuple: tuple[int, int, int]
    :ivar date: The date as a :class:`datetime.date` object.
    :vartype date: datetime.date
    """

    # Store a date parsed from a YYYY-MM-DD string.
    def __init__(self, date_string: str):
        # datetime.date validates the resulting year, month, and day.
        if matches := re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", date_string):
            self.tuple = tuple(map(int, matches.groups()))
            self.date = date(*self.tuple)
        else:
            raise ValueError

    def __str__(self):
        """
        Return the date in ISO 8601 format.

        :return: The date formatted as YYYY-MM-DD.
        :rtype: str
        """
        # Use Python's ISO date representation for display.
        return f"{self.date}"


class BirthDate(CalendarDate):
    """
    Represents a person's birth date and calculate their age
    Inherits the date parsing and validation of :class:`CalendarDate`.

    :param date_string: A date in ISO 8601 format that represent
        a person's birth date
    :type date_string: str
    :raise ValueError: if date is invalid or hasn't occurred yet
    :ivar age: Represents the person's age as a
        :class:`dateutil.relativedelta.relativedelta` object
    :vartype age: relativedelta
    """

    def __init__(self, date_string: str):
        super().__init__(date_string)
        today = date.today()  # noqa: DTZ011
        # A date of birth cannot be in the future.
        if today < self.date:
            raise ValueError
        else:
            self.age = relativedelta(today, self.date)


TIME_UNITS = ["year", "month", "day"]
"""Time units used by the calculate_date function"""

# Country labels for the menu and their ISO codes for the holidays library.
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
"""Mapping of country names to ISO country codes used by the holidays library"""


def main():
    """
    Run the date tool's interactive menu

    Guides the user
    """
    nationality = None
    p = inflect.engine()

    print("=" * 45)
    print(f"{'DATE TOOL':^45}")
    print("=" * 45)
    while True:
        print()
        choice = questionary.select(
            "What do you want to do? ",
            choices=[
                "Calculate time between two dates",
                "Add/subtract time from a date",
                "Calculate age",
                "Calculate business days",
                "Add/subtract business days from a date",
                "Exit",
            ],
        ).ask()

        match choice:
            case "Calculate time between two dates":
                first = validate_input(
                    lambda: CalendarDate(input("Enter the first date (YYYY-MM-DD): ")),
                    "Insert a valid date!",
                )
                second = validate_input(
                    lambda: CalendarDate(input("Enter the second date (YYYY-MM-DD): ")),
                    "Insert a valid date!",
                )
                parts = calculate_time(first, second)  # type: ignore
                # Use the correct singular or plural form for each unit.
                parts = [f"{part} {p.plural(TIME_UNITS[i], {part})}" for i, part in enumerate(parts)]  # type: ignore
                print(f"There are {p.join(parts)} between {first} and {second}")  # type: ignore

            case "Add/subtract time from a date":
                start = validate_input(
                    lambda: CalendarDate(
                        input("Insert the start date (YYYY-MM-DD): ").strip()
                    ),
                    "Insert a valid date!",
                )

                operator = get_operator()

                unit = questionary.select(
                    "Which time unit do you want to use?",
                    choices=["Years", "Months", "Days"],
                ).ask()

                change = validate_input(
                    lambda: validate_positve(int(input("How many? "))),
                    "Insert a positive integer!",
                )

                print(f"The new date is: {calculate_date(start, operator, unit, change)}")  # type: ignore

            case "Calculate age":
                birthdate = validate_input(
                    lambda: BirthDate(input("Insert your birthday (YYYY-MM-DD): ")),
                    "Insert a valid birth date!",
                )

                extended = questionary.select(
                    "Which format do you want to visualize the age with?",
                    choices=["Years only", "Years, months and days"],
                ).ask()

                output = age_format(birthdate.age, extended)  # type: ignore

                print(f"A person born on {birthdate} is {output} old")

            case "Calculate business days":
                if nationality == None:
                    nationality = get_nationality()

                start = validate_input(
                    lambda: CalendarDate(
                        input("Insert the starting date (YYYY-MM-DD): ")
                    ),
                    "Insert a valid date!",
                )
                end = validate_input(
                    lambda: CalendarDate(input("Insert the end date (YYYY-MM-DD): ")),
                    "Insert a valid date!",
                )

                bus_days = calculate_business_days(start, end, nationality)  # type: ignore

                print(f"There {p.plural_verb("is", bus_days)} {bus_days} business {p.plural_noun("day", bus_days)} between {start} and {end}")  # type: ignore
            case "Add/subtract business days from a date":
                if nationality == None:
                    nationality = get_nationality()

                start = validate_input(
                    lambda: CalendarDate(
                        input("Insert the starting date (YYYY-MM-DD): ")
                    ),
                    "Insert a valid date!",
                )

                operator = get_operator()

                change = validate_input(
                    lambda: validate_positve(int(input("How many business days? "))),
                    "Insert a positive integer!",
                )

                new_date = calculate_date_business_days(start, operator, change, nationality)  # type: ignore

                print(f"The new date is: {new_date}")

            case "Exit":
                sys.exit("Program terminated")

        input("Press enter to continue...")


def calculate_time(start: CalendarDate, end: CalendarDate) -> tuple[int, int, int]:
    """
    Calculates the time between two date

    :param first: the start date,
        represented by a :class:`CalendarDate` object
    :param second: the end date,
        represented by a :class:`CalendarDate` object
    :return: a tuple containing the difference in years + months + days
    """

    # Normalize input order so the interval is always non-negative.
    if start.date < end.date:
        start, end = end, start
    # relativedelta preserves calendar units instead of returning total days.
    difference = relativedelta(start.date, end.date)
    return difference.years, difference.months, difference.days


def calculate_date(start: CalendarDate, operator: str, unit: str, change: int) -> str:
    """
    Adds or subtracts time from a date

    :param start: The original :class:`CalendarDate` object
    :param operator: a string which's value decides
        if the function returns and addiction or a subtraction
    :param unit: a string that which's value decides the unit of the operation
    :param change: a positive number quantifying time being added or subtracted
    :return: a string in ISO 8061 date format containing the resulting date
    """

    # relativedelta handles variable month lengths and leap years.
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
    """
    Returns either the age in years or
        the age in years, months and days
    :param age: a :class:`dateutil.relativedelta.relativedelta`
        representing the person's age
    :param extended: a string which's value decides the format to be returned
    :return: a string containing the age format
    """

    p = inflect.engine()

    match extended:
        case "Years only":
            years = age.years
            return f"{years} {p.plural('year', years)}"  # type: ignore
        case "Years, months and days":
            parts = (age.years, age.months, age.days)
            words = [f"{part} {p.plural(TIME_UNITS[idx], part)}" for idx, part in enumerate(parts)]  # type: ignore
            return p.join(words)  # type: ignore
        case _:
            raise ValueError


def calculate_business_days(
    start: CalendarDate, end: CalendarDate, nationality: str
) -> int:
    """
    Similiarly to :func:`calculate_time`, calculates the time
        between two dates, but using business days as the time unit

    :param start: the first date,
        represented by a :class:`CalendarDate` object
    :param end: the second date,
        represented by a :class:`CalendarDate` object
    :return: an integer containing the number of business days
    """

    if end.date < start.date:
        start, end = end, start

    difference = end.date - start.date

    business_days = 0
    for i in range(1, difference.days + 1):
        current = start.date + (timedelta(days=i))
        if is_business_day(current, nationality):
            business_days += 1

    return business_days


def calculate_date_business_days(
    start: CalendarDate, operator: str, change: int, nationality: str
) -> date:
    """
    Similiar to :func:`calculate_date`, but uses
        business days as the time unit

    :param start: The original :class:`CalendarDate` object
    :param operator: a string which's value decides
        if the function returns and addiction or a subtraction
    :param change: a positive number quantifying time being added or subtracted
    :return: a string in ISO 8061 date format containing the resulting date
    """

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


def is_business_day(date_obj: date, nationality: str) -> bool:
    """
    Checks whether a date is a business day or not

    :param date_obj: A :class:`datetime.date` representing the date to parse
    :param nationality: a str containing a country's ISO code,
        used by the holidays library to know which nation's holidays to use
    :return: A boolean value that answers the question 'is today a business day'?
    """
    return not (
        date_obj.weekday() > 4 or date_obj in holidays.country_holidays(nationality)
    )


def validate_input(func, error_str: str) -> str:
    """
    Prompts for a value until a valid one is inserted

    :param func: The function with argument the value to validate
    :param error_str: The string that gets printed when the current value isn't valid
    :raises ValueError: if the value is invalid
    :return: the return value of func
    """

    while True:
        try:
            value = func()
        except ValueError:
            print(error_str)
        else:
            return value


def validate_positve(n: int) -> int:
    """
    Checks whether an integer is positive

    :param n: the integer that needs to be parsed
    :raise ValueError: if the number isn't positive
    :return: the number given as an argument
    """

    if n <= 0:
        raise ValueError
    return n


def get_operator() -> str:
    """
    Prompts the user to select an operator
        for the :func:`calculate_date` and :func:`calculate_date_business_days`

    :return: the chosen option
    """

    return questionary.select(
        "Do you want to add or subtract? ", choices=["Add", "Subtract"]
    ).ask()


def get_nationality() -> str:
    """
    Prompts the user to select a nationality from a list

    :return: the chosen option
    """
    nationality = questionary.select(
        "Pick your nationality: ", choices=[country for country in HOLIDAY_COUNTRIES]
    ).ask()
    return HOLIDAY_COUNTRIES[nationality]


if __name__ == "__main__":
    main()
