from utilities.language import get_languages, process_language

def test_get_languages_multiple():
    languages_str = "en|fr|sp"
    languages = get_languages(languages_str)
    assert languages[0] == "en" and languages[1] == "fr" and languages[2] == "sp", "String containgin en|fr|sp should return [en, fr, sp]"

def test_get_languages_single():
    languages_str = "en"
    languages = get_languages(languages_str)
    assert languages[0] == "en", "String containing en should return en"

def test_get_languages_none():
    languages_str = ""
    languages = get_languages(languages_str)
    assert languages is None, "Empty string should return None"

def test_get_languages_split_none():
    languages_str = "|"
    languages = get_languages(languages_str)
    assert languages is None, "String only containing | should return None"

def test_process_language():
    tag_str = "name|fr"
    (name, language) = process_language(tag_str)
    assert name == "name" and language == "fr"

def test_process_language2():
    tag_str = "name"
    (name, language) = process_language(tag_str)
    assert name == "name" and language == None
    

