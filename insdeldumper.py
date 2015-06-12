# Dumps all deletions and insertions into files

from docxchanges.importer import DocxImport
from docxchanges.process import DocxProcess
from lxml import etree
import os

# Path to where files will be dumped
del_path = "./del/"
ins_path = "./ins/"

if not os.path.exists(del_path):
	os.makedirs(del_path)

if not os.path.exists(ins_path):
	os.makedirs(ins_path)

#Load the importer, gets the filelist for all files
importer = DocxImport()

#All files now stored as etree objects
xmltrees = importer.import_files()

process = DocxProcess()

#All etree objects now simplified to contain only text and changes
dels = []
inss = []
for tree in xmltrees:
	dels.append(process.get_deletions(tree))
	inss.append(process.get_insertions(tree))


index = 1
for del_ in dels:
	f = open("%s%d.txt" % (del_path, index), "w")
	for line in del_:
		f.write(line.encode("utf8") + "\n")
	f.close()
	index = index + 1

index = 1
for ins in inss:
	f = open("%s%d.txt" % (ins_path, index), "w")
	for line in ins:
		f.write(line.encode("utf8") + "\n")
	f.close()
	index = index + 1

