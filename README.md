# Ozone Simulation

This repository contains a simple Python implementation to estimate ozone released from major roadways in the Salt Lake City valley. The example uses a coarse 3D grid and simple advection/diffusion scheme.  Geographic data for the major roads are loaded from a shapefile using ``geopandas`` and ``matplotlib`` is used for plotting.

## Files

- `ozone_model.py` – minimal ozone transport model.
- `visualization.py` – helpers to load road data and render maps.
- `simulate.py` – runs a 24‑hour example simulation with road sources from ``slc_roads.shp``.

## Running the example

```bash
python3 simulate.py
```

The script prints the total ozone in the domain at each hourly step.
