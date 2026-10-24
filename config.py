"""Configuration centrale du projet Jacqueline's Lab - videos 3D.

Toute couleur, resolution ou chemin vient d'ici. Ne jamais coder une valeur en dur ailleurs.
Palette : PROPOSITION v01, en attente de validation.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
CHARACTERS = ROOT / "characters"
SHOTS = ROOT / "shots"
PREVIEWS = ROOT / "previews"
RENDERS = ROOT / "renders"
STORYBOARD = ROOT / "storyboard.json"

PALETTE = {
    "cobalt":       "#1B3A9E",  # contours, typographie
    "orange":       "#FF7A1A",  # accent, CTA
    "vert":         "#4DB36B",  # digestion
    "jaune_pastel": "#FFE79A",
    "bleu_ciel":    "#BFE3F7",  # fond
    "creme":        "#FFF4E0",  # fond
}

FPS = 30
RES_FINAL = (1080, 1920)
RES_PREVIEW = (540, 960)
SAMPLES_FINAL = 32
SAMPLES_PREVIEW = 8
SEED = 1234


def hex_to_linear(hex_str, alpha=1.0):
    """Hex sRGB -> RGBA lineaire (ce qu'attend Blender)."""
    h = hex_str.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, alpha)


def color(name, alpha=1.0):
    return hex_to_linear(PALETTE[name], alpha)
