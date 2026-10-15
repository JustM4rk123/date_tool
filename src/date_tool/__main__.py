"""Interactive command-line interface for Date Tool."""

import sys

import inflect
import questionary

from .controls import (
    BirthDate,
    CalendarDate,
    get_nationality,
    get_operator,
    validate_input,
    validate_positve,
)
from .operations import (
    TIME_UNITS,
    age_format,
    calculate_business_days,
    calculate_date,
    calculate_date_business_days,
    calculate_time,
)


def main() -> None:
    """Run the date tool's interactive menu."""
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
                parts = calculate_time(first, second)
                parts = [
                    f"{part} {p.plural(TIME_UNITS[i], {part})}"
                    for i, part in enumerate(parts)
                ]
                print(f"There are {p.join(parts)} between {first} and {second}")

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

                print(
                    f"The new date is: {calculate_date(start, operator, unit, change)}"
                )

            case "Calculate age":
                birthdate = validate_input(
                    lambda: BirthDate(input("Insert your birthday (YYYY-MM-DD): ")),
                    "Insert a valid birth date!",
                )

                extended = questionary.select(
                    "Which format do you want to visualize the age with?",
                    choices=["Years only", "Years, months and days"],
                ).ask()

                output = age_format(birthdate.age, extended)
                print(f"A person born on {birthdate} is {output} old")

            case "Calculate business days":
                if nationality is None:
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

                bus_days = calculate_business_days(start, end, nationality)
                verb = p.plural_verb("is", bus_days)
                noun = p.plural_noun("day", bus_days)
                print(
                    f"There {verb} {bus_days} business {noun} between {start} and {end}"
                )

            case "Add/subtract business days from a date":
                if nationality is None:
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

                new_date = calculate_date_business_days(
                    start, operator, change, nationality
                )
                print(f"The new date is: {new_date}")

            case "Exit":
                sys.exit("Program terminated")

        input("Press enter to continue...")


if __name__ == "__main__":
    main()
