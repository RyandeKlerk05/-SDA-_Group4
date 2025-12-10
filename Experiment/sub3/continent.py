import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pycountry_convert as pc

data = pd.read_csv("IHME_original_file.csv")
data2 = pd.read_csv("percentages_population_users.csv")

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
        cdf_x = np.sum(x <= i) / len(x) # the percent of points that are smaller than the current value
        cdf_y = np.sum(y <= i) / len(y)
        diff = abs(cdf_x - cdf_y)
        if diff > max_d:
            max_d = diff
    count = 0 # the number of times that the distance is higher than real distance
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
plt.ylabel(f"Average mental disorder")
plt.title("Comparison of mental disorder by Continent")
plt.grid(True, axis='y', alpha=0.3)
plt.legend()
plt.savefig("continent_comparison_mental.png", dpi=300)
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
plt.savefig("continent_comparison_media.png", dpi=300)
plt.show()

# Continents selected for permutation test

continent_list = plot_data['Continent'] 
continent_list2 = plot_data2['Continent']

# mental disorder
print('mental disorder')
for i in range(len(continent_list)):
    for j in range(i + 1, len(continent_list)): # avoid repitition
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

        x1 = x1[~np.isnan(x1)] # filter out NaN values 
        x2 = x2[~np.isnan(x2)]

        pvalue = ks_test(x1, x2)
        print(f"{c1} vs {c2}: p-value = {pvalue:.4f}")
        if pvalue > 0.05:
            print(f"There is no proof that {c1} and {c2} show a statistically meaningful difference.\n")
        else:
            print(f"{c1} and {c2} show a statistically meaningful difference.\n")

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
        print(f"{c1} vs {c2}: p-value = {pvalue:.4f}")
        if pvalue > 0.05:
            print(f"There is no proof that {c1} and {c2} show a statistically meaningful difference.\n")
        else:
            print(f"{c1} and {c2} show a statistically meaningful difference.\n")
