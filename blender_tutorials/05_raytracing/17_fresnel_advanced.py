"""
Blender Python Tutorial - Lesson 17: Fresnel and Advanced Optics
=================================================================

Advanced optical phenomena:
- Fresnel equations (Schlick's approximation)
- Viewing angle vs reflection amount
- Brewster's angle
- Color dispersion (chromatic aberration)
- Beer's Law (absorption)
- Subsurface scattering preview

These effects make materials look truly realistic!
"""

import bpy
import math
from mathutils import Vector
import random

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("=" * 70)
print("RAYTRACING MATHEMATICS - Part 4: Fresnel and Advanced Optics")
print("=" * 70)

# ============================================
# MATHEMATICAL FUNCTIONS
# ============================================

def fresnel_schlick(cos_theta, ior):
    """
    Schlick's approximation of Fresnel equations

    Gives the ratio of reflected vs refracted light
    based on viewing angle

    F(θ) = F₀ + (1 - F₀)(1 - cos(θ))⁵

    where:
    F₀ = ((n₁ - n₂)/(n₁ + n₂))²  # reflection at normal incidence
    cos(θ) = viewing angle
    """
    # F0 - reflection at normal incidence (looking straight at surface)
    r0 = ((1.0 - ior) / (1.0 + ior)) ** 2

    # Schlick's approximation
    fresnel = r0 + (1.0 - r0) * ((1.0 - cos_theta) ** 5)

    return fresnel

def beer_lambert_law(distance, absorption_color):
    """
    Beer-Lambert Law: light absorption through a medium

    I(d) = I₀ · e^(-αd)

    where:
    I(d) = intensity at distance d
    I₀ = initial intensity
    α = absorption coefficient
    d = distance traveled
    """
    # Absorption coefficients per channel (inverse of "color")
    # More absorption = darker that channel
    absorption = Vector((
        -math.log(max(absorption_color[0], 0.01)),
        -math.log(max(absorption_color[1], 0.01)),
        -math.log(max(absorption_color[2], 0.01))
    ))

    # Calculate transmission
    transmission = Vector((
        math.exp(-absorption.x * distance),
        math.exp(-absorption.y * distance),
        math.exp(-absorption.z * distance)
    ))

    return transmission

# ============================================
# HELPER FUNCTIONS
# ============================================

def create_sphere_demo(location, name, material_func):
    """Create a sphere with custom material"""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6, location=location, subdivisions=64)
    sphere = bpy.context.active_object
    sphere.name = name

    mat = material_func(name)
    sphere.data.materials.append(mat)

    return sphere

# ============================================
# 1. FRESNEL EFFECT VISUALIZATION
# ============================================
print("\n1. FRESNEL EFFECT - Reflection vs Viewing Angle")
print("   F(θ) = F₀ + (1 - F₀)(1 - cos(θ))⁵")

# Show how Fresnel varies with angle
print("\n   Fresnel reflectance at different viewing angles (IOR=1.5):")
print("   Angle    cos(θ)   Fresnel")
print("   " + "-" * 35)

angles_deg = [0, 30, 60, 75, 85, 89]
ior_glass = 1.5

for angle_deg in angles_deg:
    angle_rad = math.radians(angle_deg)
    cos_theta = math.cos(angle_rad)
    fresnel_value = fresnel_schlick(cos_theta, ior_glass)

    print(f"   {angle_deg:3d}°     {cos_theta:.3f}    {fresnel_value:.3f} ({fresnel_value*100:.1f}%)")

print("\n   ✓ At 0° (looking straight): ~4% reflection")
print("   ✓ At 89° (grazing angle): ~100% reflection")
print("   This is why water reflects more at shallow angles!")

