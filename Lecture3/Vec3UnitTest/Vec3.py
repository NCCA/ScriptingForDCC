"""
Simple Float only Vec3 class for 3D graphics
"""
from __future__ import annotations
import math


class Vec3:
    __slots__ = ["x", "y", "z"]
    """by using slots we fix our class attributes to x,y,z
    Note below we use type hints to help mypy but these 
    are still part of the slots and there is no class dictionary"""
    x: float
    y: float
    z: float

    def __init__(self, x : float=0.0 , y : float =0.0 , z: float=0.0) -> None:
        """We prefer float here hence the type hint however other will still work"""
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, rhs: Vec3) -> Vec3:
        "return a+b vector addition"
        r = Vec3()
        r.x = self.x + rhs.x
        r.y = self.y + rhs.y
        r.z = self.z + rhs.z
        return r

    def __iadd__(self, rhs: Vec3) -> Vec3:
        "return a+=b vector addition"
        self.x += rhs.x
        self.y += rhs.y
        self.z += rhs.z
        return self

    def __sub__(self, rhs: Vec3) -> Vec3:
        "return a+b vector addition"
        r = Vec3()
        r.x = self.x - rhs.x
        r.y = self.y - rhs.y
        r.z = self.z - rhs.z
        return r

    def __isub__(self, rhs: Vec3) -> Vec3:
        "return a+=b vector addition"
        self.x -= rhs.x
        self.y -= rhs.y
        self.z -= rhs.z
        return self

    """Note mypy will give error here 
    error: Argument 1 of "__eq__" is incompatible with supertype "object"; supertype defines the argument type as "object"  [override]
    note: This violates the Liskov substitution principle
    note: See https://mypy.readthedocs.io/en/stable/common_issues.html#incompatible-overrides
    note: It is recommended for "__eq__" to work with arbitrary objects, for example:
    
    We add the ignore here as this is what we want to do
    """

    def __eq__(self, rhs: Vec3) -> bool:  # type: ignore[override]
        "test a==b using math.isclose"
        if not isinstance(rhs, Vec3):
            return NotImplemented
        return (
            math.isclose(self.x, rhs.x)
            and math.isclose(self.y, rhs.y)
            and math.isclose(self.z, rhs.z)
        )

    def __neq__(self, rhs: Vec3) -> bool:
        "test a==b using math.isclose"
        if not isinstance(rhs, Vec3):
            return NotImplemented
        return (
            math.isclose(self.x, rhs.x)
            or math.isclose(self.y, rhs.y)
            or math.isclose(self.z, rhs.z)
        )

    def __neg__(self) -> Vec3:
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self

    def set(self, x: float, y: float, z: float) -> None:
        "set from x,y,z"
        try:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
        except ValueError:
            print("need float values")
            raise

    def dot(self, rhs: Vec3) -> float:
        "return the dot product this vector with rhs"
        return self.x * rhs.x + self.y * rhs.y + self.z * rhs.z

    def length(self) -> float:
        "length of vector"
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def length_squared(self) -> float:
        "square length of vector"
        return self.x**2 + self.y**2 + self.z**2

    def inner(self, rhs: Vec3) -> float:
        return (self.x * rhs.x) + (self.y * rhs.y) + (self.z * rhs.z)

    def cross(self, rhs: Vec3) -> Vec3:
        return Vec3(
            self.y * rhs.z - self.z * rhs.y,
            self.z * rhs.x - self.x * rhs.z,
            self.x * rhs.y - self.y * rhs.x,
        )

    def normalize(self) -> None:
        "normalize this vector"
        len = self.length()
        try:
            self.x /= len
            self.y /= len
            self.z /= len
        except ZeroDivisionError:
            raise

    def reflect(self, n: Vec3) -> Vec3:
        d = self.dot(n)
        #  I - 2.0 * dot(N, I) * N
        return Vec3(
            self.x - 2.0 * d * n.x, self.y - 2.0 * d * n.y, self.z - 2.0 * d * n.z
        )

    def __repr__(self) -> str:
        return f"Vec3 [{self.x},{self.y},{self.z}]"

    def __str__(self) -> str:
        return f"[{self.x},{self.y},{self.z}]"

    def __mul__(self, rhs: float) -> Vec3:
        "piecewise scalar multiplication"
        if isinstance(rhs, (float, int)):
            self.x *= rhs
            self.y *= rhs
            self.z *= rhs
            return self
        else:
            raise ValueError

    def __rmul__(self, rhs: float) -> Vec3:
        "piecewise scalar multiplication"
        return self * rhs
