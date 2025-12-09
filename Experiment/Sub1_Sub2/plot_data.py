import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import seaborn as sns

from collect_data import load_data
from process_data import build_contingency_table


def plot_platform_freq(platform_freq):
    """ Plots a barchart of the observed frequency of each SM platform. """

    plt.figure(figsize=(10, 6))

    # Custom colors for each bar.
    colors = ['#FF0000', '#1877F2', '#feda75', '#7289DA', '#FFFC00',
              '#E60023', '#1DA1F2', '#FF4500', '#ff00e7']

    platform_freq.plot(kind='bar', color=colors)

    plt.title("Social Media Platform Usage Frequency")
    plt.xlabel("Platform")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def plot_SM_use(data):
    """ Plots a barchart of the daily social media usage per age group. """

    # Set the time order.
    sm_time_order = [
        "Less than an Hour",
        "Between 1 and 2 hours",
        "Between 2 and 3 hours",
        "Between 3 and 4 hours",
        "Between 4 and 5 hours",
        "More than 5 hours"
    ]

    data["SM_Time"] = pd.Categorical(
        data["SM_Time"],
        categories=sm_time_order,
        ordered=True
    )

    # Calculate the frequencies of each age group.
    freq_table = (
        data.groupby(["SM_Time", "Age_Group"], observed=True)
        .size()
        .unstack(fill_value=0)
    )

    # Plot the bar chart.
    freq_table.plot(
        kind="bar",
        stacked=True,
        figsize=(10, 6),
    )

    plt.title("Social Media Usage Time by Age Group")
    plt.xlabel("Daily Social Media Usage (SM_Time)")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Age Group")
    plt.tight_layout()
    plt.show()


def plot_MH_score(data):
    """ Plots a scatterplot of the calculated MH score. """

    def gender_color(g):
        """ Maps a color to each gender group. """
        if g == 'Male':
            return 'blue'
        elif g == 'Female':
            return 'red'
        else:
            return 'purple'

    colors = data['Gender'].map(gender_color)

    plt.figure(figsize=(10, 6))

    plt.scatter(data['Age'], data['MH_Score'],
                c=colors, alpha=0.4, edgecolors='k')

    plt.title("Mental Health Score vs Age")
    plt.xlabel("Age")
    plt.ylabel("Average Mental Health Score")
    plt.grid(True)
    plt.tight_layout()

    # Calculate the x-steps of the plot.
    age_min = int(data['Age'].min())
    age_max = int(data['Age'].max())
    plt.xticks(range(age_min - age_min % 5, age_max + 5, 5))

    # Plots the points.
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Male',
               markerfacecolor='blue', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Female',
               markerfacecolor='red', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Other',
               markerfacecolor='purple', markersize=10)
    ]
    plt.legend(handles=legend_elements, title="Gender")

    plt.show()


def plot_contingency_table(data, normalized):
    """Plot a heatmap of platform usage by age group."""

    contingency_table = build_contingency_table(data)

    # Normalize by row (age group) if true.
    if normalized:
        plot_table = contingency_table.div(contingency_table.sum(axis=1),
                                           axis=0)
        fmt = ".2f"
        cmap = "Blues"
        title = "Relative Platform Usage by Age Group (Normalized)"
    else:
        plot_table = contingency_table
        fmt = "d"
        cmap = "Blues"
        title = "Platform Usage by Age Group (Raw Counts)"

    plt.figure(figsize=(10, 6))
    sns.heatmap(plot_table, annot=True, fmt=fmt, cmap=cmap,
                cbar=normalized,
                cbar_kws={'label': 'Proportion'} if normalized else None)

    plt.title(title)
    plt.ylabel("Age Group")
    plt.xlabel("Platform")
    plt.tight_layout()
    plt.show()


def plot_MH_age_group(data):
    """ Plots a boxplot of the MH score for different age groups. """

    plt.figure(figsize=(8, 5))
    sns.boxplot(x="Age_Group", y="MH_Score", data=data)
    sns.stripplot(x="Age_Group", y="MH_Score", data=data,
                  color="black", alpha=0.2)

    plt.title("Mental Health Scores by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Mental Health Score")
    plt.tight_layout()
    plt.show()


def plot_avg_platform_amount(data):
    """ Plot the average number of platforms used per age group. """

    # Compute the average per age group
    avg_counts = (
        data.groupby("Age_Group", observed=True)["Platform_Count"]
        .mean()
        .reindex(data["Age_Group"].cat.categories)
    )

    plt.figure(figsize=(8, 5))
    avg_counts.plot(kind="bar", color="skyblue", edgecolor="black")

    plt.title("Average Number of Platforms Used per Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Average Platform Count")
    plt.ylim(0, avg_counts.max() + 0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data, platform_freq = load_data()

    # Uncomment the necessary tests
    # plot_platform_freq(platform_freq)
    # plot_SM_use(data)
    # plot_MH_score(data)
    # plot_MH_age_group(data)
    # plot_avg_platform_amount(data)
    # plot_contingency_table(data, False)  # Not normalized
    # plot_contingency_table(data, True)  # Normalized
