from pyng.space.phys_obj import PhysObj, Point, Circle, ConvexPolygon
from pyng.space.vectors import Vector2D
from pyng.space.grid import Grid
from pyng.config import ORIGIN, PIXELS_PER_METER, BLACK, RED, BLUE
from pyng.helper import projection, overlaps, remove_duplicates


class PhysWorld:
    def __init__(self) -> None:
        pass

    def find_collisions(self, objects: [PhysObj]):
        return self.sweep_and_prune(objects)

    def sweep_and_prune(self, objects: [PhysObj]):
        projections_x, projections_y = self.get_projections_in_x_and_y_plane(objects)
        potential_collisions = []
        for i, tup in enumerate(projections_x):
            points = tup[0], tup[1]
            for j, other_tup in enumerate(projections_x):
                if tup == other_tup:
                    continue
                other_points = other_tup[0], other_tup[1]
                if overlaps(points, other_points) and overlaps(
                    projections_y[i], projections_y[j]
                ):
                    potential_collisions.append((tup[2], other_tup[2]))

        return remove_duplicates(potential_collisions)

    def get_projections_in_x_and_y_plane(self, objects: [PhysObj]):
        projections_x = []
        projections_y = []
        for axis in (
            Vector2D(1, 0),
            Vector2D(0, 1),
        ):
            for obj in objects:
                if isinstance(obj, Point):
                    continue
                min_proj, max_proj = obj.project(axis)
                if axis.x == 1:
                    projections_x.append((min_proj, max_proj, obj))
                else:
                    projections_y.append((min_proj, max_proj, obj))

        return projections_x, projections_y
