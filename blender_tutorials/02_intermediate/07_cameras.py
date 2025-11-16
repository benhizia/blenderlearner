"""
Blender Python Tutorial - Lesson 7: Cameras
============================================

Learn how to work with cameras:
- Creating and positioning cameras
- Camera properties (focal length, sensor size)
- Aiming cameras at targets
- Camera constraints
- Multiple cameras and switching
- Depth of field
- Animating cameras
"""

import bpy
import math

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("Demonstrating cameras in Blender...\n")

# Create a simple scene to photograph
# Ground
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))

# Some objects to look at
bpy.ops.mesh.primitive_monkey_add(location=(0, 0, 1))
suzanne = bpy.context.active_object
suzanne.name = "Suzanne"

bpy.ops.mesh.primitive_cube_add(location=(-3, 0, 0.5))
bpy.ops.mesh.primitive_sphere_add(location=(3, 0, 0.5))

# Add a light
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sun = bpy.context.active_object
sun.data.energy = 3.0

print("Created scene with objects\n")

# ============================================
# 1. CREATING A BASIC CAMERA
# ============================================
print("1. CREATING A BASIC CAMERA")

bpy.ops.object.camera_add(location=(7, -7, 5))
camera = bpy.context.active_object
camera.name = "MainCamera"

# Set as the active camera for the scene
bpy.context.scene.camera = camera

print(f"  Created {camera.name} at {camera.location}")
print(f"  Set as active scene camera")

# ============================================
# 2. CAMERA PROPERTIES
# ============================================
print("\n2. CAMERA PROPERTIES")

# Access camera data
cam_data = camera.data

# Focal length (affects field of view)
# Shorter = wider angle, Longer = more telephoto
cam_data.lens = 50  # mm (default is 50mm, similar to human eye)
print(f"  Focal length: {cam_data.lens}mm")

# Sensor size (affects field of view with focal length)
cam_data.sensor_width = 36  # mm (35mm full-frame)
print(f"  Sensor width: {cam_data.sensor_width}mm")

# Clip range (what distance range is rendered)
cam_data.clip_start = 0.1  # Minimum distance
cam_data.clip_end = 1000  # Maximum distance
print(f"  Clip range: {cam_data.clip_start} to {cam_data.clip_end}")

# Camera type
cam_data.type = 'PERSP'  # 'PERSP', 'ORTHO', or 'PANO'
print(f"  Camera type: {cam_data.type}")

# ============================================
# 3. POSITIONING AND AIMING CAMERAS
# ============================================
print("\n3. POSITIONING AND AIMING CAMERAS")

# Method 1: Manual rotation
camera.rotation_euler = (math.radians(65), 0, math.radians(45))
print(f"  Manual rotation: {camera.rotation_euler}")

# Method 2: Point at target using Track To constraint (shown later)

# Method 3: Calculate rotation to look at a point
def look_at(camera_obj, target_location):
    """Point camera at a location"""
    direction = target_location - camera_obj.location
    # Cameras point along their -Z axis
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera_obj.rotation_euler = rot_quat.to_euler()

# Use the function
look_at(camera, suzanne.location)
print(f"  Aimed at Suzanne using look_at function")

# ============================================
# 4. DIFFERENT CAMERA TYPES
# ============================================
print("\n4. DIFFERENT CAMERA TYPES")

# PERSPECTIVE CAMERA (default - realistic)
bpy.ops.object.camera_add(location=(10, 0, 3))
persp_cam = bpy.context.active_object
persp_cam.name = "PerspectiveCamera"
persp_cam.data.type = 'PERSP'
persp_cam.data.lens = 35  # Wide angle
look_at(persp_cam, suzanne.location)
print(f"  Created {persp_cam.name} (35mm wide angle)")

# ORTHOGRAPHIC CAMERA (no perspective, parallel projection)
bpy.ops.object.camera_add(location=(0, -10, 5))
ortho_cam = bpy.context.active_object
ortho_cam.name = "OrthographicCamera"
ortho_cam.data.type = 'ORTHO'
ortho_cam.data.ortho_scale = 10  # Viewing area size
look_at(ortho_cam, suzanne.location)
print(f"  Created {ortho_cam.name} (ortho scale: 10)")

# PANORAMIC CAMERA (for 360° renders)
bpy.ops.object.camera_add(location=(0, 0, 5))
pano_cam = bpy.context.active_object
pano_cam.name = "PanoramicCamera"
pano_cam.data.type = 'PANO'
pano_cam.data.cycles.panorama_type = 'EQUIRECTANGULAR'
print(f"  Created {pano_cam.name} (360° panoramic)")

