from ozone_model import OzoneModel, RoadSource

# Boundaries for SLC area (arbitrary units)
# north_south: 0 at north (2300 N) to 16900 at south (14600 S)
# west_east: 0 at west (Route 85) to 20000 at east (Wasatch)
model = OzoneModel(north_south=(0, 16900), west_east=(0, 20000))

# Example emission rate functions

def rush_hour_rate(t: float) -> float:
    """Higher emission during rush hour (7-9am, 4-6pm)"""
    hour = t % 24
    if 7 <= hour < 9 or 16 <= hour < 18:
        return 5.0
    if 0 <= hour < 5:
        return 0.5
    return 1.0

# Add major roads (simplified as straight lines)
# I-15 runs north-south through center of valley
model.add_road_source(RoadSource(start=(0, 10000), end=(16900, 10000), rate_func=rush_hour_rate))
# I-215 partial loop (approx)
model.add_road_source(RoadSource(start=(5000, 18000), end=(15000, 18000), rate_func=rush_hour_rate))
# I-80 east-west
model.add_road_source(RoadSource(start=(8000, 0), end=(8000, 20000), rate_func=rush_hour_rate))

# Simple simulation
if __name__ == "__main__":
    steps = 24
    dt = 1.0  # hour
    for s in range(steps):
        model.step(dt)
        total = model.total_ozone()
        print(f"Hour {s+1}: total ozone={total:.2f}")
