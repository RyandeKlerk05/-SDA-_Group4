import pandas as pd

# Make the code able run from any folder.
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]


# get the raw data
def extract():
    # Only retain countries that are both listed in the two csv files.
    data = pd.read_csv(BASE_DIR / "Data/IHME_original_file.csv")
    data2 = pd.read_csv(BASE_DIR / "Data/ratios_countries_social_media.csv")

    # get all names of countries in data2
    countries = data2.index
    results = []
    for country in countries:
        row_country = data[data["location"] == country]

        # if the country does not exist in data1
        if row_country.empty:
            continue

        # add all values in 2020
        data_2020 = row_country[row_country["year"] == 2020]
        total_2020 = data_2020["val"].sum()
        data_2021 = row_country[row_country["year"] == 2021]
        total_2021 = data_2021["val"].sum()

        # calculate the change rate beterrn 2020 and 2021
        change_rate = (total_2021 - total_2020) / total_2020
        results.append({"location": country,
                        "total_2020": total_2020,
                        "total_2021": total_2021,
                        "change_rate": change_rate})
    results = pd.DataFrame(results)
    results.to_csv(BASE_DIR / "Data/mental_health_change_rate.csv",
                   index=False)


if __name__ == "__main__":
    extract()
