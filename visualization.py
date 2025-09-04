import matplotlib.pyplot as plt
from typing import Iterable


def plot_valley_map(north_south: tuple, west_east: tuple, roads: Iterable):
    """Create a basic map of the valley with major roadways."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(west_east)
    ax.set_ylim(north_south)
    ax.set_xlabel("West-East (m)")
    ax.set_ylabel("North-South (m)")
    ax.set_title("Salt Lake City Valley")

    for road in roads:
        x0, y0 = road.start
        x1, y1 = road.end
        xs = [y0, y1]
        ys = [x0, x1]
        ax.plot(xs, ys, color="black")
        name = getattr(road, "name", "")
        if name:
            mx = sum(xs) / 2
            my = sum(ys) / 2
            ax.text(mx, my, name, ha="center", va="center", fontsize=8, backgroundcolor="white")

    return fig, ax
