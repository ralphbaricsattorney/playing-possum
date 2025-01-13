
import polars as pl
import numpy as np
import matplotlib.pyplot as plt

def make_devil_histogram_figure_1():
    data = pl.read_csv("data/File 3_ Asymptotic whisker length of wild Tasmanian devils.csv")
    data = data.select(["sex", "name", "extradermal_length_mm"])
    males = data.filter(pl.col("sex") == "Male").group_by("name").median()
    females = data.filter(pl.col("sex") == "Female").group_by("name").median()

    male_means = males.mean()[:, 2]
    female_means = females.mean()[:, 2]

    male_variances = males.var()[:, 2]
    female_variances = females.var()[:, 2]

    cohen_ds = male_means - female_means
    pooled_sd = ((((len(males) - 1) * male_variances) + ((len(females) - 1) * female_variances)) / (len(males) + len(females) - 2))
    cohen_ds /= np.sqrt(pooled_sd)

    plt.hist(males["extradermal_length_mm"], alpha=.5, label="Male", color="Blue", bins=25)
    plt.hist(females["extradermal_length_mm"], alpha=.5, label="Female", color="Magenta", bins=25)
    plt.xlabel("Median Aggregated Tasmanian devil whisker length (mm)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    make_devil_histogram_figure_1()
