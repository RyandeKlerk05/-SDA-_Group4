import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pycountry_convert as pc

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]

data = pd.read_csv(BASE_DIR / "Data/IHME_original_file.csv")
data2 = pd.read_csv(BASE_DIR / "Data/percentages_population_users.csv")


def country_to_continent(country_name):
    '''
    convert country names to continent names
    '''
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        continent_name = pc.convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except: # if it fails to get a continent name
        return "Unknown"


def ks_test(x, y):
    '''
    ks test

    '''
    x = np.array(x)
    y = np.array(y)
    combined = np.concatenate([x, y])
    combined = np.sort(combined)
    max_d = 0

    for i in combined:
        cdf_x = np.sum(x <= i) / len(x)  # the percent of points that are smaller than the current value
        cdf_y = np.sum(y <= i) / len(y)
        diff = abs(cdf_x - cdf_y)
        if diff > max_d:
            max_d = diff
    count = 0  # the number of times that the distance is higher than real distance
    combined2 = np.concatenate([x, y])
    N = 1000

    for i in range(N):
        np.random.shuffle(combined2)
        x_2 = combined2[:len(x)]
        y_2 = combined2[len(x):]
        p_max_d = 0
        for c in combined:
            cx_2 = np.sum(x_2 <= c) / len(x_2)
            cy_2 = np.sum(y_2 <= c) / len(y_2)
            perm_d = abs(cx_2 - cy_2)
            if perm_d > p_max_d:
                p_max_d = perm_d

        if p_max_d >= max_d:
            count += 1

    pvalue = count / N
    return pvalue


# create new columns for Continents
data2['Continent'] = data2['Country'].apply(country_to_continent)
data['Continent'] = data['location'].apply(country_to_continent)

# filter out unknown Continents
data = data[data['Continent'] != "Unknown"]
data2 = data2[data2['Continent'] != "Unknown"]

data.to_csv("continent_mental_health.csv", index=False)
data2.to_csv("continent_media_use.csv", index=False)

# bootstrap
N = 10000
continents = data['Continent'].unique()
continents2 = data2['Continent'].unique()

plot_data = {
    'Continent': [],
    'Mean': [],
    'CI_Lower': [],
    'CI_Upper': []
}

plot_data2 = {
    'Continent': [],
    'Mean': [],
    'CI_Lower': [],
    'CI_Upper': []
}

for continent in continents:
    x = data[(data['Continent'] == continent) & (data['year'] == 2021)]['val'].values
    x = x[~np.isnan(x)]  # filter out NaN values
    boot_means = []
    for i in range(N):
        sample = np.random.choice(x, size=len(x), replace=True)
        boot_means.append(np.mean(sample))

    ci_l = np.percentile(boot_means, 2.5)
    ci_u = np.percentile(boot_means, 97.5)
    mean = np.mean(boot_means)

    plot_data['Continent'].append(continent)
    plot_data['Mean'].append(mean)
    plot_data['CI_Lower'].append(ci_l)
    plot_data['CI_Upper'].append(ci_u)


plt.figure(figsize=(10, 6))

x_pos = range(len(plot_data['Continent']))
means = plot_data['Mean']
y_errors = [
    [m - l for m, l in zip(means, plot_data['CI_Lower'])],
    [u - m for u, m in zip(plot_data['CI_Upper'], means)]
]

plt.errorbar(x_pos, means, yerr=y_errors, fmt='o',
             color='blue', ecolor='red', elinewidth=3, capsize=5, label='Mean & 95% CI')

plt.xticks(x_pos, plot_data['Continent'])
plt.xlabel("Continent")
plt.ylabel("Average mental disorder")
plt.title("Comparison of mental disorder by Continent")
plt.grid(True, axis='y', alpha=0.3)
plt.legend()
# plt.savefig("continent_comparison_mental.png", dpi=300)
plt.show()

for continent in continents2:
    x = data2[data2['Continent'] == continent]['Social Media Users (%)'].values
    x = x[~np.isnan(x)]  # filter out NaN values
    boot_means = []
    for i in range(N):
        sample = np.random.choice(x, size=len(x), replace=True)
        boot_means.append(np.mean(sample))

    ci_l = np.percentile(boot_means, 2.5)
    ci_u = np.percentile(boot_means, 97.5)
    mean = np.mean(boot_means)

    plot_data2['Continent'].append(continent)
    plot_data2['Mean'].append(mean)
    plot_data2['CI_Lower'].append(ci_l)
    plot_data2['CI_Upper'].append(ci_u)


plt.figure(figsize=(10, 6))

x_pos2 = range(len(plot_data2['Continent']))
means2 = plot_data2['Mean']
y_errors2 = [
    [m - l for m, l in zip(means2, plot_data2['CI_Lower'])],
    [u - m for u, m in zip(plot_data2['CI_Upper'], means2)]
]

plt.errorbar(x_pos2, means2, yerr=y_errors2, fmt='o',
             color='blue', ecolor='red', elinewidth=3, capsize=5, label='Mean & 95% CI')
plt.xticks(x_pos2, plot_data2['Continent'])
plt.xlabel("Continent")
plt.ylabel(f"Social Media Users")
plt.title("Comparison of Social Media Users by Continent")
plt.grid(True, axis='y', alpha=0.3)
plt.legend()
# plt.savefig("continent_comparison_media.png", dpi=300)
plt.show()

