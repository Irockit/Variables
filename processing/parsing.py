import re
from re import Pattern

CURLY_RE: Pattern[str] = re.compile(r"\{([a-zA-Z0-9_[\]{}()\-| ]{1,30})\}")
SQUARE_RE: Pattern[str] = re.compile(r"\[([a-zA-Z0-9_[\]{}()\-| ]{1,30})\]")
ROUND_RE: Pattern[str] = re.compile(r"\(([a-zA-Z0-9_[\]{}()\-| ]{1,30})\)")

class TagParser:
    """
    Parses tags and return the containing string ex "{{name}}" using TagParser.is_tag would return "{name}" and using TagParser.is_text with it
    would return "name"
    """
    def is_tag(tag: str) -> str|None : 
        '''Returns the text inside {} brackets'''
        return TagParser.is_match(tag, CURLY_RE)
    def is_text(tag: str) -> str|None : 
        '''Returns the text inside {} brackets'''
        return TagParser.is_match(tag, CURLY_RE)
    def is_svg(tag: str) -> str|None : 
        '''Returns the text inside [] brackets'''
        return TagParser.is_match(tag, SQUARE_RE)
    def is_global(tag: str) -> str|None : 
        '''Returns the text inside () brackets'''
        return TagParser.is_match(tag, ROUND_RE)
    def is_match(tag: str, patern: Pattern[str]) -> str|None:
        re_match = patern.match(tag)
        return re_match.group(1) if re_match else None