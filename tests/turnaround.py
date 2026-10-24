"""Phase 2 : turnaround d'un personnage (face, trois-quarts, profil, dos) + planche.

Usage : python tests/turnaround.py characters/jacqueline_v01.blend [fond]
"""
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bpy  # noqa: E402

import config  # noqa: E402
from lib import render  # noqa: E402

blend = Path(sys.argv[1])
bg = sys.argv[2] if len(sys.argv) > 2 else config.NEUTRE
bpy.ops.wm.open_mainfile(filepath=str(blend))
s = render.setup_scene(preview=True, bg=bg, frames=(1, 1))
s.render.resolution_x, s.render.resolution_y = 600, 760
s.eevee.taa_render_samples = 16

root = bpy.data.objects["JL_root"]
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(50), 0, math.radians(-40)))
bpy.context.object.data.energy = 5
bpy.context.object.data.angle = math.radians(1)
bpy.ops.object.camera_add(location=(0, -4.2, 0.62), rotation=(math.radians(90), 0, 0))
s.camera = bpy.context.object
s.camera.data.lens = 50

out = config.PREVIEWS / f"turnaround_{blend.stem}"
out.mkdir(parents=True, exist_ok=True)
views = [("1_face", 0), ("2_trois_quarts", -40), ("3_profil", -90), ("4_dos", 180)]
for name, ang in views:
    root.rotation_euler.z = math.radians(ang)
    s.render.filepath = str(out / f"{name}.png")
    bpy.ops.render.render(write_still=True)
sheet = config.PREVIEWS / f"turnaround_{blend.stem}.png"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-pattern_type", "glob", "-i", str(out / "*.png"),
                "-vf", "tile=4x1", "-frames:v", "1", str(sheet)], check=True)
print("SHEET", sheet)
