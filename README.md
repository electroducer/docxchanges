# README for docxchanges

Docxchanges is a Python module for extracting text and tracked changes from .docx files. The repository also includes several scripts that can be used "out of the box" on the command line.

## What can Docxchanges do?

Currently, this module can perform the following tasks:

 - Extract the text from a single .docx file or from a folder of files.
 - Return the text as a single string or as paragraphs.
 - Create and return a simplified version of the XML tree, with or without changes.
 - Return the insertions or deletions in arrays.
 - Return an array with the both the insertions and deletions, as well as the difference between the two.

## What can Docxchanges not do (yet)?

 - Return other docx metadata.
 - Return the name of the user who made the changes.
 - Return cumulative changes based on sentence divisions (e.g. changes made to the end of one sentence and the beginning of another are not divided).

## Why would I want to use Docxchanges?

This is an excellent tool for creating corpus data from .docx files, even if you aren't interested in tracked changes. By extracted data from tracked changes, however, an analysis based on such changes can easily be performed. For example, the most common writing errors could be easily discovered and examined.

## How can I use Docxchanges?

The simplest way is to run one of the scripts that accompany the module. It is set by default to process all .docx files located the current directory, so copying a folder into the folder where the script is located will get the job done.
Each of the scripts will return the data into .txt files and folders in the current directory.

Docxchanges is much more interesting when the text and changes are extracted and used directly with a package such as the Natural Language Toolkit (NLTK). A basic template has been provided to show how to convert extracted text to NLTK text objects.


## What if I have .doc (Old MS Word) files?

Batch conversion macros exist for MS Word that can easily be used to convert older files types to the newer one. One of them can be found here, for example.

## What if something doesn't work?

Bugs can reported by sending me a message, or if you're really smart, you can solve it for me and send it along as a pull request.


