"""
Blender Python Tutorial - Lesson 13: Complete Scene Creation
=============================================================

Putting it all together - create a complete, complex scene:
- Scene composition
- Multiple objects with relationships
- Advanced materials
- Lighting setup
- Camera animation
- Rendering setup
- Compositing basics

This script creates a complete animated scene demonstrating
all the techniques learned in previous lessons.
"""

import bpy
import math
import random
from mathutils import Vector

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("="* 60)
print("CREATING COMPLETE SCENE: 'Floating Crystal Garden'")
print("=" * 60)

# Set random seed for reproducibility
random.seed(42)

# ============================================
# SCENE SETUP
# ============================================
print("\n1. Setting up scene parameters...")

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 240
scene.frame_current = 1

# Render settings
scene.render.engine = 'CYCLES'  # or 'BLENDER_EEVEE'
scene.cycles.samples = 128
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = False

print(f"  ✓ Scene: {scene.frame_start}-{scene.frame_end} frames")
print(f"  ✓ Render: {scene.render.engine}, {scene.cycles.samples} samples")

# ============================================
# WORLD ENVIRONMENT
# ============================================
print("\n2. Setting up world environment...")

world = scene.world
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_links = world.node_tree.links

# Clear default nodes
world_nodes.clear()

# Create sky texture
sky_tex = world_nodes.new(type='ShaderNodeTexSky')
sky_tex.location = (-300, 300)
sky_tex.sky_type = 'HOSEK_WILKIE'
sky_tex.sun_elevation = math.radians(45)
sky_tex.sun_rotation = math.radians(45)

# Background node
bg_node = world_nodes.new(type='ShaderNodeBackground')
bg_node.location = (0, 300)
bg_node.inputs['Strength'].default_value = 0.8

# Output
world_output = world_nodes.new(type='ShaderNodeOutputWorld')
world_output.location = (200, 300)

# Connect
world_links.new(sky_tex.outputs['Color'], bg_node.inputs['Color'])
world_links.new(bg_node.outputs['Background'], world_output.inputs['Surface'])

print(f"  ✓ Sky texture created")

# ============================================
# GROUND/BASE
# ============================================
print("\n3. Creating ground and base...")

# Main ground plane
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"

# Add subdivision for detail
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=50)
bpy.ops.object.mode_set(mode='OBJECT')

# Ground material with texture
ground_mat = bpy.data.materials.new(name="GroundMaterial")
ground_mat.use_nodes = True
ground.data.materials.append(ground_mat)

g_nodes = ground_mat.node_tree.nodes
g_links = ground_mat.node_tree.links
g_bsdf = g_nodes.get("Principled BSDF")

# Noise texture for ground
g_tex_coord = g_nodes.new(type='ShaderNodeTexCoord')
g_tex_coord.location = (-800, 0)

g_noise = g_nodes.new(type='ShaderNodeTexNoise')
g_noise.location = (-600, 0)
g_noise.inputs['Scale'].default_value = 3.0
g_noise.inputs['Detail'].default_value = 5.0

g_ramp = g_nodes.new(type='ShaderNodeValToRGB')
g_ramp.location = (-400, 0)
g_ramp.color_ramp.elements[0].color = (0.05, 0.05, 0.08, 1)  # Dark
g_ramp.color_ramp.elements[1].color = (0.1, 0.15, 0.2, 1)  # Lighter

g_links.new(g_tex_coord.outputs['Object'], g_noise.inputs['Vector'])
g_links.new(g_noise.outputs['Fac'], g_ramp.inputs['Fac'])
g_links.new(g_ramp.outputs['Color'], g_bsdf.inputs['Base Color'])

g_bsdf.inputs['Roughness'].default_value = 0.8
g_bsdf.inputs['Metallic'].default_value = 0.1

# Add displacement
g_displace = ground.modifiers.new(name="Displace", type='DISPLACE')
g_texture = bpy.data.textures.new(name="GroundDisplace", type='CLOUDS')
g_texture.noise_scale = 0.5
g_displace.texture = g_texture
g_displace.strength = 0.3

print(f"  ✓ Ground created with displacement")

# ============================================
# FLOATING CRYSTALS
# ============================================
print("\n4. Creating floating crystals...")

