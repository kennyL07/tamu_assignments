import math
import pygame

FOV_DEGREES = 60
NEAR_PLANE = 0.05
BACKGROUND = (24, 26, 32)
AMBIENT = 0.18
LIGHT_DIRECTION = (0, 0, 1)


def minus(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def normalize(v):
    length = math.sqrt(dot(v, v))
    if length == 0:
        return (0.0, 0.0, 0.0)
    return (v[0] / length, v[1] / length, v[2] / length)


def resolve_index(token, count):
    index = int(token)
    return index - 1 if index > 0 else count + index


def load_obj(path):
    vertices = []
    triangles = []
    with open(path) as file:
        for line in file:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "v":
                vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif parts[0] == "f":
                corners = [resolve_index(p.split("/")[0], len(vertices)) for p in parts[1:]]
                for k in range(1, len(corners) - 1):
                    triangles.append((corners[0], corners[k], corners[k + 1]))
    return vertices, triangles


def center_and_scale(vertices):
    xs, ys, zs = zip(*vertices)
    center = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (min(zs) + max(zs)) / 2)
    moved = [minus(v, center) for v in vertices]
    radius = max(math.sqrt(dot(v, v)) for v in moved)
    return [(x / radius, y / radius, z / radius) for x, y, z in moved]


def load_model(path, normalize_size=True):
    vertices, triangles = load_obj(path)
    if normalize_size:
        vertices = center_and_scale(vertices)
    return vertices, triangles


def transform(vertices, position=(0, 0, 0), rotation=(0, 0, 0), scale=1.0):
    rx, ry, rz = (math.radians(a) for a in rotation)
    cx, sx = math.cos(rx), math.sin(rx)
    cy, sy = math.cos(ry), math.sin(ry)
    cz, sz = math.cos(rz), math.sin(rz)
    px, py, pz = position
    result = []
    for x, y, z in vertices:
        x, y, z = x * scale, y * scale, z * scale
        y, z = y * cx - z * sx, y * sx + z * cx
        x, z = x * cy + z * sy, -x * sy + z * cy
        x, y = x * cz - y * sz, x * sz + y * cz
        result.append((x + px, y + py, z + pz))
    return result


def camera_basis(yaw, pitch, distance, target=(0, 0, 0)):
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    offset = (distance * cp * sy, distance * sp, distance * cp * cy)
    position = (target[0] + offset[0], target[1] + offset[1], target[2] + offset[2])
    forward = normalize((-offset[0], -offset[1], -offset[2]))
    right = normalize(cross(forward, (0.0, 1.0, 0.0)))
    up = cross(right, forward)
    return position, right, up, forward


def render(surface, vertices, triangles, color,
           camera_yaw=30.0, camera_pitch=20.0, camera_distance=2.8,
           camera_target=(0, 0, 0), fov=FOV_DEGREES,
           light=LIGHT_DIRECTION, ambient=AMBIENT, background=BACKGROUND):
    light = normalize(light)
    width, height = surface.get_size()
    half_w, half_h = width / 2, height / 2
    focal = half_h / math.tan(math.radians(fov) / 2)
    position, right, up, forward = camera_basis(camera_yaw, camera_pitch,
                                                camera_distance, camera_target)

    cam_space = []
    for v in vertices:
        rel = minus(v, position)
        cam_space.append((dot(rel, right), dot(rel, up), dot(rel, forward)))

    screen = []
    for x, y, z in cam_space:
        if z > NEAR_PLANE:
            screen.append((half_w + focal * x / z, half_h - focal * y / z))
        else:
            screen.append(None)

    draw_list = []
    for i0, i1, i2 in triangles:
        p0, p1, p2 = screen[i0], screen[i1], screen[i2]
        if p0 is None or p1 is None or p2 is None:
            continue
        a, b, c = cam_space[i0], cam_space[i1], cam_space[i2]
        normal = normalize(cross(minus(c, a), minus(b, a)))
        if dot(normal, a) > 0:
            continue
        brightness = ambient + (1 - ambient) * max(0.0, dot(normal, light))
        rgb = tuple(int(ch * brightness) for ch in color)
        depth = (a[2] + b[2] + c[2]) / 3
        draw_list.append((depth, (p0, p1, p2), rgb))

    draw_list.sort(key=lambda item: item[0], reverse=True)

    if background is not None:
        surface.fill(background)
    for _, points, rgb in draw_list:
        pygame.draw.polygon(surface, rgb, points)
    return len(draw_list)
