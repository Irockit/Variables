from _types import TagName, TagType, Language

class TagHeader:
    type: TagType
    name: TagName
    language: Language
    def __init__(self, tag_type:TagType, name: TagName, language: Language|None = None) -> None:
        self.type = tag_type
        self.name = name
        self.language = language
    def __str__(self) -> str:
        return f"{self.type} {self.name} {self.language}"

class TextTagHeader(TagHeader):
    def __init__(self, name: TagName, language: Language | None = None) -> None:
        super().__init__(TagType.TEXT, name, language)

class SVGTagHeader(TagHeader):
    def __init__(self, name: TagName, language: Language | None = None) -> None:
        super().__init__(TagType.SVG, name, language)