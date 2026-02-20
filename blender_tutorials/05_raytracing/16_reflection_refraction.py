"""
Blender Python Tutorial - Lesson 16: Reflection and Refraction
===============================================================

Physics and mathematics of light behavior:
- Perfect mirror reflection
- Reflection vector calculation
- Snell's Law for refraction
- Total internal reflection
- Index of refraction (IOR)
- Visualizing reflection and refraction rays
- Multiple bounces

This is how we get realistic glass, water, and mirrors!
"""

import bpy

import math
from mathutils import Vector
import random

def ensure_object_mode():
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')


# Clear the scene

ensure_object_mode()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("=" * 70)
print("RAYTRACING MATHEMATICS - Part 3: Reflection and Refraction")
print("=" * 70)

# ============================================
# HELPER FUNCTIONS
# ============================================

def create_ray_visual(origin, direction, length=5, name="Ray", color=(1, 0, 0), thickness=0.02):
    """Create visual representation of a ray"""
    direction = direction.normalized()
    end_point = origin + direction * length

    bpy.ops.mesh.primitive_cylinder_add(
        radius=thickness,
        depth=length,
        location=origin + direction * (length / 2)
    )
    ray = bpy.context.active_object
    ray.name = name

    z_axis = Vector((0, 0, 1))
    rotation_quat = z_axis.rotation_difference(direction)
    ray.rotation_euler = rotation_quat.to_euler()

    bpy.ops.mesh.primitive_cone_add(
        radius1=thickness * 3,
        radius2=0,
        depth=thickness * 10,
        location=end_point
    )
    arrow = bpy.context.active_object
    arrow.rotation_euler = rotation_quat.to_euler()
    arrow.parent = ray

    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Emission'].default_value = (*color, 1)
    bsdf.inputs['Emission Strength'].default_value = 2.5

    ray.data.materials.append(mat)
    arrow.data.materials.append(mat)

    return ray

