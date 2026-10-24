"""Construit la mascotte Jacqueline (chiot blanc duveteux) d'apres characters/ref_jacqueline_dessin.jpg.

Repere : le chien regarde vers -Y, debout sur Z=0, hauteur totale ~1 unite (mise a l'echelle reelle
a la fin). Usage : python characters/build_jacqueline.py [version]  ->  characters/jacqueline_<version>.blend
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bpy  # noqa: E402
from mathutils import Euler, Vector  # noqa: E402

import config  # noqa: E402
from lib import style  # noqa: E402
from lib.meta import Meta  # noqa: E402

HEAD = Vector((0, -0.34, 0.86))
MUZZLE = Vector((0, -0.62, 0.74))


def build_body():
    m = Meta("JL_body_meta")
    # tronc court et rond de chiot + poitrail
    m.ellipsoid((0, 0.04, 0.40), 0.44, (0.66, 0.86, 0.66))
    m.ball((0, -0.18, 0.44), 0.32)
    # tete : grosse et bien ronde (proportions chibi), joues pleines
    m.ellipsoid(HEAD, 0.52, (0.98, 0.9, 0.92))
    m.ellipsoid(MUZZLE, 0.25, (1.0, 0.8, 0.72))
    for sx in (-1, 1):
        m.ball((sx * 0.22, -0.50, 0.70), 0.17)
    # petite meche sur le sommet du crane (comme le dessin)
    for x, z, r in ((-0.05, 1.13, 0.10), (0.04, 1.15, 0.11), (0.11, 1.12, 0.08)):
        m.ball((x, -0.40, z), r)
    # pattes avant : courtes et epaisses
    for sx in (-1, 1):
        m.capsule((sx * 0.14, -0.20, 0.36), (sx * 0.14, -0.23, 0.10), 0.16)
        m.ellipsoid((sx * 0.14, -0.27, 0.06), 0.17, (0.85, 1.05, 0.55))
    # pattes arriere : cuisse ronde
    for sx in (-1, 1):
        m.ball((sx * 0.18, 0.24, 0.34), 0.27)
        m.capsule((sx * 0.17, 0.25, 0.28), (sx * 0.16, 0.24, 0.10), 0.15)
        m.ellipsoid((sx * 0.16, 0.20, 0.06), 0.17, (0.85, 1.05, 0.55))
    # festons de duvet sur le poitrail
    for i in range(5):
        a = math.radians(-50 + i * 25)
        m.ball((math.sin(a) * 0.15, -0.36, 0.34 - math.cos(a) * 0.04), 0.10)
    return m.to_mesh("JL_body", voxel=0.008)


def build_tail():
    """Panache en virgule, lisse : des ellipsoides qui se chevauchent le long d'une courbe."""
    m = Meta("JL_tail_meta")
    pts = [(0, 0.38, 0.46), (0, 0.48, 0.58), (0, 0.55, 0.72), (0, 0.53, 0.86), (0, 0.46, 0.94)]
    radii = (0.10, 0.15, 0.20, 0.19, 0.13)
    for p, r in zip(pts, radii):
        m.ball(p, r)
    m.chain(pts, (0.06, 0.08, 0.10, 0.09, 0.07))
    return m.to_mesh("JL_tail", voxel=0.008)


def build_ear(side):
    """Grande oreille tombante, large et plate, frange ondulee en bas."""
    tag = "L" if side > 0 else "R"
    m = Meta(f"JL_ear_{tag}_meta")
    pts = [(side * 0.27, -0.32, 1.04), (side * 0.33, -0.34, 0.92), (side * 0.36, -0.34, 0.78), (side * 0.37, -0.32, 0.65)]
    for p, r in zip(pts, (0.16, 0.22, 0.24, 0.22)):
        m.ellipsoid(p, r, (0.45, 1.0, 1.0))
    for i in range(3):
        m.ellipsoid((side * 0.37, -0.42 + 0.08 * i, 0.58), 0.13, (0.45, 1.0, 1.0))
    return m.to_mesh(f"JL_ear_{tag}", voxel=0.008)


def surface_line(target, pts, mat, depth=0.009, offset=0.004, name="JL_line"):
    """Trait dessine sur la peau : points (x, z) projetes depuis l'avant sur la surface."""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = depth
    cu.bevel_resolution = 3
    cu.use_fill_caps = True
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, (x, z) in zip(sp.points, pts):
        loc, nor = surface(target, (x, -1.5, z), (0, 1, 0))
        p.co = (*(loc + nor * offset), 1)
    ob = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(ob)
    ob.data.materials.append(mat)
    return ob


def smooth_pts(pts, n=24):
    """Catmull-Rom simple pour des traits souples."""
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(P) - 2):
        for k in range(n // (len(pts) - 1)):
            t = k / (n // (len(pts) - 1))
            p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                             + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in range(2)))
    out.append(pts[-1])
    return out


