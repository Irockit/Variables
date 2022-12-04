#!/usr/bin/env python
# coding=utf-8
"""
Test elements extra logic from svg xml lxml custom classes.
"""

from inkex.tester import TestCase, ComparisonMixin
from inkex.tester.inx import InxMixin

from variables_replacement_extension import VariablesReplacementExtension

import sys
sys.path.insert(0, '.')


class UnnamedBasicTestCase(InxMixin, TestCase):
    """Test INX files and other things"""

    def test_inx_file(self):
        """Get all inx files and test each of them"""
        self.assertInxIsGood("tutorial_01.inx")

    def test_other_things(self):
        """Things work out"""
        pass


class UnnamedComparisonsTestCase(ComparisonMixin, TestCase):
    """Test input and output variations"""
    effect_class = VariablesReplacementExtension
    comparisons = [
        ('--format=png',),
        ('--dpi=12',),
    ]



# "csv_file":         [str, "path to a CSV file", {"dest": "csv_file"}],
# "tab":              [str, "not needed at all", {"default": ""}],
# "format":           [str, "file format to export to: png, pdf, svg, ps, eps", {}],
# "dpi":              [int, "dpi value for exported raster images", {"default": "300"}],
# "output_folder":    [str, "pattern for the output file", {}],
# "output_name":      [str, "pattern for the output file", {}],
# "reset_default":    [inkex.Boolean, "Keeps the values on the main file", {"default": True}],
# "parallel":         [inkex.Boolean, "Execute The extension in parallel", {"default": True}],
