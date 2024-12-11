import time
import typing as t
from bskyapi.clients import BskyApiClient
from bskyapi.storage.writers import DataWriter
from atproto import models


class SearchTermScraper:
    def __init__(self, bsky_client: BskyApiClient, writer: DataWriter = None):
        """
        :param bsky_client: Instance of BskyApiClient.
        :param writer: Optional instance of DataWriter for writing fetched data.
        """
        self.bsky_client = bsky_client
        self.writer = writer

    def _fetch(self, search_term: str, cursor: t.Union[int, None] = None) -> models.AppBskyFeedSearchPosts.Response:
        params = {"q": search_term, 'limit': 100}
        if cursor:
            params['cursor'] = cursor
        return self.bsky_client.client.app.bsky.feed.search_posts(params=params)

    def fetch_all_posts(self, search_term: str, limit: int = 1000) -> t.List[dict]:
        all_posts = []
        cursor = None
        while True:
            response = self._fetch(search_term, cursor)
            cursor = response.cursor
            posts = response.model_dump()['posts']
            all_posts.extend(posts)
            if not cursor:
                break
            if int(cursor) > limit:
                break
            time.sleep(2)
        
        # If a writer is provided, delegate the writing task
        if self.writer:
            self.writer.write(all_posts)
        
        return all_posts
