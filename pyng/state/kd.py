from numpy import array
import pprint
import math
import xml.etree.ElementTree as ET

pp = pprint.PrettyPrinter(indent=4)

CIRCLE_TAG_NAME = "{http://www.w3.org/2000/svg}circle"
GROUP_TAG_NAME = "{http://www.w3.org/2000/svg}g"


def circle_to_point(circle):
    return (float(circle.attrib["cx"]), float(circle.attrib["cy"]))


def read_svg_file(svg_file_name):
    return ET.parse(svg_file_name)


def get_all_points(tree):
    return [circle_to_point(circle) for circle in tree.iter(CIRCLE_TAG_NAME)]


def get_point_by_id(tree, point_id):
    return [
        circle_to_point(circle)
        for circle in tree.iter(CIRCLE_TAG_NAME)
        if "id" in circle.attrib
        if circle.attrib["id"] == point_id
    ]


def get_group_by_id(tree, group_id):
    return [
        circle
        for group in tree.iter(GROUP_TAG_NAME)
        if "id" in group.attrib
        if group.attrib["id"] == group_id
        for circle in get_all_points(group)
    ]


def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def closest_point_brute_force(points, point):
    closest_point = None
    smallest_distance = None
    for p in points:
        d = distance(p, point)
        if smallest_distance is None or d < smallest_distance:
            smallest_distance = d
            closest_point = p
    return closest_point


svg_tree = read_svg_file("points.svg")

[pivot] = get_point_by_id(svg_tree, "pivot")

points = get_group_by_id(svg_tree, "points")


def inbox(p, box):
    return all(box[:, 0] <= p) and all(p <= box[:, 1])


k = 2


def build_kd_tree(points, depth=0):
    n = len(points)
    if n <= 0:
        return None
    axis = depth % k
    sorted_points = sorted(points, key=lambda point: point[axis])
    median = n // 2

    return {
        "point": sorted_points[median],
        "left": build_kd_tree(sorted_points[:median], depth + 1),
        "right": build_kd_tree(sorted_points[median + 1 :], depth + 1),
    }


kd_tree = build_kd_tree(points)


def kd_tree_naive_closest_point(root, point, depth=0, best=None):
    if root is None:
        return best
    k = len(point)
    axis = depth % k
    next_best = None
    next_branch = None
    if best == None or distance(point, root["point"]) < distance(point, best):
        next_best = root["point"]
    else:
        next_best = best

    if point[axis] < root["point"][axis]:
        next_branch = root["left"]
    else:
        next_branch = root["right"]

    return kd_tree_naive_closest_point(next_branch, point, depth + 1, next_best)


def closer_distance(pivot, p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1

    d1 = distance(pivot, p1)
    d2 = distance(pivot, p2)

    if d1 < d2:
        return p1
    else:
        return p2


def kd_tree_closest_point(root, point, depth=0):
    if root is None:
        return None

    axis = depth % k
    next_branch = None
    opposite_branch = None

    if point[axis] < root["point"][axis]:
        next_branch = root["left"]
        opposite_branch = root["right"]
    else:
        next_branch = root["right"]
        opposite_branch = root["left"]

    best = closer_distance(
        point, kd_tree_closest_point(next_branch, point, depth + 1), root["point"]
    )

    if distance(point, best) > abs(point[axis] - root["point"][axis]):
        best = closer_distance(
            point,
            kd_tree_closest_point(opposite_branch, point, depth + 1),
            best,
        )

    return best


# pp.pprint(build_kd_tree(points))
print(kd_tree_naive_closest_point(kd_tree, pivot))
