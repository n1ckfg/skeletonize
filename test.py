import numpy as np
from skeletonize import skeletonize
import latk
import binvox_rw
from random import uniform as rnd

def read_binvox(path, fix_coords=True):
    voxel = None
    with open(path, 'rb') as f:
        voxel = binvox_rw.read_as_3d_array(f, fix_coords)
    return voxel

def write_binvox(data, url):
    with open(url, 'wb') as f:
        data.write(f)

skel = skeletonize(speed_power=1.2, Euler_step_size=0.5, depth_th=2, length_th=None, simple_path=False, verbose=True)

#bw_2d = np.load("./examples/bw_2d.npy")

bv = read_binvox("./examples/input_002_resample_fake.binvox")

sk = skel.skeleton(bv.data)

la = latk.Latk(init=True)

spreadReps = 3
spread = 3

for limb in sk:
	points = []
	for point in limb:
		point = latk.LatkPoint((point[0], point[2], point[1]))
		points.append(point)
	stroke = latk.LatkStroke(points)
	la.layers[0].frames[0].strokes.append(stroke)

for i in range(0, spreadReps):
	newStrokes = []
	for stroke in la.layers[0].frames[0].strokes:
		newStroke = latk.LatkStroke()
		for point in stroke.points:
			x = point.co[0] + rnd(-spread, spread)
			y = point.co[1] + rnd(-spread, spread)
			z = point.co[2] + rnd(-spread, spread)
			
			newStroke.points.append(latk.LatkPoint((x, y, z)))
		newStrokes.append(newStroke)

	for stroke in newStrokes:
		la.layers[0].frames[0].strokes.append(stroke)

la.refine()

la.write("output.latk")
