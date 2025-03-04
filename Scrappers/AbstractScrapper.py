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

import os
import string

import sys

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "site-packages")
)
from lxml import etree

import requests
import shutil


class AbstractScrapper:
    # Can be 'MATERIAL', 'WORLD'
    scrapped_type = {"MATERIAL"}

    @classmethod
    def canHandleUrl(cls, url):
        raise NotImplementedError

    def __init__(self, texture_root=""):
        self.error = None
        self.texture_root = texture_root

    def fetchHtml(self, url):
        """Get a lxml.etree object representing the scrapped page.
        Use xpath queries to browse it."""
        r = requests.get(url)
        if r.status_code != 200:
            self.error = "URL not found: {}".format(url)
            return None
        else:
            return etree.HTML(r.text)

    def getTextureDirectory(self, material_name):
        """Return the texture dir, relative to the blend file, dependent on material's name"""
        name_path = material_name.replace("/", os.path.sep)
        dirpath = os.path.join(self.texture_root, "LilySurface", name_path)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath)
        return dirpath

    def fetchImage(self, url, material_name, map_name, force_ext=False):
        """Utility helper for download textures"""
        root = self.getTextureDirectory(material_name)
        if not force_ext:
            ext = os.path.splitext(url)[1]
            map_name = map_name + ext
        path = os.path.join(root, map_name)
        if os.path.isfile(path):
            print("Using cached {}.".format(url))
        else:
            print("Downloading {}...".format(url))
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(path, "wb") as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            else:
                self.error = "URL not found: {}".format(url)
                return None
        return path

    def fetchZip(self, url, material_name, zip_name):
        """Utility helper for download textures"""
        root = self.getTextureDirectory(material_name)
        path = os.path.join(root, zip_name)
        if os.path.isfile(path):
            print("Using cached {}.".format(url))
        else:
            print("Downloading {}...".format(url))
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(path, "wb") as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            else:
                self.error = "URL not found: {}".format(url)
                return None
        return path

    def clearString(self, s):
        """Remove non printable characters"""
        printable = set(string.printable)
        return "".join(filter(lambda x: x in printable, s))

    def fetchVariantList(self, url):
        """Get a list of available variants.
        The list may be empty, and must be None in case of error."""
        raise NotImplementedError

    def fetchVariant(self, variant_index, material_data):
        """Fill material_data with data from the selected variant.
        Must fill material_data.name and material_data.maps.
        Return a boolean status, and fill self.error to add error messages."""
        raise NotImplementedError
