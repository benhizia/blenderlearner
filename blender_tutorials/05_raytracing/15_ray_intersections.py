"""
Blender Python Tutorial - Lesson 15: Ray-Surface Intersections
===============================================================

Deep dive into intersection mathematics:
- Ray-Sphere intersection (analytical solution)
- Ray-Plane intersection
- Ray-Triangle intersection (Möller-Trumbore algorithm)
- Ray-Box intersection (AABB)
- Quadratic equation solving
- Visualizing intersection points and normals

This is the CORE of raytracing - finding where rays hit objects!
"""

import bpy

import math
from mathutils import Vector
import random

# Clear the scene

ensure_object_mode()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("=" * 70)
print("RAYTRACING MATHEMATICS - Part 2: Ray-Surface Intersections")
print("=" * 70)

# ============================================
# HELPER FUNCTIONS
# ============================================

def create_ray_visual(origin, direction, length=5, name="Ray", color=(1, 0, 0)):
    """Create visual representation of a ray"""
    direction = direction.normalized()
    end_point = origin + direction * length

    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.02,
        depth=length,
        location=origin + direction * (length / 2)
    )
    ray = bpy.context.active_object
    ray.name = name

    z_axis = Vector((0, 0, 1))
    rotation_quat = z_axis.rotation_difference(direction)
    ray.rotation_euler = rotation_quat.to_euler()

    bpy.ops.mesh.primitive_cone_add(
        radius1=0.06,
        radius2=0,
        depth=0.2,
        location=end_point
    )
    arrow = bpy.context.active_object
    arrow.rotation_euler = rotation_quat.to_euler()
    arrow.parent = ray

    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Emission'].default_value = (*color, 1)
    bsdf.inputs['Emission Strength'].default_value = 2.0

    ray.data.materials.append(mat)
    arrow.data.materials.append(mat)

    return ray

