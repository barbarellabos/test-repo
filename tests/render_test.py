"""Phase 0 : rendu test 1 s (30 images) pour mesurer le temps par image.

Usage : python tests/render_test.py [preview|final] [nb_images]
"""
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bpy  # noqa: E402

import config  # noqa: E402
from lib import render, style  # noqa: E402

mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
n = int(sys.argv[2]) if len(sys.argv) > 2 else 30
bpy.ops.wm.read_factory_settings(use_empty=True)
s = render.setup_scene(preview=(mode == "preview"), frames=(1, n))

# Sol + "personnage galet" qui rebondit avec squash & stretch
bpy.ops.mesh.primitive_plane_add(size=20)
ground = bpy.context.object
ground.data.materials.append(style.toon_material("sol", "jaune_pastel"))

bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1, location=(0, 0, 1))
body = bpy.context.object
bpy.ops.object.shade_smooth()
body.data.materials.append(style.toon_material("corps", "orange"))
style.add_outline(body, 0.04)
for x in (-0.35, 0.35):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.22, location=(x, -0.85, 1.25))
    eye = bpy.context.object
    bpy.ops.object.shade_smooth()
    eye.data.materials.append(style.toon_material("oeil", (1, 1, 1, 1)))
    style.add_outline(eye, 0.02)
    eye.parent = body
    eye.matrix_parent_inverse = body.matrix_world.inverted()

for f in range(1, n + 1):
    t = (f - 1) / n
    h = abs(math.sin(t * math.pi))
    body.location.z = 1 + 1.2 * h
    squash = 1 - 0.25 * (1 - h) ** 4
    body.scale = (1 / math.sqrt(squash), 1 / math.sqrt(squash), squash)
    body.keyframe_insert("location", frame=f)
    body.keyframe_insert("scale", frame=f)

bpy.ops.object.light_add(type="SUN", rotation=(math.radians(55), 0, math.radians(-55)))
bpy.context.object.data.energy = 5
bpy.ops.object.camera_add(location=(0, -9, 2.2), rotation=(math.radians(85), 0, 0))
s.camera = bpy.context.object
s.camera.data.lens = 35

out = config.PREVIEWS / "phase0_test" / mode
out.mkdir(parents=True, exist_ok=True)
s.render.filepath = str(out / "f_")
times = []
for f in range(1, n + 1):
    s.frame_set(f)
    s.render.filepath = str(out / f"f_{f:04d}.png")
    t0 = time.time()
    bpy.ops.render.render(write_still=True)
    times.append(time.time() - t0)
warm = times[1:] or times
print(f"RESULT mode={mode} {s.render.resolution_x}x{s.render.resolution_y} "
      f"samples={s.eevee.taa_render_samples} first={times[0]:.1f}s "
      f"avg_next={sum(warm)/len(warm):.2f}s total={sum(times):.1f}s")
