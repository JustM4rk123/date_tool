from datetime import date

from dateutil.relativedelta import relativedelta

from date_tool import (
    CalendarDate,
    age_format,
    calculate_business_days,
    calculate_date,
    calculate_date_business_days,
    calculate_time,
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


def test_age_format():
    assert age_format(
        relativedelta(years=16, months=3, days=15), "Years only"
    ) == "16 years"
    assert age_format(
        relativedelta(years=1, months=5, days=10), "Years only"
    ) == "1 year"
    assert (
        age_format(
            relativedelta(years=16, months=3, days=15), "Years, months and days"
        )
        == "16 years, 3 months, and 15 days"
    )


def test_business_days():
    assert (
        calculate_business_days(
            CalendarDate("2026-9-1"), CalendarDate("2026-12-1"), "US"
        )
        == 61
    )
    assert (
        calculate_business_days(
            CalendarDate("2026-4-30"), CalendarDate("2026-5-4"), "IT"
        )
        == 1
    )
    assert (
        calculate_business_days(
            CalendarDate("2025-10-2"), CalendarDate("2025-10-6"), "DE"
        )
        == 1
    )


def test_calc_with_business():
    assert calculate_date_business_days(
        CalendarDate("2026-11-20"), "Add", 20, "US"
    ) == date(2026, 12, 21)
    assert calculate_date_business_days(
        CalendarDate("2026-4-30"), "Add", 1, "IT"
    ) == date(2026, 5, 4)
    assert calculate_date_business_days(
        CalendarDate("2025-10-2"), "Add", 1, "DE"
    ) == date(2025, 10, 6)
