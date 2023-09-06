from attrs import define


class SpaceAnalyzer:
    """Analyze space."""

    def init(self):
        pass

    def analyze(self, world):
        """Analyze world."""
        objects = world.objects
        for obj in objects:
            obj.position.x += obj.velocity.x
