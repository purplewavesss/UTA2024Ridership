import re
import sys
import pandas as pd

import data_agg as agg


def main():
    # Process and mask data
    cmd_args: list[str] = sys.argv
    ridership_data: pd.DataFrame = pd.read_csv(cmd_args[1])
    ridership_data = ridership_data.mask(ridership_data["year_"] != int(cmd_args[2]))
    ridership_data = ridership_data.dropna()
    station_ridership: dict[str, int] = calculate_data(cmd_args, ridership_data)
    write_to_file(station_ridership, f"bus_stop_ridership_{int(cmd_args[2])}.csv", "Stop")


def calculate_data(cmd_args: list[str], data: pd.DataFrame) -> dict[str, int]:
    stop_ridership: dict[str, int] = {}
    year: int = int(cmd_args[2])

    # Mask data if not explicitly requested
    if not cmd_args.__contains__("--include-all-counties"):
        data = data.mask(data["county"] != "Salt Lake")
    data = data.mask(data["month_"] != "January")
    data = data.dropna()

    stops: set[str] = get_data_items(data)

    for stop in stops:
        stop_ridership.update({stop: agg.get_ridership(year, stop, data, "stopname", 31, True)})

    return stop_ridership


def get_data_items(data: pd.DataFrame):
    items: set[str] = set()
    for row in data.itertuples():
        stop_name: str = row.stopname
        stop_name = re.sub("\\s+\\([A-Za-z]B.*\\)", "", stop_name)
        stop_name = re.sub("\\s+\\(Bay [A-Za-z]\\)", "", stop_name)
        items.add(stop_name)

    return items

def write_to_file(data: dict[str, int], filename: str, item_name: str):
    file = open(filename, "w")
    file.write(f"{item_name},Ridership,Downtown\n")
    for item, ridership_num in data.items():
        file.write(f"{item},{ridership_num},{int(is_downtown(item) is True)}\n")

    file.close()


def is_downtown(item: str) -> bool:
    single_match_downtown = ["Salt Lake Central Station", "North Temple Station", "Old Greektown Station", "Planetarium Station",
                             "Arena Station", "Temple Square Station", "City Center Station", "Gallivan Plaza Station",
                             "Courthouse Station", "Library Station", "200 S / 600 W", "200 S / Rio Grande", "Columbus"]
    double_match_downtown = ["Main", "State", "North Temple", "South Temple"]

    # Check single match regex strings
    for stop in single_match_downtown:
        if stop in item:
            return True

    # Check double match regex strings
    matches: int = 0

    # Find streets inside downtown
    for stop in double_match_downtown:
        if stop in item:
            matches += 1
        if matches == 2:
            return True

    # Find street numbers inside downtown
    # Test south matches
    match = re.search("[0-9]+ S", item)
    if match is not None and process_match(item, match) <= 500:
        matches += 1

    # Test east matches
    match = re.search("[0-9]+ E", item)
    if match is not None and process_match(item, match) <= 200:
        matches += 1

    # Test west matches
    match = re.search("[0-9]+ W", item)
    if match is not None and process_match(item, match) <= 400:
        matches += 1

    if matches >= 2:
        return True

    return False


def process_match(match_string: str, street_match: re.Match[str]) -> int:
    match_address: str = match_string[street_match.start(): street_match.end() - 2]
    return int(match_address)


if __name__ == "__main__":
    main()