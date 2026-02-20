"""
Blender Python Tutorial - Lesson 10: Procedural Generation
===========================================================

Learn how to create complex scenes procedurally:
- Creating custom meshes from scratch
- Using BMesh for mesh manipulation
- Procedural patterns and formations
- Randomization and noise
- Instancing for performance
- Procedural cities, forests, etc.
- Fractals and recursive structures
"""

import bpy

import bmesh
import math
import random
from mathutils import Vector

def ensure_object_mode():
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')


# Clear the scene

ensure_object_mode()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("Demonstrating procedural generation...\n")

# Set random seed for reproducibility
random.seed(42)

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(20, -20, 30))
bpy.context.active_object.data.energy = 3.0

# ============================================
# 1. CREATING CUSTOM MESH FROM VERTICES
# ============================================
print("1. CREATING CUSTOM MESH - Triangle")

# Create mesh data
mesh = bpy.data.meshes.new("TriangleMesh")

# Define vertices (3D coordinates)
vertices = [
    (0, 0, 0),
    (2, 0, 0),
    (1, 2, 0)
]

# Define faces (indices of vertices)
faces = [(0, 1, 2)]

# Create the mesh
mesh.from_pydata(vertices, [], faces)
mesh.update()

# Create object and link to scene
triangle_obj = bpy.data.objects.new("Triangle", mesh)
bpy.context.collection.objects.link(triangle_obj)
triangle_obj.location = (0, 0, 0)

print(f"  Created triangle with {len(vertices)} vertices")

# ============================================
# 2. BMESH - ADVANCED MESH EDITING
# ============================================
print("\n2. BMESH - Creating a pyramid")

