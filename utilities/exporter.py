import os, inkex
from inkex.command import write_svg, inkscape
from utilities.typing import Language

class Exporter:
    FORMATS: dict[str,str] = {
        "png": 'export-dpi:{dpi};export-filename:{file_name};export-do;FileClose',
        "pdf": 'export-dpi:{dpi};export-pdf-version:1.5;export-text-to-path;export-filename:{file_name};export-do;FileClose',
        "ps": 'export-dpi:{dpi};export-text-to-path;export-filename:{file_name};export-do;FileClose',
        "eps": 'export-dpi:{dpi};export-text-to-path;export-filename:{file_name};export-do;FileClose'
    }

    @classmethod
    def setup(cls, format, tempdir, output_folder, **kwargs):
        cls.format = format
        cls.tempdir = tempdir
        cls.output_folder = output_folder
        cls.options = kwargs["options"]


    @classmethod
    def export(cls, file_name: str, new_doc, index: int, language: Language):
        file_name = f"{file_name}_{language}_{index}.{cls.format}"
        if not os.path.exists(cls.output_folder): return inkex.errormsg("The selected output folder does not exist.")
        file_path = os.path.join(cls.output_folder, file_name)
        if cls.format == "svg":
            write_svg(new_doc, file_path)
        else:
            temp_svg_name = '{0}.svg'.format(file_name)
            temp_svg_path = os.path.join(cls.tempdir, temp_svg_name)
            write_svg(new_doc, temp_svg_path)
            
            export_args = Exporter.FORMATS[cls.format].format(dpi=cls.options["dpi"], file_name=file_path)
            cli_output = inkscape(temp_svg_path, actions=export_args)
            if len(cli_output) <= 0: return
            cls.debug("Inkscape returned the following output when trying to run the file export; the file export might still work")
            cls.debug(cli_output)