from collect_data import load_data
from scipy.stats import spearmanr


""" This file is used to test our own implementations, and compare them to
    the results of statistical models like scipy, to check it's accuracy.

    Results:
    - Spearman correlation between the age and daily social media use of users:
       - Own implementation: -0.2670244174912224, p_value < 1.0e-5
       - Scipy.spearmanr   : -0.2984068616564108, p_value = 2.383e-11

     - Spearman correlation between the age and mental health score of users:
       - Own implementation: -0.2197038823854176, p_value = 1.0e-5
       - Scipy.spearmanr   : -0.2277815976450574, p_value = 4.437e-07
"""


if __name__ == "__main__":
    data, platform_freq = load_data()

    # Uncomment the tests that need to be performed.
    print(spearmanr(data['Age'], data['SM_Time_val']))
    print(spearmanr(data['Age'], data['MH_Score']))
