# Writes a set of files containing simplified xmltrees with changes


from docxchanges.importer import DocxImport
from docxchanges.process import DocxProcess
from lxml import etree
import os

# default path to dump trees
path = "./xml/"

if not os.path.exists(path):
	os.makedirs(path)

#Load the importer, gets the filelist for all files
importer = DocxImport()

#All files now stored as etree objects
xmltrees = importer.import_files()

processor = DocxProcess()

#All etree objects now simplified to contain only text and changes
docs = []
for tree in xmltrees:
	docs.append(processor.simplify_tree_changes(tree))

index = 1
for doc in docs:
	f = open("%s%d.xml" % (path, index), "w")
	f.write(etree.tostring(doc, pretty_print = True))
	f.close()
	index = index + 1


