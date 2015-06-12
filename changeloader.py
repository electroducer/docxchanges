# Gathers all changes

from docxchanges.importer import DocxImport
from docxchanges.process import DocxProcess
from lxml import etree
import collections

#Load the importer, gets the filelist for all files
importer = DocxImport()

#All files now stored as etree objects
xmltrees = importer.import_files()

process = DocxProcess()

#All etree objects now simplified to contain only text and changes
docs = []
for tree in xmltrees:
	docs = docs + process.get_changes(tree)


# This counts the frequecies of the tuple pairs for us
changes = []
for pair in docs:
	changes.append((pair[0], pair[1]))

counter = collections.Counter(changes)



index = 1
for doc in docs:
	f = open("changes/%d.txt" % index, "w")
	for line in doc:
		f.write(line[0].encode("utf8") + "\t" + line[1].encode("utf8") + "\n")
	f.close()
	index = index + 1

