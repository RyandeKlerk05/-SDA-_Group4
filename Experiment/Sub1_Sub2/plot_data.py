import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from collect_data import load_data


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

    age_min = int(data['Age'].min())
    age_max = int(data['Age'].max())
    plt.xticks(range(age_min - age_min % 5, age_max + 5, 5))

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


if __name__ == "__main__":
    data, platform_freq = load_data()
    plot_platform_freq(platform_freq)
    plot_MH_score(data)
