"""Core and Cluster"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

from scipy.stats import multivariate_normal as mvn
import numpy as np

from ._utils import format_array

class Core:
	"""
	A Core Point that defines a Gaussian Distribution.

	Parameters
	----------
	mu : array-like, shape (n_features,), default=[0]
		The mean vector of the Gaussian Distribution.

	sigma : array-like, shape (n_features, n_features), default=[1]
		The variance or covariance vector of the Gaussian Distribution.
		Core uses fully independent vectors.

	delta : array-like, shape (1,), default=[1]
		The weight of the Gaussian Distribution as a component in a larger
		Gaussian Mixture

	cluster : CoreCluster, default=None
		The parent CoreCluster this Core is associated with.
	"""
	def __init__(self, mu=[0], sigma=[1], delta=1, cluster=None):
		self.dim = -1
		self.mu = np.asarray(mu)
		self.sigma = np.asarray(sigma)
		self.delta = delta
		self.cluster = cluster
		self._validate_init()

	def _validate_init(self):
		"""
		Validate the argument types for __init__
		"""
		if np.isscalar(self.mu):
			raise ValueError("Invalid argument provided for mu. Must be a vector")
		if np.isscalar(self.sigma):
			raise ValueError("Invalid argument provided for sigma. Must be a vector")
		if np.isscalar(self.delta):
			raise ValueError("Invalid argument provided for delta. Must be a vector")
		if not isinstance(self.cluster, (None, CoreCluster)):
			raise ValueError("Invalid argument provided for cluster. Must be None or CoreCluster. Found " + type(self.cluster).__name__)
		if self.mu.shape[-1] == self.sigma.shape[-1]:
			self.dim = self.mu.shape[-1]
		else:
			raise ValueError("Mismatch in dimensions between mu and sigma")

	def pdf(self, data):
		"""
		Multivariate normal probability density function.

		Parameters
        ----------
        data : array-like
            Quantiles, with the last axis of `data` denoting the features.

        Returns
        -------
        pdf : ndarray or scalar
            Probability density function evaluated at `datas`
		"""
		data = format_array(data)
		self._validate_init()
		return mvn.pdf(x=data, mean=self.mu, cov=self.sigma)


class CoreCluster:
	"""
	A CoreCluster defines a collection of Cores that belong to a cluster.

	Parameters
	----------
	cores : array-like, shape (some_cores,), default=[]
		A list of Cores associated with this CoreCluster.

	parent : CoreCluster, default=None
		The parent CoreCluster in a hierarchical manner.

	children : array-like, shape (some_cores,), default=[]
		A list of CoreCluster children in a hierarchical manner.
	"""
	def __init__(self, cores=[], parents=[], children=[]):
		self.cores = np.asarray(cores)
		self.parent = np.asarray(parents)
		self.children = np.asarray(children)
		self._validate_init()

	def _validate_init(self):
		"""
		Validate the argument types for __init__
		"""
		if np.isscalar(self.cores):
			raise ValueError("Invalid argument provided for cores. Must be a list of Cores")
		core_types = set([type(item) for item in self.cores])
		if len(core_types) != 1 or Core not in core_types:
			raise ValueError("Invalid argument provided for cores. Must be a list of Cores")

		if np.isscalar(self.parents):
			raise ValueError("Invalid argument provided for parents. Must be a list of CoreClusters")
		parent_types = set([type(item) for item in self.parents])
		if len(parent_types) != 1 or CoreCluster not in parent_types:
			raise ValueError("Invalid argument provided for parents. Must be a list of CoreClusters")

		if np.isscalar(self.children):
			raise ValueError("Invalid argument provided for children. Must be a list of CoreClusters")
		children_types = set([type(item) for item in self.children])
		if len(children_types) != 1 or CoreCluster not in children_types:
			raise ValueError("Invalid argument provided for children. Must be a list of CoreClusters")
