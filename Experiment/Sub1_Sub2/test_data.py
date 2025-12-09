from collect_data import load_data
from process_data import build_contingency_table
from scipy.stats import spearmanr, chi2_contingency


""" This file is used to test our own implementations, and compare them to
    the results of statistical models like scipy, to check it's accuracy.

    Results:
    - Spearman correlation between the age and daily social media use of users:
       - Own implementation: -0.2670244174912224, p_value < 1.0e-5
       - Scipy.spearmanr   : -0.2984068616564108, p_value = 2.383e-11

     - Spearman correlation between the age and mental health score of users:
       - Own implementation: -0.2197038823854176, p_value = 1.0e-5
       - Scipy.spearmanr   : -0.2277815976450574, p_value = 4.437e-07

     - Chi-Square statistic of the frequency of SM platform use per age group:
       - Own implementation    : 75.66603952317473, p_value < 1.0e-4
       - Scipy.chi2_contingency: 75.666           , p_value = 0.00002

"""


if __name__ == "__main__":
    data, platform_freq = load_data()

    # Spearman correlation tests:
    print(spearmanr(data['Age'], data['SM_Time_val']))
    print(spearmanr(data['Age'], data['MH_Score']))

    # Chi-Square statistic tests:
    contingency_table = build_contingency_table(data)

    chi2, p, _, _ = chi2_contingency(contingency_table)
    print(f"Chi-square: {chi2:.3f}, p-value={p:.5f}")
