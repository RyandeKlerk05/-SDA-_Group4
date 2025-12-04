''' This file collects the data for the 4th sub-question for this research:


'''

# import csv
import pandas as pd

mental_health_file = '../../Data/IHME_data/mental_health_change_rate.csv'
ratios_social_media_file = '../../Data/ratios_countries_social_media.csv'

class CollectData4:
    def __init__(self, mental_health_file, ratios_social_media_file):
        self.file_mental_health = mental_health_file
        self.file_social_media_ratios = ratios_social_media_file
        self.p_value = 0.05

    def CollectRatioUsers(self):
        df = pd.read_csv(self.file_social_media_ratios, usecols=['Country', 'Social Media Users Growth (%)'])
        return df

    def CollectRatioMentalHealth(self):
        df = pd.read_csv(self.file_mental_health, usecols=['location', 'change_rate'])
        return df


collect_data = CollectData4(mental_health_file, ratios_social_media_file)
data_users = collect_data.CollectRatioUsers()
data_mental_health = collect_data.CollectRatioMentalHealth()
