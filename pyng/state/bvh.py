import math
from pyng.space.phys_obj import ConvexPolygon


def calculate_bounding_box(objects):
    if not objects:
        return None

    if len(objects) == 1:  # Ifall det bara existerar ett objekt
        polygon = objects[0]
        min_x = min(v[0] for v in polygon.vertices)
        max_x = max(v[0] for v in polygon.vertices)
        min_y = min(v[1] for v in polygon.vertices)
        max_y = max(v[1] for v in polygon.vertices)
        return [
            (min_x, min_y),
            (max_x, max_y),
        ]  # Ger tillbaka en lista med två tuples som innehåller minsta och största x- och y-koordinaterna, vilket blir en rektangel som går runt objektet

    bounding_box = [(float("inf"), float("inf")), (float("-inf"), float("-inf"))]
    for polygon in objects:
        for vertex in polygon.vertices:
            """Går igenom alla vertices i alla objekt och uppdaterar bounding_box så att den innehåller minsta och största x- och y-koordinaterna som hittas bland objekten"""
            bounding_box[0] = (
                min(bounding_box[0][0], vertex[0]),
                min(bounding_box[0][1], vertex[1]),
            )
            bounding_box[1] = (
                max(bounding_box[1][0], vertex[0]),
                max(bounding_box[1][1], vertex[1]),
            )

    return bounding_box


def projection(polygon, axis):
    """Går igenom alla vertices i ett objekt och projicerar dem på en axel, och returnerar sedan minsta och största värdena av dessa"""
    min_proj = float("inf")
    max_proj = float("-inf")
    for vertex in polygon.vertices:
        dot_product = vertex[0] * axis[0] + vertex[1] * axis[1]
        min_proj = min(min_proj, dot_product)
        max_proj = max(max_proj, dot_product)
    return min_proj, max_proj


def overlaps(projection1, projection2):
    """Kollar om två projektioner överlappar varandra, utifrån deras minsta och största värden"""
    return projection1[1] >= projection2[0] and projection1[0] <= projection2[1]


def get_normals(polygon):
    # Get the normals of the edges of a convex polygon
    normals = []
    for i in range(len(polygon.vertices)):
        v1 = polygon.vertices[i]
        v2 = polygon.vertices[
            (i + 1) % len(polygon.vertices)
        ]  # Ser till så att sista och första vertex jämförs
        edge = (v2[0] - v1[0], v2[1] - v1[1])
        length = math.sqrt(edge[0] ** 2 + edge[1] ** 2)
        normal = (edge[1] / length, -edge[0] / length)  # Perpendicular vector
        normals.append(normal)
    return normals


def check_collision(polygon1, polygon2):
    """Går igenom alla normaler till båda polygonerna och projicerar alla vertexer på dessa, och kollar sedan om de överlappar varandra"""
    normals1 = get_normals(polygon1)
    normals2 = get_normals(polygon2)

    for normal in normals1 + normals2:
        projection1 = projection(polygon1, normal)
        projection2 = projection(polygon2, normal)

        if not overlaps(projection1, projection2):
            return False  # Separating axis found

    return True  # No separating axis found, polygons overlap


# def traverse_bvh(root, polygon):
#     if root is None:
#         return []

#     if polygon_intersects_bounding_box(polygon, root.bounding_box):
#         if len(root.objects) == 1:
#             obj = root.objects[0]
#             if check_collision(polygon, obj):
#                 resolve_collision(polygon, obj)
#                 return [obj]
#         else:
#             left_hits = traverse_bvh(root.left, polygon)
#             right_hits = traverse_bvh(root.right, polygon)
#             return left_hits + right_hits

#     return []


def find_leaf_nodes_with_two_objects(root):
    leaf_nodes = []

    if root is None:
        return leaf_nodes

    if root.left is None and root.right is None and len(root.objects) == 2:
        leaf_nodes.append(root)
    else:
        left_leaf_nodes = find_leaf_nodes_with_two_objects(root.left)
        right_leaf_nodes = find_leaf_nodes_with_two_objects(root.right)
        leaf_nodes.extend(left_leaf_nodes)
        leaf_nodes.extend(right_leaf_nodes)

    return leaf_nodes


