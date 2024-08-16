import httpx
import yagmail
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Union, List, Any
from athenaeum.logger import logger
from athenaeum.tools import get_routine_name
from config import settings  # type: ignore


class Notifier(object):
    logger = logger

    title = subject = 'athenaeum 通知提醒'
    message = content = '这是一个 `athenaeum 通知提醒` 来自 {}'

    @classmethod
    def notify_by_dingding(cls) -> None:
        method_name = get_routine_name()

    @classmethod
    def notify_by_email(cls, **kwargs: Any) -> None:
        method_name = get_routine_name()
        kw = {
            'to': settings.SMTP_USERNAME,
            'subject': cls.subject,
            'contents': cls.content.format(method_name),
        }
        kw.update(kwargs)

        try:
            yag = yagmail.SMTP(settings.SMTP_USERNAME, settings.SMTP_PASSWORD, settings.SMTP_HOST)
            yag.send(**kw)
        except Exception as exception:
            cls.logger.error(f'邮件发送失败，exception：{exception}！')
        else:
            cls.logger.success('邮件发送成功')

    @classmethod
    def notify_by_bark(cls, title: Optional[str] = None, message: Optional[str] = None) -> None:
        method_name = get_routine_name()
        if title is None:
            title = cls.title
        if message is None:
            message = cls.message.format(method_name)

        try:
            url = f'https://api.day.app/{settings.BARK_KEY}/{title}/{message}'
            _response = httpx.get(url)
        except Exception as exception:
            cls.logger.error(f'推送发送失败，exception：{exception}！')
        else:
            cls.logger.success('推送发送成功')

    @classmethod
    def notify_by_tkinter(cls, title: Optional[str] = None, message: Optional[str] = None,
                          break_cond: Union[List[Union[None, bool]], Union[None, bool]] = True) -> None:
        method_name = get_routine_name()
        if title is None:
            title = cls.title
        if message is None:
            message = cls.message.format(method_name)

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        while True:
            result = messagebox.askyesnocancel(title, message)
            if isinstance(break_cond, list):
                if result in break_cond:
                    break
            else:
                if result == break_cond:
                    break

        root.destroy()
