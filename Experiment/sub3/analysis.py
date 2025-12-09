import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_mh = pd.read_csv("merged_final.csv")
df_users = pd.read_csv("social_media_users_2021.csv")
df_pop = pd.read_csv("IHME-GBD_2023_DATA-aeeaa03f-1.csv")

df_pop_clean = df_pop[(df_pop["measure_name"] == "Population") &
                      (df_pop["metric_name"] == "Number") &
                      (df_pop["year"] == 2021)]

df_pop_clean = df_pop_clean[["location_name", "val"]]
df_pop_clean.columns = ["Country", "Population"]

df = df_mh.merge(df_users, on="Country", how="inner")
df = df.merge(df_pop_clean, on="Country", how="inner")

df["SocialMediaShare"] = (df["Social Media Users (N)"] / df["Population"]) * 100

X = df["SocialMediaShare"].values
y = df["MentalHealthPercent"].values

mask = ~np.isnan(X) & ~np.isnan(y)
X = X[mask]
y = y[mask]

x_mean = np.mean(X)
y_mean = np.mean(y)

beta1 = np.sum((X - x_mean) * (y - y_mean)) / np.sum((X - x_mean)**2)

beta0 = y_mean - beta1 * x_mean

print("Slope (β1):", beta1)
print("Intercept (β0):", beta0)

y_pred = beta0 + beta1 * X

plt.figure(figsize=(8,6))
plt.scatter(X, y, color="#4C72B0", alpha=0.8, edgecolor="white", s=70)
x_line = np.linspace(min(X), max(X), 100)
y_line = beta0 + beta1 * x_line
plt.plot(x_line, y_line, color="#DD8452", linewidth=2.5, label="Regression Line")
plt.xlabel("Social Media Share (% of Population)", fontsize=12)
plt.title("Linear Regression: Social Media Share vs Mental Health", fontsize=14, fontweight="bold")
plt.ylabel("Mental Health Prevalence (%)", fontsize=12)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

data = np.column_stack((X, y))
k = 3

np.random.seed(42)
centroids = data[np.random.choice(range(len(data)), k, replace=False)]

def assign_clusters(data, centroids):
    distances = np.linalg.norm(data[:, None] - centroids[None, :], axis=2)
    return np.argmin(distances, axis=1)

def update_centroids(data, clusters, k):
    return np.array([data[clusters == i].mean(axis=0) for i in range(k)])

for _ in range(10):
    clusters = assign_clusters(data, centroids)
    new_centroids = update_centroids(data, clusters, k)

    if np.allclose(new_centroids, centroids):
        break

    centroids = new_centroids

plt.figure(figsize=(8,6))
colors = ["#4C72B0", "#55A868", "#C44E52"]
for cluster_id in range(k):
    cluster_points = data[clusters == cluster_id]
    plt.scatter(cluster_points[:,0],
                cluster_points[:,1],
                s=70,
                alpha=0.8,
                color=colors[cluster_id],
                label=f"Cluster {cluster_id+1}",
                edgecolor="white")
plt.scatter(centroids[:,0],
            centroids[:,1],
            c="black",
            s=180,
            marker="X",
            label="Centroids")
plt.xlabel("Social Media Share (% of Population)", fontsize=12)
plt.ylabel("Mental Health Prevalence (%)", fontsize=12)
plt.title("K-Means Clustering: Social Media vs Mental Health", fontsize=14, fontweight="bold")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