# def polygon_intersects_bounding_box(polygon, bounding_box):
#     # Check if a convex polygon intersects a bounding box
#     min_x, min_y = bounding_box[0]
#     max_x, max_y = bounding_box[1]
#     for vertex in polygon.vertices:
#         if min_x <= vertex[0] <= max_x and min_y <= vertex[1] <= max_y:
#             return True
#     return False


def resolve_collision(polygon1, polygon2):
    # Implement a collision resolution mechanism
    # Adjust the positions or velocities of the polygons
    pass


# Example usage:
# Define two ConvexPolygon objects
polygon1 = ConvexPolygon(vertices=[(0, 0), (1, 0), (0.5, 1)])
polygon2 = ConvexPolygon(vertices=[(0.25, 0.5), (1.25, 0.5), (0.75, 1.5)])

# Build the BVH
objects = [polygon1, polygon2]


def build_bvh(objects, depth=0, max_depth=20):
    if len(objects) == 0:
        return None

    if len(objects) == 1:
        return {
            "objects": objects[0],
            "bounding_box": calculate_bounding_box(objects),
            "left": None,
            "right": None,
        }

    if depth >= max_depth:
        return {
            "objects": objects,
            "bounding_box": calculate_bounding_box(objects),
            "left": None,
            "right": None,
        }

    bounding_box = calculate_bounding_box(objects)

    if len(objects) == 2:
        left_objects = [objects[0]]
        right_objects = [objects[1]]
    else:
        left_objects, right_objects = partition_objects(objects, bounding_box)

    left_child = build_bvh(left_objects, depth + 1, max_depth)
    right_child = build_bvh(right_objects, depth + 1, max_depth)

    return {
        "objects": objects,
        "bounding_box": bounding_box,
        "left": left_child,
        "right": right_child,
    }


def build_bvh_2(self, objects, depth=0, max_depth=20, k=2):
    objects = list(set(objects))

    if len(objects) == 0:
        return None

    if len(objects) == 1:
        return {
            "objects": objects,
            "bounding_box": self.calculate_bounding_box(objects),
            "left": None,
            "right": None,
        }

    if len(objects) == 2:
        return {
            "objects": objects,
            "bounding_box": self.calculate_bounding_box(objects),
            "left": None,
            "right": None,
        }

    if depth >= max_depth:
        return {
            "objects": objects,
            "bounding_box": self.calculate_bounding_box(objects),
            "left": None,
            "right": None,
        }

    bounding_box = self.calculate_bounding_box(objects)

    if len(objects) == 2:
        left_objects = [objects[0]]
        right_objects = [objects[1]]
    else:
        left_objects, right_objects, k = self.partition_objects(
            objects, bounding_box, k=k
        )

    left_child = self.build_bvh(left_objects, depth + 1, max_depth, k=k)
    right_child = self.build_bvh(right_objects, depth + 1, max_depth, k=k)

    return {
        "objects": objects,
        "bounding_box": bounding_box,
        "left": left_child,
        "right": right_child,
    }


