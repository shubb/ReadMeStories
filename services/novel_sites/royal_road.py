import urllib
import requests
from bs4 import BeautifulSoup
from requests.compat import urljoin

RRD_BASE_URL = "https://www.royalroad.com/"

RRD_SEARCH_URL = "fictions/search?title={}"

def SearchByName(name_to_search):
    "Search Royal Road for fiction with title containing name_to_search"
    
    # Fetch search results as html page from RRD
    search_url = urljoin(RRD_BASE_URL, RRD_SEARCH_URL.format(name_to_search))
    search_response = requests.get(search_url)
    
    # Throw if unsuccesssful
    search_response.raise_for_status()

    # Parse the page into a soup DOM
    search_soup = BeautifulSoup(search_response.text, 'html.parser')

    # Isolate the search results div
    search_results_div = search_soup.find(class_='search-container')

    # Pick out the individual search results in a list
    hmtl_search_results_list = search_results_div.find_all(class_='search-item')

    # Extract as a list of dicts, the data in each search result
    extracted_search_results = []
    for html_search_result in hmtl_search_results_list:
        
        extracted_search_result = {}

        # Within the search result div, find the title, description, and id
        extracted_search_result['title'] = html_search_result.find('h2').text
        extracted_search_result['description'] = html_search_result.find(class_='fiction-description').text
        extracted_search_result['id'] = str(html_search_result.find(class_='fiction-detail')['data-fid'])

        # Add the resulting dict of data to the final listing
        extracted_search_results.append(extracted_search_result)

    # Return the search result as a list of dicts containing title, description, and id
    return extracted_search_results
    

def GetTableOfContentsByID(rrd_story_id):
    pass

def GetChapterTextByURL(chapter_url):
    pass

def GetStoryByID(rrd_story_id):
    pass