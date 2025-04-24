import calendar
import re
import pandas as pd


def write_to_file(data: dict[str, int], filename: str, item_name: str):
    file = open(filename, "w")
    file.write(f"{item_name},Ridership\n")
    for item, ridership_num in data.items():
        file.write(f"{item},{ridership_num}\n")
    file.close()


def get_ridership(year: int, item: str, data: pd.DataFrame, item_row: str, division_period: int, use_regex: bool) -> int:
    ridership: float = 0

    if use_regex:
        item_data = data[data[item_row].str.contains(item, regex=False)]
    else:
        item_data: pd.DataFrame = data.mask(data[item_row] != item)
        item_data = item_data.dropna()

    for row in item_data.itertuples():
        # Convert month if needed
        month: int | str | float = row.month_
        if isinstance(month, str):
            month = month_to_int(month)
        elif isinstance(month, float):
            month = int(month)

        # Convert boardings if needed
        boardings: float | str = row.avgboardings
        if isinstance(boardings, str):
            boardings = re.sub(",", "", boardings)
            boardings: float = float(boardings)

        match row.servicetype:
            case "WKD":
                ridership += (boardings * get_weekdays_in_month(year, month))
            case "SAT":
                ridership += (boardings * get_day_of_week_in_month(year, month, 5))
            case "SUN":
                ridership += (boardings * get_day_of_week_in_month(year, month, 6))

    return int(ridership / division_period)


def get_data_items(data: pd.DataFrame, item_row: str) -> set[str]:
    items: set[str] = set()
    for row in data.itertuples():
        items.add(row.__getattribute__(item_row))

    return items


def get_days_in_month(year: int, month: int) -> int:
    match month:
        case 1 | 3 | 5 | 7 | 8 | 10 | 12:
            return 31
        case 2:
            if get_days_in_year(year) != 365:
                return 29
            return 28
        case 4 | 6 | 9 | 11:
            return 30

    raise ValueError("Integer must correspond to month!")


def get_weekdays_in_month(year: int, month: int) -> int:
    cal: calendar.Calendar = calendar.Calendar()
    weekdays: int = 0

    # Calculate number of weekdays
    for date in cal.itermonthdates(year, month):
        if date.weekday() < 5:
            weekdays += 1

    return weekdays


def get_day_of_week_in_month(year: int, month: int, day: int) -> int:
    cal: calendar.Calendar = calendar.Calendar()
    days: int = 0

    # Calculate number of weekdays
    for date in cal.itermonthdates(year, month):
        if date.weekday() is day:
            days += 1

    return days


def get_days_in_year(year: int) -> int:
    if year % 400 == 0:
        return 366
    elif year % 100 == 0:
        return 365
    elif year % 4 == 0:
        return 366
    return 365


def int_to_month(month: int) -> str:
    match month:
        case 1:
            return "January"
        case 2:
            return "February"
        case 3:
            return "March"
        case 4:
            return "April"
        case 5:
            return "May"
        case 6:
            return "June"
        case 7:
            return "July"
        case 8:
            return "August"
        case 9:
            return "September"
        case 10:
            return "October"
        case 11:
            return "November"
        case 12:
            return "December"

    raise ValueError("Integer must correspond to month!")


def month_to_int(month: str) -> int:
    match month:
        case "January":
            return 1
        case "February":
            return 2
        case "March":
            return 3
        case "April":
            return 4
        case "May":
            return 5
        case "June":
            return 6
        case "July":
            return 7
        case "August":
            return 8
        case "September":
            return 9
        case "October":
            return 10
        case "November":
            return 11
        case "December":
            return 12

    raise ValueError(f"{month} is not a month!")