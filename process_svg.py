from processor import Processor
from document_tag import DocumentSvgTag, DocumentTextTag, NamedDocumentTag
from document_tag import DocumentTags, DocumentTag
from _types import TagType
from _types import TagName, DocumentId, DefaultTagValue
from inkex.elements import BaseElement, Anchor, Layer
from utils import Target, is_text, remove_tspans
from _parser import TagParser
from inkex.elements._selected import ElementList

class SVG(Processor):
    @classmethod
    def get(cls, document: ElementList, debug) -> DocumentTags:
        tags: DocumentTags = DocumentTags()
        for data in cls.explore_document(document, debug):
            name: TagName
            tag: DocumentTag
            (name, tag) = data
            tags.add(name, tag)
        return tags


    @classmethod
    def explore_document(cls, document, debug):
        for child in document:
            if isinstance(child, Layer):
                # debug("Layer")
                child = child.descendants()
                for c in child:
                    data = cls.explore_element(c, debug)
                    if data is not None: yield data
            data = cls.explore_element(child, debug)
            if data is not None: yield data

    @classmethod

        

    @classmethod
    def explore_element(cls, element, debug) -> NamedDocumentTag :
         if isinstance(element, Anchor): 
            # debug("Anchor")
            return cls.process_anchor(element, debug)
         else: 
            cls.explore_document(element, debug)

    @classmethod
    def process_anchor(cls, element: Anchor, debug) -> NamedDocumentTag :
        if Target.be(element):
            match = TagParser.is_tag(Target.get(element))
            if match is not None : 
                processed_tag = cls.process_type(match)
                if processed_tag is None : return
                name: TagName
                tag_type: TagType
                (name, tag_type) = processed_tag
                processed_child = cls.process_child(element, tag_type, debug)
                if processed_child is None: return
                element_id: DocumentId
                default: DefaultTagValue
                (element_id, default) = processed_child
                match tag_type:
                    case TagType.TEXT: 
                        # debug(name)
                        return (name, DocumentTextTag(element_id, default))
                    case TagType.SVG: 
                        # debug(name)
                        return (name, DocumentSvgTag(element_id, default))
    
    @classmethod
    def process_child(cls, element: Anchor, tag_type: TagType, debug) -> tuple[DocumentId, DefaultTagValue|None]|None:
        if element is None: return
        child = element[0]
        if is_text(child):
            remove_tspans(child)
            return (child.get_id(), child.text)
        else:
            return (child.get_id(), None)