# ============================================
# 5. FOCAL LENGTH EXAMPLES
# ============================================
print("\n5. FOCAL LENGTH VARIATIONS")

focal_lengths = [
    (24, "Wide Angle", (15, -5, 4)),
    (50, "Normal", (15, 0, 4)),
    (85, "Portrait", (15, 5, 4)),
    (200, "Telephoto", (15, 10, 4))
]

for focal_length, description, location in focal_lengths:
    bpy.ops.object.camera_add(location=location)
    cam = bpy.context.active_object
    cam.name = f"Camera_{focal_length}mm"
    cam.data.lens = focal_length
    look_at(cam, suzanne.location)
    print(f"  {description}: {focal_length}mm at {location}")

# ============================================
# 6. DEPTH OF FIELD (DOF)
# ============================================
print("\n6. DEPTH OF FIELD (Focus blur)")

bpy.ops.object.camera_add(location=(5, -5, 2))
dof_camera = bpy.context.active_object
dof_camera.name = "DOF_Camera"
look_at(dof_camera, suzanne.location)

dof_data = dof_camera.data

# Enable depth of field
dof_data.dof.use_dof = True

# Set focus distance (distance to sharp focus point)
# Calculate distance to Suzanne
focus_distance = (dof_camera.location - suzanne.location).length
dof_data.dof.focus_distance = focus_distance

# Set aperture (lower f-stop = more blur)
dof_data.dof.aperture_fstop = 2.8  # Wide aperture (blurry background)
dof_data.dof.aperture_blades = 6  # Number of blades (affects bokeh shape)

print(f"  Created {dof_camera.name} with DOF")
print(f"    Focus distance: {focus_distance:.2f}")
print(f"    f-stop: {dof_data.dof.aperture_fstop}")
print(f"    Blades: {dof_data.dof.aperture_blades}")

# ============================================
# 7. CAMERA CONSTRAINTS (Track To)
# ============================================
print("\n7. CAMERA CONSTRAINTS - Always look at target")

bpy.ops.object.camera_add(location=(8, 8, 6))
tracking_camera = bpy.context.active_object
tracking_camera.name = "TrackingCamera"

# Add Track To constraint
constraint = tracking_camera.constraints.new(type='TRACK_TO')
constraint.target = suzanne  # What to look at
constraint.track_axis = 'TRACK_NEGATIVE_Z'  # Camera's forward axis
constraint.up_axis = 'UP_Y'  # Camera's up axis

print(f"  Created {tracking_camera.name} with Track To constraint")
print(f"    Always points at: {suzanne.name}")

# Now if you move Suzanne, the camera will follow!
# suzanne.location.x = 3  # Camera automatically updates

# ============================================
# 8. MULTIPLE CAMERAS AND SWITCHING
# ============================================
print("\n8. MULTIPLE CAMERAS")

# Create a camera array for different angles
camera_positions = [
    ("Front", (0, -10, 2)),
    ("Side", (10, 0, 2)),
    ("Top", (0, 0, 10)),
    ("Close", (3, -3, 1.5))
]

all_cameras = []
for name, position in camera_positions:
    bpy.ops.object.camera_add(location=position)
    cam = bpy.context.active_object
    cam.name = f"Camera_{name}"
    look_at(cam, suzanne.location)
    all_cameras.append(cam)
    print(f"  Created {cam.name} at {position}")

# Switch active camera
def set_active_camera(camera_obj):
    """Set a camera as the active scene camera"""
    bpy.context.scene.camera = camera_obj
    print(f"  Switched to: {camera_obj.name}")

# Example: Switch to top camera
set_active_camera(all_cameras[2])

# ============================================
# 9. ANIMATING CAMERAS
# ============================================
print("\n9. ANIMATING CAMERAS")

bpy.ops.object.camera_add(location=(10, -10, 5))
anim_camera = bpy.context.active_object
anim_camera.name = "AnimatedCamera"
look_at(anim_camera, suzanne.location)

# Keyframe 1 (frame 1)
anim_camera.location = (10, -10, 5)
anim_camera.keyframe_insert(data_path="location", frame=1)

# Keyframe 2 (frame 60)
anim_camera.location = (-10, -10, 5)
anim_camera.keyframe_insert(data_path="location", frame=60)

# Keyframe 3 (frame 120)
anim_camera.location = (0, -15, 8)
anim_camera.keyframe_insert(data_path="location", frame=120)

