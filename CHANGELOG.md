# CHANGELOG

## 2026-10-24 : Phase 0, mise en place
- Fait : Blender 5.2.3 LTS (module bpy officiel, Python 3.13), ffmpeg 6.1.1 (libx264 + aac). Arborescence, config.py, lib/style.py (toon 2 paliers + contour inverted hull), lib/render.py.
- Environnement : conteneur cloud Linux, SANS GPU. Eevee tourne en rendu logiciel (Mesa llvmpipe). Pas de Metal : on n'est pas sur un Mac.
- Mesures (scène test simple) : 540x960, 8 samples ≈ 3,2 s/image ; 1080x1920, 32 samples ≈ 20 s/image.
- Décisions : Eevee ; gestion couleur "Standard" (les hex de la marque sortent fidèles, AgX les délave) ; contour = inverted hull (plus rapide que Freestyle, comparaison à refaire en phase 2) ; la coque de contour ne projette pas d'ombre.
- Bugs corrigés : (1) toon tout plat, cause : le fond du monde éclairait la scène à 100 %, d'où un éclairage ambiant découplé du fond visible ; (2) personnage entièrement dans l'ombre, cause : la coque de contour projetait son ombre sur le corps.
- Bloqué : accès réseau aux sites d'assets (Sketchfab, Poly Pizza, Quaternius, Kenney, NIH 3D) refusé par la politique réseau de l'environnement.
- En attente de validation : palette v01 (config.py), questions vidéo 1, choix de la voie pour le chien.
