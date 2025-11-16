"""
Blender Python Tutorial - Lesson 6: Lighting
=============================================

Learn how to create and control lights:
- Different light types (Point, Sun, Spot, Area)
- Light properties (energy, color, size)
- Positioning and aiming lights
- Creating three-point lighting setup
- World lighting (environment)
"""

import bpy
import math

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("Demonstrating lighting in Blender...\n")

# Create a simple scene to light
# Ground plane
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
plane = bpy.context.active_object
plane.name = "Ground"

# Add a material to the plane
mat = bpy.data.materials.new(name="GroundMaterial")
mat.use_nodes = True
mat.node_tree.nodes.get("Principled BSDF").inputs['Base Color'].default_value = (0.2, 0.2, 0.2, 1)
plane.data.materials.append(mat)

# Central subject (Suzanne)
bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 1))
suzanne = bpy.context.active_object
suzanne.name = "Suzanne"

# Add camera
bpy.ops.object.camera_add(location=(7, -7, 5))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(65), 0, math.radians(45))
bpy.context.scene.camera = camera

print("Created scene with Suzanne and camera\n")

# ============================================
# 1. POINT LIGHT (Omnidirectional)
# ============================================
print("1. POINT LIGHT - Emits light in all directions")

bpy.ops.object.light_add(type='POINT', location=(3, 0, 3))
point_light = bpy.context.active_object
point_light.name = "PointLight"

# Access the light data
light_data = point_light.data

# Set properties
light_data.energy = 1000  # Brightness (watts in Cycles)
light_data.color = (1, 0.9, 0.8)  # Warm white (R, G, B)
light_data.shadow_soft_size = 0.5  # Soft shadow size

print(f"  Created {point_light.name}")
print(f"    Energy: {light_data.energy}")
print(f"    Color: {light_data.color}")
print(f"    Shadow size: {light_data.shadow_soft_size}")

# ============================================
# 2. SUN LIGHT (Directional, parallel rays)
# ============================================
print("\n2. SUN LIGHT - Parallel rays (for outdoor scenes)")

bpy.ops.object.light_add(type='SUN', location=(0, 0, 5))
sun_light = bpy.context.active_object
sun_light.name = "SunLight"

# Rotate to angle the light
sun_light.rotation_euler = (math.radians(45), 0, math.radians(30))

sun_data = sun_light.data
sun_data.energy = 2.0  # Sun strength
sun_data.color = (1, 1, 0.95)  # Slightly warm
sun_data.angle = math.radians(1)  # Sun angular diameter (affects shadows)

print(f"  Created {sun_light.name}")
print(f"    Energy: {sun_data.energy}")
print(f"    Angle: {math.degrees(sun_data.angle)}°")

# Hide the sun for now to test other lights
sun_light.hide_viewport = True
sun_light.hide_render = True

# ============================================
# 3. SPOT LIGHT (Cone of light)
# ============================================
print("\n3. SPOT LIGHT - Cone-shaped beam")

bpy.ops.object.light_add(type='SPOT', location=(-3, 2, 4))
spot_light = bpy.context.active_object
spot_light.name = "SpotLight"

# Point the spotlight at Suzanne
# Calculate direction
direction = suzanne.location - spot_light.location
spot_light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

spot_data = spot_light.data
spot_data.energy = 500
spot_data.color = (0.8, 0.9, 1)  # Cool blue
spot_data.spot_size = math.radians(45)  # Cone angle
spot_data.spot_blend = 0.5  # Softness of the edge (0-1)
spot_data.shadow_soft_size = 1.0

print(f"  Created {spot_light.name}")
print(f"    Spot size: {math.degrees(spot_data.spot_size)}°")
print(f"    Spot blend: {spot_data.spot_blend}")

# ============================================
# 4. AREA LIGHT (Large soft light source)
# ============================================
print("\n4. AREA LIGHT - Soft, diffused light")

bpy.ops.object.light_add(type='AREA', location=(2, -3, 3))
area_light = bpy.context.active_object
area_light.name = "AreaLight"

# Rotate to face the subject
area_light.rotation_euler = (math.radians(60), 0, math.radians(30))

area_data = area_light.data
area_data.energy = 300
area_data.color = (1, 1, 1)
area_data.shape = 'RECTANGLE'  # 'SQUARE', 'RECTANGLE', 'DISK', 'ELLIPSE'
area_data.size = 2  # Width
area_data.size_y = 1  # Height (for rectangle)

print(f"  Created {area_light.name}")
print(f"    Shape: {area_data.shape}")
print(f"    Size: {area_data.size} x {area_data.size_y}")

# ============================================
# 5. THREE-POINT LIGHTING SETUP
# ============================================
print("\n5. THREE-POINT LIGHTING SETUP")
print("  (Classic photography/film lighting)")

# First, hide previous lights
for obj in [point_light, spot_light, area_light]:
    obj.hide_viewport = True
    obj.hide_render = True

# Create a new Suzanne for this demo
bpy.ops.mesh.primitive_monkey_add(location=(6, 0, 1))
demo_suzanne = bpy.context.active_object
demo_suzanne.name = "Suzanne_ThreePoint"

# KEY LIGHT (Main light - brightest)
bpy.ops.object.light_add(type='AREA', location=(8, -3, 3))
key_light = bpy.context.active_object
key_light.name = "KeyLight"
key_light.rotation_euler = (math.radians(60), 0, math.radians(45))
key_light.data.energy = 400
key_light.data.size = 2
print("  Key Light: Main light source (brightest)")

