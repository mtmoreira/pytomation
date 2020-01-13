## \file TextFileObj.py
#  \brief Edits files
#
# Handles files.
#
# Revision | Author            | Date     | Comment
#:---------|:------------------|:---------|:------------------------------------
# 1.0      | Matheus T. M.     | 01/12/20 | Initial version
#

from BaseFileObj import BaseFileObj

class TextFileObj(BaseFileObj):
	## Constructor
	#
	# Create the object depending on the
	#
	# \param path String with path of file
	# \param oper String with operation to be done.
	# \param self Instance of TextFileObj class.
	def __init__(self, path, oper):
		# Initialize file line list
		self.__lineList = []
		super(TextFileObj, self).__init__(path=path, oper=oper)

	## Access lines of file as a list.
	#
	# \param  self Instance of TextFileObj class.
	# \return List of string.
	@property
	def lineList(self):
		return self.__lineList

	## Gets number of lines.
	#
	# \param  self Instance of TextFileObj class.
	# \return Integer.
	@property
	def lineCount(self):
		return len(self.__lineList)

	## Prints info about file
	#
	# \param  self Instance of TextFileObj class.
	def printFile(self):
		for line in self.__lineList:
			print(line)

	## Private _copyFile method.
	#
	# \param  self Instance of TextFileObj class.
	# \param newPath String defining path of copied object
	def _copyFile(self, newPath):
		# Checks input
		if not isinstance(newPath, str):
			raise TypeError("Parameter newPath must be a string")
		# Nothing to be done
		pass

	## Private _writeFile method.
	#
	# \param  self Instance of TextFileObj class.
	def _writeFile(self):
		# Check if writtable
		if self.isLocked():
			raise RuntimeError("Tried to write in locked file %s" % self.path)
		# Create file
		with open(self.path, "w") as file:
			for line in self.lineList:
				file.write(line+"\n")
		file.close()

	## Private readFile method.
	#
	# \param  self Instance of TextFileObj class.
	def _readFile(self):
		self.__lineList = []
		with open(self.path) as file:
			fileLine = file.readline()
			while fileLine:
				self.__lineList.append(fileLine.strip())
				fileLine = file.readline()

	## Substitutes a string in file
	#
	# \param findStr String to be replaced.
	# \param replaceStr String used in replacement.
	# \param self Instance of TextFileObj class.
	def strSub(self, findStr, replaceStr):
		# Checks inputs
		if not isinstance(findStr, str):
			raise TypeError("Parameter findStr must be a string")
		if not isinstance(replaceStr, str):
			raise TypeError("Parameter replaceStr must be a string")
		# Iterates through all lines
		for idx, line in enumerate(self.__lineList):
			# Update line
			self.__lineList[idx] = line.replace(findStr, replaceStr)

		# Writes file
		self.write()
