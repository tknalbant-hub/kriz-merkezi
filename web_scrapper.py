# web_scrapper.py
from duckduckgo_search import DDGS

class WebSpider:
    def crawl(self, topic):
        with DDGS() as ddgs:
            results = list(ddgs.text(topic, max_results=3))
            return [res['body'] for res in results]