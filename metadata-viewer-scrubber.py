"""
Alex Collom
Module 5 - Metadata Lab
9/27/2021
Professor Bill Stackpole
This program collects, analyzes, outputs and scrubs metadata off of files
"""
import sys
import os


def list_metadata(folder_location):
    """
    Read metadata from the file and output it to a text document, metadata_list.txt
    :param folder_location: The directory of the files we wish to analyze
    :return: None
    """
    print('Outputting to metadata_list.txt')
    with open('metadata_list.txt', 'w') as output:
        os.chdir(folder_location)
        for file in os.listdir(folder_location):
            with open(file) as file_input:
                # DO METADATA READ HERE
                print('blah')


def list_tags(folder_location):
    """
    List the tags associated with all files in the folder location with no duplicates.
    Output to tag_list.txt
    :param folder_location: The directory of the files we wish to analyze
    :return: None
    """
    print('Outputting to tag_list.txt')
    with open('tag_list.txt', 'w') as output:
        output.write("Hello World!")


def scrub(folder_location):
    """
    Remove metadata from files and output the results to scrubbed_files.txt
    :param folder_location: The directory of the files we wish to analyze
    :return: None
    """
    print('Outputting to scrubbed_files.txt')
    with open('scrubbed_files.txt', 'w') as output:
        output.write("Hello World!")


def main():
    """
    Parse command line input and descend into the proper function call.
    :return: None
    """
    if len(sys.argv) == 3:
        analysis_type = sys.argv[1]
        folder_location = sys.argv[2]
        if analysis_type == "ALL":
            list_metadata(folder_location)
            list_tags(folder_location)
            scrub(folder_location)
        elif analysis_type == "LIST-METADATA":
            list_metadata(folder_location)
        elif analysis_type == "LIST-TAGS":
            list_tags(folder_location)
        elif analysis_type == "SCRUB":
            scrub(folder_location)
        else:
            print(
                'Usage: python3 metadata-viewer-scrubber.py {ALL, LIST-METADATA, LIST-TAGS, SCRUB} target_folder_path')
    else:
        print('Usage: python3 metadata-viewer-scrubber.py {ALL, LIST-METADATA, LIST-TAGS, SCRUB} target_folder_path')


if __name__ == '__main__':
    main()
