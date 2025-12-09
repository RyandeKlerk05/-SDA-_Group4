from collect_data import load_data
from process_data import build_contingency_table
from scipy.stats import spearmanr, chi2_contingency, kruskal


""" This file is used to test our own implementations, and compare them to
    the results of statistical models like scipy, to check it's accuracy.

    Results:
    - Spearman correlation between the age and daily social media use of users:
       - Own implementation: -0.2670244174912224, p_value < 1.0e-5
       - Scipy.spearmanr   : -0.2984068616564108, p_value = 2.383e-11

     - Spearman correlation between the age and mental health score of users:
       - Own implementation: -0.2197038823854176, p_value = 1.0e-5
       - Scipy.spearmanr   : -0.2277815976450574, p_value = 4.437e-07

     - Kruskal-Wallis test between the age groups and mental health scores:
       - Own implementation: 57.94384542777607, p_value < 1.0e-5
       - Scipy.kruskal     : 58.03068483012012, p_value = 7.518e-12

     - Chi-Square statistic of the frequency of SM platform use per age group:
       - Own implementation    : 75.66603952317473, p_value < 1.0e-4
       - Scipy.chi2_contingency: 75.66603952317473, p_value = 2.134e-05

    Conclusion:
      - The reported values come pretty close to the values obtained from
        Scipy.stats, and thus it can be assumed our implementations work
        as intended. The Spearman and Kruskal tests do differ a bit
        (although in both cases we still see the general same result),
        which can be explained by scipy.stats using more advanced
        algorithmes to solve ties.

      - The p-values are all also very close to 0, showing that we can
        make the assumption that there is indeed a link between our data
        and that it has not been obtained from random sampling/permutation.
"""


if __name__ == "__main__":
    data, platform_freq = load_data()

    # Spearman correlation tests:
    print(spearmanr(data['Age'], data['SM_Time_val']))
    print(spearmanr(data['Age'], data['MH_Score']))

    # Kruskal-Wallis tests:
    groups = [data[data["Age_Group"] == g]["MH_Score"].values
              for g in data["Age_Group"].cat.categories]

    H, p = kruskal(*groups)
    print(f"Kruskal-Wallis: H = {H}, p = {p}")

    # Chi-Square statistic tests:
    contingency_table = build_contingency_table(data)

    chi2, p, _, _ = chi2_contingency(contingency_table)
    print(f"Chi-square: {chi2}, p-value={p}")
