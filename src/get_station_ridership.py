import sys
import pandas as pd

import data_agg as agg


def main():
    # Process and mask data
    cmd_args: list[str] = sys.argv
    ridership_data: pd.DataFrame = pd.read_csv(cmd_args[1])
    ridership_data.mask(ridership_data["year_"] != int(cmd_args[2]), inplace=True)
    ridership_data.dropna(inplace=True)
    station_ridership: dict[str, int] = calculate_data(cmd_args, ridership_data)
    agg.write_to_file(station_ridership, f"rail_station_ridership_{int(cmd_args[2])}.csv", "station")

def calculate_data(cmd_args: list[str], data: pd.DataFrame) -> dict[str, int]:
    station_ridership: dict[str, int] = {}
    year: int = int(cmd_args[2])

    # Mask data if not explicitly requested
    if not cmd_args.__contains__("--include-frontrunner"):
        data.mask(data["route"] == "FrontRunner", inplace=True)
    if not cmd_args.__contains__("--include-s-line"):
        data.mask(data["route"] == "S-Line", inplace=True)
    data.dropna(inplace=True)

    stations: set[str] = agg.get_data_items(data, "stopname")

    for station in stations:
        station_ridership.update({station: agg.get_ridership(year, station, data, "stopname", agg.get_days_in_year(year), False)})

    return station_ridership


if __name__ == "__main__":
    main()