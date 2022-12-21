from processing.parsing import TagParser

def test_is_tag():
    tag_str = "{tag}"
    tag = TagParser.is_tag(tag_str)
    assert tag == "tag"

def test_is_not_tag():
    tag_str = "[I like chicken]"
    tag = TagParser.is_tag(tag_str)
    assert tag is None

def test_is_text():
    tag_str = "{text}"
    text = TagParser.is_text(tag_str)
    assert text == "text"

def test_is_not_text():
    tag_str = "[Would You ?]"
    text = TagParser.is_text(tag_str)
    assert text is None

def test_is_svg():
    tag_str = "[path]"
    svg = TagParser.is_svg(tag_str)
    assert svg == "path"

def test_is_not_svg():
    tag_str = "{this is not an svg}"
    svg = TagParser.is_svg(tag_str)
    assert svg == None