def surface(obj, origin, direction):
    """Point de la surface touche par un rayon (pour poser yeux et truffe pile sur la peau)."""
    hit, loc, nor, _ = obj.ray_cast(Vector(origin), Vector(direction).normalized())
    if not hit:
        raise RuntimeError(f"rayon {origin} -> {direction} ne touche pas {obj.name}")
    if nor.dot(Vector(direction)) > 0:
        nor = -nor
    return loc, nor


def feature(name, mesh_fn, loc, nor, scale, mat, push=0.0):
    mesh_fn()
    ob = bpy.context.object
    ob.name = name
    ob.location = loc + nor * push
    ob.rotation_euler = nor.to_track_quat("Z", "Y").to_euler()
    ob.scale = scale
    bpy.ops.object.shade_smooth()
    ob.data.materials.append(mat)
    return ob


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    fur = style.toon_material("JL_pelage", "pelage", shadow="pelage_ombre", steps=(0.0, 0.3))
    black = style.flat_material("JL_truffe", "truffe")
    white = style.flat_material("JL_reflet", "reflet")
    mouth_m = style.flat_material("JL_bouche", "bouche")
    tongue_m = style.toon_material("JL_langue", "langue", steps=(0.0, 0.3))

    body = build_body()
    tail = build_tail()
    ears = [build_ear(1), build_ear(-1)]
    for ob in [body, tail, *ears]:
        ob.data.materials.append(fur)

    parts = []
    line_m = style.flat_material("JL_trait", "cobalt")
    sphere = lambda: bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=32, ring_count=16)  # noqa: E731
    # yeux : petits, ronds, brillants, bien ecartes et hauts (comme le dessin)
    for sx in (-1, 1):
        tag = "L" if sx > 0 else "R"
        loc, nor = surface(body, (sx * 0.15, -1.5, 0.95), (0, 1, 0))
        parts.append(feature(f"JL_eye_{tag}", sphere, loc, nor, (0.05, 0.058, 0.03), black))
        parts.append(feature(f"JL_eye_hl_{tag}", sphere, loc + Vector((-0.014, 0, 0.022)), nor,
                             (0.017, 0.017, 0.01), white, push=0.04))
        # sourcils : petits arcs expressifs
        parts.append(surface_line(body, smooth_pts([(sx * 0.10, 1.04), (sx * 0.15, 1.065), (sx * 0.20, 1.045)], 12),
                                  line_m, depth=0.008, name=f"JL_brow_{tag}"))
    # truffe : grosse et arrondie
    loc, nor = surface(body, (0, -1.5, 0.80), (0, 1, 0))
    parts.append(feature("JL_nose", sphere, loc, nor, (0.095, 0.065, 0.055), black))
    parts.append(feature("JL_nose_hl", sphere, loc + Vector((0.03, 0, 0.028)), nor, (0.025, 0.013, 0.01), white,
                         push=0.045))
    # bouche ouverte en D sous la truffe, langue rose dedans, trait de levre en "w"
    loc, nor = surface(body, (0, -1.5, 0.645), (0, 1, 0))
    parts.append(feature("JL_mouth", sphere, loc, nor, (0.10, 0.075, 0.02), mouth_m, push=0.002))
    parts.append(feature("JL_tongue", sphere, loc + Vector((0, 0, -0.025)), nor, (0.07, 0.05, 0.015), tongue_m,
                         push=0.008))
    lip = smooth_pts([(-0.15, 0.715), (-0.08, 0.675), (0, 0.70), (0.08, 0.675), (0.15, 0.715)], 32)
    parts.append(surface_line(body, lip, line_m, depth=0.009, name="JL_lip"))
    parts.append(surface_line(body, [(0, 0.745), (0, 0.70)], line_m, depth=0.009, name="JL_philtrum"))
    # contours en dernier : sinon les rayons de placement touchent la coque au lieu de la peau
    for ob in [body, tail, *ears]:
        style.add_outline(ob, 0.016)
    for ob in parts:
        if ob.name in ("JL_eye_L", "JL_eye_R", "JL_nose", "JL_mouth"):
            style.add_outline(ob, 0.006)

    root = bpy.data.objects.new("JL_root", None)
    bpy.context.collection.objects.link(root)
    for ob in [body, tail, *ears, *parts]:
        ob.parent = root
    return root


if __name__ == "__main__":
    version = sys.argv[1] if len(sys.argv) > 1 else "v01"
    build()
    out = config.CHARACTERS / f"jacqueline_{version}.blend"
    if out.exists():
        raise SystemExit(f"{out} existe deja : choisis une nouvelle version")
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    print("SAVED", out)
