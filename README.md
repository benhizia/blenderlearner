# Blender Python Tutorials

A comprehensive, crescendo-style course on Blender Python scripting - from absolute basics to expert-level techniques.

## 📚 Course Overview

This tutorial series teaches you how to control Blender programmatically using Python. Each script is a standalone lesson that builds upon previous concepts, starting simple and progressively introducing more advanced techniques.

### What You'll Learn

- **Object Creation & Manipulation** - Create and transform 3D objects
- **Materials & Shading** - Apply colors, textures, and complex materials
- **Lighting** - Set up professional lighting for your scenes
- **Cameras** - Position and animate cameras
- **Modifiers** - Non-destructively modify geometry
- **Animation** - Keyframe and procedural animation
- **Procedural Generation** - Create complex scenes algorithmically
- **Physics** - Rigid bodies, cloth, particles, and more
- **Shader Nodes** - Advanced material creation
- **Complete Workflows** - Bring it all together

## 🎯 Course Structure

The tutorials are organized into 4 progressive levels:

### 📘 Level 1: Basics (Lessons 1-4)
**Start here if you're new to Blender Python!**

| Script | Topic | What You'll Learn |
|--------|-------|-------------------|
| `01_hello_blender.py` | Introduction | Basic API, creating objects, printing info |
| `02_primitives.py` | Primitive Objects | Cubes, spheres, cylinders, and more |
| `03_transformations.py` | Movement & Rotation | Location, rotation, scale, coordinates |
| `04_basic_operations.py` | Object Operations | Selecting, duplicating, deleting, collections |

### 📗 Level 2: Intermediate (Lessons 5-7)
**Ready to make things look good!**

| Script | Topic | What You'll Learn |
|--------|-------|-------------------|
| `05_materials_basics.py` | Materials | Colors, metallic, roughness, transparency |
| `06_lighting.py` | Lighting | Point, sun, spot, area lights, three-point setup |
| `07_cameras.py` | Cameras | FOV, depth of field, camera animation |

### 📙 Level 3: Advanced (Lessons 8-10)
**Time to get creative!**

| Script | Topic | What You'll Learn |
|--------|-------|-------------------|
| `08_modifiers.py` | Modifiers | Array, mirror, bevel, boolean, and more |
| `09_animation.py` | Animation | Keyframes, curves, shape keys, armatures |
| `10_procedural_generation.py` | Procedural Content | Custom meshes, patterns, fractals, terrain |

### 📕 Level 4: Expert (Lessons 11-13)
**Master-level techniques!**

| Script | Topic | What You'll Learn |
|--------|-------|-------------------|
| `11_physics_simulation.py` | Physics | Rigid bodies, cloth, particles, forces |
| `12_shader_nodes.py` | Shader Nodes | Node trees, procedural textures, materials |
| `13_complete_scene.py` | Complete Project | Everything combined into a full scene |

## 🚀 Getting Started

### Prerequisites

