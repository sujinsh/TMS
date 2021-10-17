# import trimesh
# import pyrender
# # fuze_trimesh = trimesh.load('D:/3Dhead/hb.obj')
# fuze_trimesh = trimesh.load('D:/lyj/pyrender/examples/models/fuze.obj')
# print(fuze_trimesh, type(fuze_trimesh))
# mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
# print(mesh, type(mesh))
# scene = pyrender.Scene()
# print(scene, type(scene))
# scene.add(mesh)
# pyrender.Viewer(scene, use_raymond_lighting=True)


# -*- coding: utf-8 -*-

import numpy as np


print(np.load('./data/scan_lmks.npy'))
