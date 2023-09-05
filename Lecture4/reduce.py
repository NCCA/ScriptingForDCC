#!/usr/bin/env python
from __future__ import annotations
import random
from functools import reduce
from typing import List

try:
    import matplotlib.pyplot as plt

    plot = True

except ImportError:
    plot = False

random.seed(1234)  # get the same result each time


class Point3:
    """A 3D point class"""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        """Initialize a Point3 instance"""
        self.x = x
        self.y = y
        self.z = z
    @classmethod
    def rand_point(cls : Point3,range: float = 10.0) -> Point3:
        """Return a random point"""
        return Point3(
            random.uniform(-range, range),
            random.uniform(range, -range),
            random.uniform(-range, range),
        )

    def __add__(self, rhs: Point3) -> Point3:
        """Add two Point3 instances"""
        return Point3(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)

    def __truediv__(self, rhs) -> Point3:
        p = Point3(self.x, self.y, self.z)
        """Add two Point3 instances"""
        if isinstance(rhs, Point3):
            p.x /= rhs.x
            p.y /= rhs.y
            p.z /= rhs.z
        else:
            p.x /= rhs
            p.y /= rhs
            p.z /= rhs
        return p

    def __repr__(self) -> str:
        """Return a string representation of a Point3"""
        return f"Point3({self.x}, {self.y}, {self.z})"

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


# create 10 random points
points = [Point3.rand_point() for i in range(100)]
print(points)
# use reduce to find the centroid of the points

centroid = reduce(lambda p1, p2: p1 + p2, points) / len(points)
print(centroid)

# This code does about the same thing as above
c = Point3(0, 0, 0)
for p in points:
    c += p
print(c / len(points))

if plot:
    for x, y, _ in points:
        plt.scatter(x, y)
    plt.scatter(centroid.x, centroid.y, marker="x")
    plt.show()