def create_crystal(location, scale, color_hue):
    """Create a crystal object with custom material"""
    # Create crystal (stretched icosphere)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, location=location)
    crystal = bpy.context.active_object
    crystal.name = f"Crystal_{len([o for o in bpy.data.objects if 'Crystal' in o.name])}"

    crystal.scale = (scale * 0.3, scale * 0.3, scale)
    crystal.rotation_euler = (
        math.radians(random.uniform(0, 360)),
        math.radians(random.uniform(0, 360)),
        math.radians(random.uniform(0, 360))
    )

    # Crystal material
    mat = bpy.data.materials.new(name=f"Crystal_Mat_{crystal.name}")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    crystal.data.materials.append(mat)

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    # Glass-like with color
    import colorsys
    rgb = colorsys.hsv_to_rgb(color_hue, 0.7, 1.0)
    bsdf.inputs['Base Color'].default_value = (rgb[0], rgb[1], rgb[2], 1)
    bsdf.inputs['Transmission'].default_value = 0.9
    bsdf.inputs['Roughness'].default_value = 0.1
    bsdf.inputs['IOR'].default_value = 1.45

    # Add emission for glow
    bsdf.inputs['Emission'].default_value = (rgb[0] * 0.5, rgb[1] * 0.5, rgb[2] * 0.5, 1)
    bsdf.inputs['Emission Strength'].default_value = 2.0

    # Animate floating motion
    height_offset = random.uniform(0, math.pi * 2)
    for frame in range(1, 241, 20):
        scene.frame_set(frame)
        time = frame / 240.0
        float_offset = math.sin(time * math.pi * 2 + height_offset) * 0.5
        crystal.location.z = location[2] + float_offset

        # Rotate slowly
        crystal.rotation_euler.z = time * math.pi * 2

        crystal.keyframe_insert(data_path="location", frame=frame)
        crystal.keyframe_insert(data_path="rotation_euler", frame=frame)

    return crystal

# Create crystal formation
crystal_count = 12
for i in range(crystal_count):
    angle = (i / crystal_count) * math.pi * 2
    radius = random.uniform(3, 6)
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    z = random.uniform(2, 5)
    scale = random.uniform(0.8, 1.5)
    hue = i / crystal_count  # Rainbow colors

    create_crystal((x, y, z), scale, hue)

print(f"  ✓ Created {crystal_count} animated crystals")

# ============================================
# CENTRAL STRUCTURE (Platform)
# ============================================
print("\n5. Creating central platform...")

# Central platform
bpy.ops.mesh.primitive_cylinder_add(radius=3, depth=0.5, location=(0, 0, 0.25))
platform = bpy.context.active_object
platform.name = "Platform"

# Platform material (stone-like)
plat_mat = bpy.data.materials.new(name="PlatformMaterial")
plat_mat.use_nodes = True
platform.data.materials.append(plat_mat)

p_nodes = plat_mat.node_tree.nodes
p_links = plat_mat.node_tree.links
p_bsdf = p_nodes.get("Principled BSDF")

# Musgrave texture for stone
p_musgrave = p_nodes.new(type='ShaderNodeTexMusgrave')
p_musgrave.location = (-400, 0)
p_musgrave.inputs['Scale'].default_value = 5.0

p_ramp = p_nodes.new(type='ShaderNodeValToRGB')
p_ramp.location = (-200, 0)
p_ramp.color_ramp.elements[0].color = (0.3, 0.25, 0.2, 1)
p_ramp.color_ramp.elements[1].color = (0.5, 0.45, 0.4, 1)

p_links.new(p_musgrave.outputs['Fac'], p_ramp.inputs['Fac'])
p_links.new(p_ramp.outputs['Color'], p_bsdf.inputs['Base Color'])

p_bsdf.inputs['Roughness'].default_value = 0.9

# Bump mapping
p_bump = p_nodes.new(type='ShaderNodeBump')
p_bump.location = (-200, -200)
p_links.new(p_musgrave.outputs['Fac'], p_bump.inputs['Height'])
p_links.new(p_bump.outputs['Normal'], p_bsdf.inputs['Normal'])

print(f"  ✓ Platform created with stone texture")

# ============================================
# PARTICLE EFFECTS (Magical dust)
# ============================================
print("\n6. Adding particle effects...")

# Particle emitter
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 0.5))
emitter = bpy.context.active_object
emitter.name = "ParticleEmitter"
emitter.hide_viewport = True
emitter.hide_render = True

# Add particle system
bpy.ops.object.modifier_add(type='PARTICLE_SYSTEM')
particle_sys = emitter.particle_systems[0]
p_settings = particle_sys.settings

