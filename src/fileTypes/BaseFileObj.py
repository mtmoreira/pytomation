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
import copy
from abc import ABC, abstractmethod

class BaseFileObj(ABC):
	operationLabelWrite = "w"
	operationLabelRead  = "r"

	## Constructor
	#
	# Create the object depending on the
	#
	# \param path String with path of file
	# \param oper String with operation to be done.
	# \param self Instance of BaseFileObj class.
	def __init__(self, path, oper):
		super(BaseFileObj, self).__init__()
		# Validate inputs
		if not isinstance(path, str):
			raise TypeError("Parameter path must be a string")
		if not isinstance(oper, str):
			raise TypeError("Parameter oper must be a string with valid option. Valid options are: %s and %s" % (self.operationLabelWrite, self.operationLabelRead))
		if not (oper == self.operationLabelRead or oper == self.operationLabelWrite):
			raise ValueError("Parameter oper must be a string with valid option. Valid options are: %s and %s" % (self.operationLabelWrite, self.operationLabelRead))

		# Store file path
		self.__path = path
		# Check if file exists
		try:
			checkPath = os.path.exists(self.__path)
		except Exception as e:
			raise RuntimeError("Error trying to check if path %s exists: %s" % (self.__path,str(e)))

		# If write
		if oper == self.operationLabelWrite:
			# Initialize file as unlocked
			self.__lock = False
			# If file exists
			if checkPath:
				raise RuntimeError("Error trying to write path %s. File already exists." % self.__path)
			# Call write method
			self.write()
		# If read
		else:
			# Initialize file as locked to avoid writing
			self.__lock = True
			# If file doesnt exist
			if not checkPath:
				raise RuntimeError("Error trying to read path %s. File does not exist." % self.__path)
			# Call read method
			self.read()

	## Gets path.
	#
	# \param  self Instance of BaseFileObj class.
	# \return String.
	@property
	def path(self):
		return self.__path

	## Sets path.
	#
	# \param self Instance of BaseFileObj class.
	# \param newPath String to be used
	@path.setter
	def path(self, newPath):
		# Locked files cannot be editted
		if self.isLocked():
			raise RuntimeError("Tried to set path of locked object with path %s" % self.path)
		# Checks input
		if not isinstance(newPath, str):
			raise TypeError("Parameter newPath must be a string")
		self.__path = newPath

	## Checks if file is locked.
	#
	# \param  self Instance of BaseFileObj class.
	# \return Boolean.
	def isLocked(self):
		return self.__lock

	## Locks file
	#
	# \param  self Instance of BaseFileObj class.
	def lock(self):
		self.__lock = True

	## Copies file, creating new file and returning unlocked copied object
	#
	# \param self Instance of BaseFileObj class.
	# \param newPath String defining path of copied object
	# \return BaseFileObj specialized class with copy
	def copyFile(self, newPath):
		# Can only copy locked files
		if not self.isLocked():
			raise RuntimeError("Only locked files can be copied")
		# Checks input
		if not isinstance(newPath, str):
			raise TypeError("Parameter newPath must be a string")
		# Unlocks cell
		self.__lock = False
		# Create a copy of this object
		cpFile = copy.deepcopy(self)
		# Locks cell
		self.__lock = True
		# Adjust path of object
		cpFile.path = newPath
		# Write file
		cpFile.write()
		# Call specialized copy method
		cpFile._copyFile(newPath=newPath)
		# Return object
		return cpFile

	## Protected _copyFile method. Must be specialized by inheriting classes.
	#
	# \param  self Instance of BaseFileObj class.
	# \param newPath String defining path of copied object
	@abstractmethod
	def _copyFile(self, newPath):
		return NotImplemented

	## Write method. Makes required checks and then calls _writeFile method.
	#
	# \param  self Instance of BaseFileObj class.
	def write(self):
		# Cant write locked objects
		if self.isLocked():
			raise RuntimeError("Cannot write locked files")
		self._writeFile()

	## Protected _writeFile method. Must be specialized by inheriting classes.
	#
	# \param  self Instance of BaseFileObj class.
	@abstractmethod
	def _writeFile(self):
		return NotImplemented

	## Read method. Makes required checks and then calls _readFile method.
	#
	# \param  self Instance of BaseFileObj class.
	def read(self):
		self._readFile()

	## Protected readFile method. Must be specialized by inheriting classes.
	#
	# \param  self Instance of BaseFileObj class.
	@abstractmethod
	def _readFile(self):
		return NotImplemented

	## printFile method. Must be specialized by inheriting classes.
	#
	# \param  self Instance of BaseFileObj class.
	@abstractmethod
	def printFile(self):
		return NotImplemented
