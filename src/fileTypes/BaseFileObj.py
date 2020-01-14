## \file BaseFileObj.py
#  \brief Aaa
#
# aaa
#
# Revision | Author            | Date     | Comment
#:---------|:------------------|:---------|:------------------------------------
# 1.0      | Matheus T. M.     | 01/11/20 | Initial version
#

import os
import re
import copy as cp
from abc import ABC, abstractmethod

class BaseFileObj(ABC):

	## Constructor
	#
	# Create the object depending on the
	#
	# \param path Optional String with path of file
	# \param name Optional String with name of file
	# \param father Optional BaseFileObj that is the father of this file
	# \param self Instance of BaseFileObj class.
	def __init__(self, path="", name="", father=None):

		# Default father is self
		if father is None:
			father = self

		# Calls super constructor
		super(BaseFileObj, self).__init__()

		# Validate input types
		if not isinstance(name, str):
			raise TypeError("Parameter name must be a string")
		if not isinstance(path, str):
			raise TypeError("Parameter path must be a string")
		if not isinstance(father, BaseFileObj):
			raise TypeError("Parameter father must be a BaseFileObj")

		# Constructor takes either the path or name+father
		if path == "":
			if name == "" or father == self:
				raise RuntimeError("Read invalid parameters. Constructor takes either the path or name+father.")
			# In this case, validate that first father is root
			currObj = self
			fatherObj = father
			while currObj != fatherObj:
				currObj = fatherObj
				fatherObj = currObj.father
			if not fatherObj.isRoot():
				raise RuntimeError("Couldnt find a root father when trying to create new object.")
		else:
			if name != "" or father != self:
				raise RuntimeError("Read invalid parameters. Constructor takes either the path or name+father.")
			## In this case, get name from path and remove it from path
			# First remove any trailing /
			path = re.sub("[/]*$", "", path)
			# Then create regexp to isolate name
			nameRegexp = "(.*)/([^/]+)"
			nameRegexp = re.compile(nameRegexp)
			# Look for name in path
			nameMatch = nameRegexp.match(path)
			# If found, get name and path
			if nameMatch:
				# Update path and remove any trailing /
				path = nameMatch.group(1)
				path = re.sub("[/]*$", "", path)
				# Update name
				name = nameMatch.group(2)
			else:
				raise RuntimeError("Failed to extract name and path from %s." % path)

		# Store attributes name
		self.__name   = name
		self.__path   = path
		self.__father = father

		# Check if file exists
		try:
			checkPath = os.path.exists(self.path)
		except Exception as e:
			raise RuntimeError("Error trying to check if path %s exists: %s" % (self.__path,str(e)))

		# If exists, read file in
		if checkPath:
			# Call read method
			self.__read()

		# If not root, update its father
		if not self.isRoot():
			self.father._isNewFather(kid=self)

	## Gets name.
	#
	# \param  self Instance of BaseFileObj class.
	# \return String.
	@property
	def name(self):
		return self.__name

	## Gets path.
	#
	# \param  self Instance of BaseFileObj class.
	# \return String.
	@property
	def path(self):
		# Get path
		if self.isRoot():
			path = self.__path
		else:
			path = self.father.path
		# Add name
		path = path + "/" + self.name
		return path

	## Gets father.
	#
	# \param  self Instance of BaseFileObj class.
	# \return String.
	@property
	def father(self):
		return self.__father

	## Checks if file is root.
	#
	# \param  self Instance of BaseFileObj class.
	# \return Boolean.
	def isRoot(self):
		# Root files dont have a father
		return (self.father == self)

	## Protected _isNewFather method. Must be specialized by inheriting classes.
	#
	# \param self Instance of BaseFileObj class.
	# \param kid Instance of BaseFileObj class.
	@abstractmethod
	def _isNewFather(self, kid):
		return NotImplemented

	## Private read method. Calls specialized _readFile method to handle different
	# file type reads
	#
	# \param  self Instance of BaseFileObj class.
	def __read(self):
		self._readFile()

	## Protected readFile method. Must be specialized by inheriting classes.
	#
	# \param  self Instance of BaseFileObj class.
	@abstractmethod
	def _readFile(self):
		return NotImplemented

	## Write method. Makes required checks and then calls _writeFile method to 
	# handle different file type writes
	#
	# \param  self Instance of BaseFileObj class.
	def write(self):
		# Checks before writing
		if self.isRoot() and self.path == "":
			raise RuntimeError("Unexpected error found while trying to write root file. No path found.")
		self._writeFile()

	## Protected _writeFile method. Must be specialized by inheriting classes.
	#
	# \param  self Instance of BaseFileObj class.
	@abstractmethod
	def _writeFile(self):
		return NotImplemented

	## Copy method.
	#
	# Copies file to new path or father
	#
	# \param self Instance of BaseFileObj class.
	# \param name String with name of file
	# \param father BaseFileObj that is the father of this file
	def copy(self, name, father):
		# Validate input types
		if not isinstance(name, str):
			raise TypeError("Parameter name must be a string")
		if not isinstance(father, BaseFileObj):
			raise TypeError("Parameter father must be a BaseFileObj")

		# Store prev name and father to backup later
		prevName = self.name
		prevPath = self.path
		prevFather = self.father
		# Update name and father to create copy
		self.__name   = name
		self.__path   = ""
		self.__father = father
		# Create a copy
		objCopy = cp.copy(self)
		# Restore attributes
		self.__name   = prevName
		self.__path   = prevPath
		self.__father = prevFather

		# Update father with new copy
		father._isNewFather(kid=objCopy)

	## Protected _copyFile method. Must be specialized by inheriting classes.
	#
	# \param self Instance of BaseFileObj class.
	# \param objCopy BaseFileObj that is the new copy created
	@abstractmethod
	def _copyFile(self, objCopy):
		return NotImplemented


	# ## printFile method. Must be specialized by inheriting classes.
	# #
	# # \param  self Instance of BaseFileObj class.
	# @abstractmethod
	# def printFile(self):
	# 	return NotImplemented

	# ## Sets path.
	# #
	# # \param self Instance of BaseFileObj class.
	# # \param newPath String to be used
	# @path.setter
	# def path(self, newPath):
	# 	# Locked files cannot be editted
	# 	if self.isLocked():
	# 		raise RuntimeError("Tried to set path of locked object with path %s" % self.path)
	# 	# Checks input
	# 	if not isinstance(newPath, str):
	# 		raise TypeError("Parameter newPath must be a string")
	# 	self.__path = newPath

	## Locks file
