from .processor import Processor

from tag.document_tag import DocumentTags, DocumentTag, NamedDocumentTag, DocumentTextTag, DocumentSvgTag, DocumentGlobalTag

from utilities.typing import TagType
from utilities.typing import TagName, DocumentId, DefaultTagValue
from inkex.elements import Anchor, Layer
from utilities.utils import Target, is_text, is_tspan, remove_tspans
from .parsing import TagParser
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
                        #debug(f"{name} {element_id} {default}")
                        return (name, DocumentTextTag(element_id, default))
                    case TagType.SVG: 
                        # debug(name)
                        return (name, DocumentSvgTag(element_id, default))
                    case TagType.GLOBAL: 
                        # debug(name)
                        return (name, DocumentGlobalTag(element_id, default))
    
    @classmethod
    def process_child(cls, element: Anchor, tag_type: TagType, debug) -> tuple[DocumentId, DefaultTagValue|None]|None:
        if element is None: return
        dbg_str = ""
        dbg_str += f"element: {element.get_id()}, {element.text}"
        for child in element:
            if is_text(child):
                dbg_str += f"is text: {child.get_id()}, {child.text}"
                #debug("is text")
                for sub in child: 
                    if is_tspan(sub):
                        return cls.process_tspan(sub)
                return (child.get_id(), child.text)
            else:
                debug(dbg_str)
                return (child.get_id(), None)

    @classmethod
    def process_tspan(cls, element):
        for child in element:
            if is_tspan(child): return cls.process_tspan(child)
        return (element.get_id(), element.text)