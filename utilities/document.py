from utilities.typing import Language, TagType, TagName
from .exporter import Exporter
from .svg_cache import SvgCache

from tag.document_tag import DocumentTag
from tag.input_tag import InputTagValues
from tag.tags import Tags

import copy

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
        if Tags.svg_tags.has(name):
            match tag_type:
                case TagType.TEXT: self.set_text(name, values, languages)
                case TagType.SVG: self.set_svg(name, values, languages)
                case TagType.GLOBAL: self.set_global(name, values, languages)
    
    def set_text(self, name: TagName, values: InputTagValues, languages): 
        language = "None" if self.language not in languages else self.language
        document_tag: DocumentTag = Tags.svg_tags.get(name)
        if document_tag.type is  TagType.TEXT: self.root.getElementById(document_tag.id).text = values.get(self.index, language)

    def set_global(self, name: TagName, values, languages): 
        language = "None" if self.language not in languages else self.language
        document_tag: DocumentTag = Tags.svg_tags.get(name)
       
        if document_tag.type is TagType.GLOBAL:
            self.debug(f"setting global for : {name}  {document_tag.id} {values}")
            self.root.getElementById(document_tag.id).text = values.get(0, language)

    def set_svg(self, name: TagName, values: InputTagValues, languages): 
        language = "None" if self.language not in languages else self.language
        self.debug(f"{self.index} | Set svg values for {name} : {values.get(self.index, language)}")
        cache = SvgCache.get(values.get(self.index, language))
        if cache is None: return
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

