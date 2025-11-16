"""
Blender Python Tutorial - Lesson 4: Basic Operations
=====================================================

Learn essential operations for working with objects:
- Selecting and deselecting objects
- Duplicating objects
- Deleting objects
- Hiding and showing objects
- Renaming objects
- Working with collections
- Accessing object data
"""

import bpy

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("Demonstrating basic operations...\n")

# ============================================
# 1. CREATING AND NAMING OBJECTS
# ============================================
print("1. CREATING AND NAMING OBJECTS")

# Create several objects
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "MyCube"

bpy.ops.mesh.primitive_sphere_add(location=(3, 0, 0))
sphere = bpy.context.active_object
sphere.name = "MySphere"

bpy.ops.mesh.primitive_cylinder_add(location=(-3, 0, 0))
cylinder = bpy.context.active_object
cylinder.name = "MyCylinder"

print(f"Created: {cube.name}, {sphere.name}, {cylinder.name}")

# ============================================
# 2. SELECTING OBJECTS
# ============================================
print("\n2. SELECTING OBJECTS")

# Deselect all
bpy.ops.object.select_all(action='DESELECT')
print("  Deselected all objects")

# Select specific object by name
obj = bpy.data.objects.get("MyCube")
if obj:
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    print(f"  Selected: {obj.name}")

# Select multiple objects
for name in ["MySphere", "MyCylinder"]:
    obj = bpy.data.objects.get(name)
    if obj:
        obj.select_set(True)
        print(f"  Selected: {name}")

# Check selection status
print("\n  Selection status:")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print(f"    {obj.name}: {'SELECTED' if obj.select_get() else 'not selected'}")

# ============================================
# 3. DUPLICATING OBJECTS
# ============================================
print("\n3. DUPLICATING OBJECTS")

# Method 1: Using operator (requires selection)
bpy.ops.object.select_all(action='DESELECT')
cube.select_set(True)
bpy.context.view_layer.objects.active = cube

bpy.ops.object.duplicate()
duplicate1 = bpy.context.active_object
duplicate1.location.y = 2
duplicate1.name = "CubeDuplicate_1"
print(f"  Created duplicate using operator: {duplicate1.name}")

# Method 2: Using copy (more control)
new_cube = cube.copy()
new_cube.data = cube.data.copy()  # Also copy the mesh data
new_cube.location = (0, -2, 0)
new_cube.name = "CubeDuplicate_2"
bpy.context.collection.objects.link(new_cube)
print(f"  Created duplicate using copy: {new_cube.name}")

# Create array of duplicates
print("\n  Creating an array of duplicates:")
for i in range(5):
    dup = sphere.copy()
    dup.data = sphere.data.copy()
    dup.location = (3, 2 + i * 1.5, 0)
    dup.name = f"SphereArray_{i}"
    bpy.context.collection.objects.link(dup)
    print(f"    Created: {dup.name}")

# ============================================
# 4. DELETING OBJECTS
# ============================================
print("\n4. DELETING OBJECTS")

# Method 1: Delete by reference
obj_to_delete = bpy.data.objects.get("CubeDuplicate_1")
if obj_to_delete:
    bpy.data.objects.remove(obj_to_delete, do_unlink=True)
    print(f"  Deleted: CubeDuplicate_1")

# Method 2: Delete using operator (requires selection)
bpy.ops.object.select_all(action='DESELECT')
sphere_array_0 = bpy.data.objects.get("SphereArray_0")
if sphere_array_0:
    sphere_array_0.select_set(True)
    bpy.ops.object.delete()
    print(f"  Deleted: SphereArray_0")

# ============================================
# 5. HIDING AND SHOWING OBJECTS
# ============================================
print("\n5. HIDING AND SHOWING OBJECTS")

# Hide an object (in viewport)
cylinder.hide_viewport = True
print(f"  Hidden in viewport: {cylinder.name}")

# Hide in render
cylinder.hide_render = True
print(f"  Hidden in render: {cylinder.name}")

# Show it again
cylinder.hide_viewport = False
cylinder.hide_render = False
print(f"  Shown again: {cylinder.name}")

