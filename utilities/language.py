from utilities.typing import TagName, Language



def process_language(tag: str) -> tuple[TagName, Language|None]|None:
    s: list[str] = tag.split("|")
    if not s: return 
    return (s[0], s[1])if len(s) > 1 else (s[0], None)

def get_languages(language_string: str): return language_string.split("|")