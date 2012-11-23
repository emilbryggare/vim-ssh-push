#! /usr/bin/env python
import os

# Configuration
servers = ["emilbryggare.se"]
files = [".vim", "vim.fork", ".vimrc", ".vimrc.fork", ".vimrc.bundles", ".vimrc.bundles.fork"]
local_home_dir = "/Users/emil"

# Clear users view
os.system("clear")

# Get remote home dir
remote_home_dir = "/home/emil"

def ssh_remove_old_files(files, server):
    remove_command = "ssh " + str(server) + " 'rm -rf "

    for file in files:
        if (file == files[-1]):
            remove_command += str(file) + "'"
        else:
            remove_command += str(file) + " "

    os.system(remove_command)

def ssh_symlink_files(files, server):
    symlink_command = "ssh " + str(server) + " '"

    for file in files:
        symlink_command += "ln -s " + str(remote_home_dir) + "/.spf13-vim-3/" + str(file) + " " + str(file)
        if (file == files[-1]):
            symlink_command += "'"
        else:
            symlink_command += " && "

    os.system(symlink_command)

os.chdir(local_home_dir)

for server in servers:
    os.system("tar --check-links -cvf  vim-ssh-push.tar .spf13-vim-3/ && scp vim-ssh-push.tar " + server + ": && ssh "+ server + " 'tar xvf vim-ssh-push.tar'")
    ssh_remove_old_files(files, server)
    ssh_symlink_files(files, server)

print "Done!"
