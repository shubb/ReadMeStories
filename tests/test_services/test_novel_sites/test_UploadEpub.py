import pprint
from unittest.mock import patch
from tests.test_assets import GetTestEpubPath
from services.novel_sites import uploaded_epub


def test_GetTableOfContentsFromEpub():
    toc_result = uploaded_epub.GetTableOfContentsFromEpub(GetTestEpubPath())

    # Ensure one of the chapters in the returned list
    # has a chapter title which we know is in the sample test html
    assert len(toc_result) == 5

def test_GetChapterTexFromChapter():
    
    toc_result = uploaded_epub.GetTableOfContentsFromEpub(GetTestEpubPath())
    chapter_result = uploaded_epub.GetChapterTexFromChapter(toc_result[0])

    # Ensure one of the results in the returned dict
    # has a story text line which we know is in the sample test html
    assert filter(lambda chapter: 'I get up and realize I can not move my entire body' in chapter['text'], chapter_result)

def test_GetStoryByLocalPath():
       # Rip story 17690
    story_rip = royal_road.GetStoryByLocalPath(GetTestEpubPath())

    # Grab the first chapter which should be called 'A Meaningless Box'
    chapter_one = next(filter(lambda chapter: 'Meaningless Box' in chapter['title'], story_rip))
    
    # First chapter should contain this text
    assert 'oversized black cloak' in chapter_one['text']
    
    # there should be at least 2 chapters in this story
    assert len(story_rip) > 2
