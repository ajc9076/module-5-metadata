# module-5-metadata

This program is a command-line python program that reads and modifies metadata on files.
You will need to install the python module pikepdf (so that we can linearize PDF files). 


Usage:
python3 metadata-viewer-scrubber.py {ALL, LIST-METADATA, LIST-TAGS, SCRUB} target_folder_path

ALL: Run all 3 functionalities (described below)

LIST-METADATA: Output all metadata that can be found in a text file, along with the tools/commands used to get that metadata

LIST-TAGS: Output an alphabetical list of all tag names (no duplicates)

SCRUB: Remove all nonessential metadata. Note: Password protected files cannot have the metadata removed. 
