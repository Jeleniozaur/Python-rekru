import sys
import os
import os.path
import zipfile
import datetime

def InvalidArgvException():
    print("Arguments invalid!")
    print("Available arguments are:\n1.Zip filename\n2.Content to be added to VERSION.txt.\n3.Optional - set it to 't' to update updated.txt with current date.")
    exit()

def sh(cmd):
    os.system(cmd)

def CreateTempFileAndZipIt(filename, content, archive):
    sh("echo " + content + " > /tmp/"+filename)
    sh("zip -q -u -j " + archive + " /tmp/"+filename)
    sh("rm /tmp/"+filename)
    print('created ' + filename + ' and added to ' + archive)

def AppendToZip(filename, content, archive):
    #if file exists in zip if yes then unzip and append to unzipped file
    zp = zipfile.ZipFile(archive)
    if filename in zp.namelist():
        sh("unzip -q -p " + archive + " " + filename + " > /tmp/"+filename)
        sh("echo " + content + " >> /tmp/"+filename)
        print('appended to ' + filename)
    else:
        #if file doesn't exist in zip then create a new one
        sh("echo " + content + " > /tmp/"+filename)
        print('created ' + filename + ' and added to ' + archive)
    
    #push file back to the archive and remove temp file
    sh("zip -q -u -j " + archive + " /tmp/"+filename)
    sh("rm /tmp/"+filename)
    print(filename + ' zipped to ' + archive)

def DoStuff():
    # Get parameters
    z = sys.argv[1]  # zip filename
    u = sys.argv[2]  # update for VERSION.txt
    o = ''           # optional - assigned later on in the script

    # Check for unused arguments
    if len(sys.argv) >= 4:
        o = sys.argv[3]  # optional, for updating updated.txt, must be set to 't' to work
    if len(sys.argv) > 4:
        print("More than 3 arguments were specified, they are going to be ignored")
        exit()

    # Check for argv syntax
    if not z.endswith('.zip'):
        print("Please provide a whole filename such as " + z + '.zip')
        exit()
    if len(sys.argv) >= 4 and o != 't':
        print("Please use 't' for this argument to be used")
        exit()

    # If all checks passed:
    # Check if zip file already exists
    if os.path.isfile(z):
        print(z + ' found')
        AppendToZip("VERSION.txt", u, z)
        if o == 't':
            AppendToZip("updated.txt", str(datetime.datetime.now()), z)
    else:
        print(z + ' not found')
        CreateTempFileAndZipIt("VERSION.txt", u, z)
        if o == 't':
            CreateTempFileAndZipIt("updated.txt", str(datetime.datetime.now()), z)

if len(sys.argv) <= 2:
    InvalidArgvException()
else:
    DoStuff()
