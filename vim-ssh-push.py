#! /usr/bin/env python
import os

# Configuration
servers = ["dev32", "emilbryggare.se"]
files = [".spf13-vim-3",
         ".vim",
         ".vimrc",
         ".vimrc.bundles",
         ".vimrc.local"]

local_home_directory = os.path.expanduser('~')
os.chdir(local_home_directory)
symlinks = {}
# Clear users view
os.system("clear")

def validate_files(files):
    print "Validating files..."
    for file in files:
        if (os.path.exists(file) == False):
            print "-> Not a valid file " + file
            files.remove(file)


def find_symlinks(files, symlinks):
    print "Finding symlinks..."
    for file in files:
        symlink =  os.popen("find ~ -name '" + file + "' -maxdepth 1 -type l -ls | awk -F \"-> \" '{ print $2}'").read().replace("\n","")
        if (symlink):
            print "-> Found " + file
            symlinks[file] = symlink.replace(local_home_directory, "~")

    # Remove files that are symlinks as we create them in the create_symlinks
    # function.
    for file in symlinks:
        files.remove(file)

def cleanup(files, symlinks, server):
    print "Removing old files and symlinks..."
    cmd = "ssh " + str(server) + " 'rm -rf "

    for file in files:
        if (file == files[-1]):
            cmd += str(file) + "'"
        else:
            cmd += str(file) + " "
    symlinks_iter = 0

    for file in symlinks:
        if (len(symlinks) == symlinks_iter):
            cmd += str(file) + "'"
        else:
            cmd += str(file) + " "


    os.system(cmd)

def create_symlinks(symlinks, server):
    print "Creating symlinks..."
    cmd = "ssh " + str(server) + " '"

    symlinks_iter = 0
    for file in symlinks:
        symlinks_iter = symlinks_iter + 1
        print symlinks[file]
        cmd += "ln -f -s " + symlinks[file] + " " + file
        if (len(symlinks) == symlinks_iter):
            cmd += "'"
        else:
            cmd += " && "

    os.system(cmd)

def transfer_archived_files(server):
    print "Transfering archived files..."
    cmd = "scp ssh-push.tar "
    cmd += server + ":"
    os.system(cmd)

def archive_files(files):
    print "Archiving files..."
    cmd = "tar --check-links -cvf ssh-push.tar "
    for file in files:
        cmd += file + " "
    os.system(cmd)

def extract_files(server):
    print "Extracting files..."
    cmd = "ssh " + server + " 'tar xvf ssh-push.tar && rm ssh-push.tar'"
    os.system(cmd)

validate_files(files)
find_symlinks(files, symlinks)
archive_files(files)
for server in servers:
    cleanup(files, symlinks, server)
    transfer_archived_files(server)
    extract_files(server)
    create_symlinks(symlinks, server)
