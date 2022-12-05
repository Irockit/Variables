from inkex.elements import Anchor, SvgDocumentElement, BaseElement
from tags import Tags, SvgTags, TagType

from utils import get_attibute, is_text, remove_tspans


class SVGProcessing:
    def __init__(self, svg: SvgDocumentElement, debug):
        self.svg: SvgDocumentElement = svg
        self.tags: SvgTags = SvgTags(debug)
        self.defaults: dict[str, str] = {}
        self.debug = debug

    def __contains__(self, item): return item in self.tags

    def get_tagged_ids(self): self.process_elements(self.svg.values())

    def process_elements(self, node):
        for child in node: 
            data: tuple[str: tuple[tuple[TagType, str], tuple[str, str]]]|None = self.process_element(child)
            if data is None: continue
            tag: tuple[TagType, str]
            values: tuple[str, str]
            (tag, values) = data
            (tag_type, name) = tag
            (id, default) = values
            self.tags.add_id(name, tag_type, id)
            self.defaults[name] = default

    def process_element(self, node: BaseElement) -> tuple[str, tuple[str, str]]|None: 
        if isinstance(node, Anchor): return self.process_anchor(node)
        else: self.process_elements(node)

    def process_anchor(self, anchor: Anchor) -> tuple[str, tuple[str, str]]|None:
        if anchor.attrib.has_key('target'): 
            if anchor is None: return None
            tag: tuple[TagType, str] | None = Tags.get_tag(get_attibute(anchor), self.debug)
            if tag is None: return None
            data: tuple[str, str]|None  = self.process_child(anchor[0], tag)
            if data is not None: return (tag, data)
            else: return None

    def process_child(self, node: BaseElement, tag: tuple[TagType, str]) -> tuple[str, str] | None:
        (tag_type, tag_name) = tag
        if not is_text(node) and tag in self.tags : return None
        remove_tspans(node)
        return (node.get_id(), node.text)