def partition_objects(objects, bounding_box):
    axis = longest_axis(bounding_box)
    midpoint = (bounding_box[axis][0] + bounding_box[axis][1]) / 2

    left_objects = []
    right_objects = []

    for obj in objects:
        if obj.bounding_box[axis][1] < midpoint:
            left_objects.append(obj)
        elif obj.bounding_box[axis][0] > midpoint:
            right_objects.append(obj)
        else:
            left_objects.append(obj)
            right_objects.append(obj)

    if len(left_objects) == 0:
        left_objects = right_objects[: len(right_objects) // 2]
        right_objects = right_objects[len(right_objects) // 2 :]
    elif len(right_objects) == 0:
        right_objects = left_objects[: len(left_objects) // 2]
        left_objects = left_objects[len(left_objects) // 2 :]

    return left_objects, right_objects


def partition_objects_2(self, objects, bounding_box, k=2):
    print("new objects: ")
    axis = self.longest_axis(bounding_box)
    objects_sorted_along_axis = sorted(
        objects, key=lambda obj: obj.position.x if axis == 0 else obj.position.y
    )

    median = objects_sorted_along_axis[len(objects_sorted_along_axis) // 2]
    median_position_in_axis = median.position.x if axis == 0 else median.position.y
    print([obj.id for obj in objects_sorted_along_axis])
    print(
        [
            obj.position.x if axis == 0 else obj.position.y
            for obj in objects_sorted_along_axis
        ]
    )
    print(f"median: {median.id}")
    print("axis: ", axis)

    left_objects = []
    right_objects = []

    for index, obj in enumerate(objects_sorted_along_axis):
        obj.update_vertices()
        obj.bounding_box = obj.calculate_polygon_bounding_box()

        if len(objects) == 3:
            print("THREE OBJECTS")
            d1 = self.distance(
                (
                    objects_sorted_along_axis[0].position.x,
                    objects_sorted_along_axis[0].position.y,
                ),
                (median.position.x, median.position.y),
            )
            d2 = self.distance(
                (
                    objects_sorted_along_axis[2].position.x,
                    objects_sorted_along_axis[2].position.y,
                ),
                (median.position.x, median.position.y),
            )
            if d1 < d2:
                left_objects.append(objects_sorted_along_axis[0])
                left_objects.append(median)
                print([obj.id for obj in left_objects])
            elif d1 > d2:
                right_objects.append(objects_sorted_along_axis[2])
                right_objects.append(median)
                print([obj.id for obj in right_objects])
            else:
                left_objects.append(obj)
                right_objects.append(obj)
            break

        obj_position_in_axis = obj.position.x if axis == 0 else obj.position.y
        if obj_position_in_axis < median_position_in_axis:
            left_objects.append(obj)
        elif obj_position_in_axis > median_position_in_axis:
            right_objects.append(obj)
        else:
            right_objects.append(obj)
            left_objects.append(obj)

    if len(left_objects) == 0 and len(objects) > 3:
        left_objects = right_objects[: len(right_objects) // 2]
        right_objects = right_objects[len(right_objects) // 2 :]
    elif len(right_objects) == 0 and len(objects) > 3:
        right_objects = left_objects[: len(left_objects) // 2]
        left_objects = left_objects[len(left_objects) // 2 :]

    k += 1

    return left_objects, right_objects, k


def longest_axis(bounding_box):
    x_length = bounding_box[0][1] - bounding_box[0][0]
    y_length = bounding_box[1][1] - bounding_box[1][0]
    z_length = bounding_box[2][1] - bounding_box[2][0]

    if x_length > y_length and x_length > z_length:
        return 0
    elif y_length > z_length:
        return 1
    else:
        return 2


def find_leaf_nodes_with_two_objects(self, root):
    leaf_nodes = []

    if root is None:
        return leaf_nodes
    if root["left"] is None and root["right"] is None and len(root["objects"]) == 2:
        leaf_nodes.append(root)
    else:
        left_leaf_nodes = self.find_leaf_nodes_with_two_objects(root["left"])
        right_leaf_nodes = self.find_leaf_nodes_with_two_objects(root["right"])
        leaf_nodes.extend(left_leaf_nodes)
        leaf_nodes.extend(right_leaf_nodes)
    return leaf_nodes


def calculate_bounding_box(self, objects):
    if not objects:
        return None

    if len(objects) == 1:
        polygon = objects[0]
        min_x = min(v.x for v in polygon.vertices)
        max_x = max(v.x for v in polygon.vertices)
        min_y = min(v.y for v in polygon.vertices)
        max_y = max(v.y for v in polygon.vertices)
        return [(min_x, min_y), (max_x, max_y)]

    bounding_box = [(float("inf"), float("inf")), (float("-inf"), float("-inf"))]
    for polygon in objects:
        if not isinstance(polygon, ConvexPolygon):
            continue
        for vertex in polygon.vertices:
            bounding_box[0] = (
                min(bounding_box[0][0], vertex.x),
                min(bounding_box[0][1], vertex.y),
            )
            bounding_box[1] = (
                max(bounding_box[1][0], vertex.x),
                max(bounding_box[1][1], vertex.y),
            )

    return bounding_box

def longest_axis(self, bounding_box):
        x_length = bounding_box[1][0] - bounding_box[0][0]
        y_length = bounding_box[1][1] - bounding_box[0][1]  # BUGG: längden blir negativ

        if x_length > y_length:
            return 0
        else:
            return 1