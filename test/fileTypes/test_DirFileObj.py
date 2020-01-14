## \file test_DirFileObj.py
#  \brief Testcases for DirFileObj class
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
from DirFileObj import DirFileObj

class DirFileObjTest(unittest.TestCase):

	def setUp(self):
		self.rootFolder = "./"
		self.testFolderName = ".DirFileObjTest"
		self.testFolder = os.path.realpath(self.rootFolder+self.testFolderName)
		# Create it
		try:
			os.mkdir(self.testFolder)
		except Exception as e:
			raise RuntimeError("Error trying to create directory %s: %s" % (self.testFolder,str(e)))
		# # Sample file to write
		# self.writeFilePath = self.testFolder+"/"+"file0.txt"
		# # Sample file to read
		# self.readFilePath = os.path.realpath("./fileTypes/dirExample/file0.txt")
		# # File to read and edit
		# self.subReadFilePath = os.path.realpath("./fileTypes/dirExample/fileSub.txt")

	def tearDown(self):
		shutil.rmtree(self.testFolder)

	## Building a DirFileObj
	def test_emptyConstructor(self):
		with self.assertRaises(RuntimeError):
			DirFileObj()

	def test_constructorPathTypeError(self):
		with self.assertRaises(TypeError):
			DirFileObj(path=0)

	def test_constructorPath(self):
		dirPath = os.path.realpath(self.rootFolder+"fileTypes/dirExample")
		d = DirFileObj(path=dirPath)
		self.assertEqual(d.getDirList(),["subdirExample"])
		self.assertEqual(d.getFileList(),["file0.txt"])
		f = d.getFile("file0.txt")
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "With\n"
		expectedFileContent += "\n"
		expectedFileContent += "5 lines of text\n"
		expectedFileContent += ""
		self.assertEqual(f.getStr(),expectedFileContent)
		d = d.getDir("subdirExample")
		self.assertEqual(d.getDirList(),[])
		self.assertEqual(d.getFileList(),["fileSub.txt"])
		f = d.getFile("fileSub.txt")
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp For Regexp For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "MyRegexp\n"
		expectedFileContent += ""
		self.assertEqual(f.getStr(),expectedFileContent)

	def test_constructorPathExtraBackSlack(self):
		dirName = "dirExample/"
		dirPath = os.path.realpath(self.rootFolder+"fileTypes/"+dirName)
		d = DirFileObj(path=dirPath)
		self.assertEqual(d.name,"dirExample")
		self.assertEqual(d.getDirList(),["subdirExample"])
		self.assertEqual(d.getFileList(),["file0.txt"])
		f = d.getFile("file0.txt")
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "With\n"
		expectedFileContent += "\n"
		expectedFileContent += "5 lines of text\n"
		expectedFileContent += ""
		self.assertEqual(f.getStr(),expectedFileContent)
		d = d.getDir("subdirExample")
		self.assertEqual(d.getDirList(),[])
		self.assertEqual(d.getFileList(),["fileSub.txt"])
		f = d.getFile("fileSub.txt")
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp For Regexp For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "MyRegexp\n"
		expectedFileContent += ""
		self.assertEqual(f.getStr(),expectedFileContent)

	def test_constructorPathExtraExtraBackSlack(self):
		dirName = "dirExample////"
		dirPath = os.path.realpath(self.rootFolder+"///fileTypes//"+dirName)
		d = DirFileObj(path=dirPath)
		self.assertEqual(d.name,"dirExample")
		self.assertEqual(d.getDirList(),["subdirExample"])
		self.assertEqual(d.getFileList(),["file0.txt"])
		f = d.getFile("file0.txt")
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "With\n"
		expectedFileContent += "\n"
		expectedFileContent += "5 lines of text\n"
		expectedFileContent += ""
		self.assertEqual(f.getStr(),expectedFileContent)
		d = d.getDir("subdirExample")
		self.assertEqual(d.getDirList(),[])
		self.assertEqual(d.getFileList(),["fileSub.txt"])
		f = d.getFile("fileSub.txt")
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp For Regexp For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "MyRegexp\n"
		expectedFileContent += ""
		self.assertEqual(f.getStr(),expectedFileContent)

	def test_constructorWithFatherNameTypeError(self):
		dirName = "tmpDir"
		rootD = DirFileObj(path=self.testFolder)
		with self.assertRaises(TypeError):
			newD0 = DirFileObj(name=0, father=rootD)

	def test_constructorWithFatherFatherTypeError(self):
		dirName = "tmpDir"
		rootD = DirFileObj(path=self.testFolder)
		with self.assertRaises(TypeError):
			newD0 = DirFileObj(name=dirName, father=0)

	def test_constructorWithFatherFileAsFather(self):
		dirName = "tmpDir"
		dirPath = os.path.realpath(self.rootFolder+"fileTypes/dirExample")
		d = DirFileObj(path=dirPath)
		f = d.getFile("file0.txt")
		with self.assertRaises(RuntimeError):
			newD = DirFileObj(name=dirName, father=f)

	def test_constructorWithFatherAlreadyHasDir(self):
		dirName = "tmpDir"
		rootD = DirFileObj(path=self.testFolder)
		newD0 = DirFileObj(name=dirName, father=rootD)
		with self.assertRaises(RuntimeError):
			newD1 = DirFileObj(name=dirName, father=rootD)

	def test_constructorWithFather(self):
		dirName = "tmpDir"
		rootD = DirFileObj(path=self.testFolder)
		self.assertEqual(rootD.getDirList(),[])
		self.assertEqual(rootD.getFileList(),[])
		newD0 = DirFileObj(name=dirName, father=rootD)
		self.assertEqual(rootD.getDirList(),[dirName])
		self.assertEqual(rootD.getFileList(),[])
		self.assertEqual(newD0.getDirList(),[])
		self.assertEqual(newD0.getFileList(),[])
		newD1 = DirFileObj(name=dirName, father=newD0)
		self.assertEqual(rootD.getDirList(),[dirName])
		self.assertEqual(rootD.getFileList(),[])
		self.assertEqual(newD0.getDirList(),[dirName])
		self.assertEqual(newD0.getFileList(),[])
		self.assertEqual(newD1.getDirList(),[])
		self.assertEqual(newD1.getFileList(),[])
		newD0.write()
		self.assertEqual(os.listdir(self.testFolder),[dirName])
		self.assertEqual(os.listdir(self.testFolder+"/"+dirName),[dirName])

	# Getting directories
	def test_getDirTypeError(self):
		dirName = "tmpDir"
		rootD = DirFileObj(path=self.testFolder)
		newD0 = DirFileObj(name=dirName, father=rootD)
		with self.assertRaises(TypeError):
			rootD.getDir(0)

	def test_getDirInvalid(self):
		dirName = "tmpDir"
		rootD = DirFileObj(path=self.testFolder)
		newD0 = DirFileObj(name=dirName, father=rootD)
		with self.assertRaises(ValueError):
			rootD.getDir("invalid")

	def test_getDir(self):
		dirName = "tmpDir"
		rootD = DirFileObj(path=self.testFolder)
		newD0 = DirFileObj(name=dirName, father=rootD)
		newD1 = DirFileObj(name=dirName, father=newD0)
		d = rootD.getDir(dirName)
		self.assertEqual(d.name,dirName)
		self.assertEqual(d.getDirList(),[dirName])
		self.assertEqual(d.getFileList(),[])
		self.assertEqual(d.father.name,self.testFolderName)

	# Getting files
	def test_getFileTypeError(self):
		dirName = "tmpDir"
		dirPath = os.path.realpath(self.rootFolder+"fileTypes/dirExample")
		d = DirFileObj(path=dirPath)
		with self.assertRaises(TypeError):
			d.getFile(0)

	def test_getFileInvalid(self):
		dirName = "tmpDir"
		dirPath = os.path.realpath(self.rootFolder+"fileTypes/dirExample")
		d = DirFileObj(path=dirPath)
		with self.assertRaises(ValueError):
			d.getFile("invalid")

	def test_getFile(self):
		dirName = "tmpDir"
		dirPath = os.path.realpath(self.rootFolder+"fileTypes/dirExample")
		d = DirFileObj(path=dirPath)
		f = d.getFile("file0.txt")
		self.assertEqual(f.name,"file0.txt")

	# Copying directories
	def test_copy(self):
		copyName = "objCopy"
		dirPath = os.path.realpath(self.rootFolder+"fileTypes/dirExample")
		rootD = DirFileObj(path=self.testFolder)
		d = DirFileObj(path=dirPath)
		# Create a copy to test folder
		d.copy(name=copyName, father=rootD)
		# Check contents
		self.assertEqual(rootD.getDirList(),[copyName])
		d = rootD.getDir(copyName)
		self.assertEqual(d.getFileList(),["file0.txt"])
		f = d.getFile("file0.txt")
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "With\n"
		expectedFileContent += "\n"
		expectedFileContent += "5 lines of text\n"
		expectedFileContent += ""
		self.assertEqual(f.getStr(),expectedFileContent)
		d = d.getDir("subdirExample")
		self.assertEqual(d.getDirList(),[])
		self.assertEqual(d.getFileList(),["fileSub.txt"])
		f = d.getFile("fileSub.txt")
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp For Regexp For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "MyRegexp\n"
		expectedFileContent += ""
		self.assertEqual(f.getStr(),expectedFileContent)
		# Check actual folder in filesys
		self.assertEqual(os.listdir(self.testFolder),[])
		rootD.write()
		self.assertEqual(sorted(os.listdir(self.testFolder+"/"+copyName)),["file0.txt", "subdirExample"])
		self.assertEqual(sorted(os.listdir(self.testFolder+"/"+copyName+"/subdirExample")),["fileSub.txt"])
		# Read new files
		d = DirFileObj(path=self.testFolder+"/"+copyName)
		self.assertEqual(d.getFileList(),["file0.txt"])
		f = d.getFile("file0.txt")
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "With\n"
		expectedFileContent += "\n"
		expectedFileContent += "5 lines of text\n"
		expectedFileContent += ""
		self.assertEqual(f.getStr(),expectedFileContent)
		d = d.getDir("subdirExample")
		self.assertEqual(d.getDirList(),[])
		self.assertEqual(d.getFileList(),["fileSub.txt"])
		f = d.getFile("fileSub.txt")
		expectedFileContent  = "Sample File\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp For Regexp For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "For Regexp\n"
		expectedFileContent += "\n"
		expectedFileContent += "MyRegexp\n"
		expectedFileContent += ""
		self.assertEqual(f.getStr(),expectedFileContent)
