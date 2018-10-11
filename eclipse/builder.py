#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Alexander Gerasimov <samik.mechanic@gmail.com>
#

import os, subprocess, sys, platform
from distutils.dir_util import copy_tree, remove_tree

TARGET_LINUX = 0
TARGET_WIN32 = 1
TARGET_BOTH  = 2

host_platform = 1 if platform.system() == "Windows" else 0
slash = "\\" if platform.system() == "Windows" else "/"
builder_dir = os.getcwd()
plugins_dir = os.getcwd() +slash+ ".." +slash+ "plugins"

#
# TODO: place your plugin names here
#
PLUGIN_NAMES = ["com.your.company.MyFeature.feature.group",
                "com.your.company.MyPlugin"]

def PrepareEclipse(target):
    global host_platform

    print ("\nPreparing Eclipse distribution\n------------------------------------")
    if target == TARGET_LINUX or target == TARGET_BOTH:
        if os.path.isdir("eclipse-linux"):
            remove_tree("eclipse-linux")
        if host_platform == 0:
            copy_tree(os.getcwd() + "/base", os.getcwd() + "/eclipse-linux")
            copy_tree(os.getcwd() + "/linux", os.getcwd() + "/eclipse-linux")
        else:
            copy_tree("\\\\?\\" + os.getcwd() + "\\base", "\\\\?\\" + os.getcwd() + "\\eclipse-linux")
            copy_tree("\\\\?\\" + os.getcwd() + "\\linux", "\\\\?\\" + os.getcwd() + "\\eclipse-linux")
    if target == TARGET_WIN32 or target == TARGET_BOTH:
        if os.path.isdir("eclipse-win32"):
            remove_tree("eclipse-win32")
        if host_platform == 0:
            copy_tree(os.getcwd() + "/base", os.getcwd() + "/eclipse-win32")
            copy_tree(os.getcwd() + "/win32", os.getcwd() + "/eclipse-win32")
        else:
            copy_tree("\\\\?\\" + os.getcwd() + "\\base", "\\\\?\\" + os.getcwd() + "\\eclipse-win32")
            copy_tree("\\\\?\\" + os.getcwd() + "\\win32", "\\\\?\\" + os.getcwd() + "\\eclipse-win32")
    print ("Done.\n")

def PreparePlugins():
    global host_platform, plugins_dir

    print("Building plugins\n------------------------------------")
    print("Executing " + plugins_dir +slash+ "builder.py...")
    os.chdir(plugins_dir)
    try:
        subprocess.check_call("python builder.py")
    except subprocess.CalledProcessError as e:
        print ("\nERROR: Error occured while building plugins. Aborting")
        os.chdir(builder_dir)
        exit(-1)
    os.chdir(builder_dir)
    print("Done.\n")

def InstallPlugins():
    global host_platform, plugins_dir, plugin_names
    install_prefix = " -nosplash -application org.eclipse.equinox.p2.director -repository file:"
    

    print("Installing plugins\n------------------------------------")
    if target == TARGET_LINUX or target == TARGET_BOTH:
        print("Installing plugins into Linux distribution...\n")
        if host_platform == 1:
            print("Cannot install plugins into Linux Eclipse distribution. Skipping")
        else:
            os.chdir("eclipse-linux")
            try:
                for plugin in PLUGIN_NAMES:
                    subprocess.check_call("./eclipse" + install_prefix + "//" + plugins_dir + "/Bin" + " -installIU " + plugin)
            except subprocess.CalledProcessError as e:
                print ("\nERROR: Error occured while installing plugins. Aborting")
                os.chdir(builder_dir)
                exit(-1)
            os.chdir(builder_dir)
    if target == TARGET_WIN32 or target == TARGET_BOTH:
        print("Installing plugins into Windows distribution...\n")
        if host_platform == 0:
            print("Cannot install plugins into Windows Eclipse distribution. Skipping")
        else:
            os.chdir("eclipse-win32")
            try:
                for plugin in PLUGIN_NAMES:
                    subprocess.check_call("eclipsec.exe" + install_prefix + plugins_dir + "\\Bin" + " -installIU " + plugin)
            except subprocess.CalledProcessError as e:
                print ("\nERROR: Error occured while installing plugins. Aborting")
                os.chdir(builder_dir)
                exit(-1)
            os.chdir(builder_dir)
    print("Done.\n")

def PrintHelp():
    print ("\nusage: builder.py [--target=OS] [options]")
    print ("\noptional arguments:")
    print ("-h, --help               show this help message and exit")
    print ("-t=OS, --target=OS       build Eclipse for target OS [linux, win32, both].")
    print ("                         (default value: native running OS)")
    print ("-nb, --nobuild           skip Eclipse plugins build")
    print ("-ni, --noinstall         skip Eclipse plugins installation")

if __name__ == '__main__':
    target          = TARGET_WIN32 if host_platform == 1 else TARGET_LINUX
    plugins_build   = True
    plugins_install = True

    for arg in sys.argv[1:]:
        if arg == "--help" or arg == "-h":
            PrintHelp()
            exit(0)
        elif arg.startswith("--target=") or arg.startswith("-t="):
            if arg.endswith("win32"):
                target = TARGET_WIN32
            elif arg.endswith("linux"):
                target = TARGET_LINUX
            elif arg.endswith("both"):
                target = TARGET_BOTH
            else:
                print ("\nError: invalid target: " + arg)
                PrintHelp()
                exit(-1)
        elif arg == "--nobuild" or arg == "-nb":
            plugins_build = False
        elif arg == "--noinstall" or arg == "-ni":
            plugins_install = False
        else:
            print ("\nError: invalid argument: " + arg)
            PrintHelp()
            exit(-1)

    PrepareEclipse(target=target)
    if plugins_build:
        PreparePlugins()
    if plugins_install:
        InstallPlugins(target=target)

    print("\nDone.")
