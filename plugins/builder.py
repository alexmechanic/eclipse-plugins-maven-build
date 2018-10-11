#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Alexander Gerasimov <samik.mechanic@gmail.com>
#

import os, stat, subprocess, sys, platform, tarfile
from distutils.dir_util import copy_tree, remove_tree

host_platform = 1 if platform.system() == "Windows" else 0
slash = "\\" if platform.system() == "Windows" else "/"
builder_dir = os.getcwd()
install_dir = os.getcwd() +slash+ "Bin"
mvn_dir     = os.getcwd() +slash+ "apache-maven-3.5.0"
mvn_bin     = mvn_dir +slash+ "bin" +slash+ "mvn"

os.environ ['JAVA_HOME'] = ''

#
# NOTE: Maven build arguments
#
MVN_BUILD_CMD = " -o -Dmaven.repo.local=" + mvn_dir +slash+ "base-repo clean verify"

def PrepareMaven():
    global host_platform, mvn_bin

    print ("\nPreparing Maven distribution\n------------------------------------")
    if os.path.isdir("apache-maven-3.5.0"):
        remove_tree("apache-maven-3.5.0")
    tar = tarfile.open("apache-maven-3.5.0.tar.gz")
    tar.extractall()
    tar.close()
    if host_platform == 0:
        st = os.stat(mvn_bin)
        os.chmod(mvn_bin, st.st_mode | stat.S_IEXEC)
    print ("Done.\n")

def BuildPlugins(quiet):
    global host_platform, builder_dir, mvn_bin

    print("Building plugins\n------------------------------------")
    os.chdir("parent")
    if host_platform == 1:
        mvn_cmd = mvn_bin + ".cmd" + (" -q")*quiet + MVN_BUILD_CMD
    else:
        mvn_cmd = mvn_bin + (" -q")*quiet + MVN_BUILD_CMD
    try:
        subprocess.check_call(mvn_cmd)
    except subprocess.CalledProcessError as e:
        print ("\nERROR: Error occured while building plugins. Aborting")
        os.chdir(builder_dir)
        exit(-1)
    os.chdir(builder_dir)
    print("Done.\n")

#
# NOTE: This project is configured to build the plugins repository.
# Change the build source folder if you are using the different way
#
def PublishPlugins():
    global host_platform, install_dir

    print("Publishing plugins\n------------------------------------")
    if os.path.isdir(install_dir):
        remove_tree(install_dir)
    copy_tree("repo" +slash+ "target" +slash+ "repository", install_dir)
    print("Done.\n")

#
# TODO: Append and directories you want to delete after the build
# e.g. plugin_name/target folders
#
def Cleanup():
    print("Cleaning up\n------------------------------------")
    remove_tree("apache-maven-3.5.0")
    remove_tree("repo" +slash+ "target")
    # remove_tree("com.your.company.plugin_name/target")
    print("Done.\n")

def PrintHelp():
    print ("\nusage: builder.py [-q]")
    print ("\noptional arguments:")
    print ("-h, --help               show this help message and exit")
    print ("-q, --quiet              supress Maven build output.")

if __name__ == '__main__':
    quiet_mode = False

    for arg in sys.argv[1:]:
        if arg == "--help" or arg == "-h":
            PrintHelp()
            exit(0)
        elif arg == "--quiet" or arg == "-q":
            quiet_mode = True
        else:
            print ("\nError: invalid argument: " + arg)
            PrintHelp()
            exit(-1)

    PrepareMaven()
    BuildPlugins(quiet=quiet_mode)
    PublishPlugins()
    # Cleanup()

    print("\nDone.")
