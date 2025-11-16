"""
Blender Python Tutorial - Lesson 14: Raytracing Basics
=======================================================

Understanding the fundamental mathematics of raytracing:
- What is a ray? (origin + direction)
- Vector mathematics for rays
- Parametric ray equation: P(t) = O + t*D
- Visualizing rays in 3D space
- Ray creation from camera
- Understanding coordinate systems

This tutorial visualizes the core concepts of raytracing!
"""

import bpy
import math
from mathutils import Vector, Matrix
import random

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("=" * 70)
print("RAYTRACING FUNDAMENTALS - Part 1: Understanding Rays")
print("=" * 70)

# ============================================
# HELPER FUNCTIONS FOR VISUALIZATION
# ============================================

def create_ray_visualization(origin, direction, length=5, name="Ray", color=(1, 0, 0)):
    """
    Create a visual representation of a ray using a cylinder

    Ray equation: P(t) = O + t*D
    where O = origin, D = direction, t = parameter
    """
    # Normalize direction
    direction = direction.normalized()

    # Calculate end point
    end_point = origin + direction * length

    # Create cylinder for ray body
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.02,
        depth=length,
        location=origin + direction * (length / 2)
    )
    ray = bpy.context.active_object
    ray.name = name

    # Align cylinder with direction
    # Cylinder default points in Z direction
    z_axis = Vector((0, 0, 1))
    rotation_quat = z_axis.rotation_difference(direction)
    ray.rotation_euler = rotation_quat.to_euler()

    # Create arrow head (cone)
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.06,
        radius2=0,
        depth=0.2,
        location=end_point
    )
    arrow = bpy.context.active_object
    arrow.name = f"{name}_Arrow"
    arrow.rotation_euler = rotation_quat.to_euler()

    # Parent arrow to ray
    arrow.parent = ray

    # Create material
    mat = bpy.data.materials.new(name=f"{name}_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Emission'].default_value = (*color, 1)
    bsdf.inputs['Emission Strength'].default_value = 2.0

    ray.data.materials.append(mat)
    arrow.data.materials.append(mat)

    return ray, arrow

def create_point_marker(location, name="Point", color=(1, 1, 0), size=0.1):
    """Create a small sphere to mark a point in space"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=size, location=location)
    marker = bpy.context.active_object
    marker.name = name

    mat = bpy.data.materials.new(name=f"{name}_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Emission'].default_value = (*color, 1)
    bsdf.inputs['Emission Strength'].default_value = 3.0

    marker.data.materials.append(mat)
    return marker

def create_text_label(text, location, name="Label"):
    """Create 3D text label"""
    bpy.ops.object.text_add(location=location)
    text_obj = bpy.context.active_object
    text_obj.name = name
    text_obj.data.body = text
    text_obj.data.size = 0.3
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    return text_obj

# ============================================
# 1. THE RAY EQUATION
# ============================================
print("\n1. THE FUNDAMENTAL RAY EQUATION")
print("   P(t) = O + t*D")
print("   where:")
print("     P(t) = point on ray at parameter t")
print("     O    = ray origin (starting point)")
print("     D    = ray direction (normalized vector)")
print("     t    = parameter (distance along ray)")

# Create coordinate system reference
bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))
origin_empty = bpy.context.active_object
origin_empty.name = "Origin"
origin_empty.empty_display_size = 2

# Create axis labels
create_text_label("X", (2, 0, 0), "X_Label")
create_text_label("Y", (0, 2, 0), "Y_Label")
create_text_label("Z", (0, 0, 2), "Z_Label")

print("\n   ✓ Coordinate system visualized")

# ============================================
# 2. BASIC RAY EXAMPLE
# ============================================
print("\n2. BASIC RAY EXAMPLE")

# Define a simple ray
ray_origin = Vector((0, 0, 0))
ray_direction = Vector((1, 0.5, 0.3))

print(f"   Origin:    O = {ray_origin}")
print(f"   Direction: D = {ray_direction}")
print(f"   Normalized D = {ray_direction.normalized()}")

# Create visual representation
create_point_marker(ray_origin, "Ray_Origin", (1, 1, 0))
create_ray_visualization(ray_origin, ray_direction, length=4, name="Example_Ray", color=(1, 0, 0))

# Show points along the ray at different t values
print("\n   Points along the ray:")
for t in [1, 2, 3, 4]:
    point = ray_origin + ray_direction.normalized() * t
    print(f"     P({t}) = {point}")
    create_point_marker(point, f"P_t{t}", (0, 1, 1), size=0.05)

# ============================================
# 3. MULTIPLE RAYS FROM ORIGIN
# ============================================
print("\n3. MULTIPLE RAYS FROM SAME ORIGIN")

multi_origin = Vector((0, -5, 1))
create_point_marker(multi_origin, "Multi_Origin", (1, 1, 0), size=0.15)

# Create rays in different directions
directions = [
    (Vector((1, 0, 0)), "Right"),
    (Vector((0, 1, 0)), "Forward"),
    (Vector((0, 0, 1)), "Up"),
    (Vector((1, 1, 0)), "Diagonal"),
    (Vector((0.5, 0.5, 0.5)), "3D_Diagonal"),
]

colors = [
    (1, 0, 0),    # Red
    (0, 1, 0),    # Green
    (0, 0, 1),    # Blue
    (1, 1, 0),    # Yellow
    (1, 0, 1),    # Magenta
]

print("   Creating rays in different directions:")
for (direction, label), color in zip(directions, colors):
    create_ray_visualization(
        multi_origin,
        direction,
        length=3,
        name=f"Ray_{label}",
        color=color
    )
    print(f"     {label}: D = {direction.normalized()}")

# ============================================
# 4. CAMERA RAY GENERATION
# ============================================
print("\n4. CAMERA RAY GENERATION")
print("   In raytracing, rays are shot from camera through each pixel")

# Create a simple camera representation
camera_pos = Vector((5, -5, 3))
camera_target = Vector((0, 0, 1))

create_point_marker(camera_pos, "Camera_Position", (1, 0.5, 0), size=0.2)

# Create image plane (what the camera sees)
bpy.ops.mesh.primitive_plane_add(size=2, location=camera_pos + Vector((0, 1, 0)))
image_plane = bpy.context.active_object
image_plane.name = "Image_Plane"

# Rotate to face camera direction
look_dir = (camera_target - camera_pos).normalized()
image_plane.rotation_euler = look_dir.to_track_quat('-Z', 'Y').to_euler()

# Material for image plane (semi-transparent)
plane_mat = bpy.data.materials.new(name="ImagePlane_Mat")
plane_mat.use_nodes = True
plane_mat.blend_method = 'BLEND'
bsdf = plane_mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (0.5, 0.5, 1, 0.3)
bsdf.inputs['Alpha'].default_value = 0.3
image_plane.data.materials.append(plane_mat)

# Generate a grid of rays through the image plane
print("   Generating camera rays through image plane...")
grid_size = 5
for i in range(grid_size):
    for j in range(grid_size):
        # Calculate pixel position on image plane
        u = (i / (grid_size - 1)) - 0.5  # -0.5 to 0.5
        v = (j / (grid_size - 1)) - 0.5

        # Position on image plane (simplified)
        pixel_pos = camera_pos + look_dir * 1.5
        pixel_pos += Vector((u * 2, 0, v * 2))

        # Ray from camera through pixel
        ray_dir = (pixel_pos - camera_pos).normalized()

        if i % 2 == 0 and j % 2 == 0:  # Only show subset for clarity
            create_ray_visualization(
                camera_pos,
                ray_dir,
                length=2,
                name=f"Camera_Ray_{i}_{j}",
                color=(0.3, 0.7, 1)
            )

print(f"   ✓ Generated {grid_size}x{grid_size} camera rays (subset shown)")

# ============================================
# 5. RAY-SPHERE VISUALIZATION
# ============================================
print("\n5. RAY-SPHERE INTERACTION PREVIEW")
print("   (Detailed intersection math in next lesson)")

# Create a sphere to intersect
sphere_center = Vector((3, -5, 1))
sphere_radius = 1.0

bpy.ops.mesh.primitive_uv_sphere_add(radius=sphere_radius, location=sphere_center)
sphere = bpy.context.active_object
sphere.name = "Target_Sphere"

# Semi-transparent material
sphere_mat = bpy.data.materials.new(name="Sphere_Mat")
sphere_mat.use_nodes = True
sphere_mat.blend_method = 'BLEND'
bsdf = sphere_mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (1, 0.5, 0, 0.5)
bsdf.inputs['Alpha'].default_value = 0.5
bsdf.inputs['Transmission'].default_value = 0.3
sphere.data.materials.append(sphere_mat)

# Create rays that will intersect and miss the sphere
print("   Creating rays to demonstrate intersection:")

# Ray that hits
hit_origin = Vector((0, -5, 1))
hit_direction = (sphere_center - hit_origin).normalized()
create_ray_visualization(hit_origin, hit_direction, length=5, name="Hit_Ray", color=(0, 1, 0))
create_point_marker(hit_origin, "Hit_Origin", (0, 1, 0), size=0.1)
print("     ✓ Green ray: HITS sphere")

# Ray that misses
miss_origin = Vector((0, -5, 3))
miss_direction = Vector((1, 0, -0.5))
create_ray_visualization(miss_origin, miss_direction, length=5, name="Miss_Ray", color=(1, 0, 0))
create_point_marker(miss_origin, "Miss_Origin", (1, 0, 0), size=0.1)
print("     ✓ Red ray: MISSES sphere")

# ============================================
# 6. VECTOR DOT PRODUCT VISUALIZATION
# ============================================
print("\n6. DOT PRODUCT - Essential for Raytracing")
print("   dot(A, B) = |A| * |B| * cos(θ)")
print("   Used for: angles, projections, testing")

dot_origin = Vector((6, 0, 0))

# Two vectors to demonstrate dot product
vec_a = Vector((1, 0, 0))
vec_b = Vector((0.7, 0.7, 0)).normalized()

create_ray_visualization(dot_origin, vec_a, length=2, name="Vec_A", color=(1, 0, 0))
create_ray_visualization(dot_origin, vec_b, length=2, name="Vec_B", color=(0, 1, 0))

dot_product = vec_a.dot(vec_b)
angle = math.acos(min(1, max(-1, dot_product)))  # Clamp for safety

print(f"   Vector A: {vec_a}")
print(f"   Vector B: {vec_b.normalized()}")
print(f"   Dot Product: {dot_product:.3f}")
print(f"   Angle: {math.degrees(angle):.1f}°")

# Create arc to show angle
create_text_label(f"{math.degrees(angle):.1f}°", dot_origin + Vector((0.8, 0.4, 0)), "Angle_Label")

# ============================================
# 7. VECTOR CROSS PRODUCT
# ============================================
print("\n7. CROSS PRODUCT - For Normals and Perpendiculars")
print("   cross(A, B) = vector perpendicular to both A and B")

cross_origin = Vector((6, -4, 0))

vec_c = Vector((1, 0, 0))
vec_d = Vector((0, 1, 0))
vec_e = vec_c.cross(vec_d)  # Result is (0, 0, 1)

create_ray_visualization(cross_origin, vec_c, length=1.5, name="Cross_A", color=(1, 0, 0))
create_ray_visualization(cross_origin, vec_d, length=1.5, name="Cross_B", color=(0, 1, 0))
create_ray_visualization(cross_origin, vec_e, length=1.5, name="Cross_Result", color=(0, 0, 1))

print(f"   A × B = {vec_e}")
print(f"   Result is perpendicular to both A and B")

# ============================================
# 8. PARAMETRIC RAY ANIMATION
# ============================================
print("\n8. ANIMATING ALONG A RAY")
print("   Showing P(t) = O + t*D with varying t")

# Create animated object that travels along ray
anim_origin = Vector((-3, 3, 0))
anim_direction = Vector((1, 0, 0.5)).normalized()

# Create the ray path
create_ray_visualization(anim_origin, anim_direction, length=6, name="Animated_Ray_Path", color=(1, 1, 0))

# Create traveling object
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=anim_origin)
traveler = bpy.context.active_object
traveler.name = "Ray_Traveler"

traveler_mat = bpy.data.materials.new(name="Traveler_Mat")
traveler_mat.use_nodes = True
bsdf = traveler_mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Emission'].default_value = (0, 1, 1, 1)
bsdf.inputs['Emission Strength'].default_value = 5.0
traveler.data.materials.append(traveler_mat)

# Animate along the ray
scene = bpy.context.scene
scene.frame_end = 120

for frame in range(1, 121, 10):
    scene.frame_set(frame)
    t = (frame / 120) * 6  # Travel 6 units
    position = anim_origin + anim_direction * t
    traveler.location = position
    traveler.keyframe_insert(data_path="location", frame=frame)

print("   ✓ Created animation showing parametric ray equation")

# ============================================
# LIGHTING AND CAMERA
# ============================================

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(10, -10, 10))
sun = bpy.context.active_object
sun.data.energy = 2.0

# Add camera for nice view
bpy.ops.object.camera_add(location=(12, -12, 8))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))
bpy.context.scene.camera = camera

# Dark background for better ray visibility
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (0.01, 0.01, 0.02, 1)
bg.inputs['Strength'].default_value = 0.1

# ============================================
# MATHEMATICAL SUMMARY
# ============================================
print("\n" + "=" * 70)
print("RAYTRACING MATHEMATICS SUMMARY")
print("=" * 70)

print("\n1. RAY EQUATION:")
print("   P(t) = O + t*D")
print("   - O: Origin point (x, y, z)")
print("   - D: Direction vector (normalized)")
print("   - t: Parameter (t ≥ 0 for forward rays)")
print("   - P(t): Any point along the ray")

print("\n2. VECTOR OPERATIONS:")
print("   Length: |V| = sqrt(x² + y² + z²)")
print("   Normalize: V̂ = V / |V|")
print("   Dot: A·B = Ax*Bx + Ay*By + Az*Bz = |A||B|cos(θ)")
print("   Cross: A×B = perpendicular vector to both A and B")

print("\n3. DOT PRODUCT PROPERTIES:")
print("   > 0  → Angle < 90° (same general direction)")
print("   = 0  → Angle = 90° (perpendicular)")
print("   < 0  → Angle > 90° (opposite directions)")

print("\n4. KEY USES IN RAYTRACING:")
print("   ✓ Ray generation from camera")
print("   ✓ Finding intersections with geometry")
print("   ✓ Calculating reflections (next lesson)")
print("   ✓ Determining surface normals")
print("   ✓ Testing ray-object hits")

print("\n5. CAMERA RAY GENERATION:")
print("   For each pixel (x, y) in image:")
print("     1. Calculate direction through pixel")
print("     2. Create ray from camera position")
print("     3. Test intersection with scene")
print("     4. Calculate color at hit point")

print("\n" + "=" * 70)
print("VISUALIZATION GUIDE")
print("=" * 70)
print("In this scene you can see:")
print("  🔴 RED rays    - Example rays and misses")
print("  🟢 GREEN rays  - Successful intersections")
print("  🔵 BLUE rays   - Camera rays")
print("  🟡 YELLOW      - Ray origins and animated path")
print("  🟠 ORANGE      - Target sphere for intersection")
print("\nPress SPACEBAR to see the animated ray travel!")
print("=" * 70)
