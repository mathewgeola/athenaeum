import urllib.parse
from furl import furl
from typing import Optional, Dict, List, Any


class Url(object):
    def __init__(self, url: str):
        self.url = url

    def get_origin_path(self, url: Optional[str] = None) -> str:
        if url is None:
            url = self.url
        return f'{furl(url).origin}{furl(url).path}'

    def is_valid(self, url: Optional[str] = None) -> bool:
        if url is None:
            url = self.url
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def quote(self, url: Optional[str] = None) -> str:
        if url is None:
            url = self.url
        return urllib.parse.quote(url)

    def unquote(self, url: Optional[str] = None) -> str:
        if url is None:
            url = self.url
        return urllib.parse.unquote(url)

    @staticmethod
    def encode(params: Dict[str, str]) -> str:
        return urllib.parse.urlencode(params)

    def decode(self, url: Optional[str] = None) -> Dict[str, str]:
        if url is None:
            url = self.url

        params = dict()

        kvs = url.split('?')[-1].split('&')
        for kv in kvs:
            k, v = kv.split('=', 1)
            params[k] = self.unquote(v)

        return params

    def join_params(self, params: Optional[Dict[str, str]], url: Optional[str] = None) -> str:
        if url is None:
            url = self.url
        if not params:
            return url

        params = self.encode(params)
        separator = '?' if '?' not in url else '&'
        return url + separator + params

    def get_query_param_value(self, key: str, default: Optional[Any] = None, url: Optional[str] = None) -> str:
        if url is None:
            url = self.url
        value = furl(url).query.params.get(key, default=default)
        return value

    def get_path_segments(self, url: str) -> List[str]:
        if url is None:
            url = self.url
        return furl(url).path.segments
