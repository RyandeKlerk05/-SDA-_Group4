import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pycountry_convert as pc

data = pd.read_csv("IHME_original_file.csv")
data2 = pd.read_csv("social_media_users_2021.csv")

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

# create new columns for Continents
data2['Continent'] = data2['Country'].apply(country_to_continent)
data['Continent'] = data['location'].apply(country_to_continent)
# filter out unidentifiable countries
data = data[data['Continent'] != "Unknown"]
data2 = data2[data2['Continent'] != "Unknown"]

data.to_csv("continent_mental_health.csv", index=False)
data2.to_csv("continent_media_use.csv", index=False)

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
    x = data2[data2['Continent'] == continent]['Social Media Users (N)'].values
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


