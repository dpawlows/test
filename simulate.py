import matplotlib.pyplot as plt

from ozone_model import OzoneModel
from visualization import load_roads, plot_valley_map


SHAPEFILE = "tl_2020_49035_roads.shp"


def rush_hour_rate(t: float) -> float:
    """Higher emission during rush hour (7-9am, 4-6pm)."""
    hour = t % 24
    if 7 <= hour < 9 or 16 <= hour < 18:
        return 5.0
    if 0 <= hour < 5:
        return 0.5
    return 1.0


roads, north_south, west_east, gdf = load_roads(SHAPEFILE, rush_hour_rate)
model = OzoneModel(north_south=north_south, west_east=west_east)

for road in roads:
    model.add_road_source(road)


if __name__ == "__main__":
    fig, _ = plot_valley_map(gdf)
    fig.savefig("slc_valley_map.png")
    plt.close(fig)

    steps = 24
    dt = 1.0  # hour
    for s in range(steps):
        model.step(dt)
        total = model.total_ozone()
        print(f"Hour {s+1}: total ozone={total:.2f}")
