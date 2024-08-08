import re
from typing import Union, Tuple, List, Dict
from ...errors import CheckUrlError


class CheckUrlMixin(object):
    url_patterns: List[str]

    def check_url(self, url: str) -> Union[None, Tuple[str, ...], Dict[str, str]]:
        if not hasattr(self, 'url_patterns') or not isinstance(self.url_patterns, list):
            raise CheckUrlError(f'{self.__class__.__name__}.url_patterns must be assigned values correctly!')

        if not self.url_patterns:
            return

        url_compilers = [re.compile(url_pattern) for url_pattern in self.url_patterns]
        for url_compiler in url_compilers:
            match = url_compiler.match(url)
            if match is None:
                continue
            groupdict = match.groupdict()  # noqa
            if groupdict:
                return groupdict
            groups = match.groups()
            if groups:
                return groups
            return

        raise CheckUrlError(f'Url does not conform to the rules of the {self.__class__.__name__}.url_patterns!')
