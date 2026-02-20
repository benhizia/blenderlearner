"""
Blender Python Tutorial - Lesson 11: Physics Simulation
========================================================

Learn how to set up physics simulations:
- Rigid body physics (falling objects, collisions)
- Soft body physics (cloth, jello)
- Cloth simulation
- Fluid simulation
- Particle systems
- Force fields
- Constraints and collision detection
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

print("Demonstrating physics simulations...\n")

# Set up scene for simulation
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 250

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(10, -10, 20))
sun = bpy.context.active_object
sun.data.energy = 3.0

# Add camera
bpy.ops.object.camera_add(location=(15, -15, 10))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))
scene.camera = camera

# ============================================
# 1. RIGID BODY PHYSICS - BASIC SETUP
# ============================================
print("1. RIGID BODY PHYSICS - Falling objects")

# Create ground (passive rigid body)
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
ground = bpy.context.active_object
ground.name = "Ground"

# Add rigid body physics (passive - doesn't move)
bpy.ops.rigidbody.object_add()
ground.rigid_body.type = 'PASSIVE'  # or 'ACTIVE'
ground.rigid_body.collision_shape = 'MESH'  # 'BOX', 'SPHERE', 'MESH', etc.

print(f"  Created passive ground plane")

# Create falling cube (active rigid body)
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 5))
falling_cube = bpy.context.active_object
falling_cube.name = "FallingCube"

bpy.ops.rigidbody.object_add()
falling_cube.rigid_body.type = 'ACTIVE'
falling_cube.rigid_body.mass = 1.0
falling_cube.rigid_body.friction = 0.5
falling_cube.rigid_body.restitution = 0.3  # Bounciness (0-1)

print(f"  Created active falling cube")
print(f"    Mass: {falling_cube.rigid_body.mass}")
print(f"    Friction: {falling_cube.rigid_body.friction}")
print(f"    Restitution: {falling_cube.rigid_body.restitution}")

# ============================================
# 2. RIGID BODY - STACK OF OBJECTS
# ============================================
print("\n2. RIGID BODY - Tower of cubes")

# Create a tower
tower_height = 8
for i in range(tower_height):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(3, 0, 0.5 + i * 1.01)  # Slight offset to make it interesting
    )
    cube = bpy.context.active_object
    cube.name = f"Tower_Cube_{i}"

    bpy.ops.rigidbody.object_add()
    cube.rigid_body.type = 'ACTIVE'
    cube.rigid_body.mass = 1.0

print(f"  Created tower with {tower_height} cubes")

# Create a sphere to knock it down
bpy.ops.mesh.primitive_sphere_add(radius=0.8, location=(-5, 0, 3))
wrecking_ball = bpy.context.active_object
wrecking_ball.name = "WreckingBall"

bpy.ops.rigidbody.object_add()
wrecking_ball.rigid_body.type = 'ACTIVE'
wrecking_ball.rigid_body.mass = 5.0  # Heavier

# Give it initial velocity
scene.frame_set(1)
wrecking_ball.location.x = -5
wrecking_ball.keyframe_insert(data_path="location", frame=1)

scene.frame_set(30)
wrecking_ball.location.x = 3
wrecking_ball.keyframe_insert(data_path="location", frame=30)

print(f"  Created wrecking ball to knock down tower")

# ============================================
# 3. DIFFERENT COLLISION SHAPES
# ============================================
print("\n3. COLLISION SHAPES")

collision_shapes = ['BOX', 'SPHERE', 'CAPSULE', 'CYLINDER', 'CONE']

for i, shape in enumerate(collision_shapes):
    bpy.ops.mesh.primitive_cube_add(location=(-8 + i * 2, 3, 3))
    obj = bpy.context.active_object
    obj.name = f"Shape_{shape}"

    bpy.ops.rigidbody.object_add()
    obj.rigid_body.type = 'ACTIVE'
    obj.rigid_body.collision_shape = shape

    print(f"  Created object with {shape} collision")

# ============================================
# 4. SOFT BODY PHYSICS
# ============================================
print("\n4. SOFT BODY PHYSICS - Deformable cube")

bpy.ops.mesh.primitive_cube_add(location=(0, -5, 5))
soft_cube = bpy.context.active_object
soft_cube.name = "SoftCube"

# Add subdivision for deformation
subsurf = soft_cube.modifiers.new(name="Subdivision", type='SUBSURF')
subsurf.levels = 2

# Add soft body physics
bpy.ops.object.modifier_add(type='SOFT_BODY')
soft_body = soft_cube.modifiers["Softbody"].settings

# Soft body settings
soft_body.mass = 1.0
soft_body.friction = 0.5
soft_body.goal_default = 0  # 0 = fully soft, 1 = rigid

# Soft body edges (springs)
soft_body.pull = 0.9  # Spring stiffness
soft_body.push = 0.9  # Compression resistance
soft_body.bend = 0.5  # Bending resistance
soft_body.damping = 0.5  # Energy loss

print(f"  Created soft body cube")
print(f"    Pull: {soft_body.pull}")
print(f"    Damping: {soft_body.damping}")

# Create obstacle for soft body
bpy.ops.mesh.primitive_cube_add(location=(0, -5, 2))
obstacle = bpy.context.active_object
obstacle.name = "SoftBodyObstacle"

# Add collision for soft body
bpy.ops.object.modifier_add(type='COLLISION')

# ============================================
# 5. CLOTH SIMULATION
# ============================================
print("\n5. CLOTH SIMULATION - Flag")

# Create a plane for cloth
bpy.ops.mesh.primitive_plane_add(size=4, location=(6, -5, 5))
cloth_plane = bpy.context.active_object
cloth_plane.name = "Cloth"
cloth_plane.rotation_euler = (0, math.radians(90), 0)

# Subdivide for better cloth simulation
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=20)
bpy.ops.object.mode_set(mode='OBJECT')

# Add cloth modifier
bpy.ops.object.modifier_add(type='CLOTH')
cloth_settings = cloth_plane.modifiers["Cloth"].settings

# Cloth properties
cloth_settings.quality = 5  # Simulation quality
cloth_settings.mass = 0.3  # Fabric weight
cloth_settings.air_damping = 1.0  # Air resistance
cloth_settings.tension_stiffness = 15  # Stretch resistance
cloth_settings.compression_stiffness = 15
cloth_settings.bending_stiffness = 0.5  # How much it resists bending

# Pin one edge (to make it hang like a flag)
# This requires vertex groups (more advanced)
# For now, we'll use goal weights
cloth_settings.vertex_group_mass = ""

print(f"  Created cloth simulation")
print(f"    Mass: {cloth_settings.mass}")
print(f"    Quality: {cloth_settings.quality}")

# Create obstacle for cloth
bpy.ops.mesh.primitive_sphere_add(radius=1, location=(6, -5, 3))
cloth_obstacle = bpy.context.active_object
cloth_obstacle.name = "ClothObstacle"
bpy.ops.object.modifier_add(type='COLLISION')

# ============================================
# 6. PARTICLE SYSTEM - EMITTER
# ============================================
print("\n6. PARTICLE SYSTEM - Emitter")

# Create emitter object
bpy.ops.mesh.primitive_plane_add(size=2, location=(-6, -5, 3))
emitter = bpy.context.active_object
emitter.name = "ParticleEmitter"

# Add particle system
bpy.ops.object.modifier_add(type='PARTICLE_SYSTEM')
particle_sys = emitter.particle_systems[0]
particle_settings = particle_sys.settings

# Particle settings
particle_settings.count = 500  # Number of particles
particle_settings.frame_start = 1
particle_settings.frame_end = 100
particle_settings.lifetime = 100
particle_settings.lifetime_random = 0.5

# Emission settings
particle_settings.emit_from = 'FACE'  # 'VERT' or 'FACE'
particle_settings.normal_factor = 2.0  # Velocity in normal direction
particle_settings.factor_random = 1.0  # Randomness

# Physics
particle_settings.physics_type = 'NEWTON'  # 'NEWTON', 'KEYED', 'BOIDS', 'FLUID'
particle_settings.mass = 1.0
particle_settings.particle_size = 0.1

# Gravity and forces
particle_settings.effector_weights.gravity = 1.0

print(f"  Created particle emitter")
print(f"    Particle count: {particle_settings.count}")
print(f"    Physics type: {particle_settings.physics_type}")

# ============================================
# 7. PARTICLE SYSTEM - HAIR/FUR
# ============================================
print("\n7. PARTICLE SYSTEM - Hair/Grass")

# Create object for hair
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(-6, -10, 2))
hairy_sphere = bpy.context.active_object
hairy_sphere.name = "HairySphere"

# Add hair particle system
bpy.ops.object.modifier_add(type='PARTICLE_SYSTEM')
hair_sys = hairy_sphere.particle_systems[0]
hair_settings = hair_sys.settings

hair_settings.type = 'HAIR'  # Instead of 'EMITTER'
hair_settings.count = 1000
hair_settings.hair_length = 0.5
hair_settings.path_end = 1.0

# Hair physics
hair_settings.physics_type = 'HAIR'  # Hair physics (not Newton)

print(f"  Created hair particle system")
print(f"    Hair count: {hair_settings.count}")
print(f"    Hair length: {hair_settings.hair_length}")

# ============================================
# 8. FORCE FIELDS
# ============================================
print("\n8. FORCE FIELDS - Wind and turbulence")

# Add wind force
bpy.ops.object.effector_add(type='WIND', location=(0, -8, 5))
wind = bpy.context.active_object
wind.name = "Wind"
wind.rotation_euler = (0, math.radians(90), 0)

wind_field = wind.field
wind_field.strength = 5.0
wind_field.noise = 0.5  # Turbulence
wind_field.use_max_distance = True
wind_field.distance_max = 10

print(f"  Created wind force field")
print(f"    Strength: {wind_field.strength}")
print(f"    Noise: {wind_field.noise}")

# Add turbulence force
bpy.ops.object.effector_add(type='TURBULENCE', location=(6, -8, 5))
turbulence = bpy.context.active_object
turbulence.name = "Turbulence"

turb_field = turbulence.field
turb_field.strength = 3.0
turb_field.noise = 1.0

print(f"  Created turbulence force field")

# ============================================
# 9. DYNAMIC PAINT
# ============================================
print("\n9. DYNAMIC PAINT - Paint canvas")

# Create canvas (receives paint)
bpy.ops.mesh.primitive_plane_add(size=6, location=(10, -5, 0.1))
canvas = bpy.context.active_object
canvas.name = "PaintCanvas"

# Add dynamic paint canvas
bpy.ops.object.modifier_add(type='DYNAMIC_PAINT')
canvas_modifier = canvas.modifiers["Dynamic Paint"]
bpy.ops.dpaint.type_toggle(type='CANVAS')

# Canvas settings
canvas_surface = canvas.modifiers["Dynamic Paint"].canvas_settings.canvas_surfaces["Surface"]
canvas_surface.surface_format = 'VERTEX'  # or 'IMAGE'
canvas_surface.surface_type = 'PAINT'  # 'PAINT', 'DISPLACE', 'WAVE'

print(f"  Created dynamic paint canvas")

# Create brush (applies paint)
bpy.ops.mesh.primitive_sphere_add(radius=0.5, location=(10, -5, 3))
brush = bpy.context.active_object
brush.name = "PaintBrush"

# Animate brush
scene.frame_set(1)
brush.location = (8, -3, 0.5)
brush.keyframe_insert(data_path="location", frame=1)

scene.frame_set(100)
brush.location = (12, -7, 0.5)
brush.keyframe_insert(data_path="location", frame=100)

# Add dynamic paint brush
bpy.ops.object.modifier_add(type='DYNAMIC_PAINT')
brush_modifier = brush.modifiers["Dynamic Paint"]
bpy.ops.dpaint.type_toggle(type='BRUSH')

print(f"  Created animated paint brush")

# ============================================
# 10. SMOKE SIMULATION (Quick Fire)
# ============================================
print("\n10. SMOKE/FIRE SIMULATION")

# Note: Smoke simulation is complex and requires domain + emitter
# Domain (contains the simulation)
bpy.ops.mesh.primitive_cube_add(size=6, location=(10, 5, 3))
smoke_domain = bpy.context.active_object
smoke_domain.name = "SmokeDomain"

# Add smoke domain
bpy.ops.object.quick_smoke()  # Quick setup
# This automatically sets up domain and flow

print(f"  Created smoke simulation (quick setup)")

# For manual setup (more control):
# bpy.ops.object.modifier_add(type='FLUID')
# smoke_domain.modifiers["Fluid"].fluid_type = 'DOMAIN'
# domain_settings = smoke_domain.modifiers["Fluid"].domain_settings
# domain_settings.domain_type = 'GAS'

# ============================================
# 11. OCEAN MODIFIER
# ============================================
print("\n11. OCEAN SIMULATION")

bpy.ops.mesh.primitive_plane_add(size=20, location=(30, 0, 0))
ocean_plane = bpy.context.active_object
ocean_plane.name = "Ocean"

# Subdivide for detail
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=10)
bpy.ops.object.mode_set(mode='OBJECT')

# Add ocean modifier
bpy.ops.object.modifier_add(type='OCEAN')
ocean_modifier = ocean_plane.modifiers["Ocean"]

ocean_modifier.resolution = 8  # Detail level
ocean_modifier.time = 1.0  # Animation time
ocean_modifier.depth = 10.0  # Ocean depth
ocean_modifier.wave_scale = 2.0  # Wave size
ocean_modifier.choppiness = 1.0  # Wave sharpness

# Animate ocean time
scene.frame_set(1)
ocean_modifier.time = 0
ocean_modifier.keyframe_insert(data_path="time", frame=1)

scene.frame_set(250)
ocean_modifier.time = 10
ocean_modifier.keyframe_insert(data_path="time", frame=250)

print(f"  Created ocean simulation")
print(f"    Resolution: {ocean_modifier.resolution}")
print(f"    Wave scale: {ocean_modifier.wave_scale}")

# ============================================
# 12. HELPER FUNCTIONS FOR PHYSICS
# ============================================
print("\n12. PHYSICS HELPER FUNCTIONS")

def add_rigid_body(obj, body_type='ACTIVE', mass=1.0, friction=0.5, restitution=0.3):
    """Add rigid body physics to an object"""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.rigidbody.object_add()

    obj.rigid_body.type = body_type
    obj.rigid_body.mass = mass
    obj.rigid_body.friction = friction
    obj.rigid_body.restitution = restitution

    return obj.rigid_body

def add_collision(obj):
    """Add collision modifier to an object"""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_add(type='COLLISION')

    return obj.modifiers["Collision"]

def setup_particle_emitter(obj, count=100, lifetime=50, size=0.1):
    """Set up basic particle emitter"""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_add(type='PARTICLE_SYSTEM')

    particle_sys = obj.particle_systems[0]
    settings = particle_sys.settings

    settings.count = count
    settings.lifetime = lifetime
    settings.particle_size = size

    return particle_sys

print(f"  Created helper functions:")
print(f"    - add_rigid_body()")
print(f"    - add_collision()")
print(f"    - setup_particle_emitter()")

# Example usage
test_cube = bpy.ops.mesh.primitive_cube_add(location=(0, 10, 5))
test_obj = bpy.context.active_object
test_obj.name = "PhysicsTest"
add_rigid_body(test_obj, mass=2.0, restitution=0.8)  # Very bouncy!

print(f"  Applied rigid body to test object")

# Reset to frame 1
scene.frame_set(1)

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 50)
print("PHYSICS SIMULATION SUMMARY")
print("=" * 50)
print("Rigid Body:")
print("  - ACTIVE: Moves with physics")
print("  - PASSIVE: Static collision object")
print("  - Properties: mass, friction, restitution")
print("\nSoft Body:")
print("  - Deformable objects (jello, cushions)")
print("  - Properties: pull, push, damping")
print("\nCloth:")
print("  - Fabric simulation")
print("  - Properties: mass, stiffness, damping")
print("\nParticles:")
print("  - EMITTER: Flowing particles (water, sparks)")
print("  - HAIR: Static strands (fur, grass)")
print("\nForce Fields:")
print("  - WIND, TURBULENCE, FORCE, VORTEX, etc.")
print("  - Affect particles and physics objects")
print("\nFluid/Smoke:")
print("  - Domain contains simulation")
print("  - Emitter creates fluid/smoke")
print("\nOcean:")
print("  - Procedural water simulation")
print("  - Animatable wave parameters")
print("\nTo see simulation:")
print("  - Press SPACEBAR to play animation")
print("  - Simulation bakes on playback")
print(f"  - Frame range: {scene.frame_start} to {scene.frame_end}")
