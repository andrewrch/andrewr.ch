andrewr.ch
===
This is my website, and it's hosted at andrewr.ch.

I doubt anyone will find this code useful, but I've left it here incase anyone 
else is looking for a quick and easy way to write simple static websites.

How it works
---
All pages are static and written in markdown (Just like this readme).  It's 
simple to write and with tools like pandoc, we can translate to other 
languages like HTML.

How to build
---
Clone this repository and then run

``
make
``

This calls `build_content.py`, which translates everything from markdown to 
HTML.

``
make install
``

will then copy the built HTML to /var/www

Repository contents
---
The file structure is expected to be similar to the following.

``
├── build_content.py
├── content
│   ├── website_1
│   │   ├── assets
│   │   │    ├── css
│   │   │    ├── js
│   │   │    └── images
│   │   └── index.md
│   ├── ...
│   ├── ...
│   └── website_N
│       ├── assets
│       │    ├── css
│       │    ├── js
│       │    └── images
│       └── index.md
└── makefile
``

The build content script first creates a build directory, and then walks
through the file hierarchy, translating any markdown files to HTML using
any available templates.  All other files are copied to the build directory.
