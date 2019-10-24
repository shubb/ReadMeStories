import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def GetTableOfContentsFromEpub(epub):
    "Given an Epub file attempt to build a TOC"

    epup_docs_unfiltered = epub.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    epup_html_chapters = [ document for document in epup_docs_unfiltered if document.is_chapter() ]

    extracted_toc = []
    for chapter_number, epup_html_chapter in enumerate(epup_html_chapters):
        
        extracted_chapter = {}

        # Within the chapter html, extract the title and url. Add a synthetic chapter number
        extracted_chapter['chapter_number'] = chapter_number
        extracted_chapter['title'] = epup_html_chapter.get_id()
        extracted_chapter['html_chapter'] = epup_html_chapter

        extracted_toc.append(extracted_chapter)

    # Return a list of chapters, with title, content as a EpubHTML, and a synthetic chapter number
    return extracted_toc


def GetChapterTexFromEpubHTMLChapter(chapter_dict):
    "Given a chapter in EpubHTML form, extract chapter text"

    epub_html_chapter = chapter_dict['html_chapter']
    chapter_soup = BeautifulSoup(epub_html_chapter.get_content(), 'html.parser')
    body_soup = chapter_soup.find('body')

    return body_soup.text
    

def GetStoryByLocalPath(epub_path):
    "Load the epub at epub_path and extract chapters"

    epub_book = epub.read_epub(epub_path)

    # Get the TOC for this story
    story = GetTableOfContentsFromEpub(epub_book)

    # For each chapter in the TOC, fetch the text and return
    # a list containing the TOC data for the chapter plus the text
    for chapter in story:
        chapter['text'] = GetChapterTexFromEpubHTMLChapter(chapter)

    return story

""" 
    # Extract compulsory title metadata attribute
    title = epub.get_metadata('DC', 'title')[0][0]
    
    description = "No description"
    try:
        description = epub.get_metadata('DC', 'title')[0][0]
    except:
        pass """