"""
Blender Python Tutorial - Lesson 9: Animation
==============================================

Learn how to create animations with Python:
- Keyframe animation basics
- Animating object properties
- Animating materials
- Animation curves and interpolation
- Path animation
- Armatures and rigging basics
- Shape keys (morphing)
- Animating modifiers
"""

import bpy
import math

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("Demonstrating animation in Blender...\n")

# Set up the scene for animation
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 120
scene.frame_current = 1

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(10, -10, 10))
sun = bpy.context.active_object
sun.data.energy = 3.0

# Add camera
bpy.ops.object.camera_add(location=(15, -15, 10))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))
scene.camera = camera

print(f"Scene setup: {scene.frame_start} to {scene.frame_end} frames\n")

# ============================================
# 1. BASIC KEYFRAME ANIMATION
# ============================================
print("1. BASIC KEYFRAME ANIMATION - Moving object")

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))
anim_cube = bpy.context.active_object
anim_cube.name = "AnimatedCube"

# Keyframe 1 - Starting position
scene.frame_set(1)
anim_cube.location = (0, 0, 1)
anim_cube.keyframe_insert(data_path="location", frame=1)

# Keyframe 2 - End position
scene.frame_set(60)
anim_cube.location = (5, 0, 1)
anim_cube.keyframe_insert(data_path="location", frame=60)

# Keyframe 3 - Return
scene.frame_set(120)
anim_cube.location = (0, 0, 1)
anim_cube.keyframe_insert(data_path="location", frame=120)

print(f"  Created animation for {anim_cube.name}")
print(f"  Keyframes at: 1, 60, 120")

# ============================================
# 2. ANIMATING ROTATION
# ============================================
print("\n2. ANIMATING ROTATION - Spinning object")

bpy.ops.mesh.primitive_cylinder_add(location=(0, -3, 1))
spin_cylinder = bpy.context.active_object
spin_cylinder.name = "SpinningCylinder"

# Animate a full rotation
scene.frame_set(1)
spin_cylinder.rotation_euler.z = 0
spin_cylinder.keyframe_insert(data_path="rotation_euler", frame=1)

scene.frame_set(120)
spin_cylinder.rotation_euler.z = math.radians(360) * 3  # 3 full rotations
spin_cylinder.keyframe_insert(data_path="rotation_euler", frame=120)

print(f"  Created spinning animation")
print(f"  3 full rotations over 120 frames")

# ============================================
# 3. ANIMATING SCALE
# ============================================
print("\n3. ANIMATING SCALE - Pulsing effect")

bpy.ops.mesh.primitive_sphere_add(location=(0, 3, 1))
pulse_sphere = bpy.context.active_object
pulse_sphere.name = "PulsingSphere"

# Create pulsing animation
for frame in [1, 30, 60, 90, 120]:
    scene.frame_set(frame)
    if frame % 60 == 30:
        pulse_sphere.scale = (1.5, 1.5, 1.5)
    else:
        pulse_sphere.scale = (1.0, 1.0, 1.0)
    pulse_sphere.keyframe_insert(data_path="scale", frame=frame)

print(f"  Created pulsing animation")
print(f"  Keyframes at: 1, 30, 60, 90, 120")

# ============================================
# 4. ANIMATING INDIVIDUAL AXES
# ============================================
print("\n4. ANIMATING INDIVIDUAL AXES")

bpy.ops.mesh.primitive_cube_add(location=(3, 0, 1))
axis_cube = bpy.context.active_object
axis_cube.name = "AxisAnimCube"

# Animate X position
scene.frame_set(1)
axis_cube.location.x = 3
axis_cube.keyframe_insert(data_path="location", index=0, frame=1)  # index 0 = X

scene.frame_set(60)
axis_cube.location.x = 6
axis_cube.keyframe_insert(data_path="location", index=0, frame=60)

