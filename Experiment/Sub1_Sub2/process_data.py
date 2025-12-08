from collect_data import load_data
import numpy as np


# -----------------------------------------------------------------------------
# This section is related to the spearman correlation calculations: -----------
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
    observed = spearman_correlation(data_a, data_b)
    count = 0

    for _ in range(num_permutations):
        perm = np.random.permutation(data_b)
        perm_rho = spearman_correlation(data_a, perm)
        if abs(perm_rho) >= abs(observed):
            count += 1

    return count / num_permutations

# -----------------------------------------------------------------------------
# This section is related to the ???: -----------
# -----------------------------------------------------------------------------


if __name__ == "__main__":
    data, platform_freq = load_data()

    print(f"corr: {spearman_correlation(data['Age'], data['SM_Time_val'])}, "
          f"p-value: {spearman_p_value(data['Age'], data['SM_Time_val'])}")

    print(f"corr: {spearman_correlation(data['Age'], data['MH_Score'])},"
          f"p-value: {spearman_p_value(data['Age'], data['MH_Score'])}")
