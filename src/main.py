import sys, calendar
import pandas as pd

def main():
    # Process and mask data
    cmd_args: list[str] = sys.argv
    ridership_data: pd.DataFrame = pd.read_csv(cmd_args[1])
    ridership_data.mask(ridership_data["year_"] != int(cmd_args[2]), inplace=True)
    ridership_data.dropna(inplace=True)
    station_ridership: dict[str, int] = calculate_data(cmd_args, ridership_data)
    write_to_file(station_ridership)

def calculate_data(cmd_args: list[str], data: pd.DataFrame) -> dict[str, int]:
    station_ridership: dict[str, int] = {}

    # Mask data if not explicitly requested
    if not cmd_args.__contains__("--include-frontrunner"):
        data.mask(data["route"] == "FrontRunner", inplace=True)
    if not cmd_args.__contains__("--include-s-line"):
        data.mask(data["route"] == "S-Line", inplace=True)
    data.dropna(inplace=True)

    stations: set[str] = get_stations(data)

    for station in stations:
        station_ridership.update({station: get_station_ridership(int(cmd_args[2]), station, data)})

    return station_ridership

def write_to_file(ridership: dict[str, int]):
    file = open("ridership.txt", "w")
    for station, ridership_num in ridership.items():
        file.write(f"{station}: {ridership_num}\n")
    file.close()

def get_stations(data: pd.DataFrame) -> set[str]:
    stations: set[str] = set()
    for row in data.iterrows():
        stations.add(row[1]["stopname"])

    return stations

def get_station_ridership(year: int, station: str, data: pd.DataFrame) -> int:
    station_data: pd.DataFrame = data.mask(data["stopname"] != station)
    station_data.dropna(inplace=True)
    ridership: float = 0

    for row in station_data.iterrows():
        match row[1]["servicetype"]:
            case "WKD":
                ridership += (row[1]["avgboardings"] * get_weekdays_in_month(year, int(row[1]["month_"])))
            case "SAT":
                ridership += (row[1]["avgboardings"] * get_day_of_week_in_month(year, int(row[1]["month_"]), 5))
            case "SUN":
                ridership += (row[1]["avgboardings"] * get_day_of_week_in_month(year, int(row[1]["month_"]), 6))

    return int(ridership / days_in_year(year))

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
    if year % 400 is 0:
        return 366
    elif year % 100 is 0:
        return 365
    elif year % 4 is 0:
        return 366
    return 365

if __name__ == "__main__":
    main()