def create_point(location, name="Point", color=(1, 1, 0), size=0.1):
    """Create a point marker"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=size, location=location)
    point = bpy.context.active_object
    point.name = name

    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Emission'].default_value = (*color, 1)
    bsdf.inputs['Emission Strength'].default_value = 4.0

    point.data.materials.append(mat)
    return point

def create_normal_visual(point, normal, length=1.0, name="Normal"):
    """Create visual representation of a normal vector"""
    return create_ray_visual(point, normal, length, name, color=(0, 1, 1))

# ============================================
# INTERSECTION MATHEMATICS
# ============================================

def ray_sphere_intersection(ray_origin, ray_direction, sphere_center, sphere_radius):
    """
    Calculate ray-sphere intersection using analytical solution

    Sphere equation: |P - C|² = r²
    Ray equation: P(t) = O + tD

    Substituting ray into sphere:
    |O + tD - C|² = r²

    Expanding:
    (O - C + tD)·(O - C + tD) = r²

    This gives us a quadratic equation:
    at² + bt + c = 0

    where:
    a = D·D (always 1 if D is normalized)
    b = 2D·(O - C)
    c = (O - C)·(O - C) - r²

    Solution: t = (-b ± √(b² - 4ac)) / 2a
    """
    # Vector from sphere center to ray origin
    oc = ray_origin - sphere_center

    # Quadratic equation coefficients
    a = ray_direction.dot(ray_direction)  # Usually 1 if direction is normalized
    b = 2.0 * ray_direction.dot(oc)
    c = oc.dot(oc) - sphere_radius * sphere_radius

    # Discriminant
    discriminant = b*b - 4*a*c

    print(f"     Quadratic: {a:.3f}t² + {b:.3f}t + {c:.3f} = 0")
    print(f"     Discriminant: {discriminant:.3f}")

    if discriminant < 0:
        # No intersection
        print(f"     Result: NO INTERSECTION (discriminant < 0)")
        return None, None

    # Two solutions (entry and exit points)
    sqrt_disc = math.sqrt(discriminant)
    t1 = (-b - sqrt_disc) / (2*a)
    t2 = (-b + sqrt_disc) / (2*a)

    print(f"     Solutions: t1={t1:.3f}, t2={t2:.3f}")

    # We want the closest positive t
    if t1 > 0:
        hit_point = ray_origin + ray_direction * t1
        normal = (hit_point - sphere_center).normalized()
        return hit_point, normal
    elif t2 > 0:
        hit_point = ray_origin + ray_direction * t2
        normal = (hit_point - sphere_center).normalized()
        return hit_point, normal

    print(f"     Result: NO VALID INTERSECTION (t < 0)")
    return None, None

def ray_plane_intersection(ray_origin, ray_direction, plane_point, plane_normal):
    """
    Calculate ray-plane intersection

    Plane equation: (P - P₀)·N = 0
    Ray equation: P(t) = O + tD

    Substituting:
    (O + tD - P₀)·N = 0

    Solving for t:
    t = (P₀ - O)·N / (D·N)
    """
    # Check if ray is parallel to plane
    denom = ray_direction.dot(plane_normal)

    print(f"     D·N = {denom:.3f}")

    if abs(denom) < 1e-6:
        print(f"     Result: RAY PARALLEL TO PLANE")
        return None, None

    # Calculate t
    t = (plane_point - ray_origin).dot(plane_normal) / denom

    print(f"     t = {t:.3f}")

    if t < 0:
        print(f"     Result: INTERSECTION BEHIND RAY")
        return None, None

    hit_point = ray_origin + ray_direction * t

    # Normal points away from ray if needed
    if denom > 0:
        normal = -plane_normal
    else:
        normal = plane_normal

    return hit_point, normal

def ray_triangle_intersection(ray_origin, ray_direction, v0, v1, v2):
    """
    Ray-triangle intersection using Möller-Trumbore algorithm

    Fast algorithm that:
    1. Finds intersection with triangle plane
    2. Uses barycentric coordinates to test if point is inside triangle

    Returns hit point and barycentric coordinates (u, v)
    Point in triangle: P = (1-u-v)*v0 + u*v1 + v*v2
    """
    # Edge vectors
    edge1 = v1 - v0
    edge2 = v2 - v0

    # Begin calculating determinant
    h = ray_direction.cross(edge2)
    a = edge1.dot(h)

    # Ray is parallel to triangle
    if abs(a) < 1e-6:
        print(f"     Result: RAY PARALLEL TO TRIANGLE")
        return None, None, None

    f = 1.0 / a
    s = ray_origin - v0
    u = f * s.dot(h)

    # Intersection point is outside triangle
    if u < 0.0 or u > 1.0:
        print(f"     Result: OUTSIDE TRIANGLE (u={u:.3f})")
        return None, None, None

    q = s.cross(edge1)
    v = f * ray_direction.dot(q)

    # Intersection point is outside triangle
    if v < 0.0 or u + v > 1.0:
        print(f"     Result: OUTSIDE TRIANGLE (v={v:.3f})")
        return None, None, None

    # Calculate t
    t = f * edge2.dot(q)

    if t > 1e-6:  # Ray intersection
        hit_point = ray_origin + ray_direction * t
        # Calculate normal from edges
        normal = edge1.cross(edge2).normalized()
        print(f"     Result: HIT at t={t:.3f}, u={u:.3f}, v={v:.3f}")
        return hit_point, normal, (u, v)

    print(f"     Result: INTERSECTION BEHIND RAY")
    return None, None, None

# ============================================
# 1. RAY-SPHERE INTERSECTION
# ============================================
print("\n1. RAY-SPHERE INTERSECTION")
print("   Solving: |O + tD - C|² = r²")

# Create sphere
sphere_center = Vector((0, 0, 1))
sphere_radius = 1.5

bpy.ops.mesh.primitive_uv_sphere_add(radius=sphere_radius, location=sphere_center)
sphere = bpy.context.active_object
sphere.name = "Intersection_Sphere"

# Semi-transparent material
mat = bpy.data.materials.new(name="Sphere_Mat")
mat.use_nodes = True
mat.blend_method = 'BLEND'
bsdf = mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (0.3, 0.6, 1, 0.4)
bsdf.inputs['Alpha'].default_value = 0.4
sphere.data.materials.append(mat)

create_point(sphere_center, "Sphere_Center", (1, 1, 0), 0.08)

# Test rays
test_rays = [
    (Vector((-3, 0, 1)), Vector((1, 0, 0)), "Hit_Center"),
    (Vector((-3, 0, 2)), Vector((1, 0, -0.2)), "Hit_Top"),
    (Vector((-3, 0, 3)), Vector((1, 0, 0)), "Miss_Above"),
]

print("\n   Testing rays against sphere:")
for i, (origin, direction, name) in enumerate(test_rays):
    print(f"\n   Ray {i+1}: {name}")
    print(f"     Origin: {origin}")
    print(f"     Direction: {direction.normalized()}")

    # Calculate intersection
    hit_point, normal = ray_sphere_intersection(origin, direction.normalized(), sphere_center, sphere_radius)

    if hit_point:
        # Hit - green ray
        create_ray_visual(origin, direction, length=5, name=f"Ray_{name}", color=(0, 1, 0))
        create_point(hit_point, f"Hit_{name}", (1, 0, 0), 0.1)
        create_normal_visual(hit_point, normal, 1.0, f"Normal_{name}")
    else:
        # Miss - red ray
        create_ray_visual(origin, direction, length=5, name=f"Ray_{name}", color=(1, 0, 0))

# ============================================
# 2. RAY-PLANE INTERSECTION
# ============================================
print("\n2. RAY-PLANE INTERSECTION")
print("   Solving: (O + tD - P₀)·N = 0")

# Create plane
plane_point = Vector((0, 5, 0))
plane_normal = Vector((0, 0, 1))  # Horizontal plane

bpy.ops.mesh.primitive_plane_add(size=4, location=plane_point)
plane = bpy.context.active_object
plane.name = "Intersection_Plane"

# Visualize plane normal
create_normal_visual(plane_point, plane_normal, 2.0, "Plane_Normal")

# Plane material
plane_mat = bpy.data.materials.new(name="Plane_Mat")
plane_mat.use_nodes = True
bsdf = plane_mat.node_tree.nodes.get("Principled BSDF")

# Checker pattern
checker = plane_mat.node_tree.nodes.new(type='ShaderNodeTexChecker')
checker.inputs['Scale'].default_value = 4
plane_mat.node_tree.links.new(
    checker.outputs['Color'],
    bsdf.inputs['Base Color']
)

plane.data.materials.append(plane_mat)

# Test rays
plane_test_rays = [
    (Vector((0, 5, 3)), Vector((0, 0, -1)), "Perpendicular"),
    (Vector((2, 5, 2)), Vector((-0.5, 0, -0.5)), "Angled"),
    (Vector((0, 5, -1)), Vector((1, 0, 0)), "Parallel"),
]

print("\n   Testing rays against plane:")
for i, (origin, direction, name) in enumerate(plane_test_rays):
    print(f"\n   Ray {i+1}: {name}")
    print(f"     Origin: {origin}")
    print(f"     Direction: {direction.normalized()}")

    hit_point, normal = ray_plane_intersection(origin, direction.normalized(), plane_point, plane_normal)

    if hit_point:
        create_ray_visual(origin, direction, length=4, name=f"PlaneRay_{name}", color=(0, 1, 0))
        create_point(hit_point, f"PlaneHit_{name}", (1, 0, 0), 0.08)
    else:
        create_ray_visual(origin, direction, length=4, name=f"PlaneRay_{name}", color=(1, 0, 0))

# ============================================
# 3. RAY-TRIANGLE INTERSECTION
# ============================================
print("\n3. RAY-TRIANGLE INTERSECTION (Möller-Trumbore)")

# Create triangle
v0 = Vector((5, 0, 0))
v1 = Vector((7, 0, 0))
v2 = Vector((6, 0, 2))

# Create triangle mesh
import bmesh

def ensure_object_mode():
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

mesh = bpy.data.meshes.new("TriangleMesh")
bm = bmesh.new()

vert0 = bm.verts.new(v0)
vert1 = bm.verts.new(v1)
vert2 = bm.verts.new(v2)

bm.faces.new([vert0, vert1, vert2])
bm.to_mesh(mesh)
bm.free()

tri_obj = bpy.data.objects.new("Triangle", mesh)
bpy.context.collection.objects.link(tri_obj)

# Triangle material
tri_mat = bpy.data.materials.new(name="Triangle_Mat")
tri_mat.use_nodes = True
tri_mat.blend_method = 'BLEND'
bsdf = tri_mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (1, 0.5, 0, 0.6)
bsdf.inputs['Alpha'].default_value = 0.6
tri_obj.data.materials.append(tri_mat)

# Mark vertices
create_point(v0, "V0", (1, 1, 0), 0.06)
create_point(v1, "V1", (1, 1, 0), 0.06)
create_point(v2, "V2", (1, 1, 0), 0.06)

# Calculate and show triangle normal
tri_normal = (v1 - v0).cross(v2 - v0).normalized()
tri_center = (v0 + v1 + v2) / 3
create_normal_visual(tri_center, tri_normal, 1.0, "Triangle_Normal")

# Test rays
triangle_rays = [
    (Vector((4, 0, 1)), Vector((1, 0, 0)), "Hit_Center"),
    (Vector((4, 0, 0.5)), Vector((1, 0, 0)), "Hit_Edge"),
    (Vector((4, 0, 3)), Vector((1, 0, 0)), "Miss_Above"),
]

print("\n   Testing rays against triangle:")
for i, (origin, direction, name) in enumerate(triangle_rays):
    print(f"\n   Ray {i+1}: {name}")
    print(f"     Origin: {origin}")
    print(f"     Direction: {direction.normalized()}")

    hit_point, normal, bary = ray_triangle_intersection(
        origin, direction.normalized(), v0, v1, v2
    )

    if hit_point:
        create_ray_visual(origin, direction, length=4, name=f"TriRay_{name}", color=(0, 1, 0))
        create_point(hit_point, f"TriHit_{name}", (1, 0, 0), 0.08)
        if normal:
            create_normal_visual(hit_point, normal, 0.8, f"TriNormal_{name}")
    else:
        create_ray_visual(origin, direction, length=4, name=f"TriRay_{name}", color=(1, 0, 0))

# ============================================
# 4. MULTIPLE SPHERES - CLOSEST HIT
# ============================================
print("\n4. FINDING CLOSEST INTERSECTION")
print("   When ray hits multiple objects, we need the closest one")

# Ray that will hit multiple spheres
multi_ray_origin = Vector((5, 5, 1))
multi_ray_direction = Vector((1, 0, 0)).normalized()

create_ray_visual(multi_ray_origin, multi_ray_direction, length=8, name="Multi_Ray", color=(1, 1, 0))

# Create multiple spheres along the ray
sphere_positions = [
    (Vector((7, 5, 1)), 0.5, "First"),
    (Vector((9, 5, 1)), 0.6, "Second"),
    (Vector((11, 5, 1)), 0.4, "Third"),
]

closest_t = float('inf')
closest_hit = None
closest_name = None

print("\n   Spheres along ray:")
for center, radius, name in sphere_positions:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=center)
    s = bpy.context.active_object
    s.name = f"Multi_{name}"

    # Semi-transparent
    m = bpy.data.materials.new(name=f"Multi_{name}_Mat")
    m.use_nodes = True
    m.blend_method = 'BLEND'
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (random.random(), random.random(), random.random(), 0.4)
    bsdf.inputs['Alpha'].default_value = 0.4
    s.data.materials.append(m)

    # Test intersection
    hit, normal = ray_sphere_intersection(multi_ray_origin, multi_ray_direction, center, radius)

    if hit:
        t = (hit - multi_ray_origin).length
        print(f"     {name}: HIT at t={t:.3f}")
        create_point(hit, f"Hit_{name}", (0.5, 0.5, 0.5), 0.06)

        if t < closest_t:
            closest_t = t
            closest_hit = hit
            closest_name = name
    else:
        print(f"     {name}: MISS")

if closest_hit:
    print(f"\n   CLOSEST HIT: {closest_name} at t={closest_t:.3f}")
    create_point(closest_hit, "Closest_Hit", (1, 0, 0), 0.15)

# ============================================
# 5. VISUALIZATION OF DISCRIMINANT
# ============================================
print("\n5. DISCRIMINANT VISUALIZATION")
print("   Discriminant b²-4ac determines number of intersections")

disc_sphere_center = Vector((0, -5, 1))
disc_sphere_radius = 1.0

bpy.ops.mesh.primitive_uv_sphere_add(radius=disc_sphere_radius, location=disc_sphere_center)
disc_sphere = bpy.context.active_object
disc_sphere.name = "Discriminant_Sphere"

m = bpy.data.materials.new(name="Disc_Mat")
m.use_nodes = True
m.blend_method = 'BLEND'
bsdf = m.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (1, 0, 1, 0.4)
bsdf.inputs['Alpha'].default_value = 0.4
disc_sphere.data.materials.append(m)

# Three types of rays
disc_rays = [
    (Vector((-3, -5, 1)), Vector((1, 0, 0)), "Two hits (disc > 0)", (0, 1, 0)),
    (Vector((-3, -5, 2)), Vector((1, 0, 0)), "One hit (disc ≈ 0)", (1, 1, 0)),
    (Vector((-3, -5, 3)), Vector((1, 0, 0)), "No hit (disc < 0)", (1, 0, 0)),
]

print("\n   Testing different discriminant cases:")
for origin, direction, description, color in disc_rays:
    print(f"\n   {description}")
    hit, normal = ray_sphere_intersection(origin, direction, disc_sphere_center, disc_sphere_radius)
    create_ray_visual(origin, direction, length=5, name=f"Disc_{description}", color=color)

# ============================================
# SCENE SETUP
# ============================================

# Lighting
bpy.ops.object.light_add(type='SUN', location=(10, -10, 10))
sun = bpy.context.active_object
sun.data.energy = 2.5

# Camera
bpy.ops.object.camera_add(location=(8, -15, 8))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(65), 0, math.radians(25))
bpy.context.scene.camera = camera

# Dark background
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (0.02, 0.02, 0.03, 1)

# ============================================
# MATHEMATICAL SUMMARY
# ============================================
print("\n" + "=" * 70)
print("RAY-SURFACE INTERSECTION MATHEMATICS")
print("=" * 70)

print("\n1. RAY-SPHERE INTERSECTION:")
print("   Sphere: |P - C|² = r²")
print("   Ray: P(t) = O + tD")
print("   ")
print("   Quadratic equation: at² + bt + c = 0")
print("   a = D·D = 1 (if D is normalized)")
print("   b = 2D·(O - C)")
print("   c = (O - C)·(O - C) - r²")
print("   ")
print("   Discriminant Δ = b² - 4ac:")
print("     Δ < 0  → No intersection")
print("     Δ = 0  → One intersection (tangent)")
print("     Δ > 0  → Two intersections (entry and exit)")
print("   ")
print("   Solutions: t = (-b ± √Δ) / 2a")

print("\n2. RAY-PLANE INTERSECTION:")
print("   Plane: (P - P₀)·N = 0")
print("   Ray: P(t) = O + tD")
print("   ")
print("   t = (P₀ - O)·N / (D·N)")
print("   ")
print("   If D·N ≈ 0 → Ray parallel to plane (no intersection)")
print("   If t < 0   → Intersection behind ray origin")

print("\n3. RAY-TRIANGLE INTERSECTION (Möller-Trumbore):")
print("   Uses barycentric coordinates (u, v)")
print("   Point in triangle if:")
print("     u ≥ 0, v ≥ 0, u + v ≤ 1")
print("   ")
print("   Very efficient - one of fastest algorithms!")

print("\n4. SURFACE NORMALS:")
print("   Sphere: N = (P - C) / r")
print("   Plane: N = plane normal (constant)")
print("   Triangle: N = (V1-V0) × (V2-V0) (normalized)")

print("\n5. CLOSEST HIT:")
print("   When ray intersects multiple objects:")
print("     1. Test all objects")
print("     2. Find smallest positive t")
print("     3. That's the visible intersection")

print("\n" + "=" * 70)
print("Scene shows:")
print("  🟢 GREEN rays   - Successful intersections")
print("  🔴 RED rays     - Misses")
print("  🟡 YELLOW dots  - Vertices and centers")
print("  🔵 CYAN arrows  - Surface normals")
print("  🔴 RED dots     - Intersection points")
print("=" * 70)