def create_pyramid(size, height, location):
    """Create a pyramid using BMesh"""
    mesh = bpy.data.meshes.new("PyramidMesh")
    bm = bmesh.new()

    # Create vertices
    # Base corners
    v1 = bm.verts.new((-size, -size, 0))
    v2 = bm.verts.new((size, -size, 0))
    v3 = bm.verts.new((size, size, 0))
    v4 = bm.verts.new((-size, size, 0))
    # Top point
    v5 = bm.verts.new((0, 0, height))

    # Create faces
    bm.faces.new([v1, v2, v3, v4])  # Base
    bm.faces.new([v1, v2, v5])  # Side 1
    bm.faces.new([v2, v3, v5])  # Side 2
    bm.faces.new([v3, v4, v5])  # Side 3
    bm.faces.new([v4, v1, v5])  # Side 4

    # Finish up
    bm.to_mesh(mesh)
    bm.free()

    # Create object
    obj = bpy.data.objects.new("Pyramid", mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location

    return obj

pyramid = create_pyramid(1, 2, (4, 0, 0))
print(f"  Created {pyramid.name} using BMesh")

# ============================================
# 3. GRID PATTERN
# ============================================
print("\n3. GRID PATTERN - Array of objects")

grid_size = 5
spacing = 2

for x in range(grid_size):
    for y in range(grid_size):
        # Vary the height based on position
        height = math.sin(x * 0.5) * math.cos(y * 0.5) + 1

        bpy.ops.mesh.primitive_cube_add(
            size=0.8,
            location=(x * spacing - 4, y * spacing + 6, height)
        )
        cube = bpy.context.active_object
        cube.name = f"Grid_{x}_{y}"
        cube.scale.z = height

print(f"  Created {grid_size}x{grid_size} grid pattern")

# ============================================
# 4. CIRCULAR PATTERN
# ============================================
print("\n4. CIRCULAR PATTERN - Ring of objects")

def create_circle_pattern(count, radius, obj_size, height, location):
    """Create objects in a circular pattern"""
    for i in range(count):
        angle = (2 * math.pi / count) * i
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        bpy.ops.mesh.primitive_cylinder_add(
            radius=obj_size,
            depth=height,
            location=(location[0] + x, location[1] + y, location[2])
        )
        obj = bpy.context.active_object
        obj.name = f"Circle_{i}"

        # Rotate to face center
        obj.rotation_euler.z = angle + math.radians(90)

create_circle_pattern(count=12, radius=8, obj_size=0.3, height=2, location=(15, 0, 1))
print(f"  Created circular pattern with 12 objects")

# ============================================
# 5. SPIRAL PATTERN
# ============================================
print("\n5. SPIRAL PATTERN - Helix")

def create_spiral(count, radius, height_per_turn, turns, location):
    """Create a spiral of objects"""
    for i in range(count):
        progress = i / count
        angle = progress * turns * 2 * math.pi
        height = progress * height_per_turn * turns

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        bpy.ops.mesh.primitive_sphere_add(
            radius=0.3,
            location=(location[0] + x, location[1] + y, location[2] + height)
        )
        obj = bpy.context.active_object
        obj.name = f"Spiral_{i}"

create_spiral(count=50, radius=3, height_per_turn=2, turns=3, location=(25, 0, 0))
print(f"  Created spiral with 50 spheres")

# ============================================
# 6. RANDOM SCATTER
# ============================================
print("\n6. RANDOM SCATTER - Procedural forest")

def scatter_objects(count, area_size, height_variation, location):
    """Scatter objects randomly in an area"""
    for i in range(count):
        x = random.uniform(-area_size, area_size)
        y = random.uniform(-area_size, area_size)
        height = random.uniform(1, height_variation)

        # Create "tree" (cylinder + cone)
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.2,
            depth=height,
            location=(location[0] + x, location[1] + y, location[2] + height/2)
        )
        trunk = bpy.context.active_object
        trunk.name = f"Tree_Trunk_{i}"

        bpy.ops.mesh.primitive_cone_add(
            radius1=0.8,
            depth=1.5,
            location=(location[0] + x, location[1] + y, location[2] + height + 0.75)
        )
        foliage = bpy.context.active_object
        foliage.name = f"Tree_Foliage_{i}"

        # Random color variation
        mat = bpy.data.materials.new(name=f"TreeMat_{i}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        green = random.uniform(0.3, 0.7)
        bsdf.inputs['Base Color'].default_value = (0.1, green, 0.1, 1)
        foliage.data.materials.append(mat)

scatter_objects(count=20, area_size=10, height_variation=4, location=(35, 15, 0))
print(f"  Created random forest with 20 trees")

# ============================================
# 7. NOISE-BASED TERRAIN
# ============================================
print("\n7. NOISE-BASED TERRAIN - Procedural landscape")

def create_terrain(size, resolution, height_scale, location):
    """Create terrain using noise"""
    mesh = bpy.data.meshes.new("TerrainMesh")
    bm = bmesh.new()

    # Create grid of vertices
    vertices = []
    for y in range(resolution):
        for x in range(resolution):
            # Normalized coordinates
            nx = x / (resolution - 1)
            ny = y / (resolution - 1)

            # Position
            pos_x = (nx - 0.5) * size
            pos_y = (ny - 0.5) * size

            # Simple noise (you could use Perlin noise library for better results)
            noise = math.sin(nx * 5) * math.cos(ny * 5)
            noise += math.sin(nx * 10) * math.cos(ny * 10) * 0.5
            pos_z = noise * height_scale

            vert = bm.verts.new((pos_x, pos_y, pos_z))
            vertices.append(vert)

    # Create faces
    for y in range(resolution - 1):
        for x in range(resolution - 1):
            i = y * resolution + x
            v1 = vertices[i]
            v2 = vertices[i + 1]
            v3 = vertices[i + resolution + 1]
            v4 = vertices[i + resolution]
            bm.faces.new([v1, v2, v3, v4])

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("Terrain", mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location

    return obj

terrain = create_terrain(size=20, resolution=30, height_scale=2, location=(50, 0, 0))
print(f"  Created procedural terrain")

# ============================================
# 8. FRACTAL - RECURSIVE TREE
# ============================================
print("\n8. FRACTAL STRUCTURE - Recursive tree")

def create_fractal_tree(start, direction, length, depth, location_offset):
    """Create a fractal tree structure using recursion"""
    if depth == 0:
        return

    # Calculate end point
    end = start + direction * length

    # Create branch
    mesh = bpy.data.meshes.new("BranchMesh")
    bm = bmesh.new()

    v1 = bm.verts.new(start)
    v2 = bm.verts.new(end)
    bm.edges.new([v1, v2])

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(f"Branch_{depth}", mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location_offset

    # Add skin modifier for thickness
    skin_mod = obj.modifiers.new(name="Skin", type='SKIN')

    # Recursively create child branches
    if depth > 1:
        # Left branch
        angle_left = 30
        rotation_left = math.radians(angle_left)
        new_direction_left = direction.copy()
        new_direction_left.rotate(Vector((0, 0, 1)).rotation_difference(Vector((1, 0, 0))))
        new_direction_left = Vector((
            math.cos(rotation_left) * direction.x - math.sin(rotation_left) * direction.z,
            direction.y,
            math.sin(rotation_left) * direction.x + math.cos(rotation_left) * direction.z
        ))

        create_fractal_tree(end, new_direction_left.normalized(), length * 0.7, depth - 1, location_offset)

        # Right branch
        angle_right = -30
        rotation_right = math.radians(angle_right)
        new_direction_right = Vector((
            math.cos(rotation_right) * direction.x - math.sin(rotation_right) * direction.z,
            direction.y,
            math.sin(rotation_right) * direction.x + math.cos(rotation_right) * direction.z
        ))

        create_fractal_tree(end, new_direction_right.normalized(), length * 0.7, depth - 1, location_offset)

# Create fractal tree
create_fractal_tree(
    start=Vector((0, 0, 0)),
    direction=Vector((0, 0, 1)),
    length=3,
    depth=5,
    location_offset=(0, -15, 0)
)

print(f"  Created fractal tree (depth 5)")

# ============================================
# 9. VORONOI PATTERN (Simple version)
# ============================================
print("\n9. VORONOI-LIKE PATTERN")

def create_voronoi_spheres(count, area_size, location):
    """Create a Voronoi-like pattern"""
    # Generate random points
    points = []
    for i in range(count):
        x = random.uniform(-area_size, area_size)
        y = random.uniform(-area_size, area_size)
        z = random.uniform(0, 2)
        points.append((x, y, z))

    # Create sphere at each point
    for i, point in enumerate(points):
        # Find distance to nearest other point
        min_dist = float('inf')
        for j, other in enumerate(points):
            if i != j:
                dist = math.sqrt(sum((a - b)**2 for a, b in zip(point, other)))
                min_dist = min(min_dist, dist)

        # Scale sphere based on distance
        radius = min_dist * 0.3

        bpy.ops.mesh.primitive_sphere_add(
            radius=radius,
            location=(location[0] + point[0], location[1] + point[1], location[2] + point[2])
        )
        obj = bpy.context.active_object
        obj.name = f"Voronoi_{i}"

create_voronoi_spheres(count=15, area_size=8, location=(-15, -15, 0))
print(f"  Created Voronoi-like pattern")

# ============================================
# 10. PROCEDURAL CITY (Simple)
# ============================================
print("\n10. PROCEDURAL CITY - Simple buildings")

def create_building(location, width, depth, height):
    """Create a simple building"""
    bpy.ops.mesh.primitive_cube_add(location=location)
    building = bpy.context.active_object
    building.scale = (width/2, depth/2, height/2)
    building.location.z += height/2
    return building

def create_city(grid_x, grid_y, block_size, spacing, location):
    """Create a simple procedural city"""
    for x in range(grid_x):
        for y in range(grid_y):
            # Random building dimensions
            width = random.uniform(block_size * 0.6, block_size * 0.9)
            depth = random.uniform(block_size * 0.6, block_size * 0.9)
            height = random.uniform(3, 15)

            pos_x = location[0] + x * (block_size + spacing)
            pos_y = location[1] + y * (block_size + spacing)

            building = create_building(
                location=(pos_x, pos_y, 0),
                width=width,
                depth=depth,
                height=height
            )
            building.name = f"Building_{x}_{y}"

            # Add material
            mat = bpy.data.materials.new(name=f"BuildingMat_{x}_{y}")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            gray = random.uniform(0.3, 0.7)
            bsdf.inputs['Base Color'].default_value = (gray, gray, gray, 1)
            building.data.materials.append(mat)

create_city(grid_x=6, grid_y=6, block_size=3, spacing=1, location=(-25, -30, 0))
print(f"  Created procedural city (6x6 buildings)")

# ============================================
# 11. INSTANCING FOR PERFORMANCE
# ============================================
print("\n11. INSTANCING - Efficient duplication")

# Create a base object
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.2, location=(60, 0, 0))
instance_base = bpy.context.active_object
instance_base.name = "InstanceBase"

# Create instances (linked duplicates - very efficient)
for i in range(100):
    x = random.uniform(-5, 5) + 60
    y = random.uniform(-5, 5)
    z = random.uniform(0, 10)

    # Create instance
    instance = bpy.data.objects.new(f"Instance_{i}", instance_base.data)
    bpy.context.collection.objects.link(instance)
    instance.location = (x, y, z)
    instance.scale = (random.uniform(0.5, 1.5),) * 3

print(f"  Created 100 instances (efficient)")

# ============================================
# 12. PARAMETRIC SURFACE
# ============================================
print("\n12. PARAMETRIC SURFACE - Mathematical shape")

def create_parametric_surface(u_res, v_res, location):
    """Create a parametric surface"""
    mesh = bpy.data.meshes.new("ParametricMesh")
    bm = bmesh.new()

    vertices = []

    # Generate vertices
    for u_i in range(u_res):
        for v_i in range(v_res):
            u = (u_i / (u_res - 1)) * 2 * math.pi
            v = (v_i / (v_res - 1)) * math.pi

            # Parametric equations (sphere-like with waves)
            x = math.sin(v) * math.cos(u) * (2 + 0.3 * math.sin(5 * u))
            y = math.sin(v) * math.sin(u) * (2 + 0.3 * math.sin(5 * u))
            z = math.cos(v) * 2

            vert = bm.verts.new((x, y, z))
            vertices.append(vert)

    # Create faces
    for u_i in range(u_res - 1):
        for v_i in range(v_res - 1):
            i = u_i * v_res + v_i
            v1 = vertices[i]
            v2 = vertices[i + 1]
            v3 = vertices[i + v_res + 1]
            v4 = vertices[i + v_res]
            bm.faces.new([v1, v2, v3, v4])

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("ParametricSurface", mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location

    return obj

param_surface = create_parametric_surface(u_res=40, v_res=20, location=(70, 0, 5))
print(f"  Created parametric surface")

# Add camera to view everything
bpy.ops.object.camera_add(location=(30, -40, 25))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(65), 0, math.radians(37))
bpy.context.scene.camera = camera

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 50)
print("PROCEDURAL GENERATION SUMMARY")
print("=" * 50)
print("Techniques covered:")
print("  1. Custom meshes from vertices and faces")
print("  2. BMesh for advanced mesh manipulation")
print("  3. Grid and circular patterns")
print("  4. Spiral formations")
print("  5. Random scattering")
print("  6. Noise-based terrain")
print("  7. Fractal/recursive structures")
print("  8. Voronoi patterns")
print("  9. Procedural architecture")
print("  10. Instancing for performance")
print("  11. Parametric surfaces")
print("\nKey concepts:")
print("  - mesh.from_pydata(verts, edges, faces)")
print("  - BMesh for procedural modeling")
print("  - Random module for variation")
print("  - Math for patterns and formulas")
print("  - Instancing for large counts")
print("  - Recursion for fractals")
print("\nApplications:")
print("  - Terrain generation")
print("  - Procedural cities")
print("  - Vegetation scattering")
print("  - Abstract art and patterns")
print("  - Game asset generation")
