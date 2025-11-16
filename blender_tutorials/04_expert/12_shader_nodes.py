"""
Blender Python Tutorial - Lesson 12: Shader Nodes
==================================================

Learn how to work with shader nodes programmatically:
- Understanding the node tree
- Creating and connecting nodes
- Common shader nodes (Principled BSDF, Mix, etc.)
- Texture nodes
- Color ramps and mapping
- Procedural textures
- Complex material setups
- Node groups
"""

import bpy
import math

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("Demonstrating shader nodes...\n")

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(10, -10, 15))
sun = bpy.context.active_object
sun.data.energy = 3.0

# Add camera
bpy.ops.object.camera_add(location=(12, -12, 8))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))
bpy.context.scene.camera = camera

# ============================================
# 1. BASIC NODE SETUP
# ============================================
print("1. BASIC NODE SETUP - Understanding the node tree")

bpy.ops.mesh.primitive_sphere_add(location=(0, 0, 1))
sphere1 = bpy.context.active_object
sphere1.name = "BasicNodeSphere"

# Create material
mat = bpy.data.materials.new(name="BasicNodeMaterial")
mat.use_nodes = True
sphere1.data.materials.append(mat)

# Get the node tree
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes
nodes.clear()

# Create nodes manually
output_node = nodes.new(type='ShaderNodeOutputMaterial')
output_node.location = (300, 0)

bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf_node.location = (0, 0)

# Connect nodes
links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

# Set properties
bsdf_node.inputs['Base Color'].default_value = (1, 0, 0, 1)  # Red

print(f"  Created basic node setup")
print(f"  Nodes: {len(nodes)}")
print(f"  Links: {len(links)}")

# ============================================
# 2. ADDING TEXTURE NODES
# ============================================
print("\n2. TEXTURE NODES - Adding patterns")

bpy.ops.mesh.primitive_sphere_add(location=(3, 0, 1))
sphere2 = bpy.context.active_object
sphere2.name = "TextureSphere"

mat2 = bpy.data.materials.new(name="TextureMaterial")
mat2.use_nodes = True
sphere2.data.materials.append(mat2)

nodes2 = mat2.node_tree.nodes
links2 = mat2.node_tree.links

# Get default nodes
bsdf = nodes2.get("Principled BSDF")
output = nodes2.get("Material Output")

# Add texture coordinate node (provides UV, position, etc.)
tex_coord = nodes2.new(type='ShaderNodeTexCoord')
tex_coord.location = (-600, 0)

# Add noise texture
noise_tex = nodes2.new(type='ShaderNodeTexNoise')
noise_tex.location = (-400, 0)
noise_tex.inputs['Scale'].default_value = 5.0
noise_tex.inputs['Detail'].default_value = 2.0

# Add color ramp to control colors
color_ramp = nodes2.new(type='ShaderNodeValToRGB')
color_ramp.location = (-200, 0)

# Configure color ramp
color_ramp.color_ramp.elements[0].color = (0, 0, 1, 1)  # Blue
color_ramp.color_ramp.elements[1].color = (1, 1, 0, 1)  # Yellow

# Connect nodes
links2.new(tex_coord.outputs['Object'], noise_tex.inputs['Vector'])
links2.new(noise_tex.outputs['Fac'], color_ramp.inputs['Fac'])
links2.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])

print(f"  Added noise texture with color ramp")

# ============================================
# 3. PROCEDURAL TEXTURES
# ============================================
print("\n3. PROCEDURAL TEXTURES - Various types")

procedural_textures = [
    ('ShaderNodeTexChecker', 'Checker', (-3, 3)),
    ('ShaderNodeTexBrick', 'Brick', (0, 3)),
    ('ShaderNodeTexWave', 'Wave', (3, 3)),
    ('ShaderNodeTexVoronoi', 'Voronoi', (6, 3)),
    ('ShaderNodeTexMagic', 'Magic', (-3, 6)),
    ('ShaderNodeTexMusgrave', 'Musgrave', (0, 6)),
]

