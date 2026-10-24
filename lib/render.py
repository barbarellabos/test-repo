"""Reglages de rendu communs (Eevee, gestion couleur, sorties)."""
import bpy

import config


def setup_scene(preview=True, bg="creme", frames=(1, 30)):
    s = bpy.context.scene
    s.render.engine = "BLENDER_EEVEE"
    w, h = config.RES_PREVIEW if preview else config.RES_FINAL
    s.render.resolution_x, s.render.resolution_y = w, h
    s.render.resolution_percentage = 100
    s.render.fps = config.FPS
    s.frame_start, s.frame_end = frames
    s.eevee.taa_render_samples = config.SAMPLES_PREVIEW if preview else config.SAMPLES_FINAL
    # "Standard" : les hex de la marque sortent tels quels (AgX les delave)
    s.view_settings.view_transform = "Standard"
    s.view_settings.look = "None"
    bgc = config.color(bg) if isinstance(bg, str) else bg
    world = bpy.data.worlds.new("JL_world")
    s.world = world
    world.use_nodes = True
    # Fond visible a la camera, mais quasi pas d'eclairage ambiant (sinon le toon est plat)
    nt = world.node_tree
    bg_node = nt.nodes["Background"]
    bg_node.inputs[0].default_value = bgc
    amb = nt.nodes.new("ShaderNodeBackground")
    amb.inputs[0].default_value = bgc
    amb.inputs[1].default_value = 0.15
    path = nt.nodes.new("ShaderNodeLightPath")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(path.outputs["Is Camera Ray"], mix.inputs[0])
    nt.links.new(amb.outputs[0], mix.inputs[1])
    nt.links.new(bg_node.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], nt.nodes["World Output"].inputs[0])
    s.render.image_settings.file_format = "PNG"
    return s
