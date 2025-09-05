"""Utilities for visualizing the simulation using geographic data."""

from typing import Callable, Iterable, List, Tuple

import geopandas as gpd
import matplotlib.pyplot as plt

from ozone_model import RoadSource


def load_roads(
    shapefile_path: str, rate_func: Callable[[float], float]
) -> Tuple[List[RoadSource], Tuple[float, float], Tuple[float, float], gpd.GeoDataFrame]:
    """Read road centerlines from ``shapefile_path``.

    Returns the generated :class:`RoadSource` objects, the domain bounds as
    ``(north_south, west_east)`` tuples, and the underlying
    :class:`geopandas.GeoDataFrame` for mapping purposes.
    """

    gdf = gpd.read_file(shapefile_path)
    roads: List[RoadSource] = []
    for _, row in gdf.iterrows():
        geom = row.geometry
        if geom.is_empty:
            continue
        name = row.get("name") or row.get("NAME") or ""

        def _add_segment(coords):
            roads.append(
                RoadSource(
                    start=(coords[0][1], coords[0][0]),
                    end=(coords[-1][1], coords[-1][0]),
                    rate_func=rate_func,
                    name=name,
                )
            )

        if geom.geom_type == "LineString":
            coords = list(geom.coords)
            _add_segment(coords)
        elif geom.geom_type == "MultiLineString":
            for line in geom.geoms:
                coords = list(line.coords)
                _add_segment(coords)

    minx, miny, maxx, maxy = gdf.total_bounds
    north_south = (miny, maxy)
    west_east = (minx, maxx)
    return roads, north_south, west_east, gdf


def plot_valley_map(gdf: gpd.GeoDataFrame):
    """Plot roads from ``gdf`` on a map of the Salt Lake City valley."""

    fig, ax = plt.subplots(figsize=(8, 8))
    gdf.plot(ax=ax, color="black", linewidth=0.5)

    ax.set_xlabel("West-East (m)")
    ax.set_ylabel("North-South (m)")
    ax.set_title("Salt Lake City Valley")

    name_field = None
    for candidate in ("name", "NAME", "Name"):
        if candidate in gdf.columns:
            name_field = candidate
            break

    if name_field:
        for _, row in gdf.iterrows():
            label = row[name_field]
            if not label:
                continue
            # Place label near the middle of the line
            pt = row.geometry.interpolate(0.5, normalized=True).coords[0]
            ax.text(
                pt[0],
                pt[1],
                label,
                ha="center",
                va="center",
                fontsize=6,
                backgroundcolor="white",
            )

    ax.set_xlim(gdf.total_bounds[[0, 2]])
    ax.set_ylim(gdf.total_bounds[[1, 3]])
    return fig, ax
