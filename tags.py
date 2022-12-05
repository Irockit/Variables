import csv, re
from re import Pattern
from enum import Enum, auto
from typing import Iterator
from inkex.elements import load_svg

CURLY_RE: Pattern[str] = re.compile(r"\{([a-zA-Z0-9_[\]{}()\- ]{1,30})\}")
SQUARE_RE: Pattern[str] = re.compile(r"\[([a-zA-Z0-9_[\]{}()\- ]{1,30})\]")
ROUND_RE: Pattern[str] = re.compile(r"\(([a-zA-Z0-9_[\]{}()\- ]{1,30})\)")

class TagType(Enum):
    TEXT = auto()
    SVG = auto()

def _load_svg(file_name) :
        file_io = open(file_name, "rb")
        document = load_svg(file_io)
        file_io.close()
        layer = document.getroot().get_current_layer()
        return layer[0]

class Tags:
    def __init__(self, debug): 
        self.tags: dict[str, str] = {}
        self.count: int = 0
        self.debug = debug
    def __contains__(self, item): return item in self.tags
    def __getitem__(self, key: str) -> str: return self.tags[key]
    def __setitem__(self, key, value: str) -> None: self.tags[key] = value
    def items(self) : return self.tags.items()
    def get_tag(tag: str, debug) -> tuple[TagType, str]|None: 
        debug("try matching: {0}".format(tag))
        match = CURLY_RE.match(tag)
        if match :
            debug("matched outer")
            inner_tag = match.group(1)
            text_match = Tags.is_text(inner_tag, debug)
            if text_match is not None: 
                # debug("text match{0}".format(text_match))
                return (TagType.TEXT, text_match)
            svg_match = Tags.is_svg(inner_tag, debug)
            
            if svg_match is not None: 
                # debug("svg match{0}".format(svg_match))
                return (TagType.SVG, svg_match)

    
    def is_text(tag: str, debug) -> str|None : return Tags.is_match(tag, CURLY_RE, debug)
    def is_svg(tag: str, debug) -> str|None : return Tags.is_match(tag, SQUARE_RE, debug)
        

    def is_match(tag: str, patern: Pattern[str], debug) -> str|None:
        re_match = patern.match(tag)
        return re_match.group(1) if re_match else None

class SvgTags(Tags):
    def __init__(self, debug): super().__init__(debug)
    def add_id(self, key: str, tag_type :TagType, id: str) -> None: 
        self[key] = (tag_type, id)
        self.count += 1

class CsvTags(Tags): 
    def __init__(self, file: str, debug):
        super().__init__(debug)
        self.row_count: int = 0
        self.svg_cache = {}
        self.load_csv_tags(file)
        

    def load_csv_tags(self, file: str):
        with open(file, 'r') as csv_file: 
            self.csv_to_tags(csv.reader(csv_file))

    def csv_to_tags(self, csv: Iterator[list[str]]): 
        names: list[str|None] = [self.process_header(header) for header in next(csv)]

        for row in csv:
            self.row_count += 1
            for i, name in enumerate(names):
                if name is not None:
                    value = row[i]
                    self[name][1].append(value)
                    if self[name][0] == TagType.SVG:
                        if not value in self.svg_cache:
                            self.svg_cache[value] = _load_svg(value)


    def process_header(self, header: str) -> tuple[TagType, str]:
        data: tuple[TagType, str]|None = Tags.get_tag(header, self.debug) 
        if data is None: return 
        tag_type, name = data
        self[name] = [tag_type, []]
        return name