"""
Blender Python Tutorial - Lesson 5: Materials Basics
=====================================================

Learn how to create and apply materials:
- Creating basic materials
- Setting material properties (color, metallic, roughness)
- Applying materials to objects
- Working with multiple materials
- Material slots
- Viewport shading modes
"""

import bpy

# Clear the scene

ensure_object_mode()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("Demonstrating materials...\n")

# ============================================
# 1. CREATING A BASIC MATERIAL
# ============================================
print("1. CREATING A BASIC MATERIAL")

# Create a cube
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "RedCube"

# Create a new material
red_material = bpy.data.materials.new(name="RedMaterial")

# Enable 'Use nodes' for the material (required for modern Blender materials)
red_material.use_nodes = True

# Get the Principled BSDF node (default shader)
# This is the main shader node in Blender
bsdf = red_material.node_tree.nodes.get("Principled BSDF")

# Set the base color to red (RGBA)
bsdf.inputs['Base Color'].default_value = (1, 0, 0, 1)  # Red

# Assign material to object
if cube.data.materials:
    # Replace existing material
    cube.data.materials[0] = red_material
else:
    # Add new material
    cube.data.materials.append(red_material)

print(f"  Created and assigned '{red_material.name}' to {cube.name}")

# ============================================
# 2. MATERIAL PROPERTIES
# ============================================
print("\n2. MATERIAL PROPERTIES")

# Create a sphere with metallic material
bpy.ops.mesh.primitive_uv_sphere_add(location=(3, 0, 0))
sphere = bpy.context.active_object
sphere.name = "MetallicSphere"

# Create metallic material
metal_material = bpy.data.materials.new(name="MetallicMaterial")
metal_material.use_nodes = True
bsdf = metal_material.node_tree.nodes.get("Principled BSDF")

# Set material properties
bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.9, 1)  # Light blue
bsdf.inputs['Metallic'].default_value = 1.0  # Fully metallic
bsdf.inputs['Roughness'].default_value = 0.2  # Shiny

sphere.data.materials.append(metal_material)
print(f"  Created metallic material for {sphere.name}")
print(f"    Metallic: {bsdf.inputs['Metallic'].default_value}")
print(f"    Roughness: {bsdf.inputs['Roughness'].default_value}")

# ============================================
# 3. DIFFERENT MATERIAL TYPES
# ============================================
print("\n3. DIFFERENT MATERIAL TYPES")

materials_data = [
    ("Glossy Plastic", (0, 1, 0, 1), 0.0, 0.3, (-3, 0, 0)),
    ("Rough Metal", (0.6, 0.6, 0.6, 1), 1.0, 0.7, (0, 3, 0)),
    ("Glass-like", (0.8, 0.9, 1, 1), 0.0, 0.1, (0, -3, 0)),
    ("Matte", (1, 0.5, 0, 1), 0.0, 1.0, (3, 3, 0)),
]