p_settings.count = 1000
p_settings.frame_start = 1
p_settings.frame_end = 10
p_settings.lifetime = 240
p_settings.lifetime_random = 0.5

p_settings.emit_from = 'FACE'
p_settings.normal_factor = 0.5
p_settings.factor_random = 1.0

p_settings.physics_type = 'NEWTON'
p_settings.mass = 0.1
p_settings.particle_size = 0.02
p_settings.size_random = 0.5

# Reduce gravity for floating effect
p_settings.effector_weights.gravity = 0.1

print(f"  ✓ Particle system created ({p_settings.count} particles)")

# ============================================
# LIGHTING
# ============================================
print("\n7. Setting up three-point lighting...")

# Key light (main)
bpy.ops.object.light_add(type='AREA', location=(8, -6, 10))
key_light = bpy.context.active_object
key_light.name = "KeyLight"
key_light.rotation_euler = (math.radians(45), 0, math.radians(45))
key_light.data.energy = 500
key_light.data.size = 5
key_light.data.color = (1, 0.95, 0.9)  # Warm

# Fill light (soften shadows)
bpy.ops.object.light_add(type='AREA', location=(-6, -4, 6))
fill_light = bpy.context.active_object
fill_light.name = "FillLight"
fill_light.rotation_euler = (math.radians(60), 0, math.radians(-30))
fill_light.data.energy = 200
fill_light.data.size = 4
fill_light.data.color = (0.9, 0.95, 1)  # Cool

# Rim light (separation)
bpy.ops.object.light_add(type='SPOT', location=(0, 10, 8))
rim_light = bpy.context.active_object
rim_light.name = "RimLight"
rim_light.rotation_euler = (math.radians(45), 0, math.radians(180))
rim_light.data.energy = 300
rim_light.data.spot_size = math.radians(60)
rim_light.data.color = (0.9, 0.7, 1)  # Purple

# Accent light (for crystals)
bpy.ops.object.light_add(type='POINT', location=(0, 0, 8))
accent_light = bpy.context.active_object
accent_light.name = "AccentLight"
accent_light.data.energy = 100
accent_light.data.color = (0.5, 0.8, 1)  # Blue

print(f"  ✓ Lighting setup complete")

# ============================================
# CAMERA SETUP AND ANIMATION
# ============================================
print("\n8. Setting up animated camera...")

bpy.ops.object.camera_add(location=(12, -12, 6))
camera = bpy.context.active_object
camera.name = "MainCamera"
scene.camera = camera

# Camera settings
camera.data.lens = 35  # Wide angle
camera.data.dof.use_dof = True
camera.data.dof.focus_distance = 10
camera.data.dof.aperture_fstop = 2.8

# Animate camera around the scene
for frame in [1, 60, 120, 180, 240]:
    scene.frame_set(frame)
    progress = (frame - 1) / 239
    angle = progress * math.pi * 2  # Full circle

    radius = 12
    height = 6 + math.sin(progress * math.pi) * 2  # Vary height

    camera.location.x = radius * math.cos(angle)
    camera.location.y = radius * math.sin(angle)
    camera.location.z = height

    # Look at center
    direction = Vector((0, 0, 2)) - camera.location
    camera.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    camera.keyframe_insert(data_path="location", frame=frame)
    camera.keyframe_insert(data_path="rotation_euler", frame=frame)

print(f"  ✓ Camera animated (circular orbit)")

# ============================================
# DECORATIVE ELEMENTS
# ============================================
print("\n9. Adding decorative elements...")

# Add some floating rings
for i in range(3):
    height = 1 + i * 1.5
    bpy.ops.mesh.primitive_torus_add(
        major_radius=4 + i,
        minor_radius=0.05,
        location=(0, 0, height)
    )
    ring = bpy.context.active_object
    ring.name = f"Ring_{i}"

    # Ring material (glowing)
    ring_mat = bpy.data.materials.new(name=f"Ring_Mat_{i}")
    ring_mat.use_nodes = True
    ring.data.materials.append(ring_mat)

    r_bsdf = ring_mat.node_tree.nodes.get("Principled BSDF")
    r_bsdf.inputs['Emission'].default_value = (0.5, 0.7, 1, 1)
    r_bsdf.inputs['Emission Strength'].default_value = 2.0

    # Animate rotation
    scene.frame_set(1)
    ring.rotation_euler.z = 0
    ring.keyframe_insert(data_path="rotation_euler", frame=1)

    scene.frame_set(240)
    ring.rotation_euler.z = math.radians(360) * (i + 1)
    ring.keyframe_insert(data_path="rotation_euler", frame=240)

