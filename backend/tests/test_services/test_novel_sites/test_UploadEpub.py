import ebooklib
from ebooklib import epub
from tests.test_assets import GetTestEpubPath
from services.novel_sites import uploaded_epub


def test_GetTableOfContentsFromEpub():
    book = epub.read_epub(GetTestEpubPath())
    toc_result = uploaded_epub.GetTableOfContentsFromEpub(book)

    # there should be 305 chapters in this story
    assert len(toc_result) == 305

def test_GetChapterTexFromEpubHTMLChapter():
    
    book = epub.read_epub(GetTestEpubPath())
    toc_result = uploaded_epub.GetTableOfContentsFromEpub(book)
    chapter_result = uploaded_epub.GetChapterTexFromEpubHTMLChapter(toc_result[1])

    # Ensure one of the results in the returned dict
    # has a story text line which we know is in the sample test html
    assert filter(lambda chapter: 'Gladly and back to the clock.' in chapter['text'], chapter_result)

def test_GetStoryByLocalPath():
       # Rip story 17690
    story_rip = uploaded_epub.GetStoryByLocalPath(GetTestEpubPath())

    # Grab the first chapter which should be called 'A Meaningless Box'
    chapter_one = next(filter(lambda chapter: 'chapter000' in chapter['title'], story_rip))
    
    # First chapter should contain this text
    assert 'Gladly and back to the clock.' in chapter_one['text']
    
    # there should be 305 chapters in this story
    assert len(story_rip) == 305
