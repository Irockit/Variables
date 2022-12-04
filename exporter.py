import os, inkex
from inkex.command import write_svg, inkscape

class Exporter:
    FORMATS: dict[str,str] = {
        "png": 'export-dpi:{dpi};export-filename:{file_name};export-do;FileClose',
        "pdf": 'export-dpi:{dpi};export-pdf-version:1.5;export-text-to-path;export-filename:{file_name};export-do;FileClose',
        "ps": 'export-dpi:{dpi};export-text-to-path;export-filename:{file_name};export-do;FileClose',
        "eps": 'export-dpi:{dpi};export-text-to-path;export-filename:{file_name};export-do;FileClose'
    }
    def __init__(self, format, tempdir, output_folder, **kwargs):
        self.format = format
        self.tempdir = tempdir
        self.output_folder = output_folder
        self.options = kwargs["options"]

    def export(self, file_name: str, new_doc, index: int):
        file_name = "{0}_{1}.{2}".format(file_name, str(index), self.format)
        if not os.path.exists(self.output_folder): return inkex.errormsg("The selected output folder does not exist.")
        file_path = os.path.join(self.output_folder, file_name)
        if self.format == "svg":
            write_svg(new_doc, file_path)
        else:
            temp_svg_name = '{0}.svg'.format(file_name)
            temp_svg_path = os.path.join(self.tempdir, temp_svg_name)
            write_svg(new_doc, temp_svg_path)
            
            export_args = Exporter.FORMATS[self.format].format(dpi=self.options["dpi"], file_name=file_path)
            cli_output = inkscape(temp_svg_path, actions=export_args)
            if len(cli_output) <= 0: return
            self.debug("Inkscape returned the following output when trying to run the file export; the file export might still work")
            self.debug(cli_output)