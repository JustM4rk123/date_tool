from datetime import date

import pytest
from dateutil.relativedelta import relativedelta

from date_tool import (
    BirthDate,
    CalendarDate,
    age_format,
    calculate_business_days,
    calculate_date,
    calculate_date_business_days,
    calculate_time,
    is_business_day,
    validate_input,
    validate_positve,
)


def test_calculate_time():
    assert calculate_time(CalendarDate("2026-9-1"), CalendarDate("2026-8-25")) == (
        0,
        0,
        7,
    )
    assert calculate_time(CalendarDate("2026-8-25"), CalendarDate("2026-9-1")) == (
        0,
        0,
        7,
    )
    assert calculate_time(CalendarDate("2024-2-28"), CalendarDate("2025-4-1")) == (
        1,
        1,
        4,
    )
    assert calculate_time(CalendarDate("2025-2-28"), CalendarDate("2026-4-1")) == (
        1,
        1,
        4,
    )
    assert calculate_time(CalendarDate("2024-2-28"), CalendarDate("2024-3-1")) == (
        0,
        0,
        2,
    )
    assert calculate_time(CalendarDate("2025-2-28"), CalendarDate("2025-3-1")) == (
        0,
        0,
        1,
    )


def test_calculate_date():
    assert calculate_date(CalendarDate("2026-8-25"), "Add", "Days", 7) == "2026-9-1"
    assert (
        calculate_date(CalendarDate("2026-9-1"), "Subtract", "Days", 7) == "2026-8-25"
    )
    assert calculate_date(CalendarDate("2026-9-1"), "Add", "Months", 3) == "2026-12-1"
    assert (
        calculate_date(CalendarDate("2027-3-1"), "Subtract", "Months", 3) == "2026-12-1"
    )
    assert calculate_date(CalendarDate("2026-9-1"), "Add", "Years", 4) == "2030-9-1"
    assert (
        calculate_date(CalendarDate("2026-3-9"), "Subtract", "Years", 6) == "2020-3-9"
    )


def test_calculate_age():
    today = date.today()  # noqa: DTZ011
    assert BirthDate("2009-10-3").age == relativedelta(today, date(2009, 10, 3))
    assert BirthDate("1961-10-4").age == relativedelta(today, date(1961, 10, 4))
    assert BirthDate("2009-5-8").age == relativedelta(today, date(2009, 5, 8))


def test_age_format():
    # Test "Years only" with multiple years
    age1 = relativedelta(years=16, months=3, days=15)
    assert age_format(age1, "Years only") == "16 years"

    # Test "Years only" with singular year
    age2 = relativedelta(years=1, months=5, days=10)
    assert age_format(age2, "Years only") == "1 year"

    # Test "Years, months and days" with all non-zero values
    age3 = relativedelta(years=16, months=3, days=15)
    assert (
        age_format(age3, "Years, months and days") == "16 years, 3 months, and 15 days"
    )


def test_business_days():
    # A three-month US range: Labor Day, Columbus Day, Veterans Day, and
    # Thanksgiving are excluded along with weekends.
    assert (
        calculate_business_days(
            CalendarDate("2026-9-1"), CalendarDate("2026-12-1"), "US"
        )
        == 61
    )

    # Italian Labor Day (May 1) and the weekend are skipped.
    assert (
        calculate_business_days(
            CalendarDate("2026-4-30"), CalendarDate("2026-5-4"), "IT"
        )
        == 1
    )

    # German Unity Day (October 3) is skipped.
    assert (
        calculate_business_days(
            CalendarDate("2025-10-2"), CalendarDate("2025-10-6"), "DE"
        )
        == 1
    )


def test_calc_with_business():
    # Twenty US business days cross Thanksgiving and two weekends.
    assert calculate_date_business_days(
        CalendarDate("2026-11-20"), "Add", 20, "US"
    ) == date(2026, 12, 21)

    # Italian Labor Day is skipped.
    assert calculate_date_business_days(
        CalendarDate("2026-4-30"), "Add", 1, "IT"
    ) == date(2026, 5, 4)

    # German Unity Day and the weekend are skipped.
    assert calculate_date_business_days(
        CalendarDate("2025-10-2"), "Add", 1, "DE"
    ) == date(2025, 10, 6)


def test_holiday():
    assert not is_business_day(date(2026, 9, 7), "US")  # Labor Day
    assert is_business_day(date(2026, 9, 8), "US")

    assert not is_business_day(date(2026, 5, 1), "IT")  # Italian Labor Day
    assert is_business_day(date(2026, 5, 4), "IT")

    assert not is_business_day(date(2025, 10, 3), "DE")  # German Unity Day
    assert is_business_day(date(2025, 10, 6), "DE")


def test_invalid_calendar_date_raises_value_error():
    with pytest.raises(ValueError):
        CalendarDate("not-a-date")
    with pytest.raises(ValueError):
        CalendarDate("2026")


def test_validate_input_prints_error_and_retries(monkeypatch, capsys):
    answers = iter(["not-a-date", "2026-09-03"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    result = validate_input(
        lambda: CalendarDate(input("Enter a date (YYYY-MM-DD): ")),
        "Insert a valid date!",
    )

    captured = capsys.readouterr()
    assert captured.out == "Insert a valid date!\n"
    assert str(result) == "2026-09-03"


def test_validate_positive():
    with pytest.raises(ValueError):
        validate_positve(-1)
        validate_positve(0)
        validate_positve(-23)

    assert validate_positve(2) == 2
    assert validate_positve(4) == 4
    assert validate_positve(23) == 23
