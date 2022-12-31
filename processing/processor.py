from utilities.typing import TagType
from .parsing import TagParser

class Processor:
    @classmethod
    def process_type(cls, tag, debug = None) -> None|tuple[str, TagType]:
        # debug("process_type")
        text_match = TagParser.is_text(tag)
        if text_match is not None: return (text_match, TagType.TEXT)
        svg_match = TagParser.is_svg(tag)
        if svg_match is not None: return (svg_match, TagType.SVG)
        svg_match = TagParser.is_global(tag)
        if svg_match is not None: return (svg_match, TagType.GLOBAL)