# FILL LIGHT (Soften shadows)
bpy.ops.object.light_add(type='AREA', location=(4, 2, 2))
fill_light = bpy.context.active_object
fill_light.name = "FillLight"
fill_light.rotation_euler = (math.radians(70), 0, math.radians(-45))
fill_light.data.energy = 150  # Softer than key
fill_light.data.size = 2
print("  Fill Light: Softens shadows from key light")

# BACK LIGHT (Rim light - separates from background)
bpy.ops.object.light_add(type='SPOT', location=(6, 3, 3))
back_light = bpy.context.active_object
back_light.name = "BackLight"
direction = demo_suzanne.location - back_light.location
back_light.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
back_light.data.energy = 300
back_light.data.spot_size = math.radians(60)
print("  Back Light: Creates rim/edge lighting")

# ============================================
# 6. WORLD LIGHTING (Environment/HDRI)
# ============================================
print("\n6. WORLD LIGHTING - Environment lighting")

# Access world settings
world = bpy.context.scene.world

if world.use_nodes:
    # Get the background node
    world_nodes = world.node_tree.nodes
    background = world_nodes.get('Background')

    if background:
        # Set world color
        background.inputs['Color'].default_value = (0.05, 0.05, 0.08, 1)  # Dark blue
        background.inputs['Strength'].default_value = 0.3  # Ambient strength

        print("  Set world background color and strength")

# ============================================
# 7. LIGHT PROPERTIES AND EFFECTS
# ============================================
print("\n7. ADVANCED LIGHT PROPERTIES")

# Create a demonstration light
bpy.ops.object.light_add(type='POINT', location=(-6, 0, 3))
demo_light = bpy.context.active_object
demo_light.name = "DemoLight"
demo_data = demo_light.data

# Various properties
demo_data.energy = 800
demo_data.color = (1, 0.5, 0.2)  # Orange
demo_data.shadow_soft_size = 1.0  # Larger = softer shadows
demo_data.use_contact_shadow = True  # More detailed close shadows

# Falloff (how light diminishes over distance)
# Note: In Cycles, this is automatic based on inverse square law
print(f"  Demo light properties:")
print(f"    Energy: {demo_data.energy}")
print(f"    Color: {demo_data.color[:3]}")
print(f"    Contact shadows: {demo_data.use_contact_shadow}")

# ============================================
# 8. ANIMATING LIGHT PROPERTIES
# ============================================
print("\n8. ANIMATING LIGHTS (Keyframe example)")

# Create a light that will be animated
bpy.ops.object.light_add(type='POINT', location=(0, -6, 2))
anim_light = bpy.context.active_object
anim_light.name = "AnimatedLight"
anim_data = anim_light.data

# Set initial state
anim_data.energy = 100
anim_data.color = (1, 0, 0)  # Red

# Insert keyframe at frame 1
anim_data.keyframe_insert(data_path="energy", frame=1)
anim_data.keyframe_insert(data_path="color", frame=1)

# Change properties
anim_data.energy = 1000
anim_data.color = (0, 0, 1)  # Blue

# Insert keyframe at frame 60
anim_data.keyframe_insert(data_path="energy", frame=60)
anim_data.keyframe_insert(data_path="color", frame=60)

print(f"  Created animated light (fades from red to blue)")
print(f"    Keyframes at frame 1 and 60")

# ============================================
# 9. HELPER FUNCTIONS
# ============================================
print("\n9. HELPER FUNCTIONS FOR LIGHTING")

def create_light(light_type, location, energy=100, color=(1, 1, 1), name=None):
    """Create a light with common properties"""
    bpy.ops.object.light_add(type=light_type.upper(), location=location)
    light = bpy.context.active_object

    if name:
        light.name = name

    light.data.energy = energy
    light.data.color = color

    return light

def point_light_at(light_obj, target_location):
    """Point a light at a specific location"""
    direction = target_location - light_obj.location
    light_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

# Test the helper functions
test_light = create_light('SPOT', (0, 6, 3), energy=500, name="TestSpot")
point_light_at(test_light, suzanne.location)
print(f"  Created {test_light.name} using helper functions")

# ============================================
# 10. LISTING ALL LIGHTS
# ============================================
print("\n10. ALL LIGHTS IN SCENE")

all_lights = [obj for obj in bpy.context.scene.objects if obj.type == 'LIGHT']
print(f"  Total lights: {len(all_lights)}\n")

for light in all_lights:
    visible = "visible" if not light.hide_viewport else "hidden"
    print(f"  {light.name} ({light.data.type})")
    print(f"    Energy: {light.data.energy}, {visible}")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 50)
print("LIGHTING SUMMARY")
print("=" * 50)
print("Light Types:")
print("  POINT  - Omnidirectional (like a bulb)")
print("  SUN    - Parallel rays (outdoor/directional)")
print("  SPOT   - Cone beam (spotlight)")
print("  AREA   - Soft diffused light (studio)")
print("\nCreate: bpy.ops.object.light_add(type='TYPE', location=(x,y,z))")
print("Access: light.data.energy, light.data.color")
print("\nThree-Point Lighting:")
print("  1. Key Light   - Main light (brightest)")
print("  2. Fill Light  - Softens shadows")
print("  3. Back Light  - Rim lighting (separation)")
print("\nTips:")
print("  - Use Area lights for soft, natural lighting")
print("  - Sun lights are position-independent (only rotation matters)")
print("  - Adjust shadow_soft_size for shadow softness")
print("  - World lighting provides ambient illumination")