for node_type, name, location in procedural_textures:
    # Create sphere
    bpy.ops.mesh.primitive_sphere_add(location=(location[0], location[1], 1))
    sphere = bpy.context.active_object
    sphere.name = f"{name}Sphere"

    # Create material
    mat = bpy.data.materials.new(name=f"{name}Material")
    mat.use_nodes = True
    sphere.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    bsdf = nodes.get("Principled BSDF")

    # Add texture node
    tex_node = nodes.new(type=node_type)
    tex_node.location = (-300, 0)

    # Connect to BSDF
    if 'Color' in tex_node.outputs:
        links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
    elif 'Fac' in tex_node.outputs:
        links.new(tex_node.outputs['Fac'], bsdf.inputs['Base Color'])

    print(f"  Created {name} texture")

# ============================================
# 4. MIX SHADERS
# ============================================
print("\n4. MIX SHADERS - Combining materials")

bpy.ops.mesh.primitive_sphere_add(location=(6, 0, 1))
mix_sphere = bpy.context.active_object
mix_sphere.name = "MixShaderSphere"

mat_mix = bpy.data.materials.new(name="MixMaterial")
mat_mix.use_nodes = True
mix_sphere.data.materials.append(mat_mix)

nodes_mix = mat_mix.node_tree.nodes
links_mix = mat_mix.node_tree.links

nodes_mix.clear()

# Create output
output = nodes_mix.new(type='ShaderNodeOutputMaterial')
output.location = (600, 0)

# Create two different shaders
diffuse_red = nodes_mix.new(type='ShaderNodeBsdfDiffuse')
diffuse_red.location = (0, 100)
diffuse_red.inputs['Color'].default_value = (1, 0, 0, 1)

glossy_blue = nodes_mix.new(type='ShaderNodeBsdfGlossy')
glossy_blue.location = (0, -100)
glossy_blue.inputs['Color'].default_value = (0, 0, 1, 1)

# Mix shader node
mix_shader = nodes_mix.new(type='ShaderNodeMixShader')
mix_shader.location = (300, 0)
mix_shader.inputs['Fac'].default_value = 0.5  # 50/50 mix

# Connect nodes
links_mix.new(diffuse_red.outputs['BSDF'], mix_shader.inputs[1])
links_mix.new(glossy_blue.outputs['BSDF'], mix_shader.inputs[2])
links_mix.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

print(f"  Created mixed shader (diffuse + glossy)")

# ============================================
# 5. IMAGE TEXTURES
# ============================================
print("\n5. IMAGE TEXTURES - Using external images")

# Note: This requires an actual image file
# For demonstration, we'll create a UV test pattern procedurally

bpy.ops.mesh.primitive_sphere_add(location=(-3, 0, 1))
uv_sphere = bpy.context.active_object
uv_sphere.name = "UVSphere"

mat_uv = bpy.data.materials.new(name="UVMaterial")
mat_uv.use_nodes = True
uv_sphere.data.materials.append(mat_uv)

nodes_uv = mat_uv.node_tree.nodes
links_uv = mat_uv.node_tree.links

bsdf_uv = nodes_uv.get("Principled BSDF")

# UV Test pattern (checker texture as substitute)
checker = nodes_uv.new(type='ShaderNodeTexChecker')
checker.location = (-300, 0)
checker.inputs['Scale'].default_value = 8

links_uv.new(checker.outputs['Color'], bsdf_uv.inputs['Base Color'])

# If you had an image:
# image_tex = nodes_uv.new(type='ShaderNodeTexImage')
# image_tex.image = bpy.data.images.load("/path/to/image.png")
# links_uv.new(image_tex.outputs['Color'], bsdf_uv.inputs['Base Color'])

print(f"  Created UV texture mapping")

# ============================================
# 6. BUMP AND NORMAL MAPS
# ============================================
print("\n6. BUMP AND NORMAL MAPS - Surface detail")

bpy.ops.mesh.primitive_sphere_add(location=(0, -3, 1))
bump_sphere = bpy.context.active_object
bump_sphere.name = "BumpSphere"