- **Blender 2.8+** (Download from [blender.org](https://www.blender.org/download/))
- **Basic Python knowledge** (helpful but not required)
- **Curiosity and creativity!**

### How to Run These Scripts

There are **three ways** to run these scripts in Blender:

#### Method 1: Scripting Workspace (Recommended for Learning)

1. Open Blender
2. Switch to the **"Scripting" workspace** (top menu bar)
3. Click **"Open"** in the text editor
4. Navigate to a tutorial script (e.g., `01_basics/01_hello_blender.py`)
5. Click **"Run Script"** button or press **Alt+P**

#### Method 2: Paste Into Console

1. Open Blender
2. Switch to the **"Scripting" workspace**
3. Open the tutorial file in a text editor outside Blender
4. Copy the entire script
5. Paste into Blender's text editor
6. Press **Alt+P** to run

#### Method 3: Command Line (Advanced)

```bash
blender --python path/to/script.py
```

or to run in background:

```bash
blender --background --python path/to/script.py
```

### Viewing the Results

- **3D Viewport**: See your created objects
- **System Console** (Windows > Toggle System Console): See `print()` output
- **Press Z**: Change viewport shading (wireframe, solid, material preview, rendered)
- **Press Numpad 0**: View through the active camera
- **Press Spacebar**: Play animations

## 📖 Learning Path

### Recommended Progression

1. **Start with the Basics** - Run scripts 01-04 in order
2. **Experiment** - Modify the values, try different numbers
3. **Read the Comments** - Each script is heavily documented
4. **Check the Console** - Watch for printed information
5. **Progress Sequentially** - Each lesson builds on previous ones
6. **Revisit** - Come back to earlier lessons as you learn more

### Tips for Success

- **Don't rush** - Take time to understand each concept
- **Modify the code** - Change values and see what happens
- **Read error messages** - They help you learn
- **Use Blender's docs** - [docs.blender.org/api](https://docs.blender.org/api/current/)
- **Experiment freely** - You can always revert changes
- **Build your own** - Try creating your own scenes

## 🎨 What Each Level Teaches

### Basics: Foundation
Learn the absolute essentials of the Blender Python API. By the end, you'll be comfortable creating objects, moving them around, and organizing your scene.

**Key Skills**: API structure, object creation, transformations, scene management

### Intermediate: Visual Quality
Make your scenes look professional with materials, lighting, and cameras. Learn how to compose and capture beautiful renders.

**Key Skills**: Material properties, lighting techniques, camera control, composition

### Advanced: Motion & Complexity
Create dynamic, animated scenes and generate complex geometry procedurally. Your scenes come to life!

**Key Skills**: Modifiers, animation, procedural modeling, algorithmic design

### Expert: Total Control
Master physics simulations, create photorealistic materials with nodes, and combine everything into complete production-ready scenes.

**Key Skills**: Physics, shader nodes, scene composition, rendering, post-processing

## 💡 Example Projects You Can Build

After completing these tutorials, you'll be able to create:

- **Animated Product Visualizations** - Showcase products with professional lighting
- **Procedural Cities** - Generate entire cities algorithmically
- **Abstract Art** - Create mathematical and procedural art pieces
- **Game Assets** - Generate variations of 3D models
- **Data Visualizations** - Turn data into 3D graphics
- **Architectural Visualizations** - Create and render buildings
- **Character Rigs** - Set up animated characters
- **Physics Simulations** - Realistic falling, bouncing, cloth
- **Scientific Visualizations** - Visualize complex data
- **Motion Graphics** - Animated logos and titles

## 📚 Additional Resources

### Official Documentation
- [Blender Python API](https://docs.blender.org/api/current/) - Complete API reference
- [Blender Manual](https://docs.blender.org/manual/en/latest/) - User manual

### Community Resources
- [Blender Artists](https://blenderartists.org/) - Community forum
- [Blender Stack Exchange](https://blender.stackexchange.com/) - Q&A site
- [r/blender](https://www.reddit.com/r/blender/) - Reddit community

### Learning More Python
- [Python.org Tutorial](https://docs.python.org/3/tutorial/) - Official Python tutorial
- [Real Python](https://realpython.com/) - Python tutorials

## 🔍 Quick Reference

### Common Operations

```python
import bpy
import math

# Create object
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
obj = bpy.context.active_object

# Transform
obj.location = (x, y, z)
obj.rotation_euler = (x, y, z)  # In radians!
obj.scale = (x, y, z)

# Material
mat = bpy.data.materials.new(name="Material")
mat.use_nodes = True
obj.data.materials.append(mat)

# Animation
obj.keyframe_insert(data_path="location", frame=1)

# Delete
bpy.data.objects.remove(obj, do_unlink=True)
```

### Helpful Shortcuts

- **Alt+P** - Run script
- **Ctrl+Z** - Undo
- **Numpad 0** - Camera view
- **Z** - Shading menu
- **Spacebar** - Play animation
- **F12** - Render image
- **Ctrl+F12** - Render animation

## 🤝 Contributing

Found a bug or want to improve a tutorial? Contributions are welcome!

## 📜 License

These tutorials are provided as educational resources. Feel free to use and modify them for learning purposes.

## 🎓 Course Completion

Completed all 13 lessons? Congratulations! 🎉

You now have the skills to:
- ✅ Create any object programmatically
- ✅ Build complex materials and shaders
- ✅ Animate cameras and objects
- ✅ Generate procedural content
- ✅ Set up physics simulations
- ✅ Compose complete production scenes
- ✅ Automate Blender workflows

### What's Next?

- **Build Your Own Projects** - Apply what you've learned
- **Explore the API** - There's always more to discover
- **Join the Community** - Share your creations
- **Automate Tasks** - Save time with Python scripts
- **Create Add-ons** - Build tools for other artists

## 🌟 Final Notes

Remember: **The best way to learn is by doing!**

Don't just run these scripts - **modify them**, **break them**, **fix them**, and **create your own**. Every artist and developer started where you are now.

Happy Blending! 🎨

---

*Created as a comprehensive, crescendo-style learning resource for Blender Python scripting.*
