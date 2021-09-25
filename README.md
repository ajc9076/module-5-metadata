# module-5-metadata

This program is a command-line python program that reads and modifies metadata on files.
You will need to install the python module pikepdf (so that we can linearize PDF files). 


Usage:
python3 metadata-viewer-scrubber.py {ALL, LIST-METADATA, LIST-TAGS, SCRUB} target_folder_path

ALL: Run all 3 functionalities (described below)

LIST-METADATA: Output all metadata that can be found in a text file, along with the tools/commands used to get that metadata

LIST-TAGS: Output an alphabetical list of all tag names (no duplicates)

SCRUB: Remove all nonessential metadata. Note: Password protected files cannot have the metadata removed. 

# File outputs:
Below are the different files outputted in this program and a short description about them.

metadata_list.txt: This file contains the output from Exiftool, NConvert, and pdfinfo

tag_list.txt: This file contains an alphabetical list of all metadata tags found in the files

deleted_tags.txt: This file contains the tags deleted during the scrub function of the program

unchanged_tags.txt: This file contains the tags that were not deleted during the scrub function

scrubbed_files.txt: This output is the same as metadata_list.txt, except it is run after the scrub function