# Disable in viewport (makes it non-selectable)
cylinder.hide_select = False  # Can be selected
print(f"  {cylinder.name} is selectable")

# ============================================
# 6. ACCESSING OBJECT DATA
# ============================================
print("\n6. ACCESSING OBJECT DATA")

# Get object properties
print(f"\n  {cube.name} properties:")
print(f"    Type: {cube.type}")
print(f"    Location: {cube.location}")
print(f"    Rotation: {cube.rotation_euler}")
print(f"    Scale: {cube.scale}")
print(f"    Dimensions: {cube.dimensions}")

# Access mesh data
if cube.type == 'MESH':
    mesh = cube.data
    print(f"    Mesh name: {mesh.name}")
    print(f"    Vertices: {len(mesh.vertices)}")
    print(f"    Edges: {len(mesh.edges)}")
    print(f"    Faces: {len(mesh.polygons)}")

# ============================================
# 7. WORKING WITH COLLECTIONS
# ============================================
print("\n7. WORKING WITH COLLECTIONS")

# Create a new collection
new_collection = bpy.data.collections.new("MyCollection")
bpy.context.scene.collection.children.link(new_collection)
print(f"  Created collection: {new_collection.name}")

# Move object to collection
# First, unlink from current collection
for coll in cube.users_collection:
    coll.objects.unlink(cube)

# Link to new collection
new_collection.objects.link(cube)
print(f"  Moved {cube.name} to {new_collection.name}")

# Create objects directly in a collection
bpy.ops.mesh.primitive_torus_add(location=(6, 0, 0))
torus = bpy.context.active_object
torus.name = "MyTorus"

for coll in torus.users_collection:
    coll.objects.unlink(torus)
new_collection.objects.link(torus)
print(f"  Added {torus.name} to {new_collection.name}")

# List all objects in a collection
print(f"\n  Objects in '{new_collection.name}':")
for obj in new_collection.objects:
    print(f"    - {obj.name}")

# ============================================
# 8. ITERATING THROUGH OBJECTS
# ============================================
print("\n8. ITERATING THROUGH OBJECTS")

# Iterate through all objects in scene
print("  All mesh objects in scene:")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print(f"    {obj.name} at {obj.location}")

# Find objects by type
print("\n  Filtering by type:")
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
print(f"    Found {len(mesh_objects)} mesh objects")

# Find objects by name pattern
print("\n  Finding objects with 'Sphere' in name:")
sphere_objects = [obj for obj in bpy.data.objects if 'Sphere' in obj.name]
for obj in sphere_objects:
    print(f"    - {obj.name}")

# ============================================
# 9. USEFUL UTILITY FUNCTIONS
# ============================================
print("\n9. USEFUL UTILITY FUNCTIONS")

def get_object_info(obj_name):
    """Get detailed information about an object"""
    obj = bpy.data.objects.get(obj_name)
    if obj:
        return {
            'name': obj.name,
            'type': obj.type,
            'location': tuple(obj.location),
            'visible': not obj.hide_viewport,
            'selected': obj.select_get()
        }
    return None

def delete_objects_by_pattern(pattern):
    """Delete all objects containing pattern in their name"""
    to_delete = [obj for obj in bpy.data.objects if pattern in obj.name]
    for obj in to_delete:
        bpy.data.objects.remove(obj, do_unlink=True)
    return len(to_delete)

# Test utility functions
info = get_object_info("MySphere")
if info:
    print(f"  Object info for 'MySphere': {info}")

deleted_count = delete_objects_by_pattern("SphereArray")
print(f"  Deleted {deleted_count} objects matching 'SphereArray'")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 50)
print("BASIC OPERATIONS SUMMARY")
print("=" * 50)
print("Selection: obj.select_set(True/False)")
print("Duplicate: obj.copy() + bpy.context.collection.objects.link()")
print("Delete: bpy.data.objects.remove(obj, do_unlink=True)")
print("Hide: obj.hide_viewport = True/False")
print("Access: bpy.data.objects.get('name') or bpy.context.scene.objects")
print("Collections: Organize objects into groups")
print("\nFinal object count:", len(bpy.context.scene.objects))
