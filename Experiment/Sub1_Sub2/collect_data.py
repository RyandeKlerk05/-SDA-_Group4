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
    data['Gender'] = raw_data.iloc[:, 2]                        # Gender

    # Retrieve the user ages and assign them an age group.
    age_bins = [0, 18, 25, 35, 50, 200]
    age_labels = ["<18", "18-25", "25-35", "35-50", "50+"]
    data['Age'] = raw_data.iloc[:, 1]
    data['Age_Group'] = pd.cut(data['Age'], bins=age_bins,
                               labels=age_labels, right=False)

    # Retrieve the daily social media usage along with a mapped version.
    mapping = {
        "Less than an Hour": 1,
        "Between 1 and 2 hours": 2,
        "Between 2 and 3 hours": 3,
        "Between 3 and 4 hours": 4,
        "Between 4 and 5 hours": 5,
        "More than 5 hours": 6
    }
    data['SM_Time'] = raw_data.iloc[:, 8]
    data["SM_Time_val"] = data["SM_Time"].map(mapping)

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
