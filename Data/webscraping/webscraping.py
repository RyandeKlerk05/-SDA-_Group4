'''
This file uses webscraping to distract data from the URLs that describe
worldwide media usage. These data will be used for the experiments of
sub-question 3 and 4.
'''

from bs4 import BeautifulSoup
import csv
import requests
import re
from websites_2021 import country_urls2021

amount_str = ['hundred', 'thousand', 'million']

MULTIPLIERS = {
    'thousand': 10 ** 3,
    'million': 10 ** 6,
    'billion': 10 ** 9
}


'''
    Section 1: Extracting data using webscraping.
'''

''' Subsection 1.1: Global function for extracting soup. '''
def get_soup(url):
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        return soup
    except:
        # print('Invalid URL')  # For debugging
        return None

'''
Subsection 1.1: Extracting and computing exact values (e.g., 48.000, 1248.)
'''

def extract_population(soup):
    '''Extracts a country's population given a soup.
    '''

    if not soup:
        print('Invalid soup')
        return None

    for bold in soup.find_all('b'):
        bold_text = bold.get_text(" ").lower().strip()

        # Skip bolds with no digits
        if not any(c.isdigit() for c in bold_text):
            continue

        sentence = bold.parent.get_text(" ").lower()

        number = 0.0
        if 'population'not in sentence:
            continue

        splitted_text = bold_text.split()

        number = float(splitted_text[0].replace(',', '.'))

        if len(splitted_text) > 1 and splitted_text[1] in MULTIPLIERS:

            number *= MULTIPLIERS[splitted_text[1]]
        else:
            number *= 1000  # value is smaller than 10000

        return int(number)

    return None


def extract_number_social_media_users(soup):
    '''
    Extracts number of social media users given a soup.
    '''

    if not soup:
        print('Invalid soup')
        return None

    for bold in soup.find_all("b"):
        bold_text = bold.get_text(" ").lower().strip()

        # Skip bolds with no digits
        if not any(c.isdigit() for c in bold_text):
            continue

        sibling = bold.next_sibling

        if not sibling or 'social media users' not in bold.next_sibling:
            continue

        splitted_text = bold_text.split()  # first value is integer
        number = float(splitted_text[0].replace(',', '.'))

        if len(splitted_text) > 1 and splitted_text[1] in MULTIPLIERS:
            number *= MULTIPLIERS[splitted_text[1]]
        else:
            number *= 1000  # value is smaller than 10000

        return int(number)

    return None


# def get_emperical_ratios(country_urls):
#     '''Returns the ratios by '''
#     ratios = {}
#     trash = 0
#     for country in country_urls.keys():

#         # if trash >= 20:
#         #     print("Too much trash: check urls")
#         #     break

#         url = country_urls[country]

#         soup = get_soup(url)

#         if not soup:
#             print(f'Invalid soup for {country}')
#             trash += 1
#             ratios[country] = ""
#             continue

#         total = extract_population(soup)
#         users = extract_number_social_media_users(soup)

#         ratio = get_ratio_social_media_users(total, users)

#         if not ratio:
#             trash += 1
#             continue

#         print(f'Country: {country}, total: {total}, social media users: {users}, ratio: {ratio}\n')

#         ratios[country] = (total, users, ratio)
#     return ratios


'''
1.2: Extracting percentages using webscraping (Sub-questions 3 and 4).
'''

def get_ratio_population(soup):
    ''' Returns the number of

    Args:
        soup: webpage file in which we need to find ratio.

    Returns:
        percentage in increase or decrease (including '-' for decrease)
        and None on failure.
    '''

    if not soup:
        print('Invalid soup')
        return None

    for bold in soup.find_all("b"):

        sentence = bold.parent.get_text(" ").lower()

        about_population = 'population' in sentence
        in_time_period = 'between january 2020 and january 2021' in sentence

        if not about_population or not in_time_period:
            continue

        if 'unchanged' in sentence:
            return 0.0

        match = re.search(r'\(([-+]?[\d\.]+)%\)', sentence)
        # print(match)

        if match:
            percentage = float(match.group(1))
            return percentage

    return None


def get_ratio_users(soup):
    '''Returns the percentage of media users a country
    increased/decreased in 2020-2021.
    '''

    if not soup:
        print('Invalid soup')
        return None

    for bold in soup.find_all("b"):

        sentence = bold.parent.get_text(" ").lower()

        about_population = 'social media users' in sentence
        in_time_period = 'between 2020 and 2021' in sentence # or 'in january 2021' in sentence  # Check this for christmas island

        if not about_population or not in_time_period:
            continue

        if 'unchanged' in sentence:
            return 0.0

        match = re.search(r'\(([-+]?[\d\.]+)%\)', sentence)

        if match:
            percentage = float(match.group(1))
            return percentage

        match2 = re.search(r'([-+]?[\d\.]+)%', sentence)

        if match2:
            percentage = float(match2.group(1))
            return percentage

    return None


