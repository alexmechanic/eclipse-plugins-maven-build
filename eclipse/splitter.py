#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Alexander Gerasimov <samik.mechanic@gmail.com>
#

import os, subprocess, sys, platform
from os import listdir
from os.path import isfile, isdir, join
from filecmp import cmp, dircmp, cmpfiles
from distutils.dir_util import copy_tree, remove_tree
from distutils.file_util import copy_file, move_file

host_platform = 1 if platform.system() == "Windows" else 0
slash = "\\" if platform.system() == "Windows" else "/"
longpath_win32_prefix = "\\\\?\\"*host_platform
#
# NOTE: Eclipse platform distributions folder names 
#
ECLIPSE_DISTRO_LINUX_DIR = os.getcwd() +slash+ "eclipse-linux"
ECLIPSE_DISTRO_WIN32_DIR = os.getcwd() +slash+ "eclipse-win32"

#
# NOTE: Eclipse components folder names 
#
ECLIPSE_BASE_DIR = os.getcwd() +slash+ "base"
ECLIPSE_LINUX_DIR = os.getcwd() +slash+ "linux"
ECLIPSE_WIN32_DIR = os.getcwd() +slash+ "win32"

# Print iterations progress
def printProgressBar (iteration, total, prefix = 'Progress:', suffix = 'Complete', decimals = 1, length = 50, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

if __name__ == '__main__':
    i = 0
    #
    # INFO: make distributions backup to restore them after the split
    #
    print ("\nBackup original distributions\n------------------------------------")
    printProgressBar(0, 2)
    copy_tree(longpath_win32_prefix + ECLIPSE_DISTRO_LINUX_DIR,
              longpath_win32_prefix + ECLIPSE_DISTRO_LINUX_DIR + ".BAK")
    printProgressBar(1, 2)
    copy_tree(longpath_win32_prefix + ECLIPSE_DISTRO_WIN32_DIR,
              longpath_win32_prefix + ECLIPSE_DISTRO_WIN32_DIR + ".BAK")
    printProgressBar(2, 2)
    print ("Done.\n")
    #
    # INFO: move all files and platform-sensitive directories from root folder with no check
    #
    print ("\nSplitting\n------------------------------------")
    print ("\nSplitting sensitive root files...")
    linux_sensitives = listdir(ECLIPSE_DISTRO_LINUX_DIR)
    win32_sensitives = listdir(ECLIPSE_DISTRO_WIN32_DIR)
    i = 0
    printProgressBar(i, len(linux_sensitives)+len(win32_sensitives))
    for f in linux_sensitives:
        path = join(ECLIPSE_DISTRO_LINUX_DIR, f)
        if isfile(path):
            move_file(join(ECLIPSE_DISTRO_LINUX_DIR, f), ECLIPSE_LINUX_DIR)
        elif path.endswith("configuration"):
            copy_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_LINUX_DIR, f),
                      longpath_win32_prefix + ECLIPSE_LINUX_DIR +slash+ "configuration")
            remove_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_LINUX_DIR, f))
        elif path.endswith("dropins"):
            copy_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_LINUX_DIR, f),
                      longpath_win32_prefix + ECLIPSE_LINUX_DIR +slash+ "dropins")
            remove_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_LINUX_DIR, f))
        elif path.endswith("p2"):
            copy_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_LINUX_DIR, f),
                      longpath_win32_prefix + ECLIPSE_LINUX_DIR +slash+ "p2")
            remove_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_LINUX_DIR, f))
        i += 1
        printProgressBar(i, len(linux_sensitives)+len(win32_sensitives))

    for f in listdir(ECLIPSE_DISTRO_WIN32_DIR):
        path = join(ECLIPSE_DISTRO_WIN32_DIR, f)
        if isfile(path):
            move_file(join(ECLIPSE_DISTRO_WIN32_DIR, f), ECLIPSE_WIN32_DIR)
        elif path.endswith("configuration"):
            copy_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_WIN32_DIR, f),
                      longpath_win32_prefix + ECLIPSE_WIN32_DIR +slash+ "configuration")
            remove_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_WIN32_DIR, f))
        elif path.endswith("dropins"):
            copy_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_WIN32_DIR, f),
                      longpath_win32_prefix + ECLIPSE_WIN32_DIR +slash+ "dropins")
            remove_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_WIN32_DIR, f))
        elif path.endswith("p2"):
            copy_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_WIN32_DIR, f),
                      longpath_win32_prefix + ECLIPSE_WIN32_DIR +slash+ "p2")
            remove_tree(longpath_win32_prefix + join(ECLIPSE_DISTRO_WIN32_DIR, f))
        i += 1
        printProgressBar(i, len(linux_sensitives)+len(win32_sensitives))
    print ("Done.\n")

    #
    # INFO: compare features and plugins folders
    #
    print ("\nSplitting subdirectories...")
    for folder in listdir(ECLIPSE_DISTRO_LINUX_DIR):
        print("\nSplitting '" + folder + "' folder...")
        os.mkdir(ECLIPSE_BASE_DIR +slash+ folder)
        os.mkdir(ECLIPSE_WIN32_DIR +slash+ folder)
        os.mkdir(ECLIPSE_LINUX_DIR +slash+ folder)
        linux_list = [f for f in listdir(ECLIPSE_DISTRO_LINUX_DIR +slash+ folder)]
        win32_list = [f for f in listdir(ECLIPSE_DISTRO_WIN32_DIR +slash+ folder)]
        i = 0
        printProgressBar(i, len(linux_list))
        for item in linux_list: # find equal items in both distributions
            if item in win32_list:
                if isfile(ECLIPSE_DISTRO_LINUX_DIR +slash+ folder +slash+ item):
                    if cmp(ECLIPSE_DISTRO_LINUX_DIR +slash+ folder +slash+ item,
                           ECLIPSE_DISTRO_WIN32_DIR +slash+ folder +slash+ item,
                           shallow=True): # files equal
                        move_file(longpath_win32_prefix + ECLIPSE_DISTRO_LINUX_DIR +slash+ folder +slash+ item,
                                  longpath_win32_prefix + ECLIPSE_BASE_DIR +slash+ folder)
                        os.remove(longpath_win32_prefix + ECLIPSE_DISTRO_WIN32_DIR +slash+ folder +slash+ item)
                else: #isdir
                    dcmp = dircmp(ECLIPSE_DISTRO_LINUX_DIR +slash+ folder +slash+ item,
                                  ECLIPSE_DISTRO_WIN32_DIR +slash+ folder +slash+ item)
                    if len(dcmp.diff_files) == 0: # dirs equal
                        copy_tree(longpath_win32_prefix + ECLIPSE_DISTRO_LINUX_DIR +slash+ folder +slash+ item,
                                  longpath_win32_prefix + ECLIPSE_BASE_DIR +slash+ folder +slash+ item)
                        remove_tree(longpath_win32_prefix + ECLIPSE_DISTRO_LINUX_DIR +slash+ folder +slash+ item)
                        remove_tree(longpath_win32_prefix + ECLIPSE_DISTRO_WIN32_DIR +slash+ folder +slash+ item)
            i += 1
            printProgressBar(i, len(linux_list))
        # move diff items to platform folders
        copy_tree(longpath_win32_prefix + ECLIPSE_DISTRO_LINUX_DIR +slash+ folder,
                  longpath_win32_prefix + ECLIPSE_LINUX_DIR +slash+ folder)
        copy_tree(longpath_win32_prefix + ECLIPSE_DISTRO_WIN32_DIR +slash+ folder,
                  longpath_win32_prefix + ECLIPSE_WIN32_DIR +slash+ folder)
        remove_tree(longpath_win32_prefix + ECLIPSE_DISTRO_LINUX_DIR +slash+ folder)
        remove_tree(longpath_win32_prefix + ECLIPSE_DISTRO_WIN32_DIR +slash+ folder)
        print ("Done.\n")
    print ("Done.\n")
    print ("Done.\n")

    #
    # INFO: restore original distributions from backup
    #
    print ("\nRestore backup\n------------------------------------")
    printProgressBar(0, 6)
    remove_tree(ECLIPSE_DISTRO_LINUX_DIR)
    printProgressBar(1, 6)
    remove_tree(ECLIPSE_DISTRO_WIN32_DIR)
    printProgressBar(2, 6)
    copy_tree(longpath_win32_prefix + ECLIPSE_DISTRO_LINUX_DIR + ".BAK",
              longpath_win32_prefix + ECLIPSE_DISTRO_LINUX_DIR)
    printProgressBar(3, 6)
    copy_tree(longpath_win32_prefix + ECLIPSE_DISTRO_WIN32_DIR + ".BAK",
              longpath_win32_prefix + ECLIPSE_DISTRO_WIN32_DIR)
    printProgressBar(4, 6)
    remove_tree(ECLIPSE_DISTRO_LINUX_DIR + ".BAK")
    printProgressBar(5, 6)
    remove_tree(ECLIPSE_DISTRO_WIN32_DIR + ".BAK")
    printProgressBar(6, 6)
    print ("Done.\n")

    print("\nDone.")
