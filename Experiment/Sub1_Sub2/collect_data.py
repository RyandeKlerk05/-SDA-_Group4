import pandas as pd


def load_data():
    """
        Loads and cleans the data from dataset 2.

        Output:
         - data: The processed dataset with all the important features.
         - platform_freq: List of frequencies of each SM platform.

    """

    # Extract the raw data from the csv file.
    raw_data = pd.read_csv("Data/age_socialmedia_mentalhealth.csv")

    data = pd.DataFrame()

    # Retrieve and process the necessary columns.
    data['Date'] = pd.to_datetime(raw_data.iloc[:, 0]).dt.date  # Date
    data['Age'] = raw_data.iloc[:, 1]                           # Age
    data['Gender'] = raw_data.iloc[:, 2]                        # Gender
    data['SM_Time'] = raw_data.iloc[:, 8]                       # Time using SM

    # Retrieve the platforms and calculate the frequency of each platform.
    data['Platforms'] = raw_data.iloc[:, 7]                     # Platforms
    platform_freq = (data['Platforms'].str.
                     split(', ', expand=True).stack().value_counts())

    # Retrieves the MH questions scores and calculates a combined score.
    data['MH_Questions'] = raw_data.iloc[:, 9:20].apply(lambda row: tuple(row),
                                                        axis=1)
    data['MH_Score'] = raw_data.iloc[:, 9:20].mean(axis=1)

    return data, platform_freq


if __name__ == "__main__":
    # Test call to see if data has loaded correctly.
    data, platform_freq = load_data()
    print(data.head())
    print(platform_freq)
