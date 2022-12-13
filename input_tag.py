from _types import Language, TagName, TagType, Languages
from svg_cache import SvgCache


class InputTagValue(dict[Language, str]):
    def set(self, value:str, language: Language|None): self[language] = value
    def get(self, language: Language|None = None) -> str: return self[language] if language in self else self[None]
    def __str__(self) -> str:
        str = f"InputTagValue : "
        for k, v in self.items():
            if k != "None": str+= f"\n\t\t\t\tlanguage: {k}"
            str+= f"\n\t\t\t\tvalue: {v}"
        return str

class InputTagValues(list[InputTagValue|None]):
    def add(self, tag: InputTagValue) -> None:
            self.append(tag)

    def get(self, index: int, language: Language):
        if  language is None: language = "None"
        if language in self[index]:
            return self[index][language]

    def __str__(self) -> str:
        str = f"InputTagValues : "
        for v in self:
            str+= f"\n\t\t\t{v}"
        return str

class InputTag:
    def __init__(self, tag_type: TagType, values: InputTagValues, languages: list[Language]):
        self.languages: list[Language] = languages
        self.type: TagType = tag_type
        self.values: InputTagValues|None = values
    def __str__(self) -> str:
        return f"InputTag : \n\t\t{self.type}\n\t\t{self.values}"
    def __iter__(self) -> tuple[TagType, InputTagValues]: return iter((self.type, self.values))

class TextInputTag(InputTag):
    def __init__(self, values: InputTagValues, languages: list[Language]):
        super().__init__(TagType.TEXT, values, languages)
    def __str__(self) -> str:
        return f"Text{super().__str__()}"
    

class SvgInputTag(InputTag):
    def __init__(self, values: InputTagValues, languages: list[Language]):
        super().__init__(TagType.SVG, values, languages)
    def __str__(self) -> str:
        return f"SVG{super().__str__()}"

class InputTags(dict[TagName, InputTag]):
    def add(self, name: TagName, values: InputTag) -> None: 
        self[name] = values
    def tags(self) : 
        for k, v in self.items():
            yield (k, v) 

    def __str__(self) -> str:
        str = f"\nInputTags : "
        for k, v in self.tags():
            str+= f"\n\t {k} : {v}"
        return str


class InputInfo:
    tags: InputTags
    languages: Languages
    count: int
    def __init__(self, tags: InputTags, languages: Languages, row_count) -> None:
        self.tags = tags
        self.languages = languages
        self.count = row_count
    def __str__(self) -> str:
        return f"{self.tags}\n{self.languages}"