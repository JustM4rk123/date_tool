from datetime import date

import pytest
from dateutil.relativedelta import relativedelta

from date_tool import (
    BirthDate,
    CalendarDate,
    is_business_day,
    validate_input,
    validate_positve,
)


def test_calculate_age():
    today = date.today()
    assert BirthDate("2009-10-3").age == relativedelta(today, date(2009, 10, 3))
    assert BirthDate("1961-10-4").age == relativedelta(today, date(1961, 10, 4))
    assert BirthDate("2009-5-8").age == relativedelta(today, date(2009, 5, 8))


def test_invalid_calendar_date_raises_value_error():
    with pytest.raises(ValueError):
        CalendarDate("not-a-date")
    with pytest.raises(ValueError):
        CalendarDate("2026")


def test_is_business_day():
    assert not is_business_day(date(2026, 9, 7), "US")
    assert is_business_day(date(2026, 9, 8), "US")
    assert not is_business_day(date(2026, 5, 1), "IT")
    assert is_business_day(date(2026, 5, 4), "IT")
    assert not is_business_day(date(2025, 10, 3), "DE")
    assert is_business_day(date(2025, 10, 6), "DE")


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


@pytest.mark.parametrize("value", [-1, 0, -23])
def test_validate_positive_rejects_non_positive_values(value):
    with pytest.raises(ValueError):
        validate_positve(value)


@pytest.mark.parametrize("value", [2, 4, 23])
def test_validate_positive_accepts_positive_values(value):
    assert validate_positve(value) == value