# Animate Z position (bouncing)
for frame in [1, 30, 60, 90, 120]:
    scene.frame_set(frame)
    if frame % 60 == 30:
        axis_cube.location.z = 3
    else:
        axis_cube.location.z = 1
    axis_cube.keyframe_insert(data_path="location", index=2, frame=frame)  # index 2 = Z

print(f"  Created multi-axis animation")
print(f"  X: linear motion, Z: bouncing")

# ============================================
# 5. ANIMATING MATERIALS
# ============================================
print("\n5. ANIMATING MATERIALS - Color change")

bpy.ops.mesh.primitive_sphere_add(location=(-3, 0, 1))
color_sphere = bpy.context.active_object
color_sphere.name = "ColorChangeSphere"

# Create material
mat = bpy.data.materials.new(name="AnimatedMaterial")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
color_sphere.data.materials.append(mat)

# Animate color
scene.frame_set(1)
bsdf.inputs['Base Color'].default_value = (1, 0, 0, 1)  # Red
bsdf.inputs['Base Color'].keyframe_insert(data_path="default_value", frame=1)

scene.frame_set(60)
bsdf.inputs['Base Color'].default_value = (0, 1, 0, 1)  # Green
bsdf.inputs['Base Color'].keyframe_insert(data_path="default_value", frame=60)

scene.frame_set(120)
bsdf.inputs['Base Color'].default_value = (0, 0, 1, 1)  # Blue
bsdf.inputs['Base Color'].keyframe_insert(data_path="default_value", frame=120)

# Animate emission (glow)
scene.frame_set(1)
bsdf.inputs['Emission Strength'].default_value = 0
bsdf.inputs['Emission Strength'].keyframe_insert(data_path="default_value", frame=1)

scene.frame_set(60)
bsdf.inputs['Emission Strength'].default_value = 5
bsdf.inputs['Emission Strength'].keyframe_insert(data_path="default_value", frame=60)

scene.frame_set(120)
bsdf.inputs['Emission Strength'].default_value = 0
bsdf.inputs['Emission Strength'].keyframe_insert(data_path="default_value", frame=120)

print(f"  Animated material color and emission")

# ============================================
# 6. PATH ANIMATION (Follow Curve)
# ============================================
print("\n6. PATH ANIMATION - Follow curve")

# Create a curve path
bpy.ops.curve.primitive_bezier_circle_add(radius=4, location=(6, 4, 1))
path = bpy.context.active_object
path.name = "AnimPath"

# Create object to follow path
bpy.ops.mesh.primitive_cone_add(location=(6, 4, 1))
follower = bpy.context.active_object
follower.name = "PathFollower"

# Add Follow Path constraint
constraint = follower.constraints.new(type='FOLLOW_PATH')
constraint.target = path
constraint.use_curve_follow = True  # Orient along path

# Animate the path offset
scene.frame_set(1)
constraint.offset_factor = 0
constraint.keyframe_insert(data_path="offset_factor", frame=1)

scene.frame_set(120)
constraint.offset_factor = 1
constraint.keyframe_insert(data_path="offset_factor", frame=120)

print(f"  Created path following animation")

# ============================================
# 7. SHAPE KEYS (Morphing)
# ============================================
print("\n7. SHAPE KEYS - Morphing animation")

bpy.ops.mesh.primitive_cube_add(location=(-3, -3, 1))
morph_cube = bpy.context.active_object
morph_cube.name = "MorphCube"

# Add shape keys
# Basis shape (original)
basis = morph_cube.shape_key_add(name='Basis')

# Deformed shape
stretched = morph_cube.shape_key_add(name='Stretched')
# Modify the shape key vertices
for vert in stretched.data:
    vert.co.z *= 2  # Stretch in Z

# Another shape
squashed = morph_cube.shape_key_add(name='Squashed')
for vert in squashed.data:
    vert.co.z *= 0.5  # Squash in Z
    vert.co.x *= 1.5  # Expand in X

# Animate shape keys
scene.frame_set(1)
stretched.value = 0
stretched.keyframe_insert(data_path="value", frame=1)

scene.frame_set(40)
stretched.value = 1
stretched.keyframe_insert(data_path="value", frame=40)

