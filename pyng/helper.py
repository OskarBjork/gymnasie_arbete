from pyng.space.vectors import Vector2D
from pyng.config import EPSILON


def dot_product(v1: Vector2D, v2: Vector2D):
    return v1.x * v2.x + v1.y * v2.y


def projection(polygon, axis):
    """Går igenom alla vertices i ett objekt och projicerar dem på en axel, och returnerar sedan minsta och största värdena av dessa"""
    min_proj = float("inf")
    max_proj = float("-inf")
    for vertex in polygon.vertices:
        dot_product = vertex.x * axis.x + vertex.y * axis.y
        min_proj = min(min_proj, dot_product)
        max_proj = max(max_proj, dot_product)
    return min_proj, max_proj


def length_squared(v: Vector2D):
    return v.x * v.x + v.y * v.y


def float_nearly_equal(a, b):
    return abs(a - b) < EPSILON


def vector_nearly_equal(v1: Vector2D, v2: Vector2D):
    return float_nearly_equal(v1.x, v2.x) and float_nearly_equal(v1.y, v2.y)


def distance_squared(v1: Vector2D, v2: Vector2D):
    return length_squared(v1 - v2)


def overlaps(projection1, projection2):
    """Kollar om två projektioner överlappar varandra, utifrån deras minsta och största värden"""
    return projection1[1] >= projection2[0] and projection1[0] <= projection2[1]


def find_arithmetic_mean(vertices):
    sum_x = 0
    sum_y = 0
    for v in vertices:
        sum_x += v.x
        sum_y += v.y

    return Vector2D(sum_x / len(vertices), sum_y / len(vertices))


def remove_duplicates(list):
    unique_collisions = set(frozenset(tup) for tup in list)
    return [tuple(phys_objs) for phys_objs in unique_collisions]
