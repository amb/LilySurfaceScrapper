# Copyright (c) 2019 Elie Michel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# The Software is provided “as is”, without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. In no event shall
# the authors or copyright holders be liable for any claim, damages or other
# liability, whether in an action of contract, tort or otherwise, arising from,
# out of or in connection with the software or the use or other dealings in the
# Software.
#
# This file is part of LilySurfaceScrapper, a Blender add-on to import materials
# from a single URL

bl_info = {
    "name": "Lily Surface Scrapper",
    "author": "Élie Michel <elie.michel@exppad.com>",
    "version": (1, 1, 3),
    "blender": (2, 80, 0),
    "location": "Properties > Material",
    "description": "Import material from a single URL",
    "warning": "",
    "wiki_url": "",
    "category": "Import",
}


def install_lib(libname):
    from subprocess import call
    import bpy

    pp = bpy.app.binary_path_python
    call([pp, "-m", "ensurepip", "--user"])
    call([pp, "-m", "pip", "install", "--user", libname])


try:
    import lxml  # noqa: F401
except ModuleNotFoundError:
    install_lib("lxml")
    import lxml  # noqa: F401


from . import frontend


def register():
    frontend.register()


def unregister():
    frontend.unregister()


if __name__ == "__main__":
    register()
