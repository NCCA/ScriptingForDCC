#!/usr/bin/env python
from __future__ import annotations
import random

random.seed(1234)  # get the same result each time


class Point3:
    """A 3D point class"""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        """Initialize a Point3 instance"""
        self.x = x
        self.y = y
        self.z = z

    def rand_point() -> Point3:
        """Return a random point"""
        return Point3(
            random.uniform(-10, 10), random.uniform(10, -10), random.uniform(-10, 10)
        )

    def __repr__(self) -> str:
        """Return a string representation of a Point3"""
        return f"Point3({self.x}, {self.y}, {self.z})"


# create 10 random points
points = [Point3.rand_point() for i in range(10)]
print(points)
print(len(points))

above_ground = list(filter(lambda p: p.y >= 0.0, points))
print(above_ground)
print(len(above_ground))

# we can also do this with a list comprehension
above_ground_lc = [p for p in points if p.y >= 0.0]
print(above_ground_lc)
print(len(above_ground_lc))
