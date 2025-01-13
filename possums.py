
import polars as pl
import numpy as np
import matplotlib.pyplot as plt


def make_effect_size_vr_scatter_plot_figure_3():
    possums = pl.read_csv("data/possums.csv")[:, 4:]
    possums = possums.filter(pl.col("footlgth") != "NA")
    possums = possums.with_columns(footlgth=pl.col("footlgth").cast(pl.Float64))
    males = possums.filter(pl.col("sex") == "m")
    females = possums.filter(pl.col("sex") == "f")

    male_means = males.mean()[:, 2:]
    female_means = females.mean()[:, 2:]

    male_variances = males.var()[:, 2:]
    female_variances = females.var()[:, 2:]

    cohen_ds = male_means - female_means
    pooled_sd = ((((len(males) - 1) * male_variances) + ((len(females) - 1) * female_variances)) / (len(males) + len(females) - 2))
    cohen_ds /= pl.DataFrame(np.sqrt(pooled_sd))

    m, b = np.polyfit(np.array(cohen_ds).flatten(), np.array(male_variances / female_variances).flatten(), 1)
    plt.scatter(cohen_ds, male_variances / female_variances)
    plt.plot(np.array(cohen_ds).T, m*np.array(cohen_ds).T + b, color='red')
    plt.xlabel("cohen's d")
    plt.ylabel("variability ratios")
    plt.show()

if __name__ == "__main__":
    make_effect_size_vr_scatter_plot_figure_3()