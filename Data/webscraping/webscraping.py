'''
This file uses webscraping to distract data from the URLs that describe
worldwide media usage.
'''

# import pymupdf.layout  # Uses layout to extract data
# import pymupdf4llm  # API interface: extracting as Markdown, JSON or TXT.

from bs4 import BeautifulSoup
import requests
from websites import country_urls

amount_str = ['hundred', 'thousand', 'million']  # hundred can be removed?


MULTIPLIERS = {
    'thousand': 10 ** 3,
    'million': 10 ** 6,
    'billion': 10 ** 9
}

def get_soup(url):
    try:
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        return soup
    except:
        print('Invalid ULR')
        return None



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

        if 'population' in sentence:
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


def get_ratio_social_media_users(total, social_media_users):
    '''Returns ratio between number of social media users in a country
        and the total population.
        Returns: value between 0 and 1.
    '''

    if not social_media_users or not total:
        return None

    return social_media_users / total


def tests():
    soup = get_soup('https://datareportal.com/reports/digital-2021-netherlands')
    assert extract_number_social_media_users(soup) == 15100000
    assert extract_population(soup) == 17150000

    soup2 = get_soup('https://datareportal.com/reports/digital-2021-christmas-island')
    assert extract_number_social_media_users(soup2) == 1200
    assert extract_population(soup2) == 1843



# tests()  # Assertion check

def get_all_ratios(country_urls):
    ratios = {}
    trash =  {}
    for country in country_urls.keys():
        url = country_urls[country]

        soup = get_soup(url)

        if not soup:
            trash[country] = url
            print(f'Trash: {country}, url = {url}')
            continue

        total = extract_population(soup)
        users = extract_number_social_media_users(soup)
        print(f'Country: {country}, total: {total}, social media users: {users}, ratio: {ratio}')

        ratio = get_ratio_social_media_users(total, users)

        if not ratio:
            trash[country] = url
            print(f'Trash: {country}, url = {url}')
            continue

        ratios[country] = ratio
    # return ratios

# tests()

get_all_ratios(country_urls)