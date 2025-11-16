"""
Blender Python Tutorial - Lesson 18: Complete Raytracer Implementation
=======================================================================

BRINGING IT ALL TOGETHER!

A complete, working raytracer implementation that demonstrates:
- Camera ray generation
- Ray-sphere and ray-plane intersections
- Reflection and refraction
- Fresnel blending
- Multiple bounces
- Shadows
- Basic path tracing concepts
- Rendering to image

This is a simplified but functional raytracer showing how
all the mathematical concepts fit together!
"""

import bpy
import math
from mathutils import Vector, Color
import random
import time

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("=" * 70)
print("COMPLETE RAYTRACER IMPLEMENTATION")
print("=" * 70)

# ============================================
# SCENE DEFINITION
# ============================================

class Sphere:
    """Sphere object for raytracing"""
    def __init__(self, center, radius, material):
        self.center = Vector(center)
        self.radius = radius
        self.material = material

class Plane:
    """Infinite plane for raytracing"""
    def __init__(self, point, normal, material):
        self.point = Vector(point)
        self.normal = Vector(normal).normalized()
        self.material = material

class Material:
    """Material properties"""
    def __init__(self, color, emission, reflectivity=0.0, transparency=0.0, ior=1.0, roughness=0.0):
        self.color = Vector(color)
        self.emission = Vector(emission)
        self.reflectivity = reflectivity
        self.transparency = transparency
        self.ior = ior
        self.roughness = roughness

class Light:
    """Point light source"""
    def __init__(self, position, color, intensity):
        self.position = Vector(position)
        self.color = Vector(color)
        self.intensity = intensity

# ============================================
# RAYTRACING CORE FUNCTIONS
# ============================================

def ray_sphere_intersect(ray_origin, ray_direction, sphere):
    """
    Ray-sphere intersection
    Returns (hit, distance, normal)
    """
    oc = ray_origin - sphere.center
    a = ray_direction.dot(ray_direction)
    b = 2.0 * ray_direction.dot(oc)
    c = oc.dot(oc) - sphere.radius * sphere.radius

    discriminant = b*b - 4*a*c

    if discriminant < 0:
        return False, float('inf'), None

    # Closest hit
    t = (-b - math.sqrt(discriminant)) / (2*a)

    if t < 0.001:  # Avoid self-intersection
        t = (-b + math.sqrt(discriminant)) / (2*a)
        if t < 0.001:
            return False, float('inf'), None

    hit_point = ray_origin + ray_direction * t
    normal = (hit_point - sphere.center).normalized()

    return True, t, normal

def ray_plane_intersect(ray_origin, ray_direction, plane):
    """
    Ray-plane intersection
    Returns (hit, distance, normal)
    """
    denom = ray_direction.dot(plane.normal)

    if abs(denom) < 1e-6:
        return False, float('inf'), None

    t = (plane.point - ray_origin).dot(plane.normal) / denom

    if t < 0.001:
        return False, float('inf'), None

    # Flip normal if needed
    normal = plane.normal if denom < 0 else -plane.normal

    return True, t, normal

def find_nearest_intersection(ray_origin, ray_direction, scene_objects):
    """
    Find the closest intersection with scene objects
    Returns (object, distance, hit_point, normal)
    """
    nearest_obj = None
    nearest_t = float('inf')
    nearest_normal = None

    for obj in scene_objects:
        if isinstance(obj, Sphere):
            hit, t, normal = ray_sphere_intersect(ray_origin, ray_direction, obj)
        elif isinstance(obj, Plane):
            hit, t, normal = ray_plane_intersect(ray_origin, ray_direction, obj)
        else:
            continue

        if hit and t < nearest_t:
            nearest_t = t
            nearest_obj = obj
            nearest_normal = normal

    if nearest_obj:
        hit_point = ray_origin + ray_direction * nearest_t
        return nearest_obj, nearest_t, hit_point, nearest_normal

    return None, float('inf'), None, None

def calculate_reflection(incident, normal):
    """Calculate reflection direction"""
    return incident - 2.0 * incident.dot(normal) * normal

def calculate_refraction(incident, normal, eta):
    """Calculate refraction direction (Snell's law)"""
    cos_i = -incident.dot(normal)
    sin_t2 = eta * eta * (1.0 - cos_i * cos_i)

    if sin_t2 > 1.0:
        # Total internal reflection
        return None

    cos_t = math.sqrt(1.0 - sin_t2)
    return eta * incident + (eta * cos_i - cos_t) * normal

