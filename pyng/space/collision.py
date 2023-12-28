from pyng.space.vectors import Vector2D


class AABB:
    """
    'Axis-Aligned Bounding Box' är
    """

    def __init__(self, lower_bound: Vector2D, upper_bound: Vector2D):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def area(self) -> float:
        pass


def create_aabb_union(a: AABB, b: AABB) -> AABB:
    lower_bound = min(a.lower_bound, b.lower_bound)
    upper_bound = max(a.upper_bound, b.upper_bound)
    return AABB(lower_bound, upper_bound)


class CollisionState:
    def __init__(self, normal: Vector2D, position: Vector2D):
        self.normal = normal
        self.position = position


class CollisionManifold:
    def __init__(
        self, body_A, body_B, normal, depth, contact1, contact2, contact_count
    ) -> None:
        self.body_A = body_A
        self.body_B = body_B
        self.normal = normal
        self.depth = depth
        self.contact1 = contact1
        self.contact2 = contact2
        self.contact_count = contact_count
        pass
