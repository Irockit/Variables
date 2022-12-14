from inkex.elements._selected import ElementList
from .input_tag import InputInfo
from .document_tag import DocumentTags
from processing.process_svg import SVG
from processing.process_csv import CSV


class Tags:
    svg_tags: DocumentTags
    csv_info: InputInfo
    @staticmethod
    def process_input(csv_file: str, debug) -> InputInfo:
        return CSV.load_tags(csv_file, debug)

    @staticmethod
    def process_document(document: ElementList, debug) -> DocumentTags:
        return SVG.get(document, debug)

