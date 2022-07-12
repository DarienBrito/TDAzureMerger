"""

Kinect Azure Merger
====================

Darien Brito, 2020
https://www.darienbrito.com
info@darienbrito.com

All credit goes to the creators of the awesome open3D 
library. All I have done is to lay it all out so 
that it can be used with ease within TouchDesigner.

See here:
http://www.open3d.org/

"""

import numpy as np
import open3d as o3d
import copy

class extAzureCalibration:
	"""
	extAzureCalibration description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp 	= ownerComp
		self.data 		= {}

	def clearData(self):
		self.data.clear()

	def preprocess_point_cloud(self, pcd, voxel_size):
		"""
		Downsample point cloud, estimate normals and compute FPHP.
		The FPFH feature is a 33-dimensional vector that describes 
		the local geometric property of a point.

		Fast Point Feature Histograms (FPFH) for 3D registration, ICRA, 2009.
		"""
		pcd_down = pcd.voxel_down_sample(voxel_size)

		radius_normal = voxel_size * 2
		pcd_down.estimate_normals(
		o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

		radius_feature = voxel_size * 5
		pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
		pcd_down,
		o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))

		return pcd_down, pcd_fpfh

	def prepare_dataset(self, voxel_size, source, target):
		"""
		Load pointclouds from the targetted pairs. Remember:
		source is the pointcloud we wish to modify and target the
		one we use as reference.
		"""
		source_down, source_fpfh = self.preprocess_point_cloud(source, voxel_size)
		target_down, target_fpfh = self.preprocess_point_cloud(target, voxel_size)
		return source, target, source_down, target_down, source_fpfh, target_fpfh

	def execute_global_registration(self, source_down, target_down, source_fpfh,
	                                target_fpfh, voxel_size):
		"""
		Runs RANSAC registration of the downsampled point clouds.

		In each RANSAC iteration, ransac_n random points are picked from the source 
		point cloud. Their corresponding points in the target point cloud are detected 
		by querying the nearest neighbor in the 33-dimensional FPFH feature space. 
		A pruning step takes fast pruning algorithms to quickly reject false matches early.
		"""
		distance_threshold = voxel_size * 1.5
		result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
		source_down, target_down, source_fpfh, target_fpfh, distance_threshold,
		o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
			4, [
				o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
				0.9),
				o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
				distance_threshold)
				], o3d.pipelines.registration.RANSACConvergenceCriteria(4000000, 500))
		return result

	def refine_registration(self, source, target, source_fpfh, target_fpfh, voxel_size, matrix):
		"""
		Run the Iterative closest point algorithm (ICP) on the estimated point-cloud transformation.
		Since we use the TransformationEstimationPointToPlane we need normals. These are part already
		of our donwsampled pointcloud objects.
		"""
		distance_threshold = voxel_size * 0.4
		result = o3d.pipelines.registration.registration_icp(source, target, distance_threshold, matrix,
		o3d.pipelines.registration.TransformationEstimationPointToPlane())
		return result

	def getPointcloudData(self, azure):
		"""
		Collect data from kinect azure
		"""
		points 	= azure.op('null_sourcePointcloud').numpyArray()
		colors 	= azure.op('null_color').numpyArray()
		return points, colors

	def image_to_vector(self, data):
		"""
		Convert input data into suitable vectors
		for open3D.
		"""
		length, height, depth = data.shape
		return data.reshape((length * height, 3))

	def createPointcloudObject(self, azure):
		points, colors = self.getPointcloudData(azure)
		# drop alpha channel
		points = points[:, :, :3]
		colors = colors[:, :, :3]
		# reshape to vector
		points = self.image_to_vector(points)
		colors = self.image_to_vector(colors)
		# Create open3D pointcloud object
		pcd = o3d.geometry.PointCloud()
		pcd.points = o3d.utility.Vector3dVector(points)
		pcd.colors = o3d.utility.Vector3dVector(colors)
		return pcd

	def writeMatrixToTable(self, matrix, table):
		"""
		Writes an open3D matrix to a TD table
		"""
		table.clear()
		for row in matrix:
			table.appendRow(row)		
		return

	def prepareData(self, pair=[1, 2], voxel_size = 0.05):
		self.clearData()
		azureTarget = op('Azure{}'.format(pair[0]))
		azureSource = op('Azure{}'.format(pair[1]))
		# Perform global registration
		target = self.createPointcloudObject(azureTarget)
		source = self.createPointcloudObject(azureSource)
		return self.prepare_dataset(voxel_size, source, target)

	def computeMatrix(self, source_down, target_down, source_fpfh, target_fpfh, voxel_size, pair=[1, 2], mode='globalRegistration'):

		matrix = None

		if mode == 'globalRegistration':
			"""
			Perform global registration (first initial guess) from where to later
			compute a refined version. Used when we want to infer the poincloud 
			if we don't have any pre-exisitng matrix.
			"""
			result_ransac = self.execute_global_registration(source_down, target_down,
			                                            source_fpfh, target_fpfh,
			                                            voxel_size)
			matrix 	= result_ransac.transformation

		elif mode == 'preExistingMatrix':
			"""
			Used when there's an existing matrix obtained via some 
			method. This could be matrices obtained via CouldCompare, 
			openCV or even manual alignments
			"""			
			op 		= op(f'Azure{pair[1]}')
			matrix 	= [float(v.val) for elem in op.rows() for v in elem]
			matrix 	= np.array([ matrix[:4], matrix[4:8], matrix[8:12], matrix[12:16]])
			debug('Using pre-existing matrix at: {}'.format(op.path))
			debug(matrix)

		return matrix

	def buildData(self, pair, mode='globalRegistration'):
		"""
		Assemble data in a dictionary
		"""
		voxel_size = 0.05  # means 5cm for the dataset
		source, target, source_down, target_down, source_fpfh, target_fpfh = self.prepareData(pair, voxel_size)
		matrix = self.computeMatrix(source_down, target_down, source_fpfh, target_fpfh, voxel_size, pair, mode)
		
		self.data 		= {	'sourceDown': source_down, 
							'targetDown': target_down,
							'sourceFPFH': source_fpfh,
							'targetFPFH': target_fpfh,
							'voxelSize' : voxel_size,
							'matrix' 	: matrix
						}
		return

	def Calibrate(self, pair=[1, 2], mode='globalRegistration'):
		"""
		Perform global registration (first initial guess) from where to later
		compute a refined version
		"""
		self.buildData(pair, mode)

		# Apply transformation matrix to azure instance
		# Source is the pointcloud we seek to change and
		# target the one that we use as reference, hence
		# we change the source 
		azureSource = op('Azure{}'.format(pair[1]))
		self.writeMatrixToTable(self.data['matrix'], azureSource.op('transformMatrix'))
		return 

	def Refine(self, pair=[1, 2]):
		# ICP Refinement
		result_icp = self.refine_registration(	self.data['sourceDown'], self.data['targetDown'], 
												self.data['sourceFPFH'], self.data['targetFPFH'],
		                                 		self.data['voxelSize'],  self.data['matrix'] )
		# Apply final transformation
		matrix = result_icp.transformation
		azureSource = op('Azure{}'.format(pair[1]))
		self.writeMatrixToTable(matrix, azureSource.op('transformMatrix'))
		return