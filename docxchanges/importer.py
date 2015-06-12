# importer module for docxchanges package
# loading the DocxImport class get the list of files to import
# run import_files to convert them to element trees (lxml.etree)


import os
import zipfile
from lxml import etree

class DocxImport:

	filelist = []

	# Initialiser creates a list of docx files to import
	def __init__(self, filename = "", directory = os.curdir):
		# Looks through all subdirs for docx files
		if filename is "":
			for root, dirs, files in os.walk(directory):
				for f in files:
					if f.endswith(".docx"):
						self.filelist.append(os.path.join(root, f))
			if len(self.filelist) < 1:
				"No docx files found"

		# Handles individual file import requests
		else:
			assert filename.endswith(".docx"), "File is not of type docx"
			self.filelist.append(filename)



	# imports the root xml file from the docx bundle
	def get_word_xml(self, docx_filename):
		with open(docx_filename) as f:
			zip = zipfile.ZipFile(f)
			xml_content = zip.read('word/document.xml')
			#should throw an exception here if file is corrupted
		return xml_content


	# makes a tree from the xml file
	def get_xml_tree(self, xml_string):
		return etree.fromstring(xml_string)



	# performs the import procedure 
	def import_files(self):
		"""Use this method to import the files to xmltrees"""
		xmltree = []
		for ind_file in self.filelist:
			xmlstring = self.get_word_xml(ind_file)
			xmltree.append(self.get_xml_tree(xmlstring))
		return xmltree