mat_bump = bpy.data.materials.new(name="BumpMaterial")
mat_bump.use_nodes = True
bump_sphere.data.materials.append(mat_bump)

nodes_bump = mat_bump.node_tree.nodes
links_bump = mat_bump.node_tree.links

bsdf_bump = nodes_bump.get("Principled BSDF")

# Create noise texture for bump
noise = nodes_bump.new(type='ShaderNodeTexNoise')
noise.location = (-600, -200)
noise.inputs['Scale'].default_value = 10.0

# Bump node
bump = nodes_bump.new(type='ShaderNodeBump')
bump.location = (-300, -200)
bump.inputs['Strength'].default_value = 1.0

# Connect
links_bump.new(noise.outputs['Fac'], bump.inputs['Height'])
links_bump.new(bump.outputs['Normal'], bsdf_bump.inputs['Normal'])

print(f"  Created bump map from noise texture")

# ============================================
# 7. DISPLACEMENT
# ============================================
print("\n7. DISPLACEMENT - Actual geometry modification")

bpy.ops.mesh.primitive_sphere_add(subdivisions=5, location=(3, -3, 1))
displace_sphere = bpy.context.active_object
displace_sphere.name = "DisplaceSphere"

mat_displace = bpy.data.materials.new(name="DisplaceMaterial")
mat_displace.use_nodes = True
displace_sphere.data.materials.append(mat_displace)

nodes_displace = mat_displace.node_tree.nodes
links_displace = mat_displace.node_tree.links

output_disp = nodes_displace.get("Material Output")

# Noise texture for displacement
noise_disp = nodes_displace.new(type='ShaderNodeTexNoise')
noise_disp.location = (-600, -400)
noise_disp.inputs['Scale'].default_value = 5.0

# Displacement node
displacement = nodes_displace.new(type='ShaderNodeDisplacement')
displacement.location = (-200, -400)
displacement.inputs['Scale'].default_value = 0.3

# Connect
links_displace.new(noise_disp.outputs['Fac'], displacement.inputs['Height'])
links_displace.new(displacement.outputs['Displacement'], output_disp.inputs['Displacement'])

# Enable displacement in material settings
mat_displace.cycles.displacement_method = 'BOTH'  # or 'DISPLACEMENT', 'BUMP'

print(f"  Created displacement from noise")

# ============================================
# 8. COLOR MIX NODES
# ============================================
print("\n8. COLOR MIX - Blending colors")

bpy.ops.mesh.primitive_sphere_add(location=(6, -3, 1))
color_sphere = bpy.context.active_object
color_sphere.name = "ColorMixSphere"

mat_color = bpy.data.materials.new(name="ColorMixMaterial")
mat_color.use_nodes = True
color_sphere.data.materials.append(mat_color)

nodes_color = mat_color.node_tree.nodes
links_color = mat_color.node_tree.links

bsdf_color = nodes_color.get("Principled BSDF")

# Create two textures to mix
noise1 = nodes_color.new(type='ShaderNodeTexNoise')
noise1.location = (-600, 0)
noise1.inputs['Scale'].default_value = 5.0

noise2 = nodes_color.new(type='ShaderNodeTexNoise')
noise2.location = (-600, -200)
noise2.inputs['Scale'].default_value = 10.0

# Color ramps for each
ramp1 = nodes_color.new(type='ShaderNodeValToRGB')
ramp1.location = (-400, 0)
ramp1.color_ramp.elements[0].color = (1, 0, 0, 1)  # Red
ramp1.color_ramp.elements[1].color = (1, 1, 0, 1)  # Yellow

ramp2 = nodes_color.new(type='ShaderNodeValToRGB')
ramp2.location = (-400, -200)
ramp2.color_ramp.elements[0].color = (0, 0, 1, 1)  # Blue
ramp2.color_ramp.elements[1].color = (0, 1, 1, 1)  # Cyan