scene.frame_set(80)
stretched.value = 0
squashed.value = 1
squashed.keyframe_insert(data_path="value", frame=80)

scene.frame_set(120)
squashed.value = 0
squashed.keyframe_insert(data_path="value", frame=120)

print(f"  Created shape key morphing")
print(f"  Shape keys: Basis, Stretched, Squashed")

# ============================================
# 8. ANIMATING MODIFIERS
# ============================================
print("\n8. ANIMATING MODIFIERS")

bpy.ops.mesh.primitive_plane_add(size=3, location=(3, -3, 0))
mod_plane = bpy.context.active_object
mod_plane.name = "ModifierAnimPlane"

# Add subdivision for displacement
subsurf = mod_plane.modifiers.new(name="Subdivision", type='SUBSURF')
subsurf.levels = 4

# Add displacement modifier
texture = bpy.data.textures.new(name="AnimTexture", type='CLOUDS')
displace = mod_plane.modifiers.new(name="Displace", type='DISPLACE')
displace.texture = texture

# Animate displacement strength
scene.frame_set(1)
displace.strength = 0
displace.keyframe_insert(data_path="strength", frame=1)

scene.frame_set(60)
displace.strength = 1.5
displace.keyframe_insert(data_path="strength", frame=60)

scene.frame_set(120)
displace.strength = 0
displace.keyframe_insert(data_path="strength", frame=120)

print(f"  Animated displacement modifier strength")

# ============================================
# 9. INTERPOLATION MODES
# ============================================
print("\n9. ANIMATION INTERPOLATION")

bpy.ops.mesh.primitive_cube_add(location=(6, -3, 1))
interp_cube = bpy.context.active_object
interp_cube.name = "InterpolationCube"

# Create animation with different interpolation
scene.frame_set(1)
interp_cube.location.x = 6
interp_cube.keyframe_insert(data_path="location", frame=1)

scene.frame_set(120)
interp_cube.location.x = 12
interp_cube.keyframe_insert(data_path="location", frame=120)

# Access the F-curve (animation curve)
action = interp_cube.animation_data.action
fcurve = action.fcurves.find('location', index=0)  # X location

# Set interpolation type
# Types: 'CONSTANT', 'LINEAR', 'BEZIER', 'SINE', 'QUAD', 'CUBIC', etc.
for keyframe in fcurve.keyframe_points:
    keyframe.interpolation = 'BEZIER'  # Smooth
    # keyframe.interpolation = 'LINEAR'  # Straight
    # keyframe.interpolation = 'CONSTANT'  # Stepped

# Set easing
for keyframe in fcurve.keyframe_points:
    keyframe.easing = 'EASE_IN_OUT'  # or 'EASE_IN', 'EASE_OUT'

print(f"  Set interpolation to BEZIER with EASE_IN_OUT")

# ============================================
# 10. SIMPLE ARMATURE (Rigging)
# ============================================
print("\n10. ARMATURE BASICS - Simple bone animation")

# Create an armature
bpy.ops.object.armature_add(location=(-6, 3, 0))
armature = bpy.context.active_object
armature.name = "SimpleRig"

# Enter edit mode to add bones
bpy.ops.object.mode_set(mode='EDIT')
edit_bones = armature.data.edit_bones

# Get the default bone
bone1 = edit_bones[0]
bone1.name = "Bone1"
bone1.head = (0, 0, 0)
bone1.tail = (0, 0, 1)

# Add a second bone
bone2 = edit_bones.new("Bone2")
bone2.head = bone1.tail
bone2.tail = (0, 0, 2)
bone2.parent = bone1

# Back to object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Animate the armature
bpy.ops.object.mode_set(mode='POSE')
pose_bones = armature.pose.bones

# Animate first bone rotation
scene.frame_set(1)
pose_bones["Bone1"].rotation_euler.y = 0
pose_bones["Bone1"].keyframe_insert(data_path="rotation_euler", frame=1)

