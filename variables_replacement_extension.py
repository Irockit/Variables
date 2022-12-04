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

from tags import CsvTags
from svg_processing import SVGProcessing

import copy, time
from concurrent.futures import ThreadPoolExecutor as tp
from options import Options
from exporter import Exporter




class VariablesReplacementExtension(inkex.base.TempDirMixin, inkex.TextExtension):

    def effect(self):
        start = time.perf_counter()
        self.exporter = Exporter(self.options.format, self.tempdir, self.options.output_folder, options= {"dpi": self.options.dpi})
        self.csv_tags = CsvTags(self.options.csv_file)
        self.svg_process = SVGProcessing(self.get_nodes(), self.debug)
        self.svg_process.get_tagged_ids()
        root = self.get_root()

        self.execute_parallel() if self.options.parallel else self.execute()
        
        end = time.perf_counter()
        self.debug("saves: Completed in {0} seconds.".format(end-start))
        self.reset_defaults(root)
    
    def execute_parallel(self):
        with tp() as ex: [ex.submit(self.update_and_export, i, copy.deepcopy(self.document)) for i in range(self.csv_tags.row_count)]

    def execute(self): [self.update_and_export(i, copy.deepcopy(self.document)) for i in range(self.csv_tags.row_count)]

    def update_and_export(self, index, new_doc):
        self.change_variables(new_doc, index)
        self.exporter.export(self.options.output_name, new_doc, index)

    def reset_defaults(self, root):
        for tag, _ in self.csv_tags.items():
            if self.has_tag(tag): self.set_text(root, tag, self.svg_process.defaults[tag])

    def change_variables(self, new_doc, index):
        for tag, values in self.csv_tags.items(): 
            self.change_variable(tag, new_doc.getroot(), values, index)

    def change_variable(self, tag, root, values, index):
        if self.has_tag(tag): self.set_text(root, tag, values[index])

    def has_tag(self, tag: str) -> bool: return tag in self.svg_process
    def set_text(self, root, tag: str, text: str) -> None: root.getElementById(self.svg_process.tags[tag]).text = text
    def add_arguments(self, pars: ArgumentParser) -> None: Options.ProcessOptions(pars, self.debug)
    def get_root(self): return self.document.getroot()
    def get_nodes(self): return self.svg.selection or {None: self.get_root()}
    

if __name__ == '__main__':
    VariablesReplacementExtension().run()