def extract_percentage_social_media_users_populaton(soup):
    ''' Returns the percentage of a population that uses social media.'''

    if not soup:
        print('Invalid soup')
        # return None

    for bold in soup.find_all("b"):

        line = bold.parent.get_text(" ").lower()

        if 'social media users' not in line or 'total population' not in line:
            continue

        match = re.search(r'\(([-+]?[\d\.]+)%\)', line)

        if match:
            percentage = float(match.group(1))
            return percentage

        match2 = re.search(r'([-+]?[\d\.]+)%', line)

        if match2:
            percentage = float(match2.group(1))
            return percentage


def get_ratio_population_vs_users(country_urls: dict):
    '''Stores the percentages of population and social media users growth
        in each country.

    Args:
        country_urls: All countries as keys with their URLs as values.

    Returns:
        A dictionary with the countries as the keys and the tuple
        (population_ratio, social_media_users_ratio) as the values.
    '''
    ratios = {}

    for country in country_urls.keys():

        url = country_urls[country]
        soup = get_soup(url)
        if not soup:
            continue

        population_ratio = get_ratio_population(soup)
        users_ratio = get_ratio_users(soup)

        if not population_ratio or not users_ratio:
            continue

        ratios[country] = (population_ratio, users_ratio)

    return ratios


''' Section 4: Saving extracted data for sub-questions 3 and 4.'''


def store_ratios_and_countries(ratios: dict, file_as_str):
    '''Stores countries and corresponding ratios in csv-file

    Args:
        Comparisons: a dictionary with key = country and
            values = (percentage_population)
    '''
    with open(file_as_str, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Country', 'Population Growth (%)', 'Social Media Users Growth (%)'])

        for country, values in ratios.items():
            writer.writerow([country, values[0], values[1]])
            print(f'Writing ({country}, ({values[0]}, {values[1]}) to csv-file')

    print('Wrote countries to ratios_countries_social_media.csv successfully')


def ratios_procedure():
    country_urls = country_urls2021
    ratios = get_ratio_population_vs_users(country_urls)
    store_ratios_and_countries(ratios, '../ratios_countries_social_media.csv')



def store_percentage_users_in_countries(country_urls: dict, files_as_str):
    ''' Stores the percentages of all the populations that are social media
    users in a specific year in a CSV-file.
    '''
    with open(files_as_str, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Country', 'Social Media Users (%)'])

        for country in country_urls.keys():
            url = country_urls[country]
            soup = get_soup(url)
            percentage = extract_percentage_social_media_users_populaton(soup)
            writer.writerow([country, percentage])
            print(f'Writing ({country}, {percentage}) to file')

        print(f'Finished storing data to {files_as_str}')

''' Section 5: Test function'''
def tests():
    soup = get_soup('https://datareportal.com/reports/digital-2021-netherlands')
    assert extract_population(soup) == 17150000
    assert get_ratio_population(soup) == 0.2
    assert extract_number_social_media_users(soup) == 15100000
    assert get_ratio_users(soup) == 0.0
    assert extract_percentage_social_media_users_populaton(soup) == 88.0

    soup2 = get_soup('https://datareportal.com/reports/digital-2021-christmas-island')
    assert extract_population(soup2) == 1843
    assert get_ratio_population(soup2) == 0.0
    assert extract_number_social_media_users(soup2) == 1200
    assert get_ratio_users(soup2) == None  #  Check if this works
    assert extract_percentage_social_media_users_populaton(soup2) == 65.1


    soup3 = get_soup('https://datareportal.com/reports/digital-2021-albania')
    assert extract_population(soup3) == 2880000
    assert get_ratio_population(soup3) == -0.1
    assert extract_number_social_media_users(soup3) == 1600000
    assert get_ratio_users(soup3) == 14.0
    assert extract_percentage_social_media_users_populaton(soup3) == 55.6


def store_changes_in_csv(country_urls, file_as_str):
    '''
    Stores the changes in population growth and social media users growth in a
    csv file.
    '''

    with open(file_as_str, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Country', 'Social Media Users (N)'])

        for country, url in country_urls.items():
            soup = get_soup(url)
            num_users = extract_number_social_media_users(soup)
            writer.writerow([country, num_users])

    print('Wrote countries to ratios_countries_social_media.csv successfully')

if __name__ == "__main__":
    # tests()  # Comment this out to prove it works

    # Run line below for getting ratios.
    ratios_procedure()

    # Comment out the line below for running
    dir_percentage_file = '../percentages_population_users.csv'

    store_percentage_users_in_countries(country_urls2021, dir_percentage_file)

    # Run line below for getting the exact values of number of social media users
    # store_changes_in_csv(country_urls2021, '../social_media_users_2021.csv')