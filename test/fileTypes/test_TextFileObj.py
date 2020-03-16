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
sys.path.append(os.path.realpath("../pytomation/fileTypes"))
from DirFileObj import DirFileObj
from TextFileObj import TextFileObj

class TextFileObjTest(unittest.TestCase):

	def setUp(self):
		self.rootFolder = "./"
		self.testFolderName = ".TextFileObjTest"
		self.testFolder = os.path.realpath(self.rootFolder+self.testFolderName)
		self.testDir = DirFileObj(path=self.testFolder)
		# Create it
		try:
			os.mkdir(self.testFolder)
		except Exception as e:
			raise RuntimeError("Error trying to create directory %s: %s" % (self.testFolder,str(e)))
		# Sample file to read
		self.readFileName = "file0.txt"
		self.readFilePath = os.path.realpath(self.rootFolder+"fileTypes/dirExample/"+self.readFileName)
		# File to read and edit
		self.subReadFilePath = os.path.realpath(self.rootFolder+"fileTypes/dirExample/subdirExample/fileSub.txt")

	def tearDown(self):
		shutil.rmtree(self.testFolder)

	## Building a TextFileObj
	def test_emptyConstructor(self):
		with self.assertRaises(RuntimeError):
			TextFileObj()

	def test_constructorPathTypeError(self):
		with self.assertRaises(TypeError):
			TextFileObj(path=0)

	def test_constructorPath(self):
		tfo = TextFileObj(path=self.readFilePath)
		self.assertEqual(tfo.path,self.readFilePath)
		self.assertEqual(tfo.name, "file0.txt")
		self.assertEqual(tfo.father,tfo)
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "With\n"
		expectedFileContent += "\n"
		expectedFileContent += "5 lines of text\n"
		expectedFileContent += ""
		self.assertEqual(tfo.getStr(),expectedFileContent)

	def test_constructorFatherNameTypeError(self):
		with self.assertRaises(TypeError):
			TextFileObj(name=0,father=self.testDir)

	def test_constructorFatherFatherTypeError(self):
		fileName = "tmp.txt"
		with self.assertRaises(TypeError):
			TextFileObj(name=fileName,father=0)

	def test_constructorFatherFileFatherSelf(self):
		tfo = TextFileObj(path=self.readFilePath)
		fileName = "tmp.txt"
		with self.assertRaises(RuntimeError):
			TextFileObj(name=fileName,father=tfo)

	def test_constructorSameFatherTwice(self):
		fileName = "tmp.txt"
		TextFileObj(name=fileName,father=self.testDir)
		with self.assertRaises(RuntimeError):
			TextFileObj(name=fileName,father=self.testDir)

	def test_constructorFather(self):
		fileName = "tmp.txt"
		tfo = TextFileObj(name=fileName,father=self.testDir)
		self.assertEqual(self.testDir.getDirList(),[])
		self.assertEqual(self.testDir.getFileList(),[fileName])
		self.assertEqual(os.listdir(self.testFolder),[])
		tfo.write()
		self.assertEqual(os.listdir(self.testFolder),[fileName])

	## Copying a TextFileObj
	def test_copyMissingName(self):
		tfo = TextFileObj(path=self.readFilePath)
		with self.assertRaises(TypeError):
			tfo.copy(father=self.testDir)

	def test_copyMissingFather(self):
		tfo = TextFileObj(path=self.readFilePath)
		with self.assertRaises(TypeError):
			tfo.copy(name="tmp")

	def test_copyNameTypeError(self):
		tfo = TextFileObj(path=self.readFilePath)
		with self.assertRaises(TypeError):
			tfo.copy(name=0,father=self.testDir)

	def test_copyFatherTypeError(self):
		tfo = TextFileObj(path=self.readFilePath)
		with self.assertRaises(TypeError):
			tfo.copy(name="tmp",father=0)

	def test_copyTwice(self):
		tfo = TextFileObj(path=self.readFilePath)
		tfo.copy(name="tmp",father=self.testDir)
		with self.assertRaises(RuntimeError):
			tfo.copy(name="tmp",father=self.testDir)

	def test_copyFile(self):
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "With\n"
		expectedFileContent += "\n"
		expectedFileContent += "5 lines of text\n"
		expectedFileContent += ""
		dir0Name = "tmp"
		dir1Name = "tmp2"
		fileName = "tmp.txt"
		dir0 = DirFileObj(name=dir0Name,father=self.testDir)
		dir1 = DirFileObj(name=dir1Name,father=dir0)
		tfo = TextFileObj(path=self.readFilePath)
		self.assertEqual(dir1.getFileList(),[])
		tfo.copy(name=fileName,father=dir1)
		self.assertEqual(dir1.getFileList(),[fileName])
		self.assertEqual(dir1.getFile(fileName).getStr(),expectedFileContent)
		self.assertEqual(sorted(os.listdir(self.testFolder)),[])
		self.testDir.write()
		self.assertEqual(sorted(os.listdir(self.testFolder)),[dir0Name])
		self.assertEqual(sorted(os.listdir(self.testFolder+"/"+dir0Name)),[dir1Name])
		self.assertEqual(sorted(os.listdir(self.testFolder+"/"+dir0Name+"/"+dir1Name)),[fileName])
		tfo = TextFileObj(path=self.testFolder+"/"+dir0Name+"/"+dir1Name+"/"+fileName)
		self.assertEqual(tfo.getStr(),expectedFileContent)

	# Writing files
	def test_writeWithoutFolder(self):
		dir0Name = "tmp"
		dir1Name = "tmp2"
		fileName = "tmp.txt"
		dir0 = DirFileObj(name=dir0Name,father=self.testDir)
		dir1 = DirFileObj(name=dir1Name,father=dir0)
		tfo = TextFileObj(path=self.readFilePath)
		copyFile = tfo.copy(name=fileName,father=dir1)
		with self.assertRaises(RuntimeError):
			copyFile.write()

	## Substituting strings in lines
	def test_strSubFindStrTypeError(self):
		tf = TextFileObj(path=self.subReadFilePath)
		with self.assertRaises(TypeError):
			tf.strSub(findStr=0,replaceStr="Example")

	def test_strSubReplaceStrTypeError(self):
		tf = TextFileObj(path=self.subReadFilePath)
		with self.assertRaises(TypeError):
			tf.strSub(findStr="Sample",replaceStr=0)

	def test_strSub(self):
		newFileName = "tmp"
		tf = TextFileObj(path=self.subReadFilePath)
		newTf = tf.copy(name=newFileName, father=self.testDir)
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp For Regexp For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "MyRegexp\n"
		expectedFileContent += ""
		self.assertEqual(newTf.getStr(), expectedFileContent)
		newTf.strSub(findStr="Sample",replaceStr="Example")
		expectedFileContent  = "Example File\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp For Regexp For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "MyRegexp\n"
		expectedFileContent += ""
		self.assertEqual(newTf.getStr(), expectedFileContent)
		newTf.strSub(findStr="For Regexp",replaceStr="0")
		expectedFileContent  = "Example File\n"
		expectedFileContent += "\n"
		expectedFileContent += "0 0 0\n"
		expectedFileContent += "\n"
		expectedFileContent += "0\n"
		expectedFileContent += "\n"
		expectedFileContent += "MyRegexp\n"
		expectedFileContent += ""
		self.assertEqual(newTf.getStr(), expectedFileContent)

	def test_strSubDoubleFile(self):
		newFile0Name = "tmp0"
		newFile1Name = "tmp1"
		tf = TextFileObj(path=self.subReadFilePath)
		newTf0 = tf.copy(name=newFile0Name, father=self.testDir)
		newTf1 = tf.copy(name=newFile1Name, father=self.testDir)
		expectedOriginalFileContent  = "Sample File\n"
		expectedOriginalFileContent += "\n"
		expectedOriginalFileContent += "For Regexp For Regexp For Regexp\n"
		expectedOriginalFileContent += "\n"
		expectedOriginalFileContent += "For Regexp\n"
		expectedOriginalFileContent += "\n"
		expectedOriginalFileContent += "MyRegexp\n"
		expectedOriginalFileContent += ""
		self.assertEqual(newTf0.getStr(), expectedOriginalFileContent)
		self.assertEqual(newTf1.getStr(), expectedOriginalFileContent)
		newTf1.strSub(findStr="Sample",replaceStr="Example")
		expectedFileContent = "Example File\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp For Regexp For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "MyRegexp\n"
		expectedFileContent += ""
		self.assertEqual(newTf0.getStr(), expectedOriginalFileContent)
		self.assertEqual(newTf1.getStr(), expectedFileContent)
