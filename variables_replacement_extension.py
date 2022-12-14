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

from tag.tags import Tags
from tag.document_tag import DocumentTags

import inkex
from argparse import ArgumentParser
import time
from concurrent.futures import ThreadPoolExecutor as tp
from utilities.options import Options
from utilities.exporter import Exporter
from utilities.svg_cache import SvgCache
from utilities.language import get_languages
from utilities.document import DocumentBuilder

class VariablesReplacementExtension(inkex.base.TempDirMixin, inkex.TextExtension):

    def effect(self):  
        start = time.perf_counter()
        if self.options.relative: 
            SvgCache.set_relative()
            SvgCache.set_relative_function(self.relative_to_absolute)
        Tags.csv_info = Tags.process_input(self.options.csv_file, self.debug) 
        Tags.svg_tags: DocumentTags = Tags.process_document(self.document.getroot(), self.debug)
        self.languages: list[str] = get_languages(self.options.translations)
        Exporter.setup(self.options.format, self.tempdir, self.options.output_folder, options= {"dpi": self.options.dpi})

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


