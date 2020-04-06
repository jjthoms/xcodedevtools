#!/usr/bin/env python
#
# Bump build number in Info.plist files if a source file have changed.
#
# usage: bump_buildnum.py buildnum.ver sourceDir Info.plist [ ... Info.plist ]
#
# Copyright (c)2019 Andy Duplain <trojanfoe@gmail.com>
# Original: https://github.com/trojanfoe/xcodedevtools/blob/master/bump_buildnum.py
#
# Modified by jjthoms, 2020
#

import sys, os, subprocess, re
import json

def read_verfile(name):
    version = None
    build = None
    verfile = open(name, "r")
    for line in verfile:
        match = re.match(r"^version\s+(\S+)", line)
        if match:
            version = match.group(1).rstrip()
        match = re.match(r"^build\s+(\S+)", line)
        if match:
            build = int(match.group(1).rstrip())
    verfile.close()
    return (version, build)

def write_verfile(name, version, build):
    verfile = open(name, "w")
    verfile.write("version {0}\n".format(version))
    verfile.write("build {0}\n".format(build))
    verfile.close()
    return True

def set_plist_version(plistname, version, build):
    if not os.path.exists(plistname):
        print("{0} does not exist".format(plistname))
        return False

    plistbuddy = '/usr/libexec/Plistbuddy'
    if not os.path.exists(plistbuddy):
        print("{0} does not exist".format(plistbuddy))
        return False

    cmdline = [plistbuddy,
        "-c", "Set CFBundleShortVersionString {0}".format(version),
        "-c", "Set CFBundleVersion {0}".format(build),
        plistname]
    if subprocess.call(cmdline) != 0:
        print("Failed to update {0}".format(plistname))
        return False

    print("Updated {0} with v{1} ({2})".format(plistname, version, build))
    return True

def should_bump(vername, srcdirs):
    verstat = os.stat(vername)
    allnames = []
    
    for dirname in srcdirs:
    
        for dirname, dirnames, filenames in os.walk(dirname):
            for filename in filenames:
                allnames.append(os.path.join(dirname, filename))

        for filename in allnames:
            if filename.endswith("Info.plist"):
                continue
        
            filestat = os.stat(filename)
            if filestat.st_mtime > verstat.st_mtime:
                print("{0} is newer than {1}".format(filename, vername))
                return True

    return False

def upver(vername, srcdirs):
    (version, build) = read_verfile(vername)
    if version == None or build == None:
        print("Failed to read version/build from {0}".format(vername))
        return False

    # Bump the version number if any files in the source directories
    # have changed, including sub-directories.
    bump = should_bump(vername, srcdirs)

    if bump:
        build += 1
        print("Incremented to build {0}".format(build))
        write_verfile(vername, version, build)
        print("Written {0}".format(vername))
    else:
        print("Staying at build {0}".format(build))

    return (version, build)

if __name__ == "__main__":
    if os.environ.has_key('ACTION') and os.environ['ACTION'] == 'clean':
        print("{0}: Not running while cleaning".format(sys.argv[0]))
        sys.exit(0)

    if len(sys.argv) != 2:
        print("Usage: {0} settings.json".format(sys.argv[0]))
        sys.exit(1)
        
    with open(sys.argv[1], "r") as settings_file:
        settings = json.load(settings_file)
        
    if settings == None:
        sys.exit(2)

    vername = settings["version_file"]
    srcdirs = settings["source_directories"]
    plistnames = settings["info_plist_files"]

    (version, build) = upver(vername, srcdirs)
    if version == None or build == None:
        sys.exit(2)

    for plistname in plistnames:
        set_plist_version(plistname, version, build)

    sys.exit(0)