# Mix RGB node
mix_rgb = nodes_color.new(type='ShaderNodeMixRGB')
mix_rgb.location = (-200, 0)
mix_rgb.blend_type = 'MIX'  # 'MIX', 'ADD', 'MULTIPLY', 'OVERLAY', etc.
mix_rgb.inputs['Fac'].default_value = 0.5

# Connect
links_color.new(noise1.outputs['Fac'], ramp1.inputs['Fac'])
links_color.new(noise2.outputs['Fac'], ramp2.inputs['Fac'])
links_color.new(ramp1.outputs['Color'], mix_rgb.inputs['Color1'])
links_color.new(ramp2.outputs['Color'], mix_rgb.inputs['Color2'])
links_color.new(mix_rgb.outputs['Color'], bsdf_color.inputs['Base Color'])

print(f"  Created color mix setup")

# ============================================
# 9. EMISSION AND TRANSPARENCY
# ============================================
print("\n9. EMISSION AND TRANSPARENCY")

# Emission (glowing)
bpy.ops.mesh.primitive_sphere_add(location=(-3, -3, 1))
emit_sphere = bpy.context.active_object
emit_sphere.name = "EmissionSphere"

mat_emit = bpy.data.materials.new(name="EmissionMaterial")
mat_emit.use_nodes = True
emit_sphere.data.materials.append(mat_emit)

nodes_emit = mat_emit.node_tree.nodes
bsdf_emit = nodes_emit.get("Principled BSDF")

bsdf_emit.inputs['Emission'].default_value = (1, 0.5, 0, 1)  # Orange
bsdf_emit.inputs['Emission Strength'].default_value = 5.0

print(f"  Created emission material")

# Transparent
bpy.ops.mesh.primitive_sphere_add(location=(-6, 0, 1))
trans_sphere = bpy.context.active_object
trans_sphere.name = "TransparentSphere"

mat_trans = bpy.data.materials.new(name="TransparentMaterial")
mat_trans.use_nodes = True
mat_trans.blend_method = 'BLEND'
trans_sphere.data.materials.append(mat_trans)

nodes_trans = mat_trans.node_tree.nodes
bsdf_trans = nodes_trans.get("Principled BSDF")

bsdf_trans.inputs['Transmission'].default_value = 1.0  # Glass-like
bsdf_trans.inputs['Roughness'].default_value = 0.0  # Clear
bsdf_trans.inputs['IOR'].default_value = 1.45  # Index of refraction (glass)

print(f"  Created transparent/glass material")

# ============================================
# 10. NODE GROUPS (Reusable node setups)
# ============================================
print("\n10. NODE GROUPS - Reusable shader setups")

def create_stripe_pattern_group():
    """Create a reusable stripe pattern node group"""
    # Create new node group
    node_group = bpy.data.node_groups.new(name="StripePattern", type='ShaderNodeTree')

    # Create group inputs and outputs
    group_inputs = node_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-400, 0)
    node_group.inputs.new('NodeSocketFloat', 'Scale')
    node_group.inputs.new('NodeSocketColor', 'Color1')
    node_group.inputs.new('NodeSocketColor', 'Color2')

    group_outputs = node_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (400, 0)
    node_group.outputs.new('NodeSocketColor', 'Color')

    # Create internal nodes
    tex_coord = node_group.nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-600, 0)

    separate_xyz = node_group.nodes.new('ShaderNodeSeparateXYZ')
    separate_xyz.location = (-400, -100)

    math_node = node_group.nodes.new('ShaderNodeMath')
    math_node.operation = 'SINE'
    math_node.location = (-200, -100)

    color_ramp = node_group.nodes.new('ShaderNodeValToRGB')
    color_ramp.location = (0, -100)

    mix_rgb = node_group.nodes.new('ShaderNodeMixRGB')
    mix_rgb.location = (200, 0)

    # Connect internal nodes
    node_group.links.new(tex_coord.outputs['Object'], separate_xyz.inputs['Vector'])
    node_group.links.new(separate_xyz.outputs['X'], math_node.inputs[0])
    node_group.links.new(math_node.outputs[0], color_ramp.inputs['Fac'])
    node_group.links.new(color_ramp.outputs['Color'], mix_rgb.inputs['Fac'])
    node_group.links.new(group_inputs.outputs['Color1'], mix_rgb.inputs['Color1'])
    node_group.links.new(group_inputs.outputs['Color2'], mix_rgb.inputs['Color2'])
    node_group.links.new(mix_rgb.outputs['Color'], group_outputs.inputs['Color'])

    return node_group