scene.frame_set(60)
pose_bones["Bone1"].rotation_euler.y = math.radians(45)
pose_bones["Bone1"].keyframe_insert(data_path="rotation_euler", frame=60)

scene.frame_set(120)
pose_bones["Bone1"].rotation_euler.y = 0
pose_bones["Bone1"].keyframe_insert(data_path="rotation_euler", frame=120)

bpy.ops.object.mode_set(mode='OBJECT')

print(f"  Created simple armature with 2 bones")
print(f"  Animated bone rotation")

# ============================================
# 11. HELPER FUNCTIONS
# ============================================
print("\n11. ANIMATION HELPER FUNCTIONS")

def animate_property(obj, data_path, start_value, end_value, start_frame, end_frame, index=None):
    """
    Animate any property from start to end value

    Args:
        obj: Object to animate
        data_path: Property path (e.g., 'location', 'rotation_euler')
        start_value: Starting value
        end_value: Ending value
        start_frame: Starting frame
        end_frame: Ending frame
        index: Property index (0=X, 1=Y, 2=Z), None for all
    """
    scene = bpy.context.scene

    scene.frame_set(start_frame)
    if index is not None:
        exec(f"obj.{data_path}[{index}] = {start_value}")
        obj.keyframe_insert(data_path=data_path, index=index, frame=start_frame)
    else:
        exec(f"obj.{data_path} = {start_value}")
        obj.keyframe_insert(data_path=data_path, frame=start_frame)

    scene.frame_set(end_frame)
    if index is not None:
        exec(f"obj.{data_path}[{index}] = {end_value}")
        obj.keyframe_insert(data_path=data_path, index=index, frame=end_frame)
    else:
        exec(f"obj.{data_path} = {end_value}")
        obj.keyframe_insert(data_path=data_path, frame=end_frame)

def clear_animation(obj):
    """Remove all animation from an object"""
    if obj.animation_data:
        obj.animation_data_clear()

# Example usage
test_sphere = bpy.ops.mesh.primitive_sphere_add(location=(0, 6, 1))
test_obj = bpy.context.active_object
test_obj.name = "TestAnimObject"

# Use helper function
animate_property(test_obj, 'location', (0, 6, 1), (0, 6, 3), 1, 60)

print(f"  Created helper functions:")
print(f"    - animate_property()")
print(f"    - clear_animation()")

# ============================================
# 12. LISTING ANIMATIONS
# ============================================
print("\n12. LISTING ALL ANIMATIONS")

animated_objects = []
for obj in bpy.context.scene.objects:
    if obj.animation_data and obj.animation_data.action:
        animated_objects.append(obj)
        print(f"\n  {obj.name}:")
        action = obj.animation_data.action
        print(f"    Action: {action.name}")
        print(f"    Curves: {len(action.fcurves)}")

        for fcurve in action.fcurves:
            keyframe_count = len(fcurve.keyframe_points)
            print(f"      {fcurve.data_path}: {keyframe_count} keyframes")

print(f"\n  Total animated objects: {len(animated_objects)}")

# Reset to frame 1
scene.frame_set(1)

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 50)
print("ANIMATION SUMMARY")
print("=" * 50)
print("Insert keyframe: obj.keyframe_insert(data_path='property', frame=N)")
print("Set frame: bpy.context.scene.frame_set(N)")
print("\nCommon data paths:")
print("  'location' - Position")
print("  'rotation_euler' - Rotation")
print("  'scale' - Size")
print("  Use index for individual axes (0=X, 1=Y, 2=Z)")
print("\nInterpolation types:")
print("  CONSTANT - Stepped")
print("  LINEAR - Straight")
print("  BEZIER - Smooth curves")
print("\nAdvanced:")
print("  - Shape keys for morphing")
print("  - Constraints for complex motion")
print("  - Armatures for character animation")
print("  - F-curves for precise control")
print("\nTo play animation: Press Spacebar in Blender")
print(f"Animation range: {scene.frame_start} to {scene.frame_end}")
