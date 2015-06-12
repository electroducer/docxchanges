## Does everything in one shot.


from docxchanges.importer import DocxImport
from docxchanges.process import DocxProcess
from lxml import etree
import os

# Path to where text files will be dumped
path = "./text/"

if not os.path.exists(path):
	os.makedirs(path)

#Load the importer, gets the filelist for all files
importer = DocxImport()

#All files now stored as etree objects
xmltrees = importer.import_files()

process = DocxProcess()

#All etree objects now simplified to contain only text
docs = []
for tree in xmltrees:
	docs.append(process.get_paragraphs(tree))

index = 1
for doc in docs:
	f = open("%s%d.txt" % (path, index), "w")
	for p in doc:
		f.write(p.encode("utf8") + "\n")
	f.close()
	index = index + 1


