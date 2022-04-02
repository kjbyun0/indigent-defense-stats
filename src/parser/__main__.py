import os, argparse, csv
from time import time

import pre2017, post2017

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "-overwrite",
    "-o",
    action="store_true",
    help="Switch to overwrite already parsed data.",
)
argparser.add_argument(
    "-county",
    "-c",
    type=str,
    default="hays",
    help="The name of the county.",
)
argparser.description = "Parse data for the specified county."
args = argparser.parse_args()

# get directories and make json dir if not present
case_html_path = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", args.county, "case_html"
)
case_json_path = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", args.county, "case_json"
)
if not os.path.exists(case_json_path):
    os.makedirs(case_json_path, exist_ok=True)

# get county version year information to determine which scraper to use
base_url = odyssey_version = None
with open(
    os.path.join(
        os.path.dirname(__file__), "..", "..", "resources", "texas_county_data.csv"
    ),
    mode="r",
) as file_handle:
    csv_file = csv.DictReader(file_handle)
    for row in csv_file:
        if row["county"].lower() == args.county.lower():
            odyssey_version = int(row["version"].split(".")[0])
            break
if not odyssey_version:
    raise Exception(
        "The required data to scrape this county is not in ./resources/texas_county_data.csv"
    )

START_TIME = time()
if odyssey_version < 2017:
    pre2017.parse(case_json_path, case_html_path, args)
else:
    post2017.parse(case_json_path, case_html_path, args)
RUN_TIME = time() - START_TIME
print(f"Parsing took {RUN_TIME} seconds")
