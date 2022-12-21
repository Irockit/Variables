import csv
from tag.input_tag import InputInfo, InputTags, InputTagValues, InputTagValue, TextInputTag, SvgInputTag
from tag.tag_header import TagHeader, TextTagHeader, SVGTagHeader
from .parsing import TagParser
from utilities.language import process_language
from utilities.typing import TagName, TagType, Language, Languages
from .processor import Processor
from utilities. svg_cache import SvgCache

class CSV(Processor):
    _temp: dict[tuple[TagName, TagType], dict[Language, list[str]]] = {}
    langs: Languages = Languages()
    rows: int = 0



    @classmethod
    def load_tags(cls, file: str, debug):
        with open(file, 'r') as f: 
            new_f = f.read().replace("\n,", ",").split("\n") #\r\n,
            return cls.to_tags(csv.reader(new_f), debug) 


    @classmethod
    def to_tags(cls, csv, debug) -> InputInfo: 
        tags: InputTags = InputTags()
        cls.get_csv_data(csv, debug)

        for info, tag in cls._temp.items():
            if info is None: continue
            tag_name, tag_type = info
            input_values = InputTagValues()
            languages, tag_values = cls.sort_values_and_languages(tag_name, tag_type, tag, debug)
            for values in tag_values.values():
                for value in values:
                    input_values.add(value)
            match tag_type:
                case TagType.TEXT: tags.add(tag_name, TextInputTag(input_values, languages))
                case TagType.SVG: tags.add(tag_name, SvgInputTag(input_values, languages))
        return InputInfo(tags, cls.langs, cls.rows)


    @classmethod
    def sort_values_and_languages(cls, name, type, tag, debug):
        tag_values: dict[str, list[InputTagValue]] = {}
        languages: list[Language|None] = []
        for i, (language, values) in enumerate(tag.items()):
            if name not in tag_values: tag_values[name] = []
            for index, value in enumerate(values):
                if i == 0: tag_values[name].append(InputTagValue())
                if language is None: language = "None"
                languages.append(language)
                if type is TagType.SVG: SvgCache.add(value, debug)
                tag_values[name][index].set(value, language)
        return (languages, tag_values)

    @classmethod
    def get_csv_data(cls, csv, debug):
        headers: list[TagHeader|None] = [cls.process_header(header, debug) for header in next(csv)]
        for row in csv:
            cls.rows+=1
            for i, header in enumerate(headers):
                if header is None: continue
                name = header.name
                tag_type = header.type
                lang = header.language
                if not (name, tag_type) in cls._temp: cls._temp[(name, tag_type)] = {} 
                if not lang in cls._temp[(name, tag_type)]: cls._temp[((name, tag_type))][lang] = []
                if lang is not None: cls.langs.add(lang)
                cls._temp[(name, tag_type)][lang].append(row[i]) 

    @classmethod
    def process_header(cls, header: str, debug) -> TagHeader|None: 
        match = TagParser.is_tag(header)
        if match is not None : return cls.get_typed_header(match, debug)

    @classmethod
    def get_typed_header(cls, tag:str, debug) -> TagHeader|None:
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