print(f"  ✓ Decorative rings added")

# ============================================
# COMPOSITING SETUP
# ============================================
print("\n10. Setting up compositing...")

scene.use_nodes = True
comp_nodes = scene.node_tree.nodes
comp_links = scene.node_tree.links

# Clear default nodes
comp_nodes.clear()

# Render layers
render_layers = comp_nodes.new(type='CompositorNodeRLayers')
render_layers.location = (0, 0)

# Glare (glow effect)
glare = comp_nodes.new(type='CompositorNodeGlare')
glare.location = (200, 100)
glare.glare_type = 'FOG_GLOW'
glare.quality = 'HIGH'
glare.threshold = 0.8

# Color correction
color_correct = comp_nodes.new(type='CompositorNodeColorCorrection')
color_correct.location = (400, 0)
color_correct.master_saturation = 1.2
color_correct.master_gain = 1.1

# Composite output
composite = comp_nodes.new(type='CompositorNodeComposite')
composite.location = (600, 0)

# Connect
comp_links.new(render_layers.outputs['Image'], glare.inputs['Image'])
comp_links.new(glare.outputs['Image'], color_correct.inputs['Image'])
comp_links.new(color_correct.outputs['Image'], composite.inputs['Image'])

print(f"  ✓ Compositing nodes set up")

# ============================================
# FINAL TOUCHES
# ============================================
print("\n11. Final scene adjustments...")

# Set all animations to ease in/out
for obj in bpy.data.objects:
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'BEZIER'
                keyframe.easing = 'EASE_IN_OUT'

print(f"  ✓ Animation curves smoothed")

# Reset to frame 1
scene.frame_set(1)

# ============================================
# SCENE STATISTICS
# ============================================
print("\n" + "=" * 60)
print("SCENE CREATION COMPLETE!")
print("=" * 60)
print(f"\nScene Statistics:")
print(f"  Objects: {len(bpy.data.objects)}")
print(f"  Materials: {len(bpy.data.materials)}")
print(f"  Lights: {len([o for o in bpy.data.objects if o.type == 'LIGHT'])}")
print(f"  Cameras: {len([o for o in bpy.data.objects if o.type == 'CAMERA'])}")

animated_objects = [o for o in bpy.data.objects if o.animation_data and o.animation_data.action]
print(f"  Animated objects: {len(animated_objects)}")

print(f"\nRender Settings:")
print(f"  Engine: {scene.render.engine}")
print(f"  Resolution: {scene.render.resolution_x}x{scene.render.resolution_y}")
print(f"  Samples: {scene.cycles.samples}")
print(f"  Frame range: {scene.frame_start}-{scene.frame_end}")

print(f"\nScene Features:")
print(f"  ✓ Procedural textures and materials")
print(f"  ✓ Three-point lighting setup")
print(f"  ✓ Animated camera orbit")
print(f"  ✓ Floating crystal animations")
print(f"  ✓ Particle system (magical dust)")
print(f"  ✓ Depth of field")
print(f"  ✓ Compositing (glare, color correction)")
print(f"  ✓ World environment (sky)")

print(f"\n" + "=" * 60)
print("To render:")
print("  - Press F12 for single frame")
print("  - Ctrl+F12 for animation")
print("  - Press SPACEBAR to preview animation")
print("=" * 60)

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 60)
print("COMPLETE SCENE TUTORIAL SUMMARY")
print("=" * 60)
print("This script demonstrated:")
print("  1. Scene setup and configuration")
print("  2. World environment with sky texture")
print("  3. Procedural ground with displacement")
print("  4. Custom objects with complex materials")
print("  5. Animation of multiple objects")
print("  6. Particle systems for effects")
print("  7. Professional lighting setup")
print("  8. Camera animation and depth of field")
print("  9. Decorative elements")
print("  10. Compositing for post-processing")
print("\nTechniques used:")
print("  - Node-based materials")
print("  - Keyframe animation")
print("  - Procedural textures")
print("  - Physics/particles")
print("  - Render settings")
print("  - Scene composition")
print("\nThis scene combines ALL previous lessons!")
print("=" * 60)
