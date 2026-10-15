# Date Tool

#### Video demo: https://youtu.be/0-MhMSnq_6A

## Description

**Date Tool** is a command-line program for performing common date-related calculations. It provides an interactive menu with options to:

1. Calculate the time between two dates.
2. Add or subtract years, months, or days from a date.
3. Calculate a person's age.
4. Calculate the number of business days between two dates.
5. Add or subtract business days from a date.

The project is designed to simplify date calculations involving calendar dates, including leap years and months of different lengths. Dates are entered in the `YYYY-MM-DD` format, also known as ISO 8601 format, and are validated before any calculation is performed.

The menu interface is implemented with the `questionary` library, which allows users to navigate the available options directly in the terminal.

## Installation

This project requires **Python 3**. If Python is not installed, download it from the [official Python website](https://www.python.org/downloads/).

Download or clone the project repository, then navigate to its directory in a terminal.

## Setup

The project depends on the following third-party packages:

- `holidays`
- `inflect`
- `questionary`
- `python-dateutil`

Install the package and its runtime dependencies with:

```console
python -m pip install .
```

To install the test dependency as well, use `python -m pip install ".[test]"`.

## Usage

Run the program from the project directory with:

```console
python -m date_tool
```

After installation, the `date-tool` command can also be used.

The program displays an interactive menu with the following options:

1. **Calculate time between two dates**
2. **Add/subtract time from a date**
3. **Calculate age**
4. **Calculate business days**
5. **Add/subtract business days from a date**
6. **Exit**

Each option except **Exit** prompts the user for the information required to perform the selected calculation.

If the input is invalid, the program prints an error message and prompts the user again. For example, if the program requests a date in `YYYY-MM-DD` format and the user enters `dog` or an invalid date such as `2026-02-31`, the program prints `Insert a valid date!` and asks for another input.

## Package structure

The package is in `src/date_tool/`. Its `__main__.py` contains the interactive
menu, `operations.py` contains date calculations and formatting, and
`controls.py` contains date parsing, validation, and selection helpers.

### `CalendarDate`

The `CalendarDate` class represents a date provided as a string in `YYYY-MM-DD` format. A regular expression checks the format and extracts the year, month, and day. The parsed values are then used to create a `datetime.date` object, which rejects dates that do not exist. The values are also stored as a tuple.

### `BirthDate`

The `BirthDate` class inherits from `CalendarDate` and adds functionality for dates of birth. It rejects dates in the future and calculates the person's age, storing it as an instance variable of type `dateutil.relativedelta.relativedelta`.

### Date calculations

The `calculate_time()` function determines the difference between two dates in years, months, and days. It accepts two `CalendarDate` objects and returns a tuple containing three integers. The `relativedelta` class is used to account for leap years and months of different lengths.

The `calculate_date()` function adds or subtracts a specified number of years, months, or days from a date. It accepts the following arguments:

- `start`: a `CalendarDate` object
- `operator`: a `str` containing `Add` or `Subtract`
- `unit`: a `str` containing `Years`, `Months`, or `Days`
- `change`: a positive `int`

To calculate a person's age, the program creates a `BirthDate` object and asks whether the user wants to see the age in years only or in years, months, and days. The `BirthDate` object's `age` attribute and the user's choice are passed to `age_format()`, which returns the age in the selected format.

### Business-day calculations

The program also supports calculations involving business days. The `is_business_day()` function checks whether a date is a business day in a selected country. It excludes weekends and holidays for the chosen country, represented by its ISO country code and handled by the `holidays` package.

The `calculate_business_days()` and `calculate_date_business_days()` functions provide business-day calculations similar to `calculate_time()` and `calculate_date()`. Their implementations differ because they iterate through dates one day at a time.

`calculate_business_days()` loops from the day after the start date through the end date, counting each date for which `is_business_day()` returns `True`.

`calculate_date_business_days()` does not require a `unit` parameter because its unit is always business days. It moves forward or backward one calendar day at a time until it has reached the requested number of business days.

### Input validation and menus

The module includes input-validation functions such as `validate_input()`, which repeatedly calls a function until it returns a valid value, and `validate_positve()`, which raises a `ValueError` when the supplied integer is not positive.

The `get_operator()` function displays a menu for choosing whether to add or subtract time. The `get_nationality()` function displays a menu of countries supported by the `holidays` package. These functions are used by the regular and business-day date calculations.

## Testing

Automated tests are in `tests/`. Run them with:

```console
python -m pytest
```

The tests cover date calculations and manipulation, age calculation and formatting, business-day calculations, holiday handling, and input validation. The test suite uses `pytest`, with separate test functions for each major feature.

Date calculations are tested with different dates and date orders to ensure consistent results. Business-day calculations are tested for multiple countries, including the United States, Germany, and Italy, to verify that weekends and national holidays are excluded. Input validation is tested by checking that the appropriate errors are raised. The `validate_input()` function is also tested with `pytest`'s `monkeypatch` and `capsys` fixtures to simulate user input and verify the resulting error message.

## Design choices

Two important design choices were the `CalendarDate` and `BirthDate` classes. They centralize date parsing and validation for use throughout the program.

The project also uses third-party packages for specific purposes:

- `dateutil` provides `relativedelta`, which simplifies calculations involving years, months, and days.
- `questionary` provides interactive terminal menus and handles the resulting input.
- `inflect` handles singular and plural forms, including the years, months, and days returned by the date calculations.
- `holidays` allows `is_business_day()` to account for national holidays in multiple countries.
