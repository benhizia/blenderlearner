"""
Blender Python Tutorial - Lesson 8: Modifiers
==============================================

Learn how to use modifiers to procedurally modify geometry:
- Array modifier (duplicate objects)
- Mirror modifier (symmetry)
- Subdivision Surface (smooth geometry)
- Boolean operations (combine/subtract)
- Solidify (add thickness)
- Bevel (round edges)
- Curve modifier (deform along curve)
- And many more!
"""

import bpy

import math

# Clear the scene

ensure_object_mode()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("Demonstrating modifiers in Blender...\n")

# Add lighting for better visibility
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
bpy.context.active_object.data.energy = 3.0

# ============================================
# 1. ARRAY MODIFIER - Create patterns
# ============================================
print("1. ARRAY MODIFIER - Duplicate objects in patterns")

bpy.ops.mesh.primitive_cube_add(size=1, location=(-8, 0, 0.5))
array_cube = bpy.context.active_object
array_cube.name = "ArrayCube"

# Add array modifier
array_mod = array_cube.modifiers.new(name="ArrayModifier", type='ARRAY')
array_mod.count = 5  # Number of duplicates
array_mod.relative_offset_displace[0] = 1.5  # Spacing in X direction
array_mod.relative_offset_displace[1] = 0.0  # No spacing in Y
array_mod.relative_offset_displace[2] = 0.0  # No spacing in Z

print(f"  Created array of {array_mod.count} cubes")
print(f"  Offset: {array_mod.relative_offset_displace}")

# 2D Array (add second array modifier)
array_mod_y = array_cube.modifiers.new(name="ArrayModifierY", type='ARRAY')
array_mod_y.count = 3
array_mod_y.relative_offset_displace[0] = 0.0
array_mod_y.relative_offset_displace[1] = 1.5
array_mod_y.relative_offset_displace[2] = 0.0

print(f"  Added second array for grid pattern")

# ============================================
# 2. MIRROR MODIFIER - Symmetry
# ============================================
print("\n2. MIRROR MODIFIER - Create symmetrical objects")

bpy.ops.mesh.primitive_cube_add(location=(0, -6, 1))
mirror_cube = bpy.context.active_object
mirror_cube.name = "MirrorCube"

# Scale it asymmetrically to see the effect
mirror_cube.scale = (2, 0.5, 1)
mirror_cube.location.x = 0.5  # Offset to one side

# Add mirror modifier
mirror_mod = mirror_cube.modifiers.new(name="Mirror", type='MIRROR')
mirror_mod.use_axis[0] = True   # Mirror on X axis
mirror_mod.use_axis[1] = False  # No mirror on Y
mirror_mod.use_axis[2] = False  # No mirror on Z
mirror_mod.use_clip = True      # Merge center vertices

print(f"  Created mirrored object")
print(f"  Mirror axes: X={mirror_mod.use_axis[0]}, Y={mirror_mod.use_axis[1]}, Z={mirror_mod.use_axis[2]}")

# ============================================
# 3. SUBDIVISION SURFACE - Smooth geometry
# ============================================
print("\n3. SUBDIVISION SURFACE - Smooth low-poly meshes")

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
subsurf_cube = bpy.context.active_object
subsurf_cube.name = "SmoothCube"

# Add subdivision surface
subsurf_mod = subsurf_cube.modifiers.new(name="Subdivision", type='SUBSURF')
subsurf_mod.levels = 2  # Viewport subdivisions
subsurf_mod.render_levels = 3  # Render subdivisions
subsurf_mod.subdivision_type = 'CATMULL_CLARK'  # or 'SIMPLE'

print(f"  Created smooth cube with subdivision")
print(f"  Viewport levels: {subsurf_mod.levels}")
print(f"  Render levels: {subsurf_mod.render_levels}")

# ============================================
# 4. BOOLEAN MODIFIER - Combine/subtract
# ============================================
print("\n4. BOOLEAN MODIFIER - Combine or subtract objects")

# Create base object
bpy.ops.mesh.primitive_cube_add(size=2, location=(4, 0, 1))
bool_base = bpy.context.active_object
bool_base.name = "BooleanBase"

# Create cutter object
bpy.ops.mesh.primitive_cylinder_add(radius=0.7, depth=3, location=(4, 0, 1))
bool_cutter = bpy.context.active_object
bool_cutter.name = "BooleanCutter"
bool_cutter.rotation_euler = (math.radians(90), 0, 0)

# Add boolean modifier to base
bool_mod = bool_base.modifiers.new(name="Boolean", type='BOOLEAN')
bool_mod.operation = 'DIFFERENCE'  # 'UNION', 'DIFFERENCE', 'INTERSECT'
bool_mod.object = bool_cutter

# Hide the cutter object
bool_cutter.hide_viewport = True
bool_cutter.hide_render = True

print(f"  Created boolean operation")
print(f"  Operation: {bool_mod.operation}")