# Continents selected for permutation test

continent_list = plot_data['Continent']
continent_list2 = plot_data2['Continent']
# create a new matrix with fully nan
p_map = pd.DataFrame(np.nan, index=continent_list, columns=continent_list)
p_map2 = pd.DataFrame(np.nan, index=continent_list2, columns=continent_list2)

# mental disorder
print('mental disorder')
for i in range(len(continent_list)):
    for j in range(i + 1, len(continent_list)):  # avoid repitition
        c1 = continent_list[i]
        c2 = continent_list[j]

        lower1 = plot_data['CI_Lower'][i]
        upper1 = plot_data['CI_Upper'][i]
        lower2 = plot_data['CI_Lower'][j]
        upper2 = plot_data['CI_Upper'][j]

        overlap = min(upper1, upper2) - max(lower1, lower2)
        # only calculate two continents that have an overlap

        if overlap <= 0:
            continue  # if there is no overlap

        x1 = data[(data['Continent'] == c1) & (data['year'] == 2021)]['val'].values
        x2 = data[(data['Continent'] == c2) & (data['year'] == 2021)]['val'].values

        x1 = x1[~np.isnan(x1)]  # filter out NaN values
        x2 = x2[~np.isnan(x2)]

        pvalue = ks_test(x1, x2)

        p_map.loc[c1, c2] = pvalue
        p_map.loc[c2, c1] = pvalue
        print(f"{c1} vs {c2}: p-value = {pvalue:.4f}")
        if pvalue > 0.05:
            print(f"There is no proof that {c1} and {c2} "
                  f"show a statistically meaningful difference.\n")
        else:
            print(f"{c1} and {c2} show a statistically "
                  f"meaningful difference.\n")

# set value of diagonal to 1.0
np.fill_diagonal(p_map.values, np.nan)

fig, ax = plt.subplots(figsize=(10, 8))
cmap = plt.cm.Blues.copy()
cmap.set_bad(color="lightgrey")  # make invalid grid grey
masked = np.ma.masked_invalid(p_map.values)  # mask all nan as invalid

im = ax.imshow(masked, vmin=0, vmax=1, cmap=cmap)
# set labels to name of continent
ax.set_xticks(np.arange(len(continent_list)))
ax.set_yticks(np.arange(len(continent_list)))
ax.set_xticklabels(continent_list, rotation=45, ha="right")
ax.set_yticklabels(continent_list)

for i in range(len(continent_list)):
    for j in range(len(continent_list)):
        val = p_map.iloc[i, j]
        if np.isnan(val):  # skip the nan
            continue
        ax.text(j, i, f"{val:.3f}", ha="center", va="center")

cbar = plt.colorbar(im, ax=ax)
cbar.set_label("p-value")

ax.set_title("Mental disorder: KS-test p-values")
plt.tight_layout()
# plt.savefig("pvalue_heatmap_mental.png", dpi=300)
plt.show()

# media usage
print('media usage')
for i in range(len(continent_list2)):
    for j in range(i + 1, len(continent_list2)):
        c1 = continent_list2[i]
        c2 = continent_list2[j]

        lower1 = plot_data2['CI_Lower'][i]
        upper1 = plot_data2['CI_Upper'][i]
        lower2 = plot_data2['CI_Lower'][j]
        upper2 = plot_data2['CI_Upper'][j]

        overlap = min(upper1, upper2) - max(lower1, lower2)

        if overlap <= 0:
            continue  # if there is no overlap

        x1 = data2[data2['Continent'] == c1]['Social Media Users (%)'].values
        x2 = data2[data2['Continent'] == c2]['Social Media Users (%)'].values

        x1 = x1[~np.isnan(x1)]
        x2 = x2[~np.isnan(x2)]

        pvalue = ks_test(x1, x2)

        p_map2.loc[c1, c2] = pvalue
        p_map2.loc[c2, c1] = pvalue
        print(f"{c1} vs {c2}: p-value = {pvalue:.4f}")
        if pvalue > 0.05:
            print(f"There is no proof that {c1} and {c2} "
                  f"show a statistically meaningful difference.\n")
        else:
            print(f"{c1} and {c2} show a statistically "
                  f"meaningful difference.\n")

np.fill_diagonal(p_map.values, np.nan)

fig, ax = plt.subplots(figsize=(10, 8))
cmap = plt.cm.Reds.copy()
cmap.set_bad(color="lightgrey")  # make invalid grid grey
masked = np.ma.masked_invalid(p_map2.values)  # mask all nan as invalid

im = ax.imshow(masked, vmin=0, vmax=1, cmap=cmap)
# set labels to name of continent
ax.set_xticks(np.arange(len(continent_list2)))
ax.set_yticks(np.arange(len(continent_list2)))
ax.set_xticklabels(continent_list2, rotation=45, ha="right")
ax.set_yticklabels(continent_list2)

for i in range(len(continent_list2)):
    for j in range(len(continent_list2)):
        val = p_map2.iloc[i, j]
        if np.isnan(val):  # skip the nan
            continue
        ax.text(j, i, f"{val:.3f}", ha="center", va="center")

cbar = plt.colorbar(im, ax=ax)
cbar.set_label("p-value")

ax.set_title("Media usage: KS-test p-values")
plt.tight_layout()
# plt.savefig("pvalue_heatmap_media.png", dpi=300)
plt.show()
