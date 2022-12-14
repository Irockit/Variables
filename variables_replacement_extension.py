#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) [YEAR] [YOUR NAME], [YOUR EMAIL]
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
Description of this extension
"""

import inkex
from argparse import ArgumentParser

from tags import Tags, InputInfo
from inkex.elements import SvgDocumentElement
#from svg_processing import SVGProcessing
from input_tag import InputTags, InputTagValues
from document_tag import DocumentTags, DocumentTag, DocumentId
import copy, time
from concurrent.futures import ThreadPoolExecutor as tp
from inkex.elements._selected import ElementList
from options import Options
from exporter import Exporter
from _types import TagType, TagName, Language
from svg_cache import SvgCache

class Document:
    debug = None
    index: int = 0
    data = None
    root = None
    language: str

    def __init__(self, document, index: int, language: Language, debug) -> None:
        self.debug = debug
        self.index = index
        self.data = copy.deepcopy(document)
        self.root = self.data.getroot()
        self.language = language

    def update_and_save(self, output_name):
        self.change_variables()
        self.save(output_name)

    def change_variables(self):
        for name, tag in Tags.csv_info.tags.tags():
            tag_type: TagType
            values: InputTagValues
            (tag_type, values) = tag
            self.change_variable(name, values, tag_type, tag.languages)
    
    def save(self, output_name):
         Exporter.export(output_name, self.data, self.index, self.language)

    def change_variable(self, name: TagName, values: InputTagValues, tag_type: TagType, languages):
        # self.debug(f"name {name} : {Tags.svg_tags}")
        if Tags.svg_tags.has(name):
            match tag_type:
                case TagType.TEXT: self.set_text(name, values, languages)
                case TagType.SVG: self.set_svg(name, values, languages)
    
    def set_text(self, name: TagName, values: InputTagValues, languages): 
        language = "None" if self.language not in languages else self.language
        document_tag: DocumentTag = Tags.svg_tags.get(name)
        if document_tag.type is  TagType.TEXT: self.root.getElementById(document_tag.id).text = values.get(self.index, language)

    def set_svg(self, name: TagName, values: InputTagValues, languages): 
        language = "None" if self.language not in languages else self.language
        self.debug(f"Set svg values for {name} : {values.get(self.index, language)}")
        cache = SvgCache.get(values.get(self.index, language))
        self.debug(cache)
        element = copy.deepcopy(cache)
        document_tag: DocumentTag = Tags.svg_tags.get(name)
        node = self.root.getElementById(document_tag.id)
        parent = node.getparent()
        parent.remove(node)
        parent.add(element)

class DocumentBuilder:
    debug = None
    data = None
    root = None
    language: str|None = None
    def __init__(self, document, debug) -> None:
        self.debug = debug
        self.data = document

    def set_language(self, language:str ): self.language = language

    def new(self, index: int) -> Document: return Document(self.data, index, self.language, self.debug)


def get_languages(language_string: str): return language_string.split("|")
    

class VariablesReplacementExtension(inkex.base.TempDirMixin, inkex.TextExtension):

    def effect(self):  
        self.debug(self.absolute_href("/A.png"))
        self.debug(self.absolute_href("./A.png"))
        self.debug(self.absolute_href("\A.png"))
        self.debug(self.absolute_href(".\A.png"))
        start = time.perf_counter()
        if self.options.relative: 
            SvgCache.set_relative()
            SvgCache.set_relative_function(self.relative_to_absolute)
        Tags.csv_info = Tags.process_input(self.options.csv_file, self.debug) 
        Tags.svg_tags: DocumentTags = Tags.process_document(self.document.getroot(), self.debug)
        self.languages: list[str] = get_languages(self.options.translations)
        
        Exporter.setup(self.options.format, self.tempdir, self.options.output_folder, options= {"dpi": self.options.dpi})
        #self.debug(f"{Tags.csv_info.tags}")
        #self.debug(f"{Tags.svg_tags}")

        with tp() as ex:
            document_builder = DocumentBuilder(self.document, self.debug)
            for language in self.languages:
                if language not in Tags.csv_info.languages: continue
                self.debug(language)
                document_builder.set_language(language)
                for i in range(Tags.csv_info.count):
                    new_document = document_builder.new(i)
                    if self.options.parallel: ex.submit(new_document.update_and_save, self.options.output_name)
                    else: new_document.update_and_save(self.options.output_name)

        end = time.perf_counter()
        self.debug("saves: Completed in {0} seconds.".format(end-start))

    @classmethod
    def relative_to_absolute(cls, name): return cls.absolute_href(name)

    def add_arguments(self, pars: ArgumentParser) -> None: Options.ProcessOptions(pars, self.debug)
    

if __name__ == '__main__':
    VariablesReplacementExtension().run()


