import pprint
from unittest.mock import patch
from tests.mock_web_responses import GetMockResponse
from services.novel_sites import royal_road


def test_SearchByName():
    
    # Mock response so we always get a sample test html instead of really hitting RRD
    with patch('services.novel_sites.royal_road.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.text = GetMockResponse('search_response.html')

        search_result = royal_road.SearchByName('my title search')

        # Ensure one of the results in the returned dictionary
        # has an ID which we know is in the sample test html
        assert filter(lambda story: story['id'] == '17690', search_result)


def test_GetTableOfContentsByID():

    # Mock response so we always get a sample test html instead of really hitting RRD
    with patch('services.novel_sites.royal_road.requests.get') as mock_get:
        mock_get.return_value.ok = True
        mock_get.return_value.text = GetMockResponse('story_top_page.html')

        toc_result = royal_road.GetTableOfContentsByID('my story id')

        # Ensure one of the results in the returned dictionary
        # has an ID which we know is in the sample test html
        assert filter(lambda story: 'Chapter 1 Coming of Age Ceremony' in story['title'], toc_result)

def test_GetChapterTextByURL():
    assert False

def test_GetStoryByID():
    assert False