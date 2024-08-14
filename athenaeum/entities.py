import random
from dataclasses import dataclass
from typing_extensions import Self
from config import settings  # type: ignore


@dataclass
class Account(object):
    """
    使用教程：
        settings.toml
        [default.account.baidu.user1]
        owner = "xxx"
        username = "111111"
        password = "999999"

        [default.account.360.user1]
        owner = "yyy"
        username = "222222"
        password = "888888"

    """
    platform: str
    owner: str
    username: str
    password: str

    @classmethod
    def get_a_random_account(cls, platform: str) -> Self:
        users = settings.account[platform]
        user = users[random.choice(list(users.keys()))]
        return cls(
            platform=platform,
            owner=user.owner,
            username=user.username,
            password=user.password
        )