def fresnel_schlick(cos_theta, ior):
    """Schlick's approximation for Fresnel"""
    r0 = ((1.0 - ior) / (1.0 + ior)) ** 2
    return r0 + (1.0 - r0) * ((1.0 - cos_theta) ** 5)

def trace_ray(ray_origin, ray_direction, scene_objects, lights, depth=0, max_depth=3):
    """
    Recursive raytracing function

    This is the heart of the raytracer!
    """
    if depth > max_depth:
        return Vector((0, 0, 0))  # Max bounces reached

    # Find nearest intersection
    obj, t, hit_point, normal = find_nearest_intersection(ray_origin, ray_direction, scene_objects)

    if not obj:
        # No hit - return sky color
        sky_color = Vector((0.5, 0.7, 1.0)) * 0.3
        return sky_color

    material = obj.material

    # Start with emission
    color = material.emission.copy()

    # Shadow rays - check if point is lit
    for light in lights:
        # Direction to light
        light_dir = (light.position - hit_point).normalized()
        light_distance = (light.position - hit_point).length

        # Check for shadows
        shadow_obj, shadow_t, _, _ = find_nearest_intersection(
            hit_point + normal * 0.001,  # Offset to avoid self-intersection
            light_dir,
            scene_objects
        )

        in_shadow = shadow_obj and shadow_t < light_distance

        if not in_shadow:
            # Diffuse lighting (Lambert)
            diffuse_factor = max(0, normal.dot(light_dir))

            # Calculate light contribution
            light_contrib = Vector((
                light.color.x * light.intensity * diffuse_factor,
                light.color.y * light.intensity * diffuse_factor,
                light.color.z * light.intensity * diffuse_factor
            ))

            # Multiply by surface color
            color.x += material.color.x * light_contrib.x
            color.y += material.color.y * light_contrib.y
            color.z += material.color.z * light_contrib.z

    # Reflection
    if material.reflectivity > 0 and depth < max_depth:
        reflect_dir = calculate_reflection(ray_direction, normal)

        # Add some roughness (simple version)
        if material.roughness > 0:
            roughness_offset = Vector((
                (random.random() - 0.5) * material.roughness,
                (random.random() - 0.5) * material.roughness,
                (random.random() - 0.5) * material.roughness
            ))
            reflect_dir = (reflect_dir + roughness_offset).normalized()

        reflect_color = trace_ray(
            hit_point + normal * 0.001,
            reflect_dir,
            scene_objects,
            lights,
            depth + 1,
            max_depth
        )

        color += reflect_color * material.reflectivity

    # Refraction/Transparency
    if material.transparency > 0 and depth < max_depth:
        # Determine if entering or exiting material
        entering = ray_direction.dot(normal) < 0
        eta = 1.0 / material.ior if entering else material.ior

        refract_dir = calculate_refraction(ray_direction, normal, eta)

        if refract_dir:
            # Fresnel blend
            cos_theta = abs(ray_direction.dot(normal))
            fresnel = fresnel_schlick(cos_theta, material.ior)

            # Refracted ray
            refract_color = trace_ray(
                hit_point - normal * 0.001,  # Offset in opposite direction
                refract_dir,
                scene_objects,
                lights,
                depth + 1,
                max_depth
            )

            # Blend reflection and refraction based on Fresnel
            color += refract_color * material.transparency * (1.0 - fresnel)
        else:
            # Total internal reflection
            reflect_dir = calculate_reflection(ray_direction, normal)
            reflect_color = trace_ray(
                hit_point + normal * 0.001,
                reflect_dir,
                scene_objects,
                lights,
                depth + 1,
                max_depth
            )
            color += reflect_color * material.transparency

    return color

# ============================================
# SCENE SETUP
# ============================================

print("\n1. Building Scene...")

# Materials
mat_red_diffuse = Material(
    color=(0.8, 0.2, 0.2),
    emission=(0, 0, 0),
    reflectivity=0.1
)

mat_green_diffuse = Material(
    color=(0.2, 0.8, 0.2),
    emission=(0, 0, 0),
    reflectivity=0.1
)

mat_mirror = Material(
    color=(0.9, 0.9, 0.9),
    emission=(0, 0, 0),
    reflectivity=0.9,
    roughness=0.0
)

