'''
This file uses webscraping to distract data from the URLs that describe
worldwide media usage.
'''

# import pymupdf.layout  # Uses layout to extract data
# import pymupdf4llm  # API interface: extracting as Markdown, JSON or TXT.

from bs4 import BeautifulSoup
import string
import requests
from websites import country_urls

amount_str = ['hundred', 'thousand', 'million']  # hundred can be removed?

url = 'https://datareportal.com/reports/digital-2021-netherlands'


MULTIPLIERS = {
    'thousand': 10 ** 3,
    'million': 10 ** 6,
    'billion': 10 ** 9
}

def get_soup(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def extract_population(soup):
    '''Extracts a country's population given a soup.
    '''

    for bold in soup.find_all('b'):
        bold_text = bold.get_text()
        sentence = bold.parent.get_text(" ").lower()

        if 'had a population of' in sentence:  # hardcode, might change it to just 'population'
            parts = bold.get_text(" ").split()
            number = float(parts[0])
            tenth_power = 1

            if len(parts) > 1:
                power = parts[1]
                tenth_power = MULTIPLIERS[power]

            return int(number * tenth_power)

    return None


def get_float_in_sentence(splitted_sentence):
    for idx in range(len(splitted_sentence)):
        if not float(splitted_sentence[idx]):
            continue
        else:
            return idx
    return None




def extract_number_social_media_users(soup):
    '''
    Extracts number of social media users given a soup.

    >>> extract_number_social_media_users('https://datareportal.com/reports/digital-2021-netherlands', 'social media users')

    >>> webscrape_one_country('https://datareportal.com/reports/digital-2021-netherlands', 'blablabla')
    None
    '''

    for bold in soup.find_all("b"):
        bold_text = bold.text.lower()
        correct = 'thousand' in bold_text or 'million' in bold_text or 'billion' in bold_text

        if correct and 'social media users' in bold.next_sibling:
            splitted_text = bold_text.split()  # first value is integer
            number = float(splitted_text[0])
            power = splitted_text[1]
            tenth_power = 1

            if len(splitted_text) > 1:
                tenth_power = MULTIPLIERS[power]

            number *= tenth_power
            return int(number)

    return None


def get_ratio_social_media_users(total: int, social_media_users: int):
    '''Returns ratio between number of social media users in a country
        and the total population.
        Returns: value between 0 and 1.
    '''
    return social_media_users / total


def tests():
    soup = get_soup('https://datareportal.com/reports/digital-2021-netherlands')
    assert extract_number_social_media_users(soup) == 15100000
    assert extract_population(soup) == 17150000


# tests()  # Assertion check
soup = get_soup('https://datareportal.com/reports/digital-2021-netherlands')
users = extract_number_social_media_users(soup)

total = extract_population(soup)

print(get_ratio_social_media_users(total, users))


