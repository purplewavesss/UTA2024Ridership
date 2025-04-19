import sys
import pandas as pd

import data_agg as agg


def main():
    # Process and mask data
    cmd_args: list[str] = sys.argv
    ridership_data: pd.DataFrame = pd.read_csv(cmd_args[1])
    ridership_data = ridership_data.mask(ridership_data["year_"] != int(cmd_args[2]))
    ridership_data = ridership_data.dropna()
    route_ridership: dict[str, int] = calculate_data(cmd_args, ridership_data)
    agg.write_to_file(route_ridership, f"route_ridership_{int(cmd_args[2])}.txt")


def calculate_data(cmd_args: list[str], data: pd.DataFrame) -> dict[str, int]:
    route_ridership: dict[str, int] = {}

    # Mask data if not explicitly requested
    if not cmd_args.__contains__("--include-rail"):
        data = data.mask(data["mode"] == "Commuter Rail")
        data = data.mask(data["mode"] == "Light Rail")
        data = data.mask(data["mode"] == "Streetcar")
    data = data.dropna()

    routes: set[str] = agg.get_data_items(data, "lineabbr")

    for route in routes:
        route_ridership.update({route: agg.get_ridership(int(cmd_args[2]), route, data, "lineabbr")})

    return route_ridership


if __name__ == "__main__":
    main()