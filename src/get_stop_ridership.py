import re
import sys
import pandas as pd

import data_agg as agg


# DO NOT RUN THIS FILE IN A NORMAL PYTHON INTERPRETER! Use a fast compiler like pypy instead.
def main():
    # Process and mask data
    cmd_args: list[str] = sys.argv
    ridership_data: pd.DataFrame = pd.read_csv(cmd_args[1])
    ridership_data = ridership_data.mask(ridership_data["year_"] != int(cmd_args[2]))
    ridership_data = ridership_data.mask(ridership_data["month_"] != agg.int_to_month(int(cmd_args[3])))
    ridership_data = ridership_data.dropna()
    station_ridership: dict[str, int] = calculate_data(cmd_args, ridership_data)
    agg.write_to_file(station_ridership, f"bus_stop_ridership_{int(cmd_args[3])}_{int(cmd_args[2])}.txt")

def calculate_data(cmd_args: list[str], data: pd.DataFrame) -> dict[str, int]:
    stop_ridership: dict[str, int] = {}

    # Mask data if not explicitly requested
    if not cmd_args.__contains__("--include-all-counties"):
        data.mask(data["county"] != "Salt Lake")
    data.dropna(inplace=True)

    stops: set[str] = get_data_items(data)

    for stop in stops:
        stop_ridership.update({stop: agg.get_ridership(int(cmd_args[2]), stop, data, "stopname")})

    return stop_ridership


def get_data_items(data: pd.DataFrame):
    items: set[str] = set()
    for row in data.itertuples():
        stop_name: str = row.stopname
        stop_name = re.sub("\\s+\\([A-Za-z]B\\)", "", stop_name)
        items.add(stop_name)

    return items


if __name__ == "__main__":
    main()