# Create spheres showing Fresnel effect
def create_fresnel_material(name, ior=1.5):
    """Create material with Fresnel effect"""
    mat = bpy.data.materials.new(name=f"{name}_Fresnel_Mat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Output
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (600, 0)

    # Mix shader (glossy + glass)
    mix = nodes.new(type='ShaderNodeMixShader')
    mix.location = (400, 0)

    # Glossy (reflection)
    glossy = nodes.new(type='ShaderNodeBsdfGlossy')
    glossy.location = (200, 100)
    glossy.inputs['Color'].default_value = (1, 1, 1, 1)
    glossy.inputs['Roughness'].default_value = 0.0

    # Glass (refraction)
    glass = nodes.new(type='ShaderNodeBsdfGlass')
    glass.location = (200, -100)
    glass.inputs['Color'].default_value = (0.9, 0.95, 1, 1)
    glass.inputs['IOR'].default_value = ior
    glass.inputs['Roughness'].default_value = 0.0

    # Fresnel node
    fresnel = nodes.new(type='ShaderNodeFresnel')
    fresnel.location = (0, 0)
    fresnel.inputs['IOR'].default_value = ior

    # Connect
    links.new(fresnel.outputs['Fac'], mix.inputs['Fac'])
    links.new(glossy.outputs['BSDF'], mix.inputs[1])
    links.new(glass.outputs['BSDF'], mix.inputs[2])
    links.new(mix.outputs['Shader'], output.inputs['Surface'])

    return mat

# Create Fresnel spheres with different IORs
fresnel_spheres = [
    ((- 2, 0, 0.6), "Water", 1.33),
    ((0, 0, 0.6), "Glass", 1.5),
    ((2, 0, 0.6), "Diamond", 2.42),
]

for location, material_name, ior in fresnel_spheres:
    sphere = create_sphere_demo(
        location,
        f"Fresnel_{material_name}",
        lambda n: create_fresnel_material(n, ior)
    )

    # Add label
    bpy.ops.object.text_add(location=(location[0], location[1], -0.5))
    label = bpy.context.active_object
    label.data.body = f"{material_name}\nIOR={ior}"
    label.data.size = 0.2
    label.data.align_x = 'CENTER'

print(f"\n   ✓ Created spheres: Water (1.33), Glass (1.5), Diamond (2.42)")

# ============================================
# 2. CHROMATIC ABERRATION (Dispersion)
# ============================================
print("\n2. CHROMATIC ABERRATION - Color Dispersion")
print("   IOR varies with wavelength → rainbow effects")

# Different IORs for different wavelengths
print("\n   Glass IOR by wavelength:")
print("     Red:    1.510")
print("     Green:  1.520")
print("     Blue:   1.530")
print("   → This causes prisms to split white light into colors!")

# Create prism visualization
bpy.ops.mesh.primitive_cone_add(
    vertices=3,
    radius1=0.8,
    depth=1.5,
    location=(0, 3, 0.75)
)
prism = bpy.context.active_object
prism.name = "Prism"
prism.rotation_euler = (0, 0, 0)

# Prism material with dispersion simulation
prism_mat = bpy.data.materials.new(name="Prism_Mat")
prism_mat.use_nodes = True
prism_mat.blend_method = 'BLEND'

nodes = prism_mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
bsdf.inputs['Transmission'].default_value = 0.95
bsdf.inputs['IOR'].default_value = 1.52
bsdf.inputs['Roughness'].default_value = 0.0

prism.data.materials.append(prism_mat)

print("   ✓ Created glass prism")

# ============================================
# 3. BEER'S LAW - ABSORPTION
# ============================================
print("\n3. BEER'S LAW - Light Absorption")
print("   I(d) = I₀ · e^(-αd)")

# Demonstrate absorption through colored glass
print("\n   Light transmission through colored glass:")

absorption_tests = [
    ((1, 0.2, 0.2), "Red Glass"),
    ((0.2, 1, 0.2), "Green Glass"),
    ((0.2, 0.2, 1), "Blue Glass"),
]

distances = [0.1, 0.5, 1.0, 2.0]

for absorption_color, material_name in absorption_tests:
    print(f"\n   {material_name}:")
    print(f"     Distance  Transmission")
    for d in distances:
        transmission = beer_lambert_law(d, absorption_color)
        avg_transmission = (transmission.x + transmission.y + transmission.z) / 3
        print(f"     {d:.1f}m      {avg_transmission:.3f} ({avg_transmission*100:.1f}%)")

# Create colored glass spheres
colored_glass_y = 6

for i, (color, name) in enumerate(absorption_tests):
    x_pos = (i - 1) * 1.5

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.5,
        location=(x_pos, colored_glass_y, 0.5),
        subdivisions=64
    )
    sphere = bpy.context.active_object
    sphere.name = f"Absorption_{name}"

    # Colored glass material
    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Transmission'].default_value = 0.9
    bsdf.inputs['IOR'].default_value = 1.5
    bsdf.inputs['Roughness'].default_value = 0.0

    sphere.data.materials.append(mat)