# ============================================
# 5. SOLIDIFY MODIFIER - Add thickness
# ============================================
print("\n5. SOLIDIFY MODIFIER - Add thickness to surfaces")

bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 4, 1))
solidify_plane = bpy.context.active_object
solidify_plane.name = "SolidPlane"

# Add solidify modifier
solid_mod = solidify_plane.modifiers.new(name="Solidify", type='SOLIDIFY')
solid_mod.thickness = 0.2
solid_mod.offset = 0  # -1 to 1 (inside to outside)

print(f"  Added thickness to plane: {solid_mod.thickness}")

# ============================================
# 6. BEVEL MODIFIER - Round edges
# ============================================
print("\n6. BEVEL MODIFIER - Create rounded edges")

bpy.ops.mesh.primitive_cube_add(location=(4, 4, 1))
bevel_cube = bpy.context.active_object
bevel_cube.name = "BeveledCube"

# Add bevel modifier
bevel_mod = bevel_cube.modifiers.new(name="Bevel", type='BEVEL')
bevel_mod.width = 0.1  # Bevel size
bevel_mod.segments = 3  # Smoothness
bevel_mod.limit_method = 'ANGLE'  # Only bevel sharp edges

print(f"  Created beveled cube")
print(f"  Bevel width: {bevel_mod.width}")
print(f"  Segments: {bevel_mod.segments}")

# ============================================
# 7. DISPLACEMENT MODIFIER - Add detail
# ============================================
print("\n7. DISPLACEMENT MODIFIER - Add surface detail")

bpy.ops.mesh.primitive_plane_add(size=4, location=(-4, 4, 0))
displace_plane = bpy.context.active_object
displace_plane.name = "DisplacedPlane"

# Subdivide the plane first (displacement needs geometry)
subsurf = displace_plane.modifiers.new(name="Subdivision", type='SUBSURF')
subsurf.levels = 5

# Create a texture for displacement
texture = bpy.data.textures.new(name="DisplaceTexture", type='CLOUDS')
texture.noise_scale = 0.5

# Add displacement modifier
displace_mod = displace_plane.modifiers.new(name="Displace", type='DISPLACE')
displace_mod.texture = texture
displace_mod.strength = 0.5
displace_mod.mid_level = 0.5

print(f"  Created displaced terrain")
print(f"  Displacement strength: {displace_mod.strength}")

# ============================================
# 8. CURVE MODIFIER - Deform along path
# ============================================
print("\n8. CURVE MODIFIER - Deform object along curve")

# Create a curve path
bpy.ops.curve.primitive_bezier_circle_add(radius=3, location=(8, -6, 1))
curve = bpy.context.active_object
curve.name = "BendPath"

# Create object to deform
bpy.ops.mesh.primitive_cube_add(size=0.5, location=(8, -6, 1))
curve_cube = bpy.context.active_object
curve_cube.name = "CurveDeformed"
curve_cube.scale = (4, 0.5, 0.5)

# Add curve modifier
curve_mod = curve_cube.modifiers.new(name="Curve", type='CURVE')
curve_mod.object = curve
curve_mod.deform_axis = 'POS_X'

print(f"  Created curve deformation")

# ============================================
# 9. SIMPLE DEFORM MODIFIER - Bend, Twist, Taper
# ============================================
print("\n9. SIMPLE DEFORM - Bend, Twist, Taper, Stretch")

# TWIST example
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=3, location=(-4, -4, 1.5))
twist_cylinder = bpy.context.active_object
twist_cylinder.name = "TwistedCylinder"

twist_mod = twist_cylinder.modifiers.new(name="Twist", type='SIMPLE_DEFORM')
twist_mod.deform_method = 'TWIST'  # 'TWIST', 'BEND', 'TAPER', 'STRETCH'
twist_mod.angle = math.radians(360)  # Full rotation
twist_mod.deform_axis = 'Z'

print(f"  Created twisted cylinder")
print(f"  Twist angle: {math.degrees(twist_mod.angle)}°")

# BEND example
bpy.ops.mesh.primitive_cube_add(size=1, location=(-8, -4, 0.5))
bend_cube = bpy.context.active_object
bend_cube.name = "BentCube"
bend_cube.scale = (2, 0.5, 0.5)

bend_mod = bend_cube.modifiers.new(name="Bend", type='SIMPLE_DEFORM')
bend_mod.deform_method = 'BEND'
bend_mod.angle = math.radians(90)
bend_mod.deform_axis = 'Z'

print(f"  Created bent cube")

# ============================================
# 10. SKIN MODIFIER - Create organic shapes
# ============================================
print("\n10. SKIN MODIFIER - Create organic shapes from edges")

# Create a simple edge structure
mesh = bpy.data.meshes.new("SkinMesh")
obj = bpy.data.objects.new("SkinObject", mesh)
bpy.context.collection.objects.link(obj)

# Create vertices and edges for a simple structure
import bmesh

def ensure_object_mode():
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

