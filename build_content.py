#!/usr/bin/env python

"""
This script builds everything in the content folder
"""
import sys
import os
import argparse
import shutil
import subprocess

TEMPLATE = "%s_template.html"
HEADER   = "%s_header.html"
FOOTER   = "%s_footer.html"

def pandoc_compile(path, build_path, file):
    # filename without extension
    filename_no_ext = os.path.splitext(file)[0]
    path = os.path.abspath(path)
    build_path = os.path.abspath(build_path)
    if os.path.exists(os.path.join(path, TEMPLATE % filename_no_ext)):
        template = os.path.join(path, filename_no_ext, TEMPLATE)
    if os.path.exists(os.path.join(path, HEADER % filename_no_ext)):
        header = os.path.join(path, HEADER % filename_no_ext)
    if os.path.exists(os.path.join(path, FOOTER % filename_no_ext)):
        footer = os.path.join(path, FOOTER % filename_no_ext)

    #pandoc_command = "pandoc %s -f markdown -t html5%s%s%s%s" % \
    #    (os.path.join(path, file),\
    #    (" -H %s" % header if 'header' in locals() else ""),\
    #    (" -A %s" % footer if 'footer' in locals() else ""),\
    #    (" --template %s" % template 'template' in locals() else ""),\
    #    (" -o %s" % os.path.join(path, "%s.html" % filename_no_ext)))

    pandoc_command = \
    ["pandoc",
     "%s" % os.path.join(path, file),
     #"-f", "markdown",
     #"-t", "html5",
     #"-H %s" % header if 'header' in locals() else "",
     #"-A %s" % footer if 'footer' in locals() else "",
     #"--template %s" % template if 'template' in locals() else "",
     "-o", "%s" % os.path.join(build_path, "%s.html" % filename_no_ext)]

    print "Compiling %s" % file
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
        if not os.path.exists(build_path):
            os.makedirs(build_path)
        for file in files:
            # If file ending in .md then pandoc it
            if file.endswith(".md"):
                pandoc_compile(path, build_path, file)
            # else copy to corresponding directory in build directory
            else:
                shutil.copyfile(os.path.join(path, file), \
                                os.path.join(build_path, file))

if __name__ == "__main__": main()
