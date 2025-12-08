''' This file plots a linear regression using the data that has been collected
    in collect_data.py for sub-queston 4:

    Do countries that have a faster uptake of social media see a faster
    in mental health compared to slow-uptake countries?

    The data points represent a country with their population growth
    as their x-coordinate and their growth in social media users within a year.
    Each data point will have a specific colour, based on their continent.


'''
# Files
from collect_data import CollectData4
from mann_whitney_u_test import MannWhitney

# Libraries
from matplotlib import pyplot as plt
from scipy.stats import mannwhitneyu


mental_health_file = '../../Data/IHME_data/mental_health_change_rate.csv'
ratios_social_media_file = '../../Data/ratios_countries_social_media.csv'

# Source: https://en.wikipedia.org/wiki/97.5th_percentile_point
ACCEPTANCE_VALUE = 1.96 # Z score for alpha = 0.05


''' Functions '''
def get_median(values: list):
    ''' Returns the median of a given list of data.'''

    if len(values) == 0:
        return None

    sorted_values = sorted(values)
    n = len(sorted_values)
    idx = n // 2

    if n % 2 == 1:
        return sorted_values[idx]
    else:
        return (sorted_values[idx - 1] + sorted_values[idx]) / 2


''' Collecting Data '''
def get_batches(mental_health_file, ratios_social_media_file, testing=False):

    collect_data = CollectData4(mental_health_file, ratios_social_media_file)
    data = collect_data.GetResults()

    users_values, mental_health_values = [], []
    fast_uptakes = []
    slow_uptakes = []

    for country, users_change, mental_health_change in data:
        users_change /= 100  # The user values are in percentages

        # print(f'Country: {country}, Users: {users_change}, mental health: {mental_health_change}')
        # if users_change > 1.00 or users_change < -0.50:
        #     print(f'Country: {country}, Users: {users_change}, mental health: {mental_health_change}')

        users_values.append(users_change)
        mental_health_values.append(mental_health_change)

    users_median = get_median(users_values)
    # mental_health_median = get_median(mental_health_values)

    for i, users_val in enumerate(users_values):
        if users_val > users_median:
            if testing:
                fast_uptakes.append(mental_health_values[i])
            else:
                fast_uptakes.append(('fast uptake', users_val, mental_health_values[i]))
        else:
            if testing:
                slow_uptakes.append(mental_health_values[i])
            else:
                slow_uptakes.append(('slow uptake', users_val, mental_health_values[i]))

    return fast_uptakes, slow_uptakes


''' Function for linear regression'''
def get_U1_U2_Z_score(mental_health_file, ratios_social_media_file):
    batch_fast, batch_slow = get_batches(mental_health_file, ratios_social_media_file)

    mann_whitney = MannWhitney(batch_fast, batch_slow)
    U1, U2 = mann_whitney.CalculateU()
    z_score = mann_whitney.CalculateZScore(U1, U2)
    return U1, U2, z_score


def run_statistical_test(mental_health_file, ratios_social_media_file):
    ''' Executes the Mann-Whitney U test in order to check the distribution.
    '''
    U1, U2, z_score = get_U1_U2_Z_score(mental_health_file,
                                        ratios_social_media_file)

    print('\nMann-Whitney U test: Our implementation')
    print(f'U1 = {U1:.2f}, U2 = {U2:.2f}')

    print(f'Absolute z-score: {abs(z_score):.2f}')

    print('\nConclusion: Hypothesis')
    if abs(z_score) <= ACCEPTANCE_VALUE:
        # Inside of acceptance interval
        message = '''FAILED TO REJECT NULL HYPOTHESIS:
        No difference in mental health scores between countries
        that have either fast or slow uptakes in number of social
        media users.
        '''
    else:
        # Outside of acceptance interval
        message = '''REJECT the NULL HYPOTHES:
        Countries with a fast uptake in number of
        social media users might have more negative changes
        in their mental health scores.
        '''
    print(message)

run_statistical_test(mental_health_file, ratios_social_media_file)


def test(mental_health_file, ratios_social_media_file):
    fast_batch, slow_batch = get_batches(mental_health_file, ratios_social_media_file, testing=True)

    stat, p_value = mannwhitneyu(fast_batch, slow_batch)
    print('\nMann-Whitney U Test: Scipy.stats')
    print(f'Statistics: {stat:.2f}, p: {p_value:.2f}')

    if p_value > 0.05:
        message = '''FAILED TO REJECT NULL HYPOTHESIS:
        No difference in mental health scores between countries
        that have either fast or slow uptakes in number of social
        media users.
        '''
    else:
        message = '''REJECT the NULL HYPOTHES:
        Countries with a fast uptake in number of
        social media users might have more negative changes
        in their mental health scores.
        '''
    print(message)


# Comment out the line below to test libary version of Mann-Whitney U test.
# test(mental_health_file, ratios_social_media_file)


def func(x):
    ''' Function for Regression'''
    pass

# model = list(map(func, x))


''' Plotting Data'''
def plot_data(mental_health_file, ratios_social_media_file):
    fast_batch, slow_batch = get_batches(mental_health_file,
                                         ratios_social_media_file,
                                         testing=True)

    plt.figure(figsize=(12, 8))
    plt.hist(fast_batch, bins=20, alpha=0.4, color='b', edgecolor='black')
    plt.hist(slow_batch, bins=20, alpha=0.4, color='g', edgecolor='black')

    plt.axvline(get_median(fast_batch), color='b', linestyle='dashed',
                linewidth=1.5, label=f'Fast median: {get_median(fast_batch):.4f}')
    plt.axvline(get_median(slow_batch), color='g', linestyle='dashed',
                linewidth=1.5, label=f'Slow median: {get_median(slow_batch):.4f}')

    plt.xlabel('Change in Mental Health Score')
    plt.ylabel('Frequency')
    title = ''' Distribution of Mental Health Changes: Fast vs. Slow
    Social Media Uptake Countries between 2020 and 2021'''
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

plot_data(mental_health_file, ratios_social_media_file)


