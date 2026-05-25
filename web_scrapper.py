# web_scrapper.py
from googleapiclient.discovery import build

class WebSpider:
    def __init__(self, api_key, cse_id):
        self.service = build("customsearch", "v1", developerKey=api_key)
        self.cse_id = cse_id

    def crawl(self, topic):
        res = self.service.cse().list(q=topic, cx=self.cse_id).execute()
        return [item['snippet'] for item in res.get('items', [])[:3]]
