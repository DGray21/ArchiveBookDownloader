# -----------------------------------------------------#
#             Archive.org Book downloader              #
# -----------------------------------------------------#
#
#   Downloads books that you need to borrow from
#   archive.org and stores the book pages in a folder.
#   This project uses selenium to interface with
#   archive.org.
#
#   Usage:
#       BookDownloader.py <ID> <username> <password> <output dir>
#       <ID> - the URL ID of the book
#       <username> - Archive.org username
#       <password> - Archive.org password
#       <output dir> - [Optional] Directory to create the <ID>
#                      output directory in. If not specified then
#                      the current working directory is used.
#   Notes:
#       The script downloads the book images to the folder
#       named <ID>. If the folder exists then the script
#       will skip any files of the same name.
#
#       This script only downloads borrowable books from
#       archive.,org. Regular files are not downloadable
#       with this script yet.

#   Import the necessary libraries

import os
import sys
import random


# Check command line arguments

username = ''   # archive.org username
password = ''   # archive.org password
archiveId = ''  # archive.org item ID

if len(sys.argv) == 4:

elif len(sys.argv) == 5:
    #Set output dir
elif len(sys.argv) > 5:
    # End script if there are too many arguments
    sys.exit('Too many arguments')
else:
    # End script if there are not enough arguments
    sys.exit('There are not enough arguments')
# Open selenium window

# Log onto archive account

# Check to see if archive ID is valid

# Check to see if the item is a book that can be borrowed

# Create folder or check if folder exists

# Start download loop

# Go to Book page

# Download page to folder (or skip if file exists)

# end download loop

# Close selenium window

# print download stats


#def permissiontest(targetdir:str):
    #Check if a file can be written to the directory


