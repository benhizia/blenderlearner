"""
Blender Python Tutorial - Lesson 3: Transformations
====================================================

Learn how to transform objects in 3D space:
- Translation (moving objects)
- Rotation (rotating objects)
- Scaling (resizing objects)
- Understanding Euler angles and radians
- Combining transformations
"""

import bpy

import math

def ensure_object_mode():
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')


# Clear the scene

ensure_object_mode()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("Demonstrating transformations...\n")

# Helper function to convert degrees to radians
def deg_to_rad(degrees):
    """Convert degrees to radians (Blender uses radians)"""
    return degrees * (math.pi / 180)

# Create a ground plane for reference
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1))
bpy.context.active_object.name = "Ground"

# ============================================
# 1. TRANSLATION (Moving objects)
# ============================================
print("1. TRANSLATION - Moving objects in 3D space")

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube1 = bpy.context.active_object
cube1.name = "Cube_Translation"

# Move the cube using location property
print(f"  Initial location: {cube1.location}")
cube1.location.x = 3
cube1.location.y = 0
cube1.location.z = 0
print(f"  After moving: {cube1.location}")

# Alternative: Set all coordinates at once
cube1.location = (3, 2, 0)
print(f"  New location: {cube1.location}")

# ============================================
# 2. ROTATION
# ============================================
print("\n2. ROTATION - Rotating objects")

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube2 = bpy.context.active_object
cube2.name = "Cube_Rotation"

# Rotate using Euler angles (in radians!)
# Rotation order: XYZ (can be changed)
cube2.rotation_euler.x = deg_to_rad(45)   # Pitch
cube2.rotation_euler.y = deg_to_rad(0)    # Yaw
cube2.rotation_euler.z = deg_to_rad(30)   # Roll

print(f"  Rotation (radians): {cube2.rotation_euler}")
print(f"  Rotation (degrees): X={math.degrees(cube2.rotation_euler.x):.1f}, "
      f"Y={math.degrees(cube2.rotation_euler.y):.1f}, "
      f"Z={math.degrees(cube2.rotation_euler.z):.1f}")

# Alternative: Set all rotations at once
cube2.rotation_euler = (deg_to_rad(45), deg_to_rad(30), deg_to_rad(15))

# Move it to a different position for visibility
cube2.location = (-3, 2, 0)

# ============================================
# 3. SCALING
# ============================================
print("\n3. SCALING - Resizing objects")

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube3 = bpy.context.active_object
cube3.name = "Cube_Scaling"

# Scale uniformly
cube3.scale = (1.5, 1.5, 1.5)
print(f"  Uniform scale: {cube3.scale}")

# Non-uniform scaling (different on each axis)
cube3.scale.x = 2.0  # Wider
cube3.scale.y = 0.5  # Thinner
cube3.scale.z = 3.0  # Taller
print(f"  Non-uniform scale: {cube3.scale}")

cube3.location = (3, -2, 1)

# ============================================
# 4. COMBINING TRANSFORMATIONS
# ============================================
print("\n4. COMBINING TRANSFORMATIONS")

bpy.ops.mesh.primitive_cylinder_add()
cylinder = bpy.context.active_object
cylinder.name = "Cylinder_Combined"

# Apply multiple transformations
cylinder.location = (-3, -3, 0)
cylinder.rotation_euler = (deg_to_rad(90), 0, 0)  # Rotate 90° on X
cylinder.scale = (0.5, 0.5, 2)

print(f"  Location: {cylinder.location}")
print(f"  Rotation: {math.degrees(cylinder.rotation_euler.x):.0f}° on X")
print(f"  Scale: {cylinder.scale}")

# ============================================
# 5. RELATIVE TRANSFORMATIONS
# ============================================
print("\n5. RELATIVE TRANSFORMATIONS")

bpy.ops.mesh.primitive_sphere_add(location=(0, -3, 0))
sphere = bpy.context.active_object
sphere.name = "Sphere_Relative"

print(f"  Initial location: {sphere.location}")

# Move relative to current position
sphere.location.x += 2
sphere.location.z += 1
print(f"  After relative move: {sphere.location}")

# Rotate relative to current rotation
sphere.rotation_euler.z += deg_to_rad(45)

# Scale relative to current scale
sphere.scale *= 1.5  # Make 50% larger

# ============================================
# 6. USING OPERATORS FOR TRANSFORMATION
# ============================================
print("\n6. USING OPERATORS (Alternative method)")

bpy.ops.mesh.primitive_cone_add(location=(0, 3, 0))
cone = bpy.context.active_object
cone.name = "Cone_Operator"

# Make sure the cone is selected
cone.select_set(True)
bpy.context.view_layer.objects.active = cone

# Use operators to transform
bpy.ops.transform.translate(value=(2, 0, 1))
bpy.ops.transform.rotate(value=deg_to_rad(45), orient_axis='Z')
bpy.ops.transform.resize(value=(1, 1, 2))

# ============================================
# 7. DEMONSTRATION: CIRCULAR ARRANGEMENT
# ============================================
print("\n7. BONUS: Creating a circular arrangement")

num_objects = 8
radius = 5

for i in range(num_objects):
    angle = (2 * math.pi / num_objects) * i
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)

    bpy.ops.mesh.primitive_cube_add(
        size=0.5,
        location=(x, y, 0)
    )
    cube = bpy.context.active_object
    cube.name = f"Circle_Cube_{i}"

    # Rotate to face center
    cube.rotation_euler.z = angle + deg_to_rad(90)

print(f"  Created {num_objects} cubes in a circle")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 50)
print("TRANSFORMATION SUMMARY")
print("=" * 50)
print("Location: object.location = (x, y, z)")
print("Rotation: object.rotation_euler = (x, y, z) in RADIANS")
print("Scale: object.scale = (x, y, z)")
print("\nRemember:")
print("  - Blender uses radians for rotation")
print("  - Default scale is (1, 1, 1)")
print("  - Transformations can be absolute or relative")
print("  - Right-handed coordinate system: +Z is up")
