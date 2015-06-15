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
	docs.append(process.get_changes(tree))


# This counts the frequecies of the tuple pairs for us
changes = []

# Only looks at the whole word changes
for doc in docs:
	for change in doc:
		changes.append((change[0].strip(), change[1].strip()))

counter = collections.Counter(changes)

freq = counter.most_common()

cfile = open("change_freq.txt", "w")
for line in freq:
	cfile.write("(%s)|(%s) %d" % (line[0][0].encode("utf8"), line[0][1].encode("utf8"), line[1])  + "\n")
cfile.close()

#Prints out each change as: del ins (surrounding words), del ins (exact)
index = 1
for doc in docs:
	f = open("changes/%d.txt" % index, "w")
	for line in doc:
		f.write("|" + line[0].encode("utf8") +
				"|" + line[1].encode("utf8") +
				"|" + line[2].encode("utf8") +
				"|" + line[3].encode("utf8") +
				"|" + "\n")
	f.close()
	index = index + 1

