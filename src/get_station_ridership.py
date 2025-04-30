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
    write_to_file(station_ridership, f"rail_station_ridership_{int(cmd_args[2])}.csv", "station")

def calculate_data(cmd_args: list[str], data: pd.DataFrame) -> dict[str, int]:
    station_ridership: dict[str, int] = {}
    year: int = int(cmd_args[2])

    # Mask data if not explicitly requested
    if not cmd_args.__contains__("--include-frontrunner"):
        data.mask(data["route"] == "FrontRunner", inplace=True)
    if not cmd_args.__contains__("--include-s-line"):
        data.mask(data["route"] == "S-Line", inplace=True)
    data = data.mask(data["month_"] != "January")
    data.dropna(inplace=True)

    stations: set[str] = agg.get_data_items(data, "stopname")

    for station in stations:
        station_ridership.update({station: agg.get_ridership(year, station, data, "stopname", 31, False)})

    return station_ridership


def write_to_file(data: dict[str, int], filename: str, item_name: str):
    downtown_stations = get_downtown_stations()

    file = open(filename, "w")
    file.write(f"{item_name},Ridership,Downtown\n")
    for item, ridership_num in data.items():
        is_downtown: bool = False

        # Check single match regex strings
        for station in downtown_stations:
            is_downtown = item == station
            if is_downtown:
                break

        file.write(f"{item},{ridership_num},{int(is_downtown is True)}\n")

    file.close()


def get_downtown_stations() -> list[str]:
    return ["Salt Lake Central Station", "North Temple Station", "Old Greektown Station", "Planetarium Station", "Arena Station",
            "Temple Square Station", "City Center Station", "Gallivan Plaza Station", "Courthouse Station", "Library Station"]


if __name__ == "__main__":
    main()