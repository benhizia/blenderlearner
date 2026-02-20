"""
Blender Python Tutorial - Lesson 19: Interactive Raytracing Visualization
==========================================================================

This tutorial combines visual demonstrations with animated text explanations!
Watch as mathematical formulas and concepts appear as 3D text next to
the actual raytracing visualizations.

Perfect for visual learners who want to see the math come alive!

Features:
- Animated text panels explaining each concept
- Mathematical formulas displayed as 3D text
- Color-coded explanations matching visual elements
- Sequential reveals showing step-by-step math
- Interactive timeline you can scrub through
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
print("INTERACTIVE RAYTRACING VISUALIZATION")
print("Press SPACEBAR to play the animation and see math come alive!")
print("=" * 70)

# ============================================
# TEXT DISPLAY SYSTEM
# ============================================

class TextPanel:
    """Creates animated text panels in 3D space"""
    def __init__(self, location, name="TextPanel"):
        self.location = Vector(location)
        self.name = name
        self.text_objects = []
        self.current_y_offset = 0

    def add_title(self, text, color=(1, 1, 0), size=0.4):
        """Add a title line"""
        text_obj = self._create_text(text, size, color)
        text_obj.location = self.location + Vector((0, 0, self.current_y_offset))
        self.current_y_offset -= size * 1.5
        self.text_objects.append(text_obj)
        return text_obj

    def add_line(self, text, color=(1, 1, 1), size=0.25):
        """Add a regular text line"""
        text_obj = self._create_text(text, size, color)
        text_obj.location = self.location + Vector((0, 0, self.current_y_offset))
        self.current_y_offset -= size * 1.2
        self.text_objects.append(text_obj)
        return text_obj

    def add_formula(self, text, color=(0.5, 1, 0.5), size=0.3):
        """Add a mathematical formula"""
        text_obj = self._create_text(text, size, color)
        text_obj.location = self.location + Vector((0, 0, self.current_y_offset))
        self.current_y_offset -= size * 1.3
        self.text_objects.append(text_obj)
        return text_obj

    def add_spacer(self, amount=0.3):
        """Add vertical space"""
        self.current_y_offset -= amount

    def _create_text(self, text, size, color):
        """Internal: Create a text object"""
        bpy.ops.object.text_add()
        text_obj = bpy.context.active_object
        text_obj.data.body = text
        text_obj.data.size = size
        text_obj.data.align_x = 'LEFT'
        text_obj.data.align_y = 'TOP'
        text_obj.name = f"{self.name}_{len(self.text_objects)}"

        # Create glowing material
        mat = bpy.data.materials.new(name=f"TextMat_{text_obj.name}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = (*color, 1)
        bsdf.inputs['Emission'].default_value = (*color, 1)
        bsdf.inputs['Emission Strength'].default_value = 2.0

        text_obj.data.materials.append(mat)

        # Start invisible
        text_obj.hide_viewport = True
        text_obj.hide_render = True

        return text_obj

    def animate_reveal(self, start_frame, duration=10):
        """Animate all text to appear sequentially"""
        current_frame = start_frame

        for text_obj in self.text_objects:
            # Keyframe: hidden
            text_obj.hide_viewport = True
            text_obj.hide_render = True
            text_obj.keyframe_insert(data_path="hide_viewport", frame=current_frame)
            text_obj.keyframe_insert(data_path="hide_render", frame=current_frame)

            # Keyframe: visible
            current_frame += duration
            text_obj.hide_viewport = False
            text_obj.hide_render = False
            text_obj.keyframe_insert(data_path="hide_viewport", frame=current_frame)
            text_obj.keyframe_insert(data_path="hide_render", frame=current_frame)

            # Scale animation for dramatic effect
            text_obj.scale = (0.1, 0.1, 0.1)
            text_obj.keyframe_insert(data_path="scale", frame=current_frame - duration)

            text_obj.scale = (1, 1, 1)
            text_obj.keyframe_insert(data_path="scale", frame=current_frame)

# ============================================
# VISUAL HELPER FUNCTIONS
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
    bsdf.inputs['Emission Strength'].default_value = 3.0

    ray.data.materials.append(mat)
    arrow.data.materials.append(mat)

    # Start invisible
    ray.hide_viewport = True
    ray.hide_render = True
    arrow.hide_viewport = True
    arrow.hide_render = True

    return ray, arrow

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
    bsdf.inputs['Emission Strength'].default_value = 5.0

    point.data.materials.append(mat)

    point.hide_viewport = True
    point.hide_render = True

    return point

def animate_visibility(obj, show_frame, hide_frame=None):
    """Animate object visibility"""
    # Hidden before
    obj.hide_viewport = True
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide_viewport", frame=show_frame - 1)
    obj.keyframe_insert(data_path="hide_render", frame=show_frame - 1)

    # Visible at show_frame
    obj.hide_viewport = False
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide_viewport", frame=show_frame)
    obj.keyframe_insert(data_path="hide_render", frame=show_frame)

    # Hide again if specified
    if hide_frame:
        obj.hide_viewport = True
        obj.hide_render = True
        obj.keyframe_insert(data_path="hide_viewport", frame=hide_frame)
        obj.keyframe_insert(data_path="hide_render", frame=hide_frame)

# ============================================
# SCENE SETUP
# ============================================

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 500

# Dark background
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (0.02, 0.02, 0.03, 1)
bg.inputs['Strength'].default_value = 0.2

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(10, -10, 10))
sun = bpy.context.active_object
sun.data.energy = 1.5

# Camera
bpy.ops.object.camera_add(location=(15, -8, 8))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(60))
scene.camera = camera

# ============================================
# CHAPTER 1: THE RAY EQUATION (Frames 1-120)
# ============================================

print("\nChapter 1: The Ray Equation")

# Text panel
panel1 = TextPanel(location=(-8, 2, 3), name="Panel_RayEquation")
panel1.add_title("THE RAY EQUATION", color=(1, 1, 0))
panel1.add_spacer()
panel1.add_formula("P(t) = O + t*D", color=(0.5, 1, 0.5))
panel1.add_spacer()
panel1.add_line("Where:", color=(0.8, 0.8, 1))
panel1.add_line("P(t) = Point on ray", color=(1, 1, 1))
panel1.add_line("O = Origin", color=(1, 1, 0))
panel1.add_line("D = Direction", color=(1, 0.5, 0))
panel1.add_line("t = Parameter", color=(0.5, 1, 1))
panel1.add_spacer()
panel1.add_line("Example:", color=(0.8, 0.8, 1))
panel1.add_line("O = (0, 0, 0)", color=(1, 1, 0))
panel1.add_line("D = (1, 0, 0)", color=(1, 0.5, 0))
panel1.add_line("t = 0 to 5", color=(0.5, 1, 1))

panel1.animate_reveal(start_frame=10, duration=8)

# Create the actual ray
ray_origin = Vector((0, 0, 0))
ray_direction = Vector((1, 0, 0))

create_point(ray_origin, "Origin", color=(1, 1, 0), size=0.1)
animate_visibility(bpy.context.active_object, show_frame=20)

ray, arrow = create_ray_visual(ray_origin, ray_direction, length=5, name="Example_Ray", color=(1, 0.5, 0))
animate_visibility(ray, show_frame=60)
animate_visibility(arrow, show_frame=60)

# Animate points along the ray
for t in range(6):
    point_pos = ray_origin + ray_direction * t
    point = create_point(point_pos, f"P_t{t}", color=(0.5, 1, 1), size=0.06)
    animate_visibility(point, show_frame=80 + t * 5)

# ============================================
# CHAPTER 2: RAY-SPHERE INTERSECTION (Frames 121-280)
# ============================================

print("\nChapter 2: Ray-Sphere Intersection")

# Text panel
panel2 = TextPanel(location=(-8, -3, 3), name="Panel_Sphere")
panel2.add_title("RAY-SPHERE INTERSECTION", color=(1, 1, 0))
panel2.add_spacer()
panel2.add_line("Sphere equation:", color=(0.8, 0.8, 1))
panel2.add_formula("|P - C|^2 = r^2", color=(0.5, 1, 0.5))
panel2.add_spacer()
panel2.add_line("Substitute ray:", color=(0.8, 0.8, 1))
panel2.add_formula("|O + tD - C|^2 = r^2", color=(0.5, 1, 0.5))
panel2.add_spacer()
panel2.add_line("Gives quadratic:", color=(0.8, 0.8, 1))
panel2.add_formula("at^2 + bt + c = 0", color=(1, 0.5, 0.5))
panel2.add_spacer()
panel2.add_line("a = D.D = 1", color=(1, 1, 1))
panel2.add_line("b = 2D.(O-C)", color=(1, 1, 1))
panel2.add_line("c = |O-C|^2 - r^2", color=(1, 1, 1))
panel2.add_spacer()
panel2.add_line("Discriminant:", color=(0.8, 0.8, 1))
panel2.add_formula("D = b^2 - 4ac", color=(1, 1, 0.5))
panel2.add_spacer()
panel2.add_line("If D < 0: No hit", color=(1, 0.5, 0.5))
panel2.add_line("If D >= 0: Hit!", color=(0.5, 1, 0.5))

panel2.animate_reveal(start_frame=130, duration=6)

# Create sphere
sphere_center = Vector((3, 0, 1))
sphere_radius = 1.0

bpy.ops.mesh.primitive_uv_sphere_add(radius=sphere_radius, location=sphere_center)
sphere = bpy.context.active_object
sphere.name = "Target_Sphere"

mat = bpy.data.materials.new(name="Sphere_Mat")
mat.use_nodes = True
mat.blend_method = 'BLEND'
bsdf = mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (0.3, 0.6, 1, 0.4)
bsdf.inputs['Alpha'].default_value = 0.4
bsdf.inputs['Transmission'].default_value = 0.3
sphere.data.materials.append(mat)

sphere.hide_viewport = True
sphere.hide_render = True
animate_visibility(sphere, show_frame=180)

# Ray that hits
hit_ray_origin = Vector((0, 0, 1))
hit_ray_direction = (sphere_center - hit_ray_origin).normalized()

hit_ray, hit_arrow = create_ray_visual(hit_ray_origin, hit_ray_direction, length=5, name="Hit_Ray", color=(0, 1, 0))
animate_visibility(hit_ray, show_frame=220)
animate_visibility(hit_arrow, show_frame=220)

# Calculate actual intersection
oc = hit_ray_origin - sphere_center
a = 1.0
b = 2.0 * hit_ray_direction.dot(oc)
c = oc.dot(oc) - sphere_radius * sphere_radius
discriminant = b*b - 4*a*c
t = (-b - math.sqrt(discriminant)) / (2*a)
hit_point = hit_ray_origin + hit_ray_direction * t

hit_marker = create_point(hit_point, "Hit_Point", color=(1, 0, 0), size=0.12)
animate_visibility(hit_marker, show_frame=250)

# Surface normal
normal = (hit_point - sphere_center).normalized()
normal_ray, normal_arrow = create_ray_visual(hit_point, normal, length=1.5, name="Normal", color=(0, 1, 1))
animate_visibility(normal_ray, show_frame=260)
animate_visibility(normal_arrow, show_frame=260)

# ============================================
# CHAPTER 3: REFLECTION (Frames 281-400)
# ============================================

print("\nChapter 3: Reflection")

# Text panel
panel3 = TextPanel(location=(5, -3, 3), name="Panel_Reflection")
panel3.add_title("REFLECTION", color=(1, 1, 0))
panel3.add_spacer()
panel3.add_formula("R = I - 2(I.N)N", color=(0.5, 1, 0.5))
panel3.add_spacer()
panel3.add_line("Where:", color=(0.8, 0.8, 1))
panel3.add_line("R = Reflected ray", color=(0, 1, 0.5))
panel3.add_line("I = Incident ray", color=(1, 1, 0))
panel3.add_line("N = Surface normal", color=(0, 1, 1))
panel3.add_spacer()
panel3.add_line("Law of reflection:", color=(0.8, 0.8, 1))
panel3.add_line("Angle in = Angle out", color=(1, 1, 1))

panel3.animate_reveal(start_frame=290, duration=8)

# Create mirror
bpy.ops.mesh.primitive_plane_add(size=3, location=(5, 0, 0))
mirror = bpy.context.active_object
mirror.name = "Mirror"
mirror.rotation_euler = (0, math.radians(90), 0)

mirror_mat = bpy.data.materials.new(name="Mirror_Mat")
mirror_mat.use_nodes = True
bsdf = mirror_mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.05
mirror.data.materials.append(mirror_mat)

mirror.hide_viewport = True
mirror.hide_render = True
animate_visibility(mirror, show_frame=330)

# Incident ray to mirror
incident_origin = Vector((7, -2, 1))
incident_dir = Vector((-1, 1, -0.3)).normalized()

incident_ray, incident_arrow = create_ray_visual(
    incident_origin, incident_dir, length=2.5,
    name="Incident_Ray", color=(1, 1, 0)
)
animate_visibility(incident_ray, show_frame=350)
animate_visibility(incident_arrow, show_frame=350)

# Hit point on mirror
mirror_hit = Vector((5, 0, 0.5))
hit_marker2 = create_point(mirror_hit, "Mirror_Hit", color=(1, 0, 0), size=0.1)
animate_visibility(hit_marker2, show_frame=360)

# Surface normal
mirror_normal = Vector((-1, 0, 0))
normal_ray2, normal_arrow2 = create_ray_visual(
    mirror_hit, mirror_normal, length=1,
    name="Mirror_Normal", color=(0, 1, 1)
)
animate_visibility(normal_ray2, show_frame=365)
animate_visibility(normal_arrow2, show_frame=365)

# Reflected ray
reflected_dir = incident_dir - 2.0 * incident_dir.dot(mirror_normal) * mirror_normal
reflected_ray, reflected_arrow = create_ray_visual(
    mirror_hit, reflected_dir, length=2.5,
    name="Reflected_Ray", color=(0, 1, 0.5)
)
animate_visibility(reflected_ray, show_frame=380)
animate_visibility(reflected_arrow, show_frame=380)

# ============================================
# CHAPTER 4: FRESNEL EFFECT (Frames 401-500)
# ============================================

print("\nChapter 4: Fresnel Effect")

# Text panel
panel4 = TextPanel(location=(-8, 5, 3), name="Panel_Fresnel")
panel4.add_title("FRESNEL EFFECT", color=(1, 1, 0))
panel4.add_spacer()
panel4.add_line("Schlick's approximation:", color=(0.8, 0.8, 1))
panel4.add_formula("F = F0 + (1-F0)(1-cos)^5", color=(0.5, 1, 0.5))
panel4.add_spacer()
panel4.add_line("Where:", color=(0.8, 0.8, 1))
panel4.add_formula("F0 = ((n1-n2)/(n1+n2))^2", color=(1, 1, 0.5))
panel4.add_spacer()
panel4.add_line("Result:", color=(0.8, 0.8, 1))
panel4.add_line("0 degrees: ~4% reflect", color=(1, 1, 1))
panel4.add_line("89 degrees: ~100% reflect", color=(1, 1, 1))
panel4.add_spacer()
panel4.add_line("Makes glass look real!", color=(0.5, 1, 0.5))

panel4.animate_reveal(start_frame=410, duration=7)

# Create glass sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(0, 5, 1), subdivisions=64)
glass_sphere = bpy.context.active_object
glass_sphere.name = "Fresnel_Sphere"

# Fresnel material
fresnel_mat = bpy.data.materials.new(name="Fresnel_Mat")
fresnel_mat.use_nodes = True
fresnel_mat.blend_method = 'BLEND'

nodes = fresnel_mat.node_tree.nodes
links = fresnel_mat.node_tree.links
nodes.clear()

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

links.new(fresnel.outputs['Fac'], mix_shader.inputs['Fac'])
links.new(glossy.outputs['BSDF'], mix_shader.inputs[1])
links.new(glass.outputs['BSDF'], mix_shader.inputs[2])
links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])

glass_sphere.data.materials.append(fresnel_mat)

glass_sphere.hide_viewport = True
glass_sphere.hide_render = True
animate_visibility(glass_sphere, show_frame=450)

# Rays showing Fresnel at different angles
fresnel_rays = [
    (Vector((-2, 5, 1)), Vector((1, 0, 0)), "Perpendicular", 0.04),  # Low reflection
    (Vector((-1, 5, 2.5)), Vector((1, 0, -1.5)), "Grazing", 0.95),   # High reflection
]

for i, (origin, direction, name, fresnel_val) in enumerate(fresnel_rays):
    # Incident ray
    inc_ray, inc_arrow = create_ray_visual(
        origin, direction.normalized(), length=1.5,
        name=f"Fresnel_Inc_{name}",
        color=(1, 1, 0)
    )
    animate_visibility(inc_ray, show_frame=470 + i * 15)
    animate_visibility(inc_arrow, show_frame=470 + i * 15)

# ============================================
# TIMELINE MARKERS
# ============================================

# Add timeline markers for easy navigation
scene.timeline_markers.new("1: Ray Equation", frame=10)
scene.timeline_markers.new("2: Intersection", frame=130)
scene.timeline_markers.new("3: Reflection", frame=290)
scene.timeline_markers.new("4: Fresnel", frame=410)

# ============================================
# FINAL TOUCHES
# ============================================

# Add area light for better illumination
bpy.ops.object.light_add(type='AREA', location=(-5, -5, 6))
area_light = bpy.context.active_object
area_light.data.energy = 200
area_light.data.size = 3

# Set playback to 24 fps
scene.render.fps = 24

# Enable motion blur for smoother animation
scene.render.use_motion_blur = True

# ============================================
# SUMMARY
# ============================================

print("\n" + "=" * 70)
print("INTERACTIVE RAYTRACING VISUALIZATION CREATED!")
print("=" * 70)

print("\n📺 HOW TO USE:")
print("  1. Press SPACEBAR to play the animation")
print("  2. Watch math explanations appear as 3D text")
print("  3. Scrub the timeline to review any section")
print("  4. Use timeline markers to jump between chapters")

print("\n📖 CHAPTERS:")
print("  Frame 1-120:   The Ray Equation")
print("  Frame 121-280: Ray-Sphere Intersection")
print("  Frame 281-400: Reflection")
print("  Frame 401-500: Fresnel Effect")

print("\n🎨 VISUAL ELEMENTS:")
print("  🟡 Yellow text   - Titles")
print("  🟢 Green text    - Formulas")
print("  ⚪ White text    - Explanations")
print("  🟡 Yellow rays   - Incident rays")
print("  🟢 Green rays    - Reflected/successful rays")
print("  🔵 Cyan arrows   - Surface normals")
print("  🔴 Red points    - Intersection points")

print("\n⚙️  FEATURES:")
print("  ✓ Sequential text reveals")
print("  ✓ Synchronized visual demos")
print("  ✓ Color-coded elements")
print("  ✓ Timeline markers")
print("  ✓ Scale animations")
print("  ✓ Glowing materials")

print("\n💡 TIPS:")
print("  • Pause at any frame to study the math")
print("  • Click on text panels in outliner to select all text")
print("  • Render animation for presentation (Ctrl+F12)")
print("  • Export as video to share!")

print("\n" + "=" * 70)
print("This is perfect for:")
print("  📚 Teaching raytracing concepts")
print("  🎓 Presentations and lectures")
print("  🎬 Tutorial videos")
print("  📖 Visual learning")
print("  🚀 Understanding render engines")
print("=" * 70)

print("\n🎬 PRESS SPACEBAR TO START THE SHOW!")
