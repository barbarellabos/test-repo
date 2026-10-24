"""Style toon de la marque : materiau a paliers + contour inverted hull."""
import bpy

import config


def toon_material(name, base, shadow=None, steps=(0.0, 0.3)):
    """Materiau cel-shade 2 niveaux : Diffuse -> Shader to RGB -> ColorRamp constant."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    diff = nt.nodes.new("ShaderNodeBsdfDiffuse")
    to_rgb = nt.nodes.new("ShaderNodeShaderToRGB")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    emit = nt.nodes.new("ShaderNodeEmission")
    base_c = config.color(base) if isinstance(base, str) else base
    if isinstance(shadow, str):
        shadow = config.color(shadow)
    shadow_c = shadow or tuple(c * 0.55 for c in base_c[:3]) + (1.0,)
    ramp.color_ramp.interpolation = "CONSTANT"
    ramp.color_ramp.elements[0].position = steps[0]
    ramp.color_ramp.elements[0].color = shadow_c
    ramp.color_ramp.elements[1].position = steps[1]
    ramp.color_ramp.elements[1].color = base_c
    nt.links.new(diff.outputs[0], to_rgb.inputs[0])
    nt.links.new(to_rgb.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], emit.inputs[0])
    nt.links.new(emit.outputs[0], out.inputs[0])
    return mat


def flat_material(name, col):
    """Aplat pur (yeux, truffe, reflets) : pas d'ombrage, couleur garantie."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    emit = nt.nodes.new("ShaderNodeEmission")
    emit.inputs[0].default_value = config.color(col) if isinstance(col, str) else col
    nt.links.new(emit.outputs[0], out.inputs[0])
    return mat


def outline_material(color_name="cobalt"):
    mat = bpy.data.materials.get("JL_outline")
    if mat:
        return mat
    mat = bpy.data.materials.new("JL_outline")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    emit = nt.nodes.new("ShaderNodeEmission")
    emit.inputs[0].default_value = config.color(color_name)
    # La coque ne doit pas projeter d'ombre sur le personnage qu'elle entoure
    path = nt.nodes.new("ShaderNodeLightPath")
    transp = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(path.outputs["Is Shadow Ray"], mix.inputs[0])
    nt.links.new(emit.outputs[0], mix.inputs[1])
    nt.links.new(transp.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    mat.use_backface_culling = True
    mat.use_transparent_shadow = True
    return mat


def add_outline(obj, thickness=0.02):
    """Contour inverted hull : solidify a normales inversees, faces avant masquees."""
    obj.data.materials.append(outline_material())
    mod = obj.modifiers.new("JL_outline", "SOLIDIFY")
    mod.thickness = thickness
    mod.offset = 1.0
    mod.use_flip_normals = True
    mod.use_rim = False
    mod.material_offset = len(obj.data.materials) - 1
    return mod
