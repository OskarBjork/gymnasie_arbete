from pyng.space.phys_obj import PhysObj


def check_collisions(objects: list[PhysObj]):
    for obj in objects:
        for other_obj in objects:
            if obj == other_obj:
                continue
            if obj.is_inside_of(other_obj):
                resolve_collision(obj, other_obj)


def resolve_collision(obj: PhysObj, other_obj: PhysObj):
    d = obj.position.distance_to(other_obj.position)

    overlap_length = obj.radius + other_obj.radius - d

    direction = obj.position - other_obj.position

    direction = direction.normalize()

    magnitude = overlap_length / 2

    direction = direction * magnitude

    obj.position = obj.position + direction

    other_obj.position = other_obj.position - direction
