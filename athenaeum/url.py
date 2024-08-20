import urllib.parse
from furl import furl
from typing import Optional, Dict, List, Any


class Url(object):

    @classmethod
    def get_origin_path(cls, url: str) -> str:
        return f'{furl(url).origin}{furl(url).path}'

    @classmethod
    def is_valid(cls, url: str) -> bool:
        try:
            result = urllib.parse.urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    @classmethod
    def quote(cls, url: str) -> str:
        return urllib.parse.quote(url)

    @classmethod
    def unquote(cls, url: str) -> str:
        return urllib.parse.unquote(url)

    @staticmethod
    def encode(params: Dict[str, str]) -> str:
        return urllib.parse.urlencode(params)

    @classmethod
    def decode(cls, url: str) -> Dict[str, str]:
        params = dict()
        kvs = url.split('?')[-1].split('&')
        for kv in kvs:
            k, v = kv.split('=', 1)
            params[k] = cls.unquote(v)
        return params

    @classmethod
    def join_params(cls, url: str, params: Optional[Dict[str, str]] = None) -> str:
        if not params:
            return url
        params = cls.encode(params)
        separator = '?' if '?' not in url else '&'
        return url + separator + params

    @classmethod
    def get_query_param_value(cls, url: str, key: str, default: Optional[Any] = None) -> str:
        value = furl(url).query.params.get(key, default=default)
        return value

    @classmethod
    def get_path_segments(cls, url: str) -> List[str]:
        return furl(url).path.segments
