import csv, re
from re import Pattern

from typing import Iterator

TAG_RE: Pattern[str] = re.compile(r"\{\{([a-zA-Z0-9_\- ]{1,30})\}\}")

class Tags:
    def __init__(self): 
        self.tags: dict[str, str] = {}
        self.count: int = 0
    def __contains__(self, item): return item in self.tags
    def __getitem__(self, key: str) -> str: return self.tags[key]
    def __setitem__(self, key, value: str) -> None: self.tags[key] = value
    def items(self) : return self.tags.items()
    def get_tag(tag: str) -> str|None: 
         for match in TAG_RE.finditer(tag):
           return match.group(1)

class SvgTags(Tags):
    def __init__(self): super().__init__()
    def add_id(self, key: str, id: str) -> None: 
        self[key] = id
        self.count += 1

class CsvTags(Tags): 
    def __init__(self, file: str):
        super().__init__()
        self.row_count: int = 0
        self.load_csv_tags(file)
        

    def load_csv_tags(self, file: str):
        with open(file, 'r') as csv_file: 
            self.csv_to_tags(csv.reader(csv_file))

    def csv_to_tags(self, csv: Iterator[list[str]]): 
        names: list[str|None] = list([self.names_from_headers(header) for header in next(csv)])

        for row in csv:
            self.row_count += 1
            for i, name in enumerate(names):
                if name is not None:
                    self[name].append(row[i])


    def names_from_headers(self, header: str) -> str:
        tag: str|None = Tags.get_tag(header) 
        if tag is None: return 
        self[tag] = []
        return tag