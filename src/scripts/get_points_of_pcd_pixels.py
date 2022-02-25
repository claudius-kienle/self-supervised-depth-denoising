
from pathlib import Path

import numpy as np

from dataset.dataset_interface import DatasetInterface
from utils.transformation_utils import imgs_to_pcd, rs_ci
import open3d as o3d


file = Path("resources/images/calibrated_masked/not-cropped/ycb_video/10022022/1644493461.1656203.npz")

rs_rgb, rs_depth, zv_rgb, zv_depth, _ = DatasetInterface.load(file)
rs_pcd = imgs_to_pcd(rs_rgb, rs_depth, rs_ci)
zv_pcd = imgs_to_pcd(zv_rgb, zv_depth, rs_ci)

v = o3d.visualization.VisualizerWithEditing()
v.create_window()
v.add_geometry(zv_pcd)
v.run()
v.destroy_window()
picked_points_indices = v.get_picked_points()
points = np.array(np.asarray(zv_pcd.points)[picked_points_indices])
print(points)