print("\n   ✓ Created colored glass spheres")

# ============================================
# 4. BREWSTER'S ANGLE
# ============================================
print("\n4. BREWSTER'S ANGLE - Perfect Polarization")
print("   At Brewster's angle: reflected light is perfectly polarized")

# Brewster's angle formula: θB = arctan(n2/n1)
brewster_angle = math.degrees(math.atan(ior_glass / 1.0))

print(f"\n   Brewster's angle (air to glass): {brewster_angle:.1f}°")
print(f"   At this angle:")
print(f"     - Reflected light is 100% polarized")
print(f"     - Used in polarizing filters")
print(f"     - Photographers use this for anti-glare")

# ============================================
# 5. ADVANCED MATERIAL EXAMPLES
# ============================================
print("\n5. ADVANCED REALISTIC MATERIALS")

# Ground plane
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -0.5))
ground = bpy.context.active_object
ground.name = "Ground"

ground_mat = bpy.data.materials.new(name="Ground_Mat")
ground_mat.use_nodes = True

nodes = ground_mat.node_tree.nodes
links = ground_mat.node_tree.links

bsdf = nodes.get("Principled BSDF")

# Checker texture
checker = nodes.new(type='ShaderNodeTexChecker')
checker.location = (-400, 0)
checker.inputs['Scale'].default_value = 10

links.new(checker.outputs['Color'], bsdf.inputs['Base Color'])
bsdf.inputs['Roughness'].default_value = 0.7

ground.data.materials.append(ground_mat)

# Collection of realistic materials
advanced_materials = [
    # (location, name, material_function)
    ((6, -3, 0.6), "Frosted_Glass", lambda n: create_frosted_glass(n)),
    ((8, -3, 0.6), "Brushed_Metal", lambda n: create_brushed_metal(n)),
    ((6, -5, 0.6), "Gemstone", lambda n: create_gemstone(n)),
    ((8, -5, 0.6), "Opalescent", lambda n: create_opalescent(n)),
]

def create_frosted_glass(name):
    """Frosted glass with rough refraction"""
    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Transmission'].default_value = 0.9
    bsdf.inputs['Roughness'].default_value = 0.3  # Frosted!
    bsdf.inputs['IOR'].default_value = 1.5

    return mat

def create_brushed_metal(name):
    """Anisotropic metallic reflection"""
    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.9, 1)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.2
    bsdf.inputs['Anisotropic'].default_value = 0.8  # Brushed effect

    return mat

def create_gemstone(name):
    """High IOR gemstone with dispersion hint"""
    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0.2, 0.8, 0.3, 1)  # Emerald green
    bsdf.inputs['Transmission'].default_value = 0.95
    bsdf.inputs['IOR'].default_value = 2.42  # Diamond-like
    bsdf.inputs['Roughness'].default_value = 0.0

    return mat

def create_opalescent(name):
    """Sheen effect for fabric/pearl-like surfaces"""
    mat = bpy.data.materials.new(name=f"{name}_Mat")
    mat.use_nodes = True

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0.9, 0.85, 0.9, 1)
    bsdf.inputs['Sheen'].default_value = 1.0
    bsdf.inputs['Sheen Tint'].default_value = 0.8
    bsdf.inputs['Roughness'].default_value = 0.4

    return mat

for location, name, mat_func in advanced_materials:
    create_sphere_demo(location, name, mat_func)

print("   ✓ Created advanced material examples:")
print("     - Frosted glass (rough transmission)")
print("     - Brushed metal (anisotropic reflection)")
print("     - Gemstone (high IOR)")
print("     - Opalescent (sheen effect)")

# ============================================
# LIGHTING AND CAMERA
# ============================================