for mat_name, color, metallic, roughness, location in materials_data:
    # Create object
    bpy.ops.mesh.primitive_sphere_add(location=location, radius=0.8)
    obj = bpy.context.active_object
    obj.name = f"Sphere_{mat_name.replace(' ', '_')}"

    # Create material
    material = bpy.data.materials.new(name=mat_name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")

    # Set properties
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness

    # Assign to object
    obj.data.materials.append(material)

    print(f"  Created: {mat_name} at {location}")

# ============================================
# 4. EMISSION MATERIALS (Glowing)
# ============================================
print("\n4. EMISSION MATERIAL (Glowing)")

bpy.ops.mesh.primitive_sphere_add(location=(-3, -3, 0), radius=0.5)
glow_sphere = bpy.context.active_object
glow_sphere.name = "GlowingSphere"

# Create emission material
glow_material = bpy.data.materials.new(name="EmissionMaterial")
glow_material.use_nodes = True
bsdf = glow_material.node_tree.nodes.get("Principled BSDF")

# Set emission
bsdf.inputs['Base Color'].default_value = (1, 1, 0, 1)  # Yellow
bsdf.inputs['Emission Color'].default_value = (1, 1, 0, 1)  # Yellow glow
bsdf.inputs['Emission Strength'].default_value = 5.0  # Glow intensity

glow_sphere.data.materials.append(glow_material)
print(f"  Created glowing material with emission strength: 5.0")

# ============================================
# 5. TRANSPARENCY
# ============================================
print("\n5. TRANSPARENT MATERIAL")

bpy.ops.mesh.primitive_cylinder_add(location=(3, -3, 0))
transparent_obj = bpy.context.active_object
transparent_obj.name = "TransparentCylinder"

# Create transparent material
trans_material = bpy.data.materials.new(name="TransparentMaterial")
trans_material.use_nodes = True
bsdf = trans_material.node_tree.nodes.get("Principled BSDF")

# Set transparency
bsdf.inputs['Base Color'].default_value = (0, 0.5, 1, 1)  # Blue
bsdf.inputs['Alpha'].default_value = 0.5  # 50% transparent
bsdf.inputs['Transmission'].default_value = 0.8  # Glass-like transmission

# Enable transparency in material settings
trans_material.blend_method = 'BLEND'  # Or 'OPAQUE', 'CLIP', 'HASHED'

transparent_obj.data.materials.append(trans_material)
print(f"  Created transparent material with alpha: 0.5")

# ============================================
# 6. MULTIPLE MATERIALS ON ONE OBJECT
# ============================================
print("\n6. MULTIPLE MATERIALS ON ONE OBJECT")

bpy.ops.mesh.primitive_cube_add(location=(-3, 3, 0))
multi_mat_cube = bpy.context.active_object
multi_mat_cube.name = "MultiMaterialCube"

# Create two materials
mat1 = bpy.data.materials.new(name="Material_1")
mat1.use_nodes = True
mat1.node_tree.nodes.get("Principled BSDF").inputs['Base Color'].default_value = (1, 0, 1, 1)

mat2 = bpy.data.materials.new(name="Material_2")
mat2.use_nodes = True
mat2.node_tree.nodes.get("Principled BSDF").inputs['Base Color'].default_value = (0, 1, 1, 1)

# Add both materials to the cube
multi_mat_cube.data.materials.append(mat1)
multi_mat_cube.data.materials.append(mat2)

# Assign different materials to different faces (requires edit mode operations)
# This is more advanced - just showing the concept
print(f"  Added {len(multi_mat_cube.data.materials)} materials to {multi_mat_cube.name}")

# ============================================
# 7. ACCESSING AND MODIFYING EXISTING MATERIALS
# ============================================
print("\n7. ACCESSING AND MODIFYING MATERIALS")

# Get material by name
red_mat = bpy.data.materials.get("RedMaterial")
if red_mat:
    bsdf = red_mat.node_tree.nodes.get("Principled BSDF")
    # Modify the material
    bsdf.inputs['Roughness'].default_value = 0.5
    print(f"  Modified '{red_mat.name}' roughness to 0.5")

# List all materials in the project
print("\n  All materials in project:")
for mat in bpy.data.materials:
    print(f"    - {mat.name}")

# ============================================
# 8. ADDING LIGHTS FOR BETTER VISIBILITY
# ============================================
print("\n8. ADDING LIGHTS TO SEE MATERIALS")

# Add a sun light
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun = bpy.context.active_object
sun.name = "Sun"
sun.data.energy = 3.0
print(f"  Added {sun.name} for lighting")

# Add a camera to view the scene
bpy.ops.object.camera_add(location=(10, -10, 8))
camera = bpy.context.active_object
camera.name = "Camera"

# Point camera at origin
import math

def ensure_object_mode():
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

camera.rotation_euler = (math.radians(60), 0, math.radians(45))

# Set as active camera
bpy.context.scene.camera = camera
print(f"  Added {camera.name}")

# ============================================
# 9. HELPER FUNCTIONS
# ============================================
print("\n9. HELPER FUNCTIONS")

def create_simple_material(name, color, metallic=0.0, roughness=0.5):
    """Helper function to create a simple material"""
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    return material

# Use the helper function
test_material = create_simple_material("TestMaterial", (1, 0.5, 0.5, 1), roughness=0.3)
print(f"  Created material using helper: {test_material.name}")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 50)
print("MATERIALS SUMMARY")
print("=" * 50)
print("Create: mat = bpy.data.materials.new('name')")
print("Enable nodes: mat.use_nodes = True")
print("Get shader: bsdf = mat.node_tree.nodes.get('Principled BSDF')")
print("Set color: bsdf.inputs['Base Color'].default_value = (R,G,B,A)")
print("Assign: obj.data.materials.append(mat)")
print("\nKey properties:")
print("  - Base Color: The main color")
print("  - Metallic: 0 (plastic) to 1 (metal)")
print("  - Roughness: 0 (mirror) to 1 (matte)")
print("  - Emission: Make objects glow")
print("  - Transmission: Glass/transparent effects")
print("\nTo see materials: Use Viewport Shading (Z key in Blender)")
print("  - Material Preview: Quick preview")
print("  - Rendered: Full quality preview")
