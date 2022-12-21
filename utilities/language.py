from utilities.typing import TagName, Language


def process_language(tag: str) -> tuple[TagName, Language|None]|None:
    '''
    This function takes a string like "name|fr" or "name" and returns a tuple (name, fr) or (name, None)
    '''
    s: list[str] = tag.split("|")
    if not s: return 
    return (s[0], s[1])if len(s) > 1 else (s[0], None)

def get_languages(language_string: str):
    '''
    This function takes a string of values separated by | like "en|fr|sp" and returns a list ["en", "fr", "sp"]
    '''
    if language_string is None: return ["None"]
    languages = list(filter(lambda l: l != "",language_string.split("|")))
    if len(languages) >= 1:
        return languages 