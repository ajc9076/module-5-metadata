"""
Alex Collom
Module 5 - Metadata Lab
9/27/2021
Professor Bill Stackpole
This program collects, analyzes, outputs and scrubs metadata off of files
"""
import sys
import os
import subprocess
import pathlib


def list_metadata(folder_location):
    """
    Read metadata from the file and output it to a text document, metadata_list.txt
    :param folder_location: The directory of the files we wish to analyze
    :return: None
    """
    print('Outputting to metadata_list.txt')
    with open('metadata_list.txt', 'r+') as output:
        # Find TOOLS directory
        tools_path = str(pathlib.Path().resolve()) + "/TOOLS/"
        # Delete previous file contents
        output.seek(0)
        output.truncate()
        # Change to folder with files to analyze
        os.chdir(folder_location)
        # Iterate over files
        for file in os.listdir(folder_location):
            # Run Exiftool to analyze files
            output.write("Exiftool analyzing " + file + "...\n")
            output.write("Command used: exiftool.exe " + file + "\n")
            exif_path = tools_path + "exiftool.exe"
            (out, err) = subprocess.Popen([exif_path, file], stdout=subprocess.PIPE).communicate()
            out = out.decode()
            print(out, file=output)
            # get the true file type
            for line in out.split('\n'):
                if 'File Type Extension' in line:
                    extension = line.split('             : ')[1].strip()
            output.write("\n--------------------------------------------------------------------------\n")
            # Run additional tools based on the file type
            if extension == 'pdf':
                output.write("pdfinfo analyzing " + file + "...\n")
                output.write("Command used: pdfinfo.exe " + file + "\n")
                pdf_path = tools_path + "pdfinfo.exe"
                (out, err) = subprocess.Popen([pdf_path, file], stdout=subprocess.PIPE).communicate()
                print(out.decode('cp1252'), file=output)
                output.write("\n--------------------------------------------------------------------------\n")
            if extension == 'jpg' or extension == 'png':
                output.write("NConvert analyzing " + file + "...\n")
                output.write("Command used: nconvert.exe -fullinfo " + file + "\n")
                nconvert_path = tools_path + "nconvert.exe"
                (out, err) = subprocess.Popen([nconvert_path, "-fullinfo", file], stdout=subprocess.PIPE).communicate()
                print(out.decode(), file=output)
                output.write("\n--------------------------------------------------------------------------\n")


def list_tags(folder_location):
    """
    List the tags associated with all files in the folder location with no duplicates.
    Output to tag_list.txt
    :param folder_location: The directory of the files we wish to analyze
    :return: None
    """
    print('Outputting to tag_list.txt')
    with open('tag_list.txt', 'w') as output:
        # Find TOOLS directory
        tools_path = str(pathlib.Path().resolve()) + "/TOOLS/"
        # Delete previous file contents
        output.seek(0)
        output.truncate()
        # Change to folder with files to analyze
        os.chdir(folder_location)
        # Create set to contain tags
        tag_list = set()
        # Iterate over files to generate set of tags
        for file in os.listdir(folder_location):
            # Run Exiftool to analyze files
            exif_path = tools_path + "exiftool.exe"
            (out, err) = subprocess.Popen([exif_path, file], stdout=subprocess.PIPE).communicate()
            out = out.decode()
            # get the true file type and add tag to the set
            extension = '.default'
            for line in out.split('\n'):
                if 'File Type Extension' in line:
                    line = line.split('             : ')
                    extension = line[1].strip()
                    tag_list.add(line[0].strip())
                else:
                    tag_list.add(line.split(':')[0].strip())
            # Run additional tools based on the file type
            if extension == 'pdf':
                pdf_path = tools_path + "pdfinfo.exe"
                (out, err) = subprocess.Popen([pdf_path, file], stdout=subprocess.PIPE).communicate()
                out = out.decode('cp1252')
                # Add tags to the set
                for line in out.split('\n'):
                    tag_list.add(line.split(':')[0].strip())
            if extension == 'jpg' or extension == 'png':
                nconvert_path = tools_path + "nconvert.exe"
                (out, err) = subprocess.Popen([nconvert_path, "-fullinfo", file], stdout=subprocess.PIPE).communicate()
                out = out.decode()
                # Parse nconvert output (yeah it gets complicated)
                start_meta_read = False
                for line in out.split('\n'):
                    # don't add anything to set unless we reach "Success"
                    if line.endswith('Success'):
                        start_meta_read = True
                    # Don't add organizational headers
                    if not (line.startswith('EXIF:') or line.startswith('  Camera:') or line.startswith('  Image:') or
                            line.startswith('  IOP:') or line.startswith('  Makernotes:') or line.startswith('  GPS:')
                            or line.startswith('  Thumbnail:')) and start_meta_read:
                        # Parse the line
                        line = line.split(':')[0].strip()
                        # Exception case for splitting by parentheses
                        if 'Page(s)' in line:
                            tag_list.add(line)
                        # Final parse to add to tag list
                        else:
                            tag_list.add(line.split('(')[0].strip().split('[')[0].strip())


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
