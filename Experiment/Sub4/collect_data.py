''' This file collects the data for the 4th sub-question for this research:


'''

import csv

mental_health_file = ''
ratios_social_media_file = '../Data/ratios_countries_social_media.csv'

class CollectData4:
    def __init__(self, mental_health_file, ratios_social_media_file, idx_mentalhealth, idx_social_media_users):
        file_mental_health = mental_health_file
        file_social_media_ratios = ratios_social_media_file
        idx_mental_health = idx_mentalhealth
        idx_social_media = idx_social_media_users
        p_value = 0.05


    def GetDataColumn(self, file):
        ''' Returns the data from a column '''
        with open(file, 'r', newline='') as filename:
            lines = filename.readlies()[1:]
            

    def CollectRatioUsers(self):
        pass

    def CollectRatioMentalHealth(self):
        pass



collect_data = CollectData4()