# Key light
bpy.ops.object.light_add(type='AREA', location=(5, -5, 8))
key_light = bpy.context.active_object
key_light.data.energy = 500
key_light.data.size = 3
key_light.rotation_euler = (math.radians(45), 0, math.radians(45))

# Fill light
bpy.ops.object.light_add(type='AREA', location=(-3, -3, 5))
fill_light = bpy.context.active_object
fill_light.data.energy = 200
fill_light.data.size = 2

# Rim light
bpy.ops.object.light_add(type='AREA', location=(0, 5, 3))
rim_light = bpy.context.active_object
rim_light.data.energy = 300
rim_light.data.size = 2

# Environment
world = bpy.context.scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links

bg = nodes.get('Background')
bg.inputs['Strength'].default_value = 0.3

# Add sky texture
sky = nodes.new(type='ShaderNodeTexSky')
sky.location = (-300, 300)
links.new(sky.outputs['Color'], bg.inputs['Color'])

# Camera
bpy.ops.object.camera_add(location=(8, -8, 5))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(65), 0, math.radians(45))
bpy.context.scene.camera = camera
camera.data.lens = 50
camera.data.dof.use_dof = True
camera.data.dof.focus_distance = 10
camera.data.dof.aperture_fstop = 2.8

# Render settings for better Fresnel/refraction
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 256
scene.cycles.use_denoising = True

# ============================================
# MATHEMATICAL SUMMARY
# ============================================
print("\n" + "=" * 70)
print("FRESNEL AND ADVANCED OPTICS MATHEMATICS")
print("=" * 70)

print("\n1. FRESNEL EQUATIONS (Schlick's Approximation):")
print("   F(θ) = F₀ + (1 - F₀)(1 - cos(θ))⁵")
print("   ")
print("   where:")
print("     F₀ = ((n₁ - n₂)/(n₁ + n₂))²")
print("     θ = angle between view direction and surface normal")
print("   ")
print("   Results:")
print("     - At normal incidence (0°): minimum reflection")
print("     - At grazing angles (85°+): nearly 100% reflection")
print("     - Creates realistic glass, water, etc.")

print("\n2. BEER-LAMBERT LAW (Absorption):")
print("   I(d) = I₀ · e^(-αd)")
print("   ")
print("   where:")
print("     I(d) = intensity after traveling distance d")
print("     I₀ = initial intensity")
print("     α = absorption coefficient")
print("     d = distance traveled through medium")
print("   ")
print("   Used for:")
print("     - Colored glass")
print("     - Water depth coloring")
print("     - Subsurface scattering")

print("\n3. BREWSTER'S ANGLE:")
print("   θB = arctan(n₂/n₁)")
print(f"   ")
print(f"   For air (1.0) to glass (1.5): {brewster_angle:.1f}°")
print("   ")
print("   At this angle:")
print("     - Reflected light is perfectly polarized")
print("     - Used in polarizing filters")

print("\n4. CHROMATIC ABERRATION:")
print("   IOR varies with wavelength:")
print("     IOR_red < IOR_green < IOR_blue")
print("   ")
print("   Causes:")
print("     - Prism rainbow effects")
print("     - Lens color fringing")
print("     - Diamond 'fire'")

print("\n5. REALISTIC RENDERING EQUATION:")
print("   L_o = L_e + ∫ f_r · L_i · cos(θ) dω")
print("   ")
print("   where:")
print("     L_o = outgoing light")
print("     L_e = emitted light")
print("     f_r = BRDF (Bidirectional Reflectance Distribution Function)")
print("     L_i = incoming light")
print("     θ = angle")
print("   ")
print("   Simplified: reflected = emitted + ∑(material × incoming)")

print("\n6. IMPLEMENTATION IN RAYTRACER:")
print("   At each ray-surface intersection:")
print("     1. Calculate Fresnel term F(θ)")
print("     2. Generate reflection ray with probability F")
print("     3. Generate refraction ray with probability (1-F)")
print("     4. Apply Beer's law if ray travels through medium")
print("     5. Accumulate color weighted by probability")

print("\n" + "=" * 70)
print("Render in Cycles for accurate Fresnel and refraction!")
print("Notice how spheres reflect more at edges - that's Fresnel!")
print("=" * 70)
