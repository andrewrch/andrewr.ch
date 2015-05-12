#!/usr/bin/env python

"""
This script builds everything in the content folder
"""
import sys
import os
import argparse
import shutil
import subprocess
import fnmatch

PANDOC   = "/home/andrew/.cabal/bin/pandoc"
TEMPLATE = "*template.html"
HEADER   = "*header.html"
FOOTER   = "*footer.html"
IGNORE_EXT = ["html", "sass", "map", "md", "cache"]
IGNORE_DIRS = [".sass-cache"]

def find_file_upward(path, pattern):
    for file in fnmatch.filter(os.listdir(path), pattern):
        return os.path.abspath(os.path.join(path, file))
    return find_file_upward(os.path.join(path, os.path.pardir), pattern)

def pandoc_compile(path, build_path, file):
    # filename without extension
    filename_no_ext = os.path.splitext(file)[0]
    path = os.path.abspath(path)
    build_path = os.path.abspath(build_path)

    template = find_file_upward(path, TEMPLATE)
    header = find_file_upward(path, HEADER)
    footer = find_file_upward(path, FOOTER)

    pandoc_command = \
    [PANDOC,
     "%s" % os.path.join(path, file),
     "-f", "markdown",
     "-t", "html5",
     "-H", "%s" % header,
     "-A", "%s" % footer,
     "--template", "%s" % template,
     "-o", "%s" % os.path.join(build_path, "%s.html" % filename_no_ext)]

    print "Compiling %s" % file
    print pandoc_command
    subprocess.call(pandoc_command)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("contents_dir")
    parser.add_argument("build_dir")
    args = parser.parse_args()
    for path, dirs, files in os.walk(args.contents_dir):
        # If directory, first check if exists in build directory and if not
        # then create it.
        build_path = path.replace(args.contents_dir, args.build_dir)
        if not os.path.exists(build_path) and \
           not any([dir in path for dir in IGNORE_DIRS]):
            os.makedirs(build_path)
        # Compile all markdown files
        md_files = fnmatch.filter(files, '*.md')
        for file in md_files:
            pandoc_compile(path, build_path, file)
        # Copy any other files that dont have an extension which we ignore
        other_files = [f for f in files if
                       not any([f.endswith(ext) for ext in IGNORE_EXT]) and
                       not any([dir in path for dir in IGNORE_DIRS])]
        for file in other_files:
            shutil.copyfile(os.path.join(path, file), \
                            os.path.join(build_path, file))

if __name__ == "__main__": main()
