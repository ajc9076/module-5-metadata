"""
Alex Collom
Module 5 - Metadata Lab
9/27/2021
Professor Bill Stackpole
This program collects, analyzes, outputs and scrubs metadata off of files
"""
import random
import sys
import os
import subprocess
import pathlib
import pikepdf


global working_directory
global tools_directory


def remove_blank_lines(file_name):
    """
    For some reason, certain commands used here produce many blank lines.
    This helper function helps remove those lines.
    :param file_name: The name for the file to strip newlines out of.
    :return: None
    """
    os.chdir(working_directory)
    with open(file_name, 'r+') as file_handle:
        with open('temp_file.txt', 'w') as temp:
            for line in file_handle:
                if line.strip():
                    temp.write(line)
            file_handle.seek(0)
            file_handle.truncate()
        with open('temp_file.txt', 'r+') as temp:
            for line in temp.readlines():
                file_handle.write(line)
    os.remove('temp_file.txt')


def print_set_alphabetical(input_set, file_handle):
    """
    Helper function to output a set alphabetically to a file
    :param input_set: The input set
    :param file_handle: The opened file to write to
    :return: None
    """
    # Generate alphabetical list from the set
    alphabetical_tags = sorted(input_set)
    for entry in alphabetical_tags:
        # Output the list to the file
        file_handle.write(entry)
        file_handle.write('\n')


def list_metadata(folder_location):
    """
    Read metadata from the file and output it to a text document, metadata_list.txt
    :param folder_location: The directory of the files we wish to analyze
    :return: None
    """
    print('Outputting to metadata_list.txt')
    os.chdir(working_directory)
    with open('metadata_list.txt', 'w') as output:
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
            exif_path = tools_directory + "exiftool.exe"
            (out, err) = subprocess.Popen([exif_path, file], stdout=subprocess.PIPE,
                                          stderr=subprocess.DEVNULL).communicate()
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
                pdf_path = tools_directory + "pdfinfo.exe"
                (out, err) = subprocess.Popen([pdf_path, file], stdout=subprocess.PIPE,
                                              stderr=subprocess.DEVNULL).communicate()
                print(out.decode('cp1252'), file=output)
                output.write("\n--------------------------------------------------------------------------\n")
            if extension == 'jpg' or extension == 'png':
                output.write("NConvert analyzing " + file + "...\n")
                output.write("Command used: nconvert.exe -fullinfo " + file + "\n")
                nconvert_path = tools_directory + "nconvert.exe"
                (out, err) = subprocess.Popen([nconvert_path, "-fullinfo", file], stdout=subprocess.PIPE,
                                              stderr=subprocess.DEVNULL).communicate()
                print(out.decode(), file=output)
                output.write("\n--------------------------------------------------------------------------\n")
    remove_blank_lines('metadata_list.txt')


def list_tags(folder_location, suppress_file_writes=False):
    """
    List the tags associated with all files in the folder location with no duplicates.
    Output to tag_list.txt
    :param folder_location: The directory of the files we wish to analyze
    :param suppress_file_writes: Disallow output to a file (useful so that I can reuse this function elsewhere)
    :return: The set that was generated containing all tags
    """
    if not suppress_file_writes:
        print('Outputting to tag_list.txt')
    os.chdir(working_directory)
    with open('tag_list.txt', 'a+') as output:
        # Delete previous file contents
        if not suppress_file_writes:
            output.seek(0)
            output.truncate()
        # Change to folder with files to analyze
        os.chdir(folder_location)
        # Create set to contain tags. A set will have no duplicates
        tag_list = set()
        # Iterate over files to generate set of tags
        for file in os.listdir(folder_location):
            # Run Exiftool to analyze files
            exif_path = tools_directory + "exiftool.exe"
            (out, err) = subprocess.Popen([exif_path, file], stdout=subprocess.PIPE,
                                          stderr=subprocess.DEVNULL).communicate()
            out = out.decode()
            # get the true file type and add tag to the set
            extension = '.default'
            for line in out.split('\n'):
                if 'File Type Extension' in line:
                    line = line.split('             : ')
                    extension = line[1].strip()
                    tag_list.add(line[0].strip().lower())
                else:
                    tag_list.add(line.split(':')[0].strip().lower())
            # Run additional tools based on the file type
            if extension == 'pdf':
                pdf_path = tools_directory + "pdfinfo.exe"
                (out, err) = subprocess.Popen([pdf_path, file], stdout=subprocess.PIPE,
                                              stderr=subprocess.DEVNULL).communicate()
                out = out.decode('cp1252')
                # Add tags to the set
                for line in out.split('\n'):
                    tag_list.add(line.split(':')[0].strip().lower())
            if extension == 'jpg' or extension == 'png':
                nconvert_path = tools_directory + "nconvert.exe"
                (out, err) = subprocess.Popen([nconvert_path, "-fullinfo", file], stdout=subprocess.PIPE,
                                              stderr=subprocess.DEVNULL).communicate()
                out = out.decode()
                # Parse nconvert output (yeah it gets complicated)
                start_meta_read = False
                for line in out.split('\n'):
                    # don't add anything to set unless we reach "Success"
                    if line.endswith('Success'):
                        start_meta_read = True
                    # Don't add organizational headers
                    elif not (line.startswith('EXIF:') or line.startswith('  Camera:') or line.startswith('  Image:') or
                              line.startswith('  IOP:') or line.startswith('  Makernotes:') or line.startswith('  GPS:')
                              or line.startswith('  Thumbnail:')) and start_meta_read:
                        # Parse the line
                        line = line.split(':')[0].strip().lower()
                        # Exception case for splitting by parentheses
                        if 'Page(s)' in line:
                            tag_list.add(line)
                        # Final parse to add to tag list
                        else:
                            tag_list.add(line.split('(')[0].strip().split('[')[0].strip())
        # Create list, sort it alphabetically, and write it to the file
        if not suppress_file_writes:
            print_set_alphabetical(tag_list, output)
    return tag_list


def scrub(folder_location):
    """
    Remove metadata from files and output the results to scrubbed_files.txt
    NOTE: The function renames files with invalid extensions so that they can be processed.
    :param folder_location: The directory of the files we wish to analyze
    :return: None
    """
    os.chdir(working_directory)
    print('Outputting to scrubbed_files.txt')
    pre_scrub_list = list_tags(folder_location, True)
    os.chdir(working_directory)
    with open('scrubbed_files.txt', 'w') as output:
        # Delete previous file contents
        output.seek(0)
        output.truncate()
        # Change to folder with files to analyze
        os.chdir(folder_location)
        for file in os.listdir(folder_location):
            # Run Exiftool to remove all non-essential metadata
            output.write("Exiftool removing metadata from " + file + "...\n")
            output.write("Command used: exiftool.exe -overwrite_original -all= " + file + "\n")
            exif_path = tools_directory + "exiftool.exe"
            # Run exiftool to get the file type and rewrite the file extension (otherwise things break)
            (out, err) = subprocess.Popen([exif_path, file], stdout=subprocess.PIPE,
                                          stderr=subprocess.DEVNULL).communicate()
            out = out.decode()
            pass_protected = False
            for line in out.split('\n'):
                if 'File Type Extension' in line:
                    # Get the true extension
                    extension = line.split(':')[1].strip()
                    # Create the new filename from the extension
                    new_file = file.split('.')[0] + "." + extension
                    # Fix the filename
                    try:
                        os.rename(file, new_file)
                    # Put a random number on the filename to prevent conflict
                    except FileExistsError:
                        num = random.randint(0, 255)
                        new_file = str(num) + new_file
                        os.rename(file, new_file)
                    file = new_file
                elif 'Document is password protected' in line:
                    # will be used to determine if we can run pikepdf. It causes errors if there is a password
                    pass_protected = True
            # Strip metadata
            (out, err) = subprocess.Popen([exif_path, "-overwrite_original", "-all=", file],
                                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).communicate()
            # Linearize PDF files (so the metadata cant be recovered)
            if file.endswith('.pdf') and not pass_protected:
                output.write("PikePDF is linearizing the PDF...\n")
                curr_pdf = pikepdf.Pdf.open(file, allow_overwriting_input=True)
                curr_pdf.save(file, linearize=True)
            # Display results by running metadata viewers again
            (out, err) = subprocess.Popen([exif_path, file], stdout=subprocess.PIPE,
                                          stderr=subprocess.DEVNULL).communicate()
            print(out.decode(), file=output)
            output.write("\n--------------------------------------------------------------------------\n")
            if extension == 'pdf':
                output.write("pdfinfo analyzing " + file + "...\n")
                output.write("Command used: pdfinfo.exe " + file + "\n")
                pdf_path = tools_directory + "pdfinfo.exe"
                (out, err) = subprocess.Popen([pdf_path, file], stdout=subprocess.PIPE,
                                              stderr=subprocess.DEVNULL).communicate()
                print(out.decode('cp1252'), file=output)
                output.write("\n--------------------------------------------------------------------------\n")
            if extension == 'jpg' or extension == 'png':
                output.write("NConvert analyzing " + file + "...\n")
                output.write("Command used: nconvert.exe -fullinfo " + file + "\n")
                nconvert_path = tools_directory + "nconvert.exe"
                (out, err) = subprocess.Popen([nconvert_path, "-fullinfo", file], stdout=subprocess.PIPE,
                                              stderr=subprocess.DEVNULL).communicate()
                print(out.decode(), file=output)
                output.write("\n--------------------------------------------------------------------------\n")
    remove_blank_lines('scrubbed_files.txt')
    post_scrub_list = list_tags(folder_location, True)
    os.chdir(working_directory)
    # Generate a list of tags that were deleted and which remained in tact
    tag_list_unchanged = pre_scrub_list.intersection(post_scrub_list)
    with open('unchanged_tags.txt', 'w') as output:
        print("Outputting unchanged tags to unchanged_tags.txt...")
        output.seek(0)
        output.truncate()
        print_set_alphabetical(tag_list_unchanged, output)
    tag_list_deleted = pre_scrub_list.difference(post_scrub_list)
    with open('deleted_tags.txt', 'w') as output:
        print("Outputting deleted tags to deleted_tags.txt...")
        output.seek(0)
        output.truncate()
        print_set_alphabetical(tag_list_deleted, output)


def main():
    """
    Parse command line input and descend into the proper function call.
    :return: None
    """
    if len(sys.argv) == 3:
        analysis_type = sys.argv[1]
        folder_location = sys.argv[2]
        global working_directory
        working_directory = str(pathlib.Path().resolve())
        global tools_directory
        tools_directory = working_directory + "/TOOLS/"
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
