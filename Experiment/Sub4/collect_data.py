''' This file collects the data for the 4th sub-question for this research: '''

# import csv
import pandas as pd


# Make the code able run from any folder.
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]

mental_health_file = BASE_DIR / 'Data/mental_health_change_rate.csv'
ratios_social_media_file = BASE_DIR / 'Data/ratios_countries_social_media.csv'


class CollectData4:
    def __init__(self, mental_health_file, ratios_social_media_file):
        self.file_mental_health = mental_health_file
        self.file_social_media_ratios = ratios_social_media_file
        self.p_value = 0.05

    def CollectRatioUsers(self):
        df = pd.read_csv(self.file_social_media_ratios,
                         usecols=['Country', 'Social Media Users Growth (%)'])
        return df

    def CollectRatioMentalHealth(self):
        df = pd.read_csv(self.file_mental_health,
                         usecols=['location', 'change_rate'])
        return df

    def FindIntersection(self):
        ''' Returns the countries that are in both CSV files.'''
        # Social media Growth
        df1 = pd.read_csv(self.file_social_media_ratios,
                          usecols=['Country', 'Social Media Users Growth (%)'])

        # Mental health
        df2 = pd.read_csv(self.file_mental_health,
                          usecols=['location', 'change_rate'])

        countries_intersection = (set(df1['Country'].values).
                                  intersection(df2['location'].values))
        return countries_intersection

    def FindDifference(self):
        ''' Returns the countries that are not in both CSV files.'''

        df1 = pd.read_csv(self.file_social_media_ratios,
                          usecols=['Country', 'Social Media Users Growth (%)'])

        # Mental health
        df2 = pd.read_csv(self.file_mental_health,
                          usecols=['location', 'change_rate'])

        countries_diff = (set(df1['Country'].values).
                          difference(df2['location'].values))

        return countries_diff

    def GetResults(self):
        ''' Returns the results as a list of 3-tuples:
            (country, ratio_social_media_users, ratio_mental_health)
        '''
        countries_intersection = self.FindIntersection()
        df1 = self.CollectRatioUsers()
        df2 = self.CollectRatioMentalHealth()

        results = []

        for country in countries_intersection:
            ratio_users = df1.loc[df1['Country'] == country,
                                  'Social Media Users Growth (%)'].values[0]
            ratio_mental_health = df2.loc[df2['location'] == country,
                                          'change_rate'].values[0]
            results.append((country, ratio_users, ratio_mental_health))
        return results


if __name__ == "__main__":
    collect_data = CollectData4(mental_health_file, ratios_social_media_file)

    results = collect_data.GetResults()
    print(results)
