from attrs import define
from random import randint

from pyng.space.phys_obj import Point
from pyng.space.vectors import TwoDimensionalVector


@define
class State:
    """State of the game."""

    def init(self):
        pass

    def create_objects(self, world):
        """Create objects."""
        for _ in range(1, 4):
            world.add_object(
                Point(
                    position=TwoDimensionalVector(
                        randint(0, world.width), randint(0, 100)
                    ),
                    mass=1,
                    velocity=TwoDimensionalVector(0, 0),
                    force=TwoDimensionalVector(0, 0),
                )
            )

        pass
