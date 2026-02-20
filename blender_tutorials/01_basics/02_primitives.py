"""
Blender Python Tutorial - Lesson 2: Creating Primitives
========================================================

Learn how to create different primitive objects:
- Cube, Sphere, Cylinder, Cone, Torus
- UV Sphere vs Icosphere
- Setting parameters for each primitive
- Positioning objects in 3D space
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

print("Creating primitive objects...\n")

# 1. CUBE
print("1. Creating a Cube")
bpy.ops.mesh.primitive_cube_add(
    size=2,
    location=(-6, 0, 0)
)
cube = bpy.context.active_object
cube.name = "Cube_Primitive"

# 2. UV SPHERE
print("2. Creating a UV Sphere")
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=1,
    segments=32,        # Horizontal segments
    ring_count=16,      # Vertical segments
    location=(-3, 0, 0)
)
uv_sphere = bpy.context.active_object
uv_sphere.name = "UVSphere_Primitive"

# 3. ICOSPHERE (more uniform triangles than UV sphere)
print("3. Creating an Icosphere")
bpy.ops.mesh.primitive_ico_sphere_add(
    radius=1,
    subdivisions=2,     # Number of subdivisions (more = smoother)
    location=(0, 0, 0)
)
ico_sphere = bpy.context.active_object
ico_sphere.name = "IcoSphere_Primitive"

# 4. CYLINDER
print("4. Creating a Cylinder")
bpy.ops.mesh.primitive_cylinder_add(
    radius=1,
    depth=2,            # Height of the cylinder
    vertices=32,        # Number of vertices in the circle
    location=(3, 0, 0)
)
cylinder = bpy.context.active_object
cylinder.name = "Cylinder_Primitive"

# 5. CONE
print("5. Creating a Cone")
bpy.ops.mesh.primitive_cone_add(
    radius1=1,          # Base radius
    radius2=0,          # Top radius (0 for sharp point)
    depth=2,
    vertices=32,
    location=(6, 0, 0)
)
cone = bpy.context.active_object
cone.name = "Cone_Primitive"

# 6. TORUS
print("6. Creating a Torus")
bpy.ops.mesh.primitive_torus_add(
    major_radius=1,     # Distance from center to tube center
    minor_radius=0.25,  # Tube radius
    major_segments=48,
    minor_segments=12,
    location=(0, -3, 0)
)
torus = bpy.context.active_object
torus.name = "Torus_Primitive"

# 7. MONKEY (Suzanne - Blender's mascot)
print("7. Creating Suzanne (Monkey)")
bpy.ops.mesh.primitive_monkey_add(
    size=1.5,
    location=(0, 3, 0)
)
monkey = bpy.context.active_object
monkey.name = "Suzanne"

# 8. PLANE
print("8. Creating a Plane")
bpy.ops.mesh.primitive_plane_add(
    size=10,
    location=(0, 0, -2)
)
plane = bpy.context.active_object
plane.name = "Ground_Plane"

# Print summary
print("\n" + "=" * 50)
print("Summary of created objects:")
print("=" * 50)
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        vertex_count = len(obj.data.vertices)
        face_count = len(obj.data.polygons)
        print(f"{obj.name}:")
        print(f"  Location: ({obj.location.x:.1f}, {obj.location.y:.1f}, {obj.location.z:.1f})")
        print(f"  Vertices: {vertex_count}, Faces: {face_count}")

print("\nTip: Different primitives are better for different purposes!")
print("  - UV Sphere: Good for texturing (like Earth)")
print("  - Icosphere: Better topology for subdivision")
print("  - Suzanne: Standard test model in Blender")
