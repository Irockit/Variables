from utilities.typing import TagType, TagName, DocumentId, DefaultTagValue

class DocumentTag:
    type: TagType 
    id: DocumentId
    default: DefaultTagValue
    def __init__(self, tag_type: TagType, document_id: DocumentId, default: DefaultTagValue = None) -> None:
        self.type = tag_type
        self.id = document_id
        self.default = default
    def __str__(self) -> str:
        return f"\n\t{self.type}\n\t{self.id}\n\t{self.default}"

class DocumentTextTag(DocumentTag):
    def __init__(self, document_id: DocumentId, default: DefaultTagValue = None) -> None: super().__init__(TagType.TEXT, document_id, default)
class DocumentSvgTag(DocumentTag):
    def __init__(self, document_id: DocumentId, default: DefaultTagValue = None) -> None: super().__init__(TagType.SVG, document_id, default)

class DocumentTags(dict[TagName, DocumentTag]):
    def add(self, name: TagName, tag: DocumentTag) -> None: self[name] = tag
    def get(self, name: TagName)-> DocumentTag: return self[name]
    def has(self, name: TagName) -> bool: return name in self
    def __str__(self) -> str:
        str = f"\nDocumentTags : "
        for k, v in self.items():
            str+= f"\n{k}{v}\n"
        return str

class NamedDocumentTag(tuple[TagName, DocumentTag]): pass
