# FITS_FMS
Scan FITS files and save filenames and metadata in a SQLite database for easy searching.

FITS_FMS: (Database for *.FITS filenames and metadata search)

1. Specifications

a. The app is only tested on a Windows system.

b. Written in Python 3.11 and compiled to an .exe file.

c. Only *.fts, *.fit or *.fits files will be scanned.

d. A SQLite database (metadata.db) is used as database.

e. The log and other files are stored in C:/users/”username”/AppData/Local/FITS_DB

 

2. Assumptions

a. All your images are in one root folder or at least in one drive. (But scanning the whole drive may take very long)

b. Your metadata of the images are updated with your specific info.

Note: All the data and info are in the images. The database is just an image of the image’s metadata, excluding the image itself. If you lose the database, you can just run  "Create" again.

3. Process

     Step 1: Select a folder where to store the database.
   
     Step 2: Select a folder (sub folders are automatically added) which contains the images to scan.
   
     Step 3: Create the database.
             Please note that a new database and log file are created with each “Create” and the old one are deleted.
   
     Step 4: View the database created. Filters can be applied to the three fields (Filename, Header and Value of the header). If a more complex search needs to done - any SQLite file browser can be used to read the database. DB Browser (SQLite) is a popular choice.

The program tries to correct errors in the metadata, but check the log file if experiencing problems.