def create_point(location, name="Point", color=(1, 1, 0), size=0.08):
    """Create a point marker"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=size, location=location)
    point = bpy.context.active_object
    point.name = name

    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Emission'].default_value = (*color, 1)
    bsdf.inputs['Emission Strength'].default_value = 4.0

    point.data.materials.append(mat)
    return point

# ============================================
# REFLECTION AND REFRACTION MATHEMATICS
# ============================================

def calculate_reflection(incident, normal):
    """
    Calculate perfect mirror reflection

    Formula: R = I - 2(I·N)N

    where:
    I = incident direction (pointing toward surface)
    N = surface normal
    R = reflected direction

    The dot product I·N tells us how much the incident
    ray is aligned with the normal.
    """
    # Ensure vectors are normalized
    incident = incident.normalized()
    normal = normal.normalized()

    # Calculate reflection
    # R = I - 2(I·N)N
    dot_in = incident.dot(normal)
    reflection = incident - 2 * dot_in * normal

    return reflection.normalized(), dot_in

def calculate_refraction(incident, normal, ior_from, ior_to):
    """
    Calculate refraction using Snell's Law

    Snell's Law: n₁ sin(θ₁) = n₂ sin(θ₂)

    where:
    n₁, n₂ = indices of refraction
    θ₁ = incident angle
    θ₂ = refracted angle

    Vector form:
    T = (n₁/n₂)[I - (I·N)N] - N√[1 - (n₁/n₂)²(1 - (I·N)²)]

    Returns None if total internal reflection occurs
    """
    incident = incident.normalized()
    normal = normal.normalized()

    # Ratio of indices
    eta = ior_from / ior_to

    # Cosine of incident angle
    cos_i = -incident.dot(normal)

    # Calculate discriminant for total internal reflection
    k = 1.0 - eta * eta * (1.0 - cos_i * cos_i)

    if k < 0:
        # Total internal reflection
        return None

    # Calculate refracted direction
    refracted = eta * incident + (eta * cos_i - math.sqrt(k)) * normal

    return refracted.normalized()

# ============================================
# 1. PERFECT MIRROR REFLECTION
# ============================================
print("\n1. PERFECT MIRROR REFLECTION")
print("   Formula: R = I - 2(I·N)N")

# Create mirror surface (plane)
mirror_pos = Vector((0, 0, 0))
mirror_normal = Vector((0, 0, 1))

bpy.ops.mesh.primitive_plane_add(size=4, location=mirror_pos)
mirror = bpy.context.active_object
mirror.name = "Mirror"

# Shiny mirror material
mirror_mat = bpy.data.materials.new(name="Mirror_Mat")
mirror_mat.use_nodes = True
bsdf = mirror_mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.9, 1)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.05
mirror.data.materials.append(mirror_mat)

# Visualize surface normal
create_ray_visual(mirror_pos, mirror_normal, length=1.5, name="Mirror_Normal", color=(0, 1, 1))

# Test different incident angles
incident_rays = [
    (Vector((0, 0, 3)), Vector((0, 0, -1)), "Perpendicular", 0),
    (Vector((-2, 0, 2)), Vector((1, 0, -1)), "45_Degrees", -2),
    (Vector((-3, 0, 1.5)), Vector((1, 0, -0.5)), "Shallow", -4),
]

print("\n   Testing reflection at different angles:")
for origin, incident_dir, name, x_offset in incident_rays:
    incident_dir = incident_dir.normalized()

    print(f"\n   {name}:")
    print(f"     Incident direction: {incident_dir}")

    # Calculate where ray hits mirror (simplified - assuming it hits)
    if abs(incident_dir.z) > 0.001:
        t = -origin.z / incident_dir.z
        hit_point = origin + incident_dir * t
        hit_point.z = 0  # Ensure on plane
    else:
        continue

    # Calculate reflection
    reflected_dir, dot_product = calculate_reflection(incident_dir, mirror_normal)

    print(f"     Hit point: {hit_point}")
    print(f"     I·N = {dot_product:.3f}")
    print(f"     Reflected direction: {reflected_dir}")
    print(f"     Incident angle: {math.degrees(math.acos(-dot_product)):.1f}°")
    print(f"     Reflection angle: {math.degrees(math.acos(reflected_dir.dot(mirror_normal))):.1f}°")

    # Visualize
    create_ray_visual(origin, incident_dir, length=t, name=f"Incident_{name}", color=(1, 0.5, 0))
    create_point(hit_point, f"Hit_{name}", (1, 0, 0), 0.08)
    create_ray_visual(hit_point, reflected_dir, length=3, name=f"Reflected_{name}", color=(0, 1, 0.5))

print("\n   ✓ Note: Angle of incidence = Angle of reflection")

# ============================================
# 2. REFRACTION - SNELL'S LAW
# ============================================
print("\n2. REFRACTION - Snell's Law")
print("   n₁ sin(θ₁) = n₂ sin(θ₂)")

# Create glass surface
glass_y = 5
glass_normal = Vector((0, 1, 0))

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, glass_y, 1))
glass_cube = bpy.context.active_object
glass_cube.name = "Glass_Block"
glass_cube.scale = (3, 2, 2)

# Glass material
glass_mat = bpy.data.materials.new(name="Glass_Mat")
glass_mat.use_nodes = True
glass_mat.blend_method = 'BLEND'
bsdf = glass_mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (0.9, 0.95, 1, 0.1)
bsdf.inputs['Transmission'].default_value = 0.95
bsdf.inputs['Roughness'].default_value = 0.0
bsdf.inputs['IOR'].default_value = 1.5
bsdf.inputs['Alpha'].default_value = 0.1
glass_cube.data.materials.append(glass_mat)

# Front surface of glass
glass_surface = Vector((0, glass_y - 1, 1))

# Visualize surface normal
create_ray_visual(glass_surface, glass_normal, length=1.0, name="Glass_Normal", color=(0, 1, 1))

# Test refraction with different IORs
ior_air = 1.0
ior_glass = 1.5
ior_water = 1.33

refraction_tests = [
    (Vector((-1, 2, 1)), Vector((0, 1, 0)), ior_air, ior_glass, "Air_to_Glass", 0),
    (Vector((0, 2, 1)), Vector((0.3, 1, 0)), ior_air, ior_glass, "Angled", 1),
    (Vector((1, 2, 1)), Vector((0.5, 1, 0)), ior_air, ior_water, "Air_to_Water", 2),
]

print("\n   Testing refraction:")
for origin, incident_dir, n1, n2, name, offset in refraction_tests:
    incident_dir = incident_dir.normalized()

    # Calculate hit point (simplified)
    t = (glass_surface.y - origin.y) / incident_dir.y
    hit_point = origin + incident_dir * t

    print(f"\n   {name}:")
    print(f"     n₁ = {n1} (incident medium)")
    print(f"     n₂ = {n2} (refracted medium)")
    print(f"     Incident: {incident_dir}")

    # Calculate refraction
    refracted_dir = calculate_refraction(incident_dir, glass_normal, n1, n2)

    if refracted_dir:
        # Calculate angles
        cos_i = -incident_dir.dot(glass_normal)
        cos_t = refracted_dir.dot(glass_normal)
        angle_i = math.degrees(math.acos(abs(cos_i)))
        angle_t = math.degrees(math.acos(abs(cos_t)))

        print(f"     Refracted: {refracted_dir}")
        print(f"     Incident angle: {angle_i:.1f}°")
        print(f"     Refracted angle: {angle_t:.1f}°")
        print(f"     Bent {'toward' if n2 > n1 else 'away from'} normal")

        # Visualize
        create_ray_visual(origin, incident_dir, length=t, name=f"Refract_In_{name}", color=(1, 1, 0))
        create_point(hit_point, f"Refract_Hit_{name}", (1, 0, 0), 0.06)
        create_ray_visual(hit_point, refracted_dir, length=2, name=f"Refract_Out_{name}", color=(0, 1, 1))
    else:
        print(f"     TOTAL INTERNAL REFLECTION!")

# ============================================
# 3. TOTAL INTERNAL REFLECTION
# ============================================
print("\n3. TOTAL INTERNAL REFLECTION")
print("   Occurs when light tries to exit to less dense medium at steep angle")

# Critical angle calculation
critical_angle = math.degrees(math.asin(ior_air / ior_glass))
print(f"\n   Critical angle (glass to air): {critical_angle:.1f}°")

# Create test scenario - light inside glass trying to exit
tir_surface = Vector((5, 5, 0))
tir_normal = Vector((0, 0, 1))  # Points up (into air)

# Glass floor
bpy.ops.mesh.primitive_plane_add(size=3, location=tir_surface)
glass_floor = bpy.context.active_object
glass_floor.name = "Glass_Floor"
glass_floor.data.materials.append(glass_mat)

create_ray_visual(tir_surface, tir_normal, length=1.0, name="TIR_Normal", color=(0, 1, 1))

# Test angles around critical angle
test_angles = [30, 40, 42, 45, 50, 60]  # Degrees from normal

print("\n   Testing angles from inside glass:")
for i, angle_deg in enumerate(test_angles):
    angle_rad = math.radians(angle_deg)

    # Incident direction (from inside glass, toward surface)
    incident_dir = Vector((math.sin(angle_rad), 0, math.cos(angle_rad)))

    origin = tir_surface - incident_dir * 1.5
    hit_point = tir_surface

    print(f"\n   {angle_deg}° from normal:")

    # Try to refract (glass to air)
    refracted_dir = calculate_refraction(incident_dir, tir_normal, ior_glass, ior_air)

    x_pos = 5 + (i - 2.5) * 1.2

    if refracted_dir:
        print(f"     → Refracts into air")
        create_ray_visual(
            Vector((x_pos, 0, origin.z)),
            Vector((0, 0, incident_dir.z)),
            length=1.5,
            name=f"TIR_In_{angle_deg}",
            color=(1, 1, 0),
            thickness=0.015
        )
        create_ray_visual(
            Vector((x_pos, 0, 0)),
            refracted_dir,
            length=1.5,
            name=f"TIR_Out_{angle_deg}",
            color=(0, 1, 1),
            thickness=0.015
        )
    else:
        print(f"     → TOTAL INTERNAL REFLECTION!")
        # Calculate reflection instead
        reflected_dir, _ = calculate_reflection(incident_dir, tir_normal)
        create_ray_visual(
            Vector((x_pos, 0, origin.z)),
            Vector((0, 0, incident_dir.z)),
            length=1.5,
            name=f"TIR_In_{angle_deg}",
            color=(1, 1, 0),
            thickness=0.015
        )
        create_ray_visual(
            Vector((x_pos, 0, 0)),
            reflected_dir,
            length=1.5,
            name=f"TIR_Reflect_{angle_deg}",
            color=(1, 0, 0),
            thickness=0.015
        )

# ============================================
# 4. MULTIPLE BOUNCES
# ============================================
print("\n4. MULTIPLE BOUNCES")
print("   Realistic raytracing traces rays through multiple reflections")

# Create a scene with multiple mirrors
bounce_y = -5

# Bottom mirror
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, bounce_y, -0.5))
bottom_mirror = bpy.context.active_object
bottom_mirror.name = "Bottom_Mirror"
bottom_mirror.data.materials.append(mirror_mat)

# Top mirror
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, bounce_y, 2.5))
top_mirror = bpy.context.active_object
top_mirror.name = "Top_Mirror"
top_mirror.rotation_euler = (math.pi, 0, 0)
top_mirror.data.materials.append(mirror_mat)

# Trace a ray bouncing between mirrors
ray_origin = Vector((-1.5, bounce_y, 0.5))
ray_dir = Vector((1, 0, 0.5)).normalized()

max_bounces = 6
current_origin = ray_origin.copy()
current_dir = ray_dir.copy()

print(f"\n   Tracing {max_bounces} bounces:")

for bounce in range(max_bounces):
    # Determine which surface we'll hit
    if current_dir.z > 0:
        # Heading up - hit top mirror
        normal = Vector((0, 0, -1))
        surface_z = 2.5
        surface_name = "top"
    else:
        # Heading down - hit bottom mirror
        normal = Vector((0, 0, 1))
        surface_z = -0.5
        surface_name = "bottom"

    # Calculate intersection
    t = (surface_z - current_origin.z) / current_dir.z
    hit_point = current_origin + current_dir * t

    # Stop if ray exits the mirror region
    if abs(hit_point.x) > 2 or t < 0.001:
        break

    print(f"     Bounce {bounce + 1}: hits {surface_name} mirror at {hit_point}")

    # Visualize this segment
    color = (
        1.0 - bounce / max_bounces,  # Red decreases
        bounce / max_bounces,          # Green increases
        0.5
    )

    create_ray_visual(
        current_origin,
        current_dir,
        length=t,
        name=f"Bounce_{bounce}",
        color=color,
        thickness=0.015
    )

    create_point(hit_point, f"Bounce_Point_{bounce}", (1, 1, 0), 0.04)

    # Calculate reflection for next bounce
    reflected_dir, _ = calculate_reflection(current_dir, normal)

    # Setup for next iteration
    current_origin = hit_point + reflected_dir * 0.001  # Small offset
    current_dir = reflected_dir

print(f"\n   ✓ Ray bounced {bounce + 1} times before exiting")

# ============================================
# 5. FRESNEL REFLECTION (Preview)
# ============================================
print("\n5. FRESNEL EFFECT (Preview - full detail in next lesson)")
print("   Real materials reflect AND refract based on viewing angle")

# Create sphere to show Fresnel effect
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, -10, 1))
fresnel_sphere = bpy.context.active_object
fresnel_sphere.name = "Fresnel_Sphere"

# Fresnel material
fresnel_mat = bpy.data.materials.new(name="Fresnel_Mat")
fresnel_mat.use_nodes = True
fresnel_mat.blend_method = 'BLEND'

nodes = fresnel_mat.node_tree.nodes
links = fresnel_mat.node_tree.links

# Clear default
nodes.clear()

# Create nodes
output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (400, 0)

mix_shader = nodes.new(type='ShaderNodeMixShader')
mix_shader.location = (200, 0)

glossy = nodes.new(type='ShaderNodeBsdfGlossy')
glossy.location = (0, 100)

glass = nodes.new(type='ShaderNodeBsdfGlass')
glass.location = (0, -100)
glass.inputs['IOR'].default_value = 1.5

fresnel = nodes.new(type='ShaderNodeFresnel')
fresnel.location = (-200, 0)
fresnel.inputs['IOR'].default_value = 1.5

# Connect
links.new(fresnel.outputs['Fac'], mix_shader.inputs['Fac'])
links.new(glossy.outputs['BSDF'], mix_shader.inputs[1])
links.new(glass.outputs['BSDF'], mix_shader.inputs[2])
links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

fresnel_sphere.data.materials.append(fresnel_mat)

print("   ✓ Fresnel effect: more reflection at grazing angles")
print("   ✓ More refraction when looking straight at surface")

# ============================================
# SCENE SETUP
# ============================================

# Lighting
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sun = bpy.context.active_object
sun.data.energy = 3.0
sun.rotation_euler = (math.radians(45), 0, math.radians(45))

# Camera
bpy.ops.object.camera_add(location=(8, -8, 6))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(55), 0, math.radians(45))
bpy.context.scene.camera = camera
camera.data.lens = 50

# Dark background
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (0.01, 0.01, 0.02, 1)
bg.inputs['Strength'].default_value = 0.1

# ============================================
# MATHEMATICAL SUMMARY
# ============================================
print("\n" + "=" * 70)
print("REFLECTION AND REFRACTION MATHEMATICS")
print("=" * 70)

print("\n1. REFLECTION (Mirror):")
print("   R = I - 2(I·N)N")
print("   ")
print("   where:")
print("     I = incident direction (toward surface)")
print("     N = surface normal")
print("     R = reflected direction")
print("   ")
print("   Law: θᵢ = θᵣ (angle in = angle out)")

print("\n2. REFRACTION (Snell's Law):")
print("   n₁ sin(θ₁) = n₂ sin(θ₂)")
print("   ")
print("   Vector form:")
print("   T = (n₁/n₂)I + [n₁/n₂ · cos(θ₁) - cos(θ₂)]N")
print("   ")
print("   Common IOR values:")
print("     Vacuum: 1.0")
print("     Air: 1.000293 (≈ 1.0)")
print("     Water: 1.33")
print("     Glass: 1.5 - 1.9")
print("     Diamond: 2.42")

print("\n3. TOTAL INTERNAL REFLECTION:")
print("   Occurs when: n₁ > n₂ AND θ₁ > θc")
print("   ")
print("   Critical angle: θc = arcsin(n₂/n₁)")
print("   ")
print("   For glass to air:")
print(f"     θc = arcsin(1.0/1.5) = {critical_angle:.1f}°")
print("   ")
print("   Beyond critical angle: complete reflection, no refraction")

print("\n4. WHEN TO USE WHAT:")
print("   Reflection:")
print("     - Mirrors")
print("     - Metallic surfaces")
print("     - Glancing angles on any surface")
print("   ")
print("   Refraction:")
print("     - Glass")
print("     - Water")
print("     - Any transparent material")
print("   ")
print("   Both (Fresnel):")
print("     - Realistic materials (next lesson)")
print("     - Mix based on viewing angle")

print("\n5. RAYTRACING WITH BOUNCES:")
print("   for each ray:")
print("     for bounce in range(max_bounces):")
print("       1. Find nearest intersection")
print("       2. Calculate surface normal")
print("       3. Compute reflected/refracted ray")
print("       4. Trace new ray from hit point")
print("       5. Accumulate color")

print("\n" + "=" * 70)
print("Color coding in scene:")
print("  🟡 YELLOW/ORANGE - Incident rays")
print("  🟢 GREEN/CYAN    - Reflected/refracted rays")
print("  🔴 RED           - Total internal reflection")
print("  🔵 CYAN arrows   - Surface normals")
print("=" * 70)