bm = bmesh.new()
v1 = bm.verts.new((0, -8, 0))
v2 = bm.verts.new((0, -8, 1))
v3 = bm.verts.new((0, -8, 2))
v4 = bm.verts.new((0.5, -8, 2.5))

bm.edges.new((v1, v2))
bm.edges.new((v2, v3))
bm.edges.new((v3, v4))

bm.to_mesh(mesh)
bm.free()

# Add skin modifier
skin_mod = obj.modifiers.new(name="Skin", type='SKIN')

# Add subdivision for smoothness
subsurf = obj.modifiers.new(name="Smooth", type='SUBSURF')
subsurf.levels = 2

print(f"  Created organic shape with skin modifier")

# ============================================
# 11. MODIFIER STACK ORDER
# ============================================
print("\n11. MODIFIER STACK - Order matters!")

bpy.ops.mesh.primitive_cube_add(location=(4, -4, 1))
stack_cube = bpy.context.active_object
stack_cube.name = "ModifierStack"

# Add multiple modifiers in order
mod1 = stack_cube.modifiers.new(name="Bevel", type='BEVEL')
mod1.width = 0.1
mod1.segments = 2

mod2 = stack_cube.modifiers.new(name="Subdivision", type='SUBSURF')
mod2.levels = 2

mod3 = stack_cube.modifiers.new(name="Array", type='ARRAY')
mod3.count = 3
mod3.relative_offset_displace[0] = 1.5

print(f"  Created modifier stack:")
for i, mod in enumerate(stack_cube.modifiers):
    print(f"    {i+1}. {mod.name} ({mod.type})")

# ============================================
# 12. MODIFIER OPERATIONS
# ============================================
print("\n12. MODIFIER OPERATIONS")

def apply_modifier(obj, modifier_name):
    """Apply a modifier (make it permanent)"""
    # Note: This requires the object to be in object mode
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=modifier_name)

def remove_modifier(obj, modifier_name):
    """Remove a modifier"""
    modifier = obj.modifiers.get(modifier_name)
    if modifier:
        obj.modifiers.remove(modifier)

def toggle_modifier(obj, modifier_name):
    """Toggle modifier visibility"""
    modifier = obj.modifiers.get(modifier_name)
    if modifier:
        modifier.show_viewport = not modifier.show_viewport

# Example: Toggle subdivision visibility
print(f"  Modifier operations defined:")
print(f"    - apply_modifier(obj, name)")
print(f"    - remove_modifier(obj, name)")
print(f"    - toggle_modifier(obj, name)")

# ============================================
# 13. LISTING MODIFIERS
# ============================================
print("\n13. LISTING ALL MODIFIERS IN SCENE")

modifier_count = 0
for obj in bpy.context.scene.objects:
    if obj.modifiers:
        modifier_count += len(obj.modifiers)
        print(f"\n  {obj.name}:")
        for mod in obj.modifiers:
            visible = "✓" if mod.show_viewport else "✗"
            print(f"    {visible} {mod.name} ({mod.type})")

print(f"\n  Total modifiers in scene: {modifier_count}")

# ============================================
# 14. ADVANCED: PARTICLE SYSTEM (Quick demo)
# ============================================
print("\n14. BONUS: PARTICLE SYSTEM")

bpy.ops.mesh.primitive_plane_add(size=5, location=(8, 4, 0))
particle_plane = bpy.context.active_object
particle_plane.name = "ParticleEmitter"

# Add particle system (this is a modifier!)
particle_mod = particle_plane.modifiers.new(name="ParticleSystem", type='PARTICLE_SYSTEM')
particle_settings = particle_mod.particle_system.settings

particle_settings.count = 100
particle_settings.frame_start = 1
particle_settings.frame_end = 50
particle_settings.lifetime = 50
particle_settings.normal_factor = 1.0  # Emit upward

print(f"  Created particle system")
print(f"    Particle count: {particle_settings.count}")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 50)
print("MODIFIERS SUMMARY")
print("=" * 50)
print("Add modifier: obj.modifiers.new(name='Name', type='TYPE')")
print("Remove modifier: obj.modifiers.remove(modifier)")
print("Apply modifier: bpy.ops.object.modifier_apply(modifier='Name')")
print("\nCommon Modifiers:")
print("  ARRAY       - Duplicate in patterns")
print("  MIRROR      - Symmetrical modeling")
print("  SUBSURF     - Smooth subdivision")
print("  BOOLEAN     - Combine/subtract objects")
print("  SOLIDIFY    - Add thickness")
print("  BEVEL       - Round edges")
print("  DISPLACE    - Add surface detail")
print("  CURVE       - Deform along path")
print("  SIMPLE_DEFORM - Twist, bend, taper")
print("  SKIN        - Organic shapes from edges")
print("\nImportant:")
print("  - Modifier order matters!")
print("  - Non-destructive (until applied)")
print("  - Can be toggled on/off")
print("  - Some modifiers require subdivision")
