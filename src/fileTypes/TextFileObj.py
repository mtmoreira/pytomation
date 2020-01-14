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
	# \param self Instance of BaseFileObj class.
	# \param path Optional String with path of file
	# \param name Optional String with name of file
	# \param father Optional BaseFileObj that is the father of this file
	def __init__(self, path="", name="", father=None):
		# Initializes its line list
		self.__lineList = []
		# Calls super constructor
		super(TextFileObj, self).__init__(path=path, name=name, father=father)

	## Protected _isNewFather method
	#
	# \param self Instance of TextFileObj class.
	# \param kid Instance of BaseFileObj class.
	def _isNewFather(self, kid):
		raise RuntimeError("TextFileObj cannot be a father")

	## Private _writeFile method.
	#
	# \param  self Instance of TextFileObj class.
	def _writeFile(self):
		# Create file
		with open(self.path, "w") as file:
			for line in self.__lineList:
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

	## Private _copyFile method.
	#
	# \param  self Instance of TextFileObj class.
	def _copyFile(self):
		# Nothing to do here
		pass

	## Substitutes a string in file
	#
	# \param self Instance of TextFileObj class.
	# \param findStr String to be replaced.
	# \param replaceStr String used in replacement.
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

	## Returns a string with contents of file.
	#
	# \param  self Instance of TextFileObj class.
	# \return String
	def getStr(self):
		returnStr = ""
		for line in self.__lineList:
			returnStr += line + "\n"

		return returnStr