#asked chatgpt for continent grouping
continent_map = {
    # Asia
    'Philippines':'Asia','Thailand':'Asia','Sri Lanka':'Asia','Myanmar':'Asia','Malaysia':'Asia',
    'China':'Asia','Indonesia':'Asia','Cambodia':'Asia','Kazakhstan':'Asia','Armenia':'Asia',
    'Turkmenistan':'Asia','Tonga':'Oceania','Tajikistan':'Asia','Mongolia':'Asia','Kiribati':'Oceania',
    'Samoa':'Oceania','Papua New Guinea':'Oceania','Georgia':'Asia','Japan':'Asia','Singapore':'Asia',
    'Uzbekistan':'Asia','Palestine':'Asia','Nepal':'Asia','Bangladesh':'Asia','Pakistan':'Asia',
    'India':'Asia','Yemen':'Asia','Bhutan':'Asia','Maldives':'Asia','Saudi Arabia':'Asia',
    'Bahrain':'Asia','Iraq':'Asia','Jordan':'Asia','Turkey':'Asia','Israel':'Asia','Afghanistan': 'Asia',

    # Oceania
    'Fiji':'Oceania','Solomon Islands':'Oceania','Vanuatu':'Oceania','New Zealand':'Oceania',
    'American Samoa':'Oceania','Cook Islands':'Oceania','Tuvalu':'Oceania','Palau':'Oceania','Nauru':'Oceania',
    'Australia':'Oceania','Samoa':'Oceania',

    # Europe
    'Russian Federation':'Europe','Andorra':'Europe','Lithuania':'Europe','Romania':'Europe',
    'Czechia':'Europe','Serbia':'Europe','Ukraine':'Europe','Croatia':'Europe','Estonia':'Europe',
    'Belgium':'Europe','Bulgaria':'Europe','Hungary':'Europe','Slovakia':'Europe','North Macedonia':'Europe',
    'Slovenia':'Europe','Montenegro':'Europe','Latvia':'Europe','Poland':'Europe','Albania':'Europe',
    'Denmark':'Europe','Finland':'Europe','France':'Europe','Greece':'Europe','Germany':'Europe',
    'Ireland':'Europe','Spain':'Europe','Sweden':'Europe','Norway':'Europe','Iceland':'Europe',
    'Italy':'Europe','Portugal':'Europe','Luxembourg':'Europe','Malta':'Europe','Netherlands':'Europe',
    'United Kingdom':'Europe','San Marino':'Europe','Monaco':'Europe','Switzerland':'Europe',

    # Africa
    'Egypt':'Africa','Algeria':'Africa','Morocco':'Africa','Tunisia':'Africa','Libya':'Africa',
    'Djibouti':'Africa','Mozambique':'Africa','Gabon':'Africa','Kenya':'Africa','Ethiopia':'Africa',
    'Malawi':'Africa','Somalia':'Africa','Eritrea':'Africa','Madagascar':'Africa','Comoros':'Africa',
    'Mauritius':'Africa','Angola':'Africa','Burundi':'Africa','Uganda':'Africa','Zambia':'Africa',
    'Zimbabwe':'Africa','South Africa':'Africa','Botswana':'Africa','Lesotho':'Africa','Ghana':'Africa',
    'Cabo Verde':'Africa','Burkina Faso':'Africa','Eswatini':'Africa','Cameroon':'Africa','Benin':'Africa',
    'Liberia':'Africa','Chad':'Africa','Gambia':'Africa','Mali':'Africa','Namibia':'Africa','Niger':'Africa',
    'Nigeria':'Africa','Mauritania':'Africa','Seychelles':'Africa','Senegal':'Africa','South Sudan':'Africa',
    'Sierra Leone':'Africa','Togo':'Africa','Sudan':'Africa','Rwanda':'Africa','Guinea':'Africa','Equatorial Guinea': 'Africa',

    # North America
    'United States':'North America','Canada':'North America','Bahamas':'North America','Grenada':'North America',
    'Cuba':'North America','Haiti':'North America','Jamaica':'North America','Barbados':'North America',
    'Belize':'North America','Guyana':'South America','Panama':'North America','Honduras':'North America',
    'El Salvador':'North America','Costa Rica':'North America','Guatemala':'North America','Mexico':'North America',
    'Bermuda':'North America','Dominica':'North America','Saint Lucia':'North America','Nicaragua':'North America',

    # South America
    'Argentina':'South America','Brazil':'South America','Chile':'South America','Peru':'South America',
    'Ecuador':'South America','Colombia':'South America','Paraguay':'South America','Uruguay':'South America',
    'Suriname':'South America','Bolivia':'South America','Venezuela':'South America','Guyana':'South America',

    # Middle East (treated under Asia or Africa depending on country)
    'Kuwait':'Asia','Oman':'Asia','Qatar':'Asia','United Arab Emirates':'Asia',

    # Missing small territories (assign manually)
    'Guam':'Oceania','Greenland':'North America'
}
#checked for missing countries already

df_cont = pd.DataFrame(list(continent_map.items()), columns=['Country','Continent'])
df = df.merge(df_cont, on="Country", how="left")
print(df.columns)
print("Missing continents:", df["Continent"].isna().sum())
continent_sm = df.groupby("Continent")["SocialMediaShare"].mean()
continent_sm_df = continent_sm.reset_index()
continent_sm_df.columns = ["Continent", "AverageSocialMediaShare"]

print("Average Social Media Share per Continent:")
print(continent_sm_df)

plt.figure(figsize=(10,6))
plt.bar(
    continent_sm_df["Continent"],
    continent_sm_df["AverageSocialMediaShare"],
    color="#4C72B0",
    edgecolor="black"
)
plt.xlabel("Continent", fontsize=12)
plt.ylabel("Average Social Media Share (% of Population)", fontsize=12)
plt.title("Average Social Media Share by Continent", fontsize=14, fontweight="bold")
plt.grid(axis="y", alpha=0.3)
plt.show()
