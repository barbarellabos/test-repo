"""Construction de volumes organiques par metaballs, puis conversion en maillage."""
import bpy
from mathutils import Vector


class Meta:
    def __init__(self, name, resolution=0.012, threshold=0.6):
        self.data = bpy.data.metaballs.new(name)
        self.data.resolution = resolution
        self.data.render_resolution = resolution
        self.data.threshold = threshold
        self.obj = bpy.data.objects.new(name, self.data)
        bpy.context.collection.objects.link(self.obj)

    def ball(self, co, r, stiff=2.0, neg=False):
        el = self.data.elements.new(type="BALL")
        el.co, el.radius, el.stiffness, el.use_negative = co, r, stiff, neg
        return el

    def ellipsoid(self, co, r, size, stiff=2.0, rot=None):
        el = self.data.elements.new(type="ELLIPSOID")
        el.co, el.radius, el.stiffness = co, r, stiff
        el.size_x, el.size_y, el.size_z = size
        if rot is not None:
            el.rotation = rot
        return el

    def capsule(self, p1, p2, r, stiff=2.0):
        p1, p2 = Vector(p1), Vector(p2)
        d = p2 - p1
        el = self.data.elements.new(type="CAPSULE")
        el.co, el.radius, el.stiffness = (p1 + p2) / 2, r, stiff
        el.size_x = d.length / 2
        el.rotation = Vector((1, 0, 0)).rotation_difference(d.normalized())
        return el

    def chain(self, pts, radii, stiff=2.0):
        for i in range(len(pts) - 1):
            self.capsule(pts[i], pts[i + 1], (radii[i] + radii[i + 1]) / 2, stiff)

    def to_mesh(self, name, voxel=None):
        """Metaball -> maillage reel (necessaire pour rig, contour et export)."""
        dg = bpy.context.evaluated_depsgraph_get()
        me = bpy.data.meshes.new_from_object(self.obj.evaluated_get(dg))
        me.name = name
        ob = bpy.data.objects.new(name, me)
        bpy.context.collection.objects.link(ob)
        bpy.data.objects.remove(self.obj)
        if voxel:
            me.remesh_voxel_size = voxel
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.voxel_remesh()
        for p in me.polygons:
            p.use_smooth = True
        return ob
