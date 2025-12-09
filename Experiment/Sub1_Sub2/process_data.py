from collect_data import load_data
import numpy as np
import pandas as pd


# -----------------------------------------------------------------------------
# This section is related to the Spearman correlation calculations: -----------
# -----------------------------------------------------------------------------

def rank_data(data):
    """ Asigns the data ranks in order of their value. """

    # Give each data point a rank based on their value.
    sorter = np.argsort(data)
    ranks = np.empty_like(sorter, dtype=float)
    ranks[sorter] = np.arange(len(data))

    # Change duplicate values into averages.
    _, inverse, counts = np.unique(data, return_inverse=True,
                                   return_counts=True)

    # Calculate the average based on how many duplicates it has.
    for i, count in enumerate(counts):
        if count > 1:
            tie_positions = np.where(inverse == i)[0]
            avg_rank = np.mean(ranks[tie_positions])
            ranks[tie_positions] = avg_rank

    # Add 1 so we have 1-based ranks.
    for i in range(len(ranks)):
        ranks[i] += 1

    return ranks


def spearman_correlation(data_a, data_b):
    """ Calculates the Spearman correlation of two datasets. """

    # Calculate the ranks of both datasets.
    rank_a = rank_data(data_a)
    rank_b = rank_data(data_b)

    # Calculate the difference in rank.
    d = rank_a - rank_b
    n = len(data_a)

    # Calculate the correlation value.
    numerator = 6 * np.sum(d ** 2)
    denominator = n * (n**2 - 1)

    rho = 1 - numerator / denominator
    return rho


def spearman_p_value(data_a, data_b, num_permutations=10000):
    """ Calculate the p-value through a permutation test. """

    observed = spearman_correlation(data_a, data_b)
    count = 0

    for _ in range(num_permutations):
        perm = np.random.permutation(data_b)
        perm_rho = spearman_correlation(data_a, perm)
        if abs(perm_rho) >= abs(observed):
            count += 1

    return count / num_permutations


# -----------------------------------------------------------------------------
# This section is related to the Kruskal-Wallis calculations:  ----------------
# -----------------------------------------------------------------------------

def kruskal_wallis(groups):
    """ Perform the Kruskal-Wallis test to obtain the H-statistic. """

    # Flatten the groups (but keep track of original groups).
    all_values = np.concatenate(groups)
    group_labels = np.concatenate([[i] * len(g) for i, g in enumerate(groups)])

    # Rank all values.
    ranks = rank_data(all_values)

    # Calculate the H statistic
    N = len(all_values)
    H = 0.0

    for i, g in enumerate(groups):
        n_i = len(g)
        R_i = np.sum(ranks[group_labels == i])
        H += (R_i ** 2) / n_i

    H = (12 / (N * (N + 1))) * H - 3 * (N + 1)

    return H


def kruskal_p_value(groups, num_permutations=10000):
    """ Calculate the p-value through a permutation test. """

    # Calculate the H-statistic for the actual data.
    observed_H = kruskal_wallis(groups)
    combined = np.concatenate(groups)
    lengths = [len(g) for g in groups]

    count = 0

    # Check to see if a better random permutation exists.
    for _ in range(num_permutations):
        perm = np.random.permutation(combined)

        # Split into same-sized groups.
        perm_groups = []
        start = 0
        for L in lengths:
            perm_groups.append(perm[start:start+L])
            start += L

        perm_H = kruskal_wallis(perm_groups)
        if perm_H >= observed_H:
            count += 1

    return count / num_permutations

# -----------------------------------------------------------------------------
# This section is related to the Chi-Square test: -----------------------------
# -----------------------------------------------------------------------------


def build_contingency_table(data):
    """ Build a contingency table with the use of SM apps per age group. """

    # Make empty table of the age groups compared to SM platforms.
    platforms = data['Platforms'].str.split(', ').explode().unique()
    age_groups = data['Age_Group'].cat.categories
    contingency = pd.DataFrame(0, index=age_groups, columns=platforms)

    # Count the platform frequency per age group.
    for _, row in data.iterrows():
        for platform in row['Platforms'].split(', '):
            contingency.loc[row['Age_Group'], platform] += 1

    return contingency


def chi_square(contingency):
    """ Calculate the Chi-Square statistic from the contigency table. """

    # Calculate the total uses of each row/column.
    observed = contingency.values
    row_totals = observed.sum(axis=1).reshape(-1, 1)
    col_totals = observed.sum(axis=0).reshape(1, -1)

    # Calculate the total and compare to the expected amount.
    grand_total = observed.sum()
    expected = row_totals @ col_totals / grand_total

    # Calculate the statistic.
    chi2 = ((observed - expected)**2 / expected).sum()
    return chi2


def chi_square_p_value(data, num_permutations=1000):
    """ Calculate the p-value through a permutation test. """

    # Build the table and calculate chi score.
    contingency_table = build_contingency_table(data)
    observed_chi2 = chi_square(contingency_table)
    count = 0

    user_platforms = data['Platforms'].copy().values

    # Calculate random permutations and see if they get a better score.
    for _ in range(num_permutations):
        permuted = np.random.permutation(user_platforms)
        data_perm = data.copy()
        data_perm['Platforms'] = permuted

        # Check permutated table score.
        perm_table = build_contingency_table(data_perm)
        perm_chi2 = chi_square(perm_table)
        if perm_chi2 >= observed_chi2:
            count += 1

    p_value = count / num_permutations
    return p_value


if __name__ == "__main__":
    data, platform_freq = load_data()

    # Perform the spearman correlation tests:
    print(f"corr: {spearman_correlation(data['Age'], data['SM_Time_val'])}, "
          f"p-value: {spearman_p_value(data['Age'], data['SM_Time_val'])}")

    print(f"corr: {spearman_correlation(data['Age'], data['MH_Score'])},"
          f"p-value: {spearman_p_value(data['Age'], data['MH_Score'])}")

    # Perform the Kruskal-Wallis test:
    groups = [data[data["Age_Group"] == g]["MH_Score"].values
              for g in data["Age_Group"].cat.categories]
    print(f"H: {kruskal_wallis(groups)},"
          f"p-value: {kruskal_p_value(groups)}")

    # Perform the Chi-Square statistic test:
    contingency_table = build_contingency_table(data)
    print(f"chi: {chi_square(contingency_table)},"
          f"p-value: {chi_square_p_value(data)}")
