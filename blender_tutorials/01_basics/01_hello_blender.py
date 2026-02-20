"""
Blender Python Tutorial - Lesson 1: Hello Blender
==================================================

This is your first Blender Python script!
Learn how to:
- Import the Blender Python API (bpy)
- Access and understand the context
- Create a simple cube
- Print information about objects

To run this script in Blender:
1. Open Blender
2. Switch to the "Scripting" workspace
3. Click "Open" and select this file (or paste the code)
4. Click "Run Script" or press Alt+P
"""

import bpy

def ensure_object_mode():
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')


# Print a welcome message to the console

print("=" * 50)
print("Welcome to Blender Python Scripting!")
print("=" * 50)

# Clear the default scene (remove default cube, light, camera)
# This ensures we start with a clean slate
ensure_object_mode()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a new cube
# bpy.ops contains operators - actions that modify the Blender scene
bpy.ops.mesh.primitive_cube_add(
    size=2,                    # Size of the cube
    location=(0, 0, 0)         # Position in 3D space (X, Y, Z)
)

# Get a reference to the cube we just created
# The active object is the last object we created/selected
cube = bpy.context.active_object

# Set the cube's name
cube.name = "MyCube"

# Print information about our cube
print(f"\nCreated object: {cube.name}")
print(f"Object type: {cube.type}")
print(f"Location: {cube.location}")
print(f"Dimensions: {cube.dimensions}")

# Access the scene
scene = bpy.context.scene
print(f"\nScene name: {scene.name}")
print(f"Total objects in scene: {len(scene.objects)}")

# List all objects in the scene
print("\nObjects in scene:")
for obj in scene.objects:
    print(f"  - {obj.name} (Type: {obj.type})")

print("\n" + "=" * 50)
print("Script completed successfully!")
print("=" * 50)
