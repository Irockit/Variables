from enum import Enum, auto

class TagType(Enum):
    TEXT = auto()
    SVG = auto()


class TagName(str): pass
class Language(str): pass
class Languages(set[Language]):pass
class DefaultTagValue(str): pass
class DocumentId(str): pass