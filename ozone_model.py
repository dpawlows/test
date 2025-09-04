from dataclasses import dataclass, field
from typing import Callable, List, Tuple
import math

# Simple 3D ozone model using finite difference scheme

@dataclass
class RoadSource:
    start: Tuple[float, float]
    end: Tuple[float, float]
    rate_func: Callable[[float], float]
    name: str = ""

    def cells(self, dx: float, dy: float) -> List[Tuple[int, int]]:
        """Return grid cells along the road"""
        x0, y0 = self.start
        x1, y1 = self.end
        length_x = x1 - x0
        length_y = y1 - y0
        steps = int(max(abs(length_x / dx), abs(length_y / dy))) + 1
        cells = []
        for s in range(steps + 1):
            t = s / steps
            xi = x0 + t * length_x
            yi = y0 + t * length_y
            i = int(xi / dx)
            j = int(yi / dy)
            cells.append((i, j))
        return list(dict.fromkeys(cells))

@dataclass
class OzoneModel:
    north_south: Tuple[float, float]
    west_east: Tuple[float, float]
    top_altitude: float = 2000.0
    dx: float = 1000.0
    dy: float = 1000.0
    dz: float = 100.0
    u: float = 1.0  # north-south wind velocity
    v: float = 0.0  # west-east wind velocity
    w: float = 0.1  # vertical velocity
    D: float = 0.1  # diffusion coefficient
    top_open: bool = True

    grid: List[List[List[float]]] = field(init=False)
    sources: List[Tuple[RoadSource, List[Tuple[int, int]]]] = field(default_factory=list)
    current_time: float = 0.0

    def __post_init__(self):
        self.nx = int((self.north_south[1] - self.north_south[0]) / self.dx) + 1
        self.ny = int((self.west_east[1] - self.west_east[0]) / self.dy) + 1
        self.nz = int(self.top_altitude / self.dz) + 1
        self.grid = [[[0.0 for _ in range(self.nz)] for _ in range(self.ny)] for _ in range(self.nx)]

    def add_road_source(self, road: RoadSource):
        cells = road.cells(self.dx, self.dy)
        self.sources.append((road, cells))

    def step(self, dt: float):
        new_grid = [[[0.0 for _ in range(self.nz)] for _ in range(self.ny)] for _ in range(self.nx)]
        for i in range(self.nx):
            for j in range(self.ny):
                for k in range(self.nz):
                    c = self.grid[i][j][k]
                    # Advection (upwind difference)
                    if i > 0:
                        c -= dt * self.u * (c - self.grid[i - 1][j][k]) / self.dx
                    if j > 0:
                        c -= dt * self.v * (c - self.grid[i][j - 1][k]) / self.dy
                    if k > 0:
                        c -= dt * self.w * (c - self.grid[i][j][k - 1]) / self.dz
                    # Diffusion (simple)
                    if i > 0 and i < self.nx - 1:
                        c += dt * self.D * (self.grid[i + 1][j][k] - 2 * c + self.grid[i - 1][j][k]) / (self.dx ** 2)
                    if j > 0 and j < self.ny - 1:
                        c += dt * self.D * (self.grid[i][j + 1][k] - 2 * c + self.grid[i][j - 1][k]) / (self.dy ** 2)
                    if k > 0 and k < self.nz - 1:
                        c += dt * self.D * (self.grid[i][j][k + 1] - 2 * c + self.grid[i][j][k - 1]) / (self.dz ** 2)
                    new_grid[i][j][k] = c

        # Apply sources at ground level
        for road, cells in self.sources:
            rate = road.rate_func(self.current_time)
            for i, j in cells:
                if 0 <= i < self.nx and 0 <= j < self.ny:
                    new_grid[i][j][0] += rate * dt

        # Apply top boundary
        if self.top_open:
            for i in range(self.nx):
                for j in range(self.ny):
                    new_grid[i][j][self.nz - 1] = 0.0

        self.grid = new_grid
        self.current_time += dt

    def total_ozone(self) -> float:
        return sum(sum(sum(layer for layer in row) for row in plane) for plane in self.grid)

