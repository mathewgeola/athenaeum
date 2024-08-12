import re
from typing import Union, Tuple, Sequence, AnyStr
from ...errors import CheckUrlError


class CheckUrlMixin(object):
    """
    example:

        class Example(CheckUrlMixin):
            url_patterns = (
                r'https?://www\.baidu\.com/s\?\S*?wd=(?P<wd>\S+?)(?:&|$)',
                r'https?://www\.so\.com/s\?\S*?q=(\S+?)(?:&|$)'
            )


        example = Example()
        print(example.check_url('https://www.baidu.com/s?wd=Example'))
        print(example.check_url('https://www.so.com/s?q=Example'))

    """
    url_patterns: Tuple[str, ...]

    def __repr__(self) -> str:
        return self.__class__.__name__

    __str__ = __repr__

    def check_url(self, url: str) -> Union[None, dict[str, AnyStr], Sequence[AnyStr]]:
        if not hasattr(self, 'url_patterns') or \
                not isinstance(self.url_patterns, tuple) or \
                not all(map(lambda x: isinstance(x, str), self.url_patterns)):
            raise CheckUrlError(f'{self.__class__.__name__}.url_patterns：`{self.__class__.url_patterns}` 赋值错误，'
                                f'其值只能是字符串元组！')

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

        raise CheckUrlError(f'url：`{url}` 没有匹配 {self.__class__.__name__}.url_patterns：'
                            f'{self.__class__.url_patterns}！')