# Create the node group
stripe_group = create_stripe_pattern_group()

# Use the node group
bpy.ops.mesh.primitive_sphere_add(location=(0, -6, 1))
group_sphere = bpy.context.active_object
group_sphere.name = "NodeGroupSphere"

mat_group = bpy.data.materials.new(name="NodeGroupMaterial")
mat_group.use_nodes = True
group_sphere.data.materials.append(mat_group)

nodes_group = mat_group.node_tree.nodes
links_group = mat_group.node_tree.links

bsdf_group = nodes_group.get("Principled BSDF")

# Add the node group
group_node = nodes_group.new(type='ShaderNodeGroup')
group_node.node_tree = stripe_group
group_node.location = (-300, 0)

# Set input values
group_node.inputs['Scale'].default_value = 10.0
group_node.inputs['Color1'].default_value = (1, 0, 0, 1)  # Red
group_node.inputs['Color2'].default_value = (1, 1, 1, 1)  # White

# Connect to BSDF
links_group.new(group_node.outputs['Color'], bsdf_group.inputs['Base Color'])

print(f"  Created and used node group")

# ============================================
# 11. HELPER FUNCTIONS
# ============================================
print("\n11. SHADER NODE HELPER FUNCTIONS")

def create_simple_material(name, color, metallic=0.0, roughness=0.5):
    """Create a simple Principled BSDF material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness

    return mat

def add_texture_to_material(material, texture_type='NOISE', scale=5.0):
    """Add a procedural texture to a material"""
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    bsdf = nodes.get("Principled BSDF")

    # Create texture node
    tex_node = nodes.new(type=f'ShaderNodeTex{texture_type.capitalize()}')
    tex_node.location = (-300, 0)

    if 'Scale' in tex_node.inputs:
        tex_node.inputs['Scale'].default_value = scale

    # Connect to BSDF
    if 'Color' in tex_node.outputs:
        links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])

    return tex_node

# Test helper functions
test_mat = create_simple_material("TestMaterial", (0.5, 0.5, 1, 1), metallic=0.8)
add_texture_to_material(test_mat, 'VORONOI', scale=10)

print(f"  Created helper functions")

# Add ground plane
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 50)
print("SHADER NODES SUMMARY")
print("=" * 50)
print("Node Tree Access:")
print("  nodes = material.node_tree.nodes")
print("  links = material.node_tree.links")
print("\nCreate Node:")
print("  node = nodes.new(type='ShaderNodeXXX')")
print("\nConnect Nodes:")
print("  links.new(node1.outputs['Out'], node2.inputs['In'])")
print("\nCommon Shader Nodes:")
print("  ShaderNodeBsdfPrincipled - Main shader")
print("  ShaderNodeTexNoise - Noise texture")
print("  ShaderNodeTexImage - Image texture")
print("  ShaderNodeBump - Bump mapping")
print("  ShaderNodeMixShader - Mix shaders")
print("  ShaderNodeMixRGB - Mix colors")
print("  ShaderNodeValToRGB - Color ramp")
print("\nTexture Nodes:")
print("  Noise, Wave, Voronoi, Magic, Musgrave")
print("  Checker, Brick, Gradient")
print("\nTips:")
print("  - Use Texture Coordinate for UV/position")
print("  - Color Ramp for controlling colors")
print("  - Node Groups for reusable setups")
print("  - Principled BSDF covers most needs")
print("\nView in Blender:")
print("  - Switch to Shading workspace")
print("  - Use Material Preview or Rendered view")
