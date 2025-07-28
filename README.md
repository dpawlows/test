# Ozone Simulation

This repository contains a simple Python implementation to estimate ozone released from major roadways in the Salt Lake City valley. The example uses a coarse 3D grid and simple advection/diffusion scheme implemented without external dependencies.

## Files

- `ozone_model.py` – minimal ozone transport model.
- `simulate.py` – runs a 24‑hour example simulation with basic road sources.

## Running the example

```bash
python3 simulate.py
```

The script prints the total ozone in the domain at each hourly step.
