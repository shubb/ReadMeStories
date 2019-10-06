import pprint
from unittest.mock import patch
from tests.mock_web_responses import GetMockResponse
from services.novel_sites import royal_road


def test_SearchByName():
    
    # Mock response so we always get a sample test html instead of really hitting RRD
    with patch('services.novel_sites.royal_road.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.text = GetMockResponse('rrd_search_response.html')

        search_result = royal_road.SearchByName('my title search')

        # Ensure one of the results in the returned list
        # has an ID which we know is in the sample test html
        assert filter(lambda story: story['id'] == '17690', search_result)


def test_GetTableOfContentsByID():

    # Mock response so we always get a sample test html instead of really hitting RRD
    with patch('services.novel_sites.royal_road.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.text = GetMockResponse('rrd_story_top_page.html')

        toc_result = royal_road.GetTableOfContentsByID('my story id')

        # Ensure one of the chapters in the returned list
        # has a chapter title which we know is in the sample test html
        assert filter(lambda chapter: 'Chapter 1 Coming of Age Ceremony' in chapter['title'], toc_result)

def test_GetChapterTextByURL():
    with patch('services.novel_sites.royal_road.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.text = GetMockResponse('rrd_story_chapter.html')

        chapter_result = royal_road.GetChapterTextByURL('my chapter url')

        # Ensure one of the results in the returned dict
        # has a story text line which we know is in the sample test html
        assert filter(lambda chapter: 'I get up and realize I can not move my entire body' in chapter['text'], chapter_result)

def test_GetStoryByID():
    # This one we will do live on RRD instead of sample htmls

    # Rip story 17690
    story_rip = royal_road.GetStoryByID('17690')

    # Grab the first chapter which should be called 'A Meaningless Box'
    chapter_one = next(filter(lambda chapter: 'Meaningless Box' in chapter['title'], story_rip))
    
    # First chapter should contain this text
    assert 'oversized black cloak' in chapter_one['text']
    
    # there should be at least 2 chapters in this story
    assert len(story_rip) > 2