mat_glass = Material(
    color=(1, 1, 1),
    emission=(0, 0, 0),
    reflectivity=0.1,
    transparency=0.9,
    ior=1.5
)

mat_light = Material(
    color=(1, 1, 1),
    emission=(2, 2, 2)
)

mat_ground = Material(
    color=(0.5, 0.5, 0.5),
    emission=(0, 0, 0),
    reflectivity=0.05
)

# Scene objects
scene_objects = [
    Sphere((-1.5, 0, 0.5), 0.5, mat_red_diffuse),
    Sphere((0, 0, 0.5), 0.5, mat_mirror),
    Sphere((1.5, 0, 0.5), 0.5, mat_glass),
    Sphere((0, 2, 0.3), 0.3, mat_green_diffuse),
    Sphere((0, 2, 2), 0.3, mat_light),  # Light sphere
    Plane((0, 0, 0), (0, 0, 1), mat_ground),  # Ground
]

# Lights
lights = [
    Light((3, -3, 4), (1, 1, 1), 20),
    Light((-2, -2, 3), (1, 0.9, 0.8), 10),
]

print(f"   ✓ {len(scene_objects)} objects")
print(f"   ✓ {len(lights)} lights")

# ============================================
# RENDER FUNCTION
# ============================================

def render_image(width, height, camera_pos, camera_target, fov=60):
    """
    Render the scene to an image
    """
    print(f"\n2. Rendering {width}x{height} image...")

    # Camera setup
    aspect_ratio = width / height
    fov_rad = math.radians(fov)

    # Camera coordinate system
    forward = (camera_target - camera_pos).normalized()
    right = forward.cross(Vector((0, 0, 1))).normalized()
    up = right.cross(forward).normalized()

    # Viewport dimensions
    viewport_height = 2.0 * math.tan(fov_rad / 2.0)
    viewport_width = viewport_height * aspect_ratio

    # Create image
    pixels = []

    start_time = time.time()

    for y in range(height):
        if y % 10 == 0:
            progress = (y / height) * 100
            print(f"   Progress: {progress:.1f}%", end='\r')

        for x in range(width):
            # Calculate ray direction through pixel
            u = (x + 0.5) / width  # 0 to 1
            v = (y + 0.5) / height  # 0 to 1

            # Convert to -1 to 1
            u = u * 2 - 1
            v = v * 2 - 1

            # Flip Y (image coordinates)
            v = -v

            # Ray direction
            ray_dir = (
                forward +
                right * (u * viewport_width / 2) +
                up * (v * viewport_height / 2)
            ).normalized()

            # Trace ray
            color = trace_ray(camera_pos, ray_dir, scene_objects, lights, depth=0, max_depth=3)

            # Clamp color
            color.x = min(1.0, max(0.0, color.x))
            color.y = min(1.0, max(0.0, color.y))
            color.z = min(1.0, max(0.0, color.z))

            # Store pixel (Blender uses RGBA)
            pixels.extend([color.x, color.y, color.z, 1.0])

    elapsed = time.time() - start_time
    print(f"\n   ✓ Rendered in {elapsed:.2f} seconds")

    # Create image in Blender
    image_name = "Raytraced_Output"
    if image_name in bpy.data.images:
        bpy.data.images.remove(bpy.data.images[image_name])

    image = bpy.data.images.new(image_name, width, height, alpha=True)
    image.pixels = pixels

    print(f"   ✓ Image created: '{image_name}'")
    print(f"   (View in UV/Image Editor)")

    return image

# ============================================
# RENDER THE IMAGE
# ============================================

# Camera parameters
camera_position = Vector((5, -5, 3))
camera_target = Vector((0, 0, 0.5))

# Render (start small for speed)
width = 200
height = 150

rendered_image = render_image(width, height, camera_position, camera_target, fov=60)

# ============================================
# CREATE 3D SCENE VISUALIZATION
# ============================================

print("\n3. Creating 3D Scene Visualization...")

# Create visual representations of scene objects
for i, obj in enumerate(scene_objects):
    if isinstance(obj, Sphere):
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=obj.radius,
            location=obj.center
        )
        sphere = bpy.context.active_object
        sphere.name = f"Sphere_{i}"

        # Create material
        mat = bpy.data.materials.new(name=f"Mat_{i}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")

        bsdf.inputs['Base Color'].default_value = (*obj.material.color, 1)
        bsdf.inputs['Emission'].default_value = (*obj.material.emission, 1)
        bsdf.inputs['Emission Strength'].default_value = 1.0
        bsdf.inputs['Metallic'].default_value = obj.material.reflectivity
        bsdf.inputs['Transmission'].default_value = obj.material.transparency
        bsdf.inputs['IOR'].default_value = obj.material.ior

        sphere.data.materials.append(mat)

    elif isinstance(obj, Plane):
        bpy.ops.mesh.primitive_plane_add(
            size=20,
            location=obj.point
        )
        plane = bpy.context.active_object
        plane.name = f"Plane_{i}"

        mat = bpy.data.materials.new(name=f"Mat_Plane_{i}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = (*obj.material.color, 1)

        plane.data.materials.append(mat)

# Add lights
for i, light in enumerate(lights):
    bpy.ops.object.light_add(type='POINT', location=light.position)
    light_obj = bpy.context.active_object
    light_obj.name = f"Light_{i}"
    light_obj.data.energy = light.intensity * 10
    light_obj.data.color = light.color

# Add camera
bpy.ops.object.camera_add(location=camera_position)
camera = bpy.context.active_object
camera.rotation_euler = (camera_target - camera_position).to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = camera

# Display rendered image in background
# (Advanced: could be shown on a plane)

print("   ✓ 3D visualization created")

# ============================================
# STATISTICS AND SUMMARY
# ============================================

print("\n" + "=" * 70)
print("RAYTRACER IMPLEMENTATION COMPLETE!")
print("=" * 70)

print("\nFeatures Implemented:")
print("  ✓ Camera ray generation")
print("  ✓ Ray-sphere intersection")
print("  ✓ Ray-plane intersection")
print("  ✓ Perfect reflection")
print("  ✓ Refraction with Snell's Law")
print("  ✓ Fresnel blending")
print("  ✓ Total internal reflection")
print("  ✓ Recursive ray bounces")
print("  ✓ Shadow rays")
print("  ✓ Multiple light sources")
print("  ✓ Diffuse shading")
print("  ✓ Emission materials")

print("\nScene Contents:")
print(f"  • {len(scene_objects)} objects")
print(f"  • {len(lights)} lights")
print(f"  • Max ray depth: 3 bounces")
print(f"  • Image size: {width}x{height} pixels")
print(f"  • Total rays traced: ~{width * height * 4:,}")  # Approximate with bounces

print("\nHow It Works:")
print("  1. For each pixel:")
print("     a. Generate ray from camera through pixel")
print("     b. Find nearest intersection")
print("     c. Calculate lighting at hit point")
print("     d. Trace reflection/refraction rays recursively")
print("     e. Combine colors weighted by material properties")
print("  2. Shadow rays check light visibility")
print("  3. Fresnel determines reflection/refraction mix")

print("\nLimitations (for simplicity):")
print("  ⚠ No anti-aliasing (single sample per pixel)")
print("  ⚠ Simple lighting model (Lambert diffuse)")
print("  ⚠ No global illumination (indirect lighting)")
print("  ⚠ No texture mapping")
print("  ⚠ Limited primitive types (spheres, planes)")

print("\nImprovements for Production Raytracer:")
print("  → Multiple samples per pixel (anti-aliasing)")
print("  → Path tracing for global illumination")
print("  → Importance sampling")
print("  → BVH (Bounding Volume Hierarchy) acceleration")
print("  → More geometry types (triangles, meshes)")
print("  → Texture mapping")
print("  → Advanced BRDFs")
print("  → Denoising")

print("\n" + "=" * 70)
print(f"Rendered image: '{rendered_image.name}'")
print("View in UV/Image Editor or use Image Editor workspace")
print("Compare with Blender's Cycles render of the same scene!")
print("=" * 70)

print("\nCODE STRUCTURE:")
print("""
1. Scene Definition (Classes)
   - Sphere, Plane, Material, Light

2. Core Ray Functions
   - ray_sphere_intersect()
   - ray_plane_intersect()
   - find_nearest_intersection()

3. Optics Functions
   - calculate_reflection()
   - calculate_refraction()
   - fresnel_schlick()

4. Main Rendering
   - trace_ray() - Recursive raytracing
   - render_image() - Loop through pixels

5. Scene Setup
   - Define objects, materials, lights

6. Execute Render
   - Generate and save image
""")

print("\nThis raytracer demonstrates ALL the mathematics from")
print("the previous lessons working together in a real renderer!")
print("=" * 70)