print(f"  Created {anim_camera.name} with animation")
print(f"    Keyframes at frames: 1, 60, 120")

# Animate focal length (zoom effect)
anim_camera.data.lens = 35
anim_camera.data.keyframe_insert(data_path="lens", frame=1)

anim_camera.data.lens = 85
anim_camera.data.keyframe_insert(data_path="lens", frame=120)

print(f"    Focal length animates from 35mm to 85mm")

# ============================================
# 10. CAMERA PASSEPARTOUT (Overlay)
# ============================================
print("\n10. CAMERA OVERLAY SETTINGS")

camera.data.show_passepartout = True  # Dim area outside frame
camera.data.passepartout_alpha = 0.75  # Opacity of overlay
print(f"  Enabled passepartout on {camera.name}")
print(f"    Alpha: {camera.data.passepartout_alpha}")

# Show composition guides
camera.data.show_composition_center = True
camera.data.show_composition_thirds = True  # Rule of thirds
print(f"  Enabled composition guides")

# ============================================
# 11. CAMERA UTILITY FUNCTIONS
# ============================================
print("\n11. UTILITY FUNCTIONS")

def create_camera_at_distance(target, distance, angle_h, angle_v, name="Camera"):
    """
    Create a camera at a specific distance and angles from target

    Args:
        target: Target object or location
        distance: Distance from target
        angle_h: Horizontal angle (degrees)
        angle_v: Vertical angle (degrees)
        name: Camera name
    """
    # Convert angles to radians
    h_rad = math.radians(angle_h)
    v_rad = math.radians(angle_v)

    # Calculate position
    target_loc = target.location if hasattr(target, 'location') else target
    x = target_loc.x + distance * math.cos(v_rad) * math.sin(h_rad)
    y = target_loc.y + distance * math.cos(v_rad) * math.cos(h_rad)
    z = target_loc.z + distance * math.sin(v_rad)

    # Create camera
    bpy.ops.object.camera_add(location=(x, y, z))
    cam = bpy.context.active_object
    cam.name = name
    look_at(cam, target_loc)

    return cam

# Test the function
test_cam = create_camera_at_distance(
    suzanne,
    distance=10,
    angle_h=45,
    angle_v=30,
    name="UtilityCamera"
)
print(f"  Created {test_cam.name} using utility function")

def get_camera_info(camera_obj):
    """Get detailed camera information"""
    data = camera_obj.data
    return {
        'name': camera_obj.name,
        'location': tuple(camera_obj.location),
        'type': data.type,
        'focal_length': data.lens if data.type == 'PERSP' else None,
        'ortho_scale': data.ortho_scale if data.type == 'ORTHO' else None,
        'dof_enabled': data.dof.use_dof,
        'clip_start': data.clip_start,
        'clip_end': data.clip_end,
    }

# Get info about main camera
info = get_camera_info(camera)
print(f"\n  Main camera info:")
for key, value in info.items():
    if value is not None:
        print(f"    {key}: {value}")

# ============================================
# 12. LISTING ALL CAMERAS
# ============================================
print("\n12. ALL CAMERAS IN SCENE")

all_scene_cameras = [obj for obj in bpy.context.scene.objects if obj.type == 'CAMERA']
print(f"  Total cameras: {len(all_scene_cameras)}\n")

for cam in all_scene_cameras:
    is_active = "★ ACTIVE" if cam == bpy.context.scene.camera else ""
    print(f"  {cam.name} {is_active}")
    print(f"    Type: {cam.data.type}, Lens: {cam.data.lens}mm")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 50)
print("CAMERA SUMMARY")
print("=" * 50)
print("Create: bpy.ops.object.camera_add(location=(x,y,z))")
print("Set active: bpy.context.scene.camera = camera_obj")
print("\nCamera Types:")
print("  PERSP - Perspective (realistic, default)")
print("  ORTHO - Orthographic (no perspective)")
print("  PANO  - Panoramic (360° renders)")
print("\nKey Properties:")
print("  cam.data.lens - Focal length (mm)")
print("  cam.data.dof.use_dof - Enable depth of field")
print("  cam.data.dof.aperture_fstop - Blur amount")
print("\nCommon focal lengths:")
print("  24mm - Wide angle (landscapes)")
print("  50mm - Normal (human eye)")
print("  85mm - Portrait")
print("  200mm - Telephoto")
print("\nTips:")
print("  - Use Track To constraint for following targets")
print("  - Lower f-stop = more background blur")
print("  - Press Numpad 0 to see through active camera")
print("  - Use multiple cameras for different shot angles")
