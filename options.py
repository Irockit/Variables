from argparse import ArgumentParser
import inkex

class Options:
    OPTIONS = {
            "csv_file":         [str, "path to a CSV file", {"dest": "csv_file"}],
            "tab":              [str, "not needed at all", {"default": ""}],
            "format":           [str, "file format to export to: png, pdf, svg, ps, eps", {}],
            "dpi":              [int, "dpi value for exported raster images", {"default": "300"}],
            "output_folder":    [str, "pattern for the output file", {}],
            "output_name":      [str, "pattern for the output file", {}],
            "reset_default":    [inkex.Boolean, "Keeps the values on the main file", {"default": True}],
            "parallel":         [inkex.Boolean, "Execute The extension in parallel", {"default": True}],
            "translations":     [str, "Localisations string", {}]
        }

    @classmethod
    def ProcessOptions(cls, parser: ArgumentParser, debug):
        for name, args in cls.OPTIONS.items():
            parser.add_argument("--{0}".format(name), type=args[0], help=args[1],  **args[2])