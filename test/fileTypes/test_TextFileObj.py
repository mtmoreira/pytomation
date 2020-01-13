## \file test_TextFileObj.py
#  \brief Testcases for TextFileObj class
#
# Revision | Author            | Date     | Comment
#:---------|:------------------|:---------|:----------------
# 1.0      | Matheus T. M.     | 01/12/20 | Initial version
#
import unittest
import os
import sys
import shutil
sys.path.append(os.path.realpath("../src/fileTypes"))
from TextFileObj import TextFileObj

class TextFileObjTest(unittest.TestCase):

	def setUp(self):
		self.testFolder = os.path.realpath("./.TextFileObjTest")
		# Create it
		try:
			os.mkdir(self.testFolder)
		except Exception as e:
			raise RuntimeError("Error trying to create directory %s: %s" % (self.testFolder,str(e)))
		self.operW    = TextFileObj.operationLabelWrite
		self.operR    = TextFileObj.operationLabelRead
		# Sample file to write
		self.writeFilePath = self.testFolder+"/"+"file0.txt"
		# Sample file to read
		self.readFilePath = os.path.realpath("./fileTypes/dirExample/file0.txt")
		# File to read and edit
		self.subReadFilePath = os.path.realpath("./fileTypes/dirExample/fileSub.txt")

	def tearDown(self):
		shutil.rmtree(self.testFolder)

	## Building a TextFileObj
	def test_constructorMissingPath(self):
		with self.assertRaises(TypeError):
			TextFileObj(oper=self.operW)
		self.assertEqual(os.path.exists(self.writeFilePath),False)

	def test_constructorMissingOper(self):
		with self.assertRaises(TypeError):
			TextFileObj(path=self.writeFilePath)
		self.assertEqual(os.path.exists(self.writeFilePath),False)

	def test_constructorPathTypeError(self):
		with self.assertRaises(TypeError):
			TextFileObj(path=0,oper=self.operW)
		self.assertEqual(os.path.exists(self.writeFilePath),False)

	def test_constructorPathExists(self):
		with self.assertRaises(RuntimeError):
			TextFileObj(path=self.testFolder,oper=self.operW)
		self.assertEqual(os.path.exists(self.writeFilePath),False)

	def test_constructorOperTypeError(self):
		with self.assertRaises(TypeError):
			TextFileObj(path=self.writeFilePath,oper=0)
		self.assertEqual(os.path.exists(self.writeFilePath),False)

	def test_constructorOperValueError(self):
		with self.assertRaises(ValueError):
			TextFileObj(path=self.writeFilePath,oper="invalid")
		self.assertEqual(os.path.exists(self.writeFilePath),False)

	def test_constructorWriteExistingFile(self):
		with self.assertRaises(RuntimeError):
			TextFileObj(path=self.readFilePath,oper=self.operW)

	def test_constructorReadNonExistingFile(self):
		with self.assertRaises(RuntimeError):
			TextFileObj(path=self.writeFilePath,oper=self.operR)

	def test_constructorWrite(self):
		tf = TextFileObj(path=self.writeFilePath,oper=self.operW)
		self.assertEqual(os.path.exists(self.writeFilePath),True)
		self.assertEqual(tf.path, self.writeFilePath)
		self.assertEqual(tf.isLocked(), False)
		self.assertEqual(tf.lineList, [])
		self.assertEqual(tf.lineCount, 0)

	def test_constructorRead(self):
		tf = TextFileObj(path=self.readFilePath,oper=self.operR)
		self.assertEqual(tf.path, self.readFilePath)
		self.assertEqual(tf.isLocked(), True)
		self.assertEqual(tf.lineList, ['Sample File', '', 'With', '', '5 lines of text'])
		self.assertEqual(tf.lineCount, 5)

	## Setting a path
	def test_setPathTypeError(self):
		tf = TextFileObj(path=self.writeFilePath,oper=self.operW)
		with self.assertRaises(TypeError):
			tf.path = 0

	def test_setPathLocked(self):
		tf = TextFileObj(path=self.readFilePath,oper=self.operR)
		with self.assertRaises(RuntimeError):
			tf.path = 0

	def test_setPath(self):
		tf = TextFileObj(path=self.writeFilePath,oper=self.operW)
		tf.path = "new_path"
		self.assertEqual(tf.path, "new_path")

# TODO: Add write/read checks

	## Copying a TextFileObj
	def test_copyTypeError(self):
		tf = TextFileObj(path=self.readFilePath,oper=self.operR)
		with self.assertRaises(TypeError):
			tf.copyFile(newPath=0)

	def test_copyFile(self):
		tf = TextFileObj(path=self.readFilePath,oper=self.operR)
		newTf = tf.copyFile(newPath=self.writeFilePath)
		self.assertEqual(newTf.isLocked(), False)
		self.assertEqual(newTf.lineList, ['Sample File', '', 'With', '', '5 lines of text'])
		self.assertEqual(newTf.lineCount, 5)
		newTf.lock()
		self.assertEqual(newTf.isLocked(), True)
		tf = TextFileObj(path=self.writeFilePath,oper=self.operR)
		self.assertEqual(tf.path, self.writeFilePath)
		self.assertEqual(tf.isLocked(), True)
		self.assertEqual(tf.lineList, ['Sample File', '', 'With', '', '5 lines of text'])
		self.assertEqual(tf.lineCount, 5)

	## Substituting strings in lines
	def test_strSubFindStrTypeError(self):
		tf = TextFileObj(path=self.subReadFilePath,oper=self.operR)
		with self.assertRaises(TypeError):
			tf.strSub(findStr=0,replaceStr="Example")

	def test_strSubReplaceStrTypeError(self):
		tf = TextFileObj(path=self.subReadFilePath,oper=self.operR)
		with self.assertRaises(TypeError):
			tf.strSub(findStr="Sample",replaceStr=0)

	def test_strSub(self):
		tf = TextFileObj(path=self.subReadFilePath,oper=self.operR)
		newTf = tf.copyFile(newPath=self.writeFilePath)
		newTf.strSub(findStr="Sample",replaceStr="Example")
		self.assertEqual(newTf.lineList, ['Example File', '', 'For Regexp For Regexp For Regexp', '', 'For Regexp', '', 'MyRegexp'])
		self.assertEqual(newTf.lineCount, 7)
		tf = TextFileObj(path=self.writeFilePath,oper=self.operR)
		self.assertEqual(tf.lineList, ['Example File', '', 'For Regexp For Regexp For Regexp', '', 'For Regexp', '', 'MyRegexp'])
		self.assertEqual(tf.lineCount, 7)
		newTf.strSub(findStr="For Regexp",replaceStr="0")
		self.assertEqual(newTf.lineList, ['Example File', '', '0 0 0', '', '0', '', 'MyRegexp'])
		self.assertEqual(newTf.lineCount, 7)
		tf = TextFileObj(path=self.writeFilePath,oper=self.operR)
		self.assertEqual(tf.lineList, ['Example File', '', '0 0 0', '', '0', '', 'MyRegexp'])
		self.assertEqual(tf.lineCount, 7)
