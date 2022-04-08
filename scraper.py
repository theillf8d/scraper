""" scraper.py - gets stories from Hacker News with scores >= 100 (first 3 pages only) """
import sys
import pprint
import requests
from bs4 import BeautifulSoup


def get_links(response):
    """ return elements with class 'titlelink' """
    return response.select(".titlelink")


def get_subtext(response):
    """ return elements with class 'subtext' """
    return response.select(".subtext")


def get_page_response(num):
    """ returns BeautifulSoupified response for number of pages requested """
    base_url = 'http://news.ycombinator.com'
    suffix = "/news?p="
    url = base_url if num == 1 else f"{base_url}{suffix}{num}"
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")


def create_custom_hn(links, scores):
    """ returns list of stories and links sorted by score """
    zipt = zip(links, scores)
    stories = []
    for link, score in zipt:
        score = int(score.text.split(" ")[0])
        if score >= 100:
            stories.append({link.getText(): link.get("href", None), 'score': score})
    return sort_stories_by_vote(stories)


def sort_stories_by_vote(lst):
    """ sorts list by 'score' key """
    return sorted(lst, key=lambda k: k["score"], reverse=True)


def main():
    """ entrypoint """
    links = []
    scores = []

    for i in range(0, 3):
        resp = get_page_response(i + 1)
        # print(resp)
        links += get_links(resp)
        scores += get_subtext(resp)

    stories = create_custom_hn(links, scores)
    for item in stories:
        pprint.pprint(item)


if __name__ == "__main__":
    sys.exit(main())
