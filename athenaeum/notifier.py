import yagmail
from typing import Any
from athenaeum.logger import logger
from config import settings  # type: ignore


class Notifier(object):
    logger = logger

    def notify_by_dingding(self):
        pass

    @classmethod
    def notify_by_email(cls, **kwargs: Any) -> None:
        kw = {
            'to': settings.SMTP_USERNAME,
            'subject': 'athenaeum 通知提醒',
            'contents': '这是一封 `athenaeum 通知提醒` 的邮件',
        }
        kw.update(kwargs)

        try:
            yag = yagmail.SMTP(settings.SMTP_USERNAME, settings.SMTP_PASSWORD, settings.SMTP_HOST)
            yag.send(**kw)
        except Exception as exception:
            cls.logger.error(f'邮件发送失败，exception：{exception}！')
        else:
            cls.logger.success('邮件发送成功')
