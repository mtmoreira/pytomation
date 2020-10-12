## \file DirFileObj.py
#  \brief Edits files
#
# Handles files.
#
# Revision | Author            | Date     | Comment
#:---------|:------------------|:---------|:------------------------------------
# 1.0      | Matheus T. M.     | 01/13/20 | Initial version
#

import os
import shutil
from pytomation.fileTypes.BaseFileObj import BaseFileObj
from pytomation.fileTypes.TextFileObj import TextFileObj

class DirFileObj(BaseFileObj):

	## Constructor
	#
	# Create the object depending on the
	#
	# \param self Instance of BaseFileObj class.
	# \param path Optional String with path of file
	# \param name Optional String with name of file
	# \param father Optional BaseFileObj that is the father of this file
	def __init__(self, path="", name="", father=None):
		# Initializes contents (dictionary of subdirectories and dictionary of files, as text files)
		self.__dirDict = {}
		self.__fileDict = {}
		# Calls super constructor
		super(DirFileObj, self).__init__(path=path, name=name, father=father)

	## Protected _isNewFather method
	#
	# \param self Instance of DirFileObj class.
	# \param kid Instance of BaseFileObj class.
	def _isNewFather(self, kid):
		# Checks inputs
		if not isinstance(kid, BaseFileObj):
			raise TypeError("When adding new kid to a father, kid must be BaseFileObj instance")
		# Validate that kid is not root and actually a kid of this object
		if kid.isRoot():
			raise RuntimeError("Unexpected error when adding kid object that is a root")
		if kid.father != self:
			raise RuntimeError("Unexpected error when adding kid of another object")
		# Get name of kid
		kidName = kid.name
		# Send kid to right place
		if isinstance(kid, TextFileObj):
			# Check if kid is not already in dictionary
			if kidName in self.getFileList():
				raise RuntimeError("File %s already present in dir %s. Cannot overwrite." % (kidName, self.path))
			self.__fileDict[kidName] = kid
		elif isinstance(kid, DirFileObj):
			# Check if kid is not already in dictionary
			if kidName in self.getDirList():
				raise RuntimeError("Dir %s already present in dir %s. Cannot overwrite." % (kidName, self.path))
			self.__dirDict[kidName] = kid

	## Private _writeFile method.
	#
	# \param  self Instance of DirFileObj class.
	def _writeFile(self):
		# Gets path
		path = self.path
		# Remove current folder if exists
		if os.path.exists(path):
			try:
				shutil.rmtree(path)
			except Exception as e:
				raise RuntimeError("Error writing DirFileObj to path %s. Unexpected when removing old dir: %s" % (path,str(e)))
		# Create folder
		try:
			os.mkdir(path)
		except Exception as e:
			raise RuntimeError("Error writing DirFileObj to path %s. Unexpected when creating new dir: %s" % (path,str(e)))
		# Write all files it contains
		for fileName in self.getFileList():
			self.__fileDict[fileName].write()
		# Write all dirs it contains
		for dirName in self.getDirList():
			self.__dirDict[dirName].write()

	## Private readFile method.
	#
	# \param  self Instance of DirFileObj class.
	def _readFile(self):
		# Gets path
		path = self.path
		# Read everything
		for (myPath, subdirList, fileList) in os.walk(path):
			# Reads all sub directories
			for subdirName in subdirList:
				self.__dirDict[subdirName] = DirFileObj(name=subdirName, father=self)
			# Reads all files
			for fileName in fileList:
				self.__fileDict[fileName] = TextFileObj(name=fileName, father=self)
			# Avoid recursive reading
			break

	## Private _copyFile method.
	#
	# \param  self Instance of TextFileObj class.
	def _copyFile(self):
		# Copy old dictionaries
		oldFileDict = self.__fileDict
		oldDirDict = self.__dirDict
		# Initialize new dictionaries
		self.__fileDict = {}
		self.__dirDict = {}
		# Copies all files it contains
		for fileName in oldFileDict.keys():
			self.__fileDict[fileName]=oldFileDict[fileName].copy(name=fileName, father=self)
		# Copies all dirs it contains
		for dirName in oldDirDict.keys():
			self.__dirDict[dirName]=oldDirDict[dirName].copy(name=dirName, father=self)

	## Gets a list of directories contained in this directory.
	#
	# \param  self Instance of DirFileObj class.
	def getDirList(self):
		return list(self.__dirDict.keys())

	## Gets a directory contained in this directory.
	#
	# \param self Instance of DirFileObj class.
	# \param dirName String with name of dir to look for
	# \return DirFileObj
	def getDir(self, dirName):
		# Validate input type
		if not isinstance(dirName, str):
			raise TypeError("Parameter dirName must be a string")
		# Look for dir
		if dirName in self.getDirList():
			return self.__dirDict[dirName]
		else:
			raise ValueError("Could not find directory %s" % dirName)

	## Gets a list of files contained in this directory.
	#
	# \param  self Instance of DirFileObj class.
	def getFileList(self):
		return list(self.__fileDict.keys())

	## Gets a file contained in this directory.
	#
	# \param self Instance of DirFileObj class.
	# \param fileName String with name of file to look for
	# \return TextFileObj
	def getFile(self, fileName):
		# Validate input type
		if not isinstance(fileName, str):
			raise TypeError("Parameter fileName must be a string")
		# Look for dir
		if fileName in self.getFileList():
			return self.__fileDict[fileName]
		else:
			raise ValueError("Could not find file %s" % fileName)
