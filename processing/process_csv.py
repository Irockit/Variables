import csv
from tag.input_tag import InputInfo, InputTags, InputTagValues, InputTagValue, TextInputTag, SvgInputTag
from tag.tag_header import TagHeader, TextTagHeader, SVGTagHeader
from .parsing import TagParser
from utilities.language import process_language
from utilities.typing import TagName, TagType, Language, Languages
from .processor import Processor
from utilities. svg_cache import SvgCache

class CSV(Processor):
    @classmethod
    def load_tags(cls, file: str, debug):
        with open(file, 'r') as f: return cls.to_tags(csv.reader(f), debug)


    @classmethod
    def to_tags(cls, csv, debug) -> InputInfo: 
        headers: list[TagHeader|None] = [cls.process_header(header, debug) for header in next(csv)]
        tags: InputTags = InputTags()
        langs = Languages()

        _t: dict[tuple[TagName, TagType], dict[Language, list[str]]] = {} # {(TagName, TagType), {Language, [str]}}
        row_count: int = 0
        for row in csv:
            row_count+=1
            for i, header in enumerate(headers):
                if header is not None:
                    value = row[i]
                    name = header.name
                    tag_type = header.type
                    lang = header.language
                    if not (name, tag_type) in _t: _t[(name, tag_type)] = {} 
                    if not lang in _t[(name, tag_type)]: _t[((name, tag_type))][lang] = []
                    if lang is not None:
                        langs.add(lang)
                    _t[(name, tag_type)][lang].append(value) 
        
        for info, tag in _t.items():
            if info is None: continue
            tag_name, tag_type = info
            input_values = InputTagValues()
            languages: list[Language|None] = []
            tag_values: dict[str, list[InputTagValue]] = {}
            for i, (language, values) in enumerate(tag.items()):
                if tag_name not in tag_values: tag_values[tag_name] = []
                for index, value in enumerate(values):
                    if i == 0 :tag_values[tag_name].append(InputTagValue())
                    if language is  None: language = "None"
                    languages.append(language)
                    if tag_type is TagType.SVG:
                        SvgCache.add(value, debug)
                    tag_values[tag_name][index].set(value, language)
            for values in tag_values.values():
                for value in values:
                    input_values.add(value)
            match tag_type:
                case TagType.TEXT: tags.add(tag_name, TextInputTag(input_values, languages))
                case TagType.SVG: tags.add(tag_name, SvgInputTag(input_values, languages))
        return InputInfo(tags, langs, row_count)


    @classmethod
    def process_header(cls, header: str, debug) -> TagHeader|None: 
        # debug(f"process header: {header}")
        match = TagParser.is_tag(header)
        # debug(f"match: {match}")
        if match is not None : return cls.get_typed_header(match, debug)

    @classmethod
    def get_typed_header(cls, tag:str, debug) -> TagHeader|None:
        #debug("get typed header")
        processed_tag = cls.process_type(tag, debug)
        if processed_tag is None :return
        (inner_tag, tag_type) = processed_tag
        languages: Language|None 
        name: TagName
        processed_language = process_language(inner_tag)
        (name, languages) = processed_language
        match tag_type:
            case TagType.TEXT:return TextTagHeader(name, languages)
            case TagType.SVG:return SVGTagHeader(name, languages)



