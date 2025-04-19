import calendar
import pandas as pd


def write_to_file(data: dict[str, int], filename: str):
    file = open(filename, "w")
    for item, ridership_num in data.items():
        file.write(f"{item}: {ridership_num}\n")
    file.close()


def get_ridership(year: int, item: str, data: pd.DataFrame, item_row: str) -> int:
    item_data: pd.DataFrame = data.mask(data[item_row] != item)
    item_data = item_data.dropna()
    ridership: float = 0

    for row in item_data.itertuples():
        match row.servicetype:
            case "WKD":
                ridership += (row.avgboardings * get_weekdays_in_month(year, int(row.month_)))
            case "SAT":
                ridership += (row.avgboardings * get_day_of_week_in_month(year, int(row.month_), 5))
            case "SUN":
                ridership += (row.avgboardings * get_day_of_week_in_month(year, int(row.month_), 6))

    return int(ridership / days_in_year(year))


def get_data_items(data: pd.DataFrame, item_row: str) -> set[str]:
    items: set[str] = set()
    for row in data.itertuples():
        items.add(row.__getattribute__(item_row))

    return items


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

def days_in_year(year: int) -> int:
    if year % 400 == 0:
        return 366
    elif year % 100 == 0:
        return 365
    elif year % 4 == 0:
        return 366
    return 365