import yagmail
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Union, List, Any
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

    @classmethod
    def notify_by_tkinter(cls, title: Optional[str] = None, message: Optional[str] = None,
                          break_cond: Union[List[Union[None, bool]], Union[None, bool]] = True) -> None:
        if title is None:
            title = 'athenaeum 通知提醒'
        if message is None:
            message = '这是一个 `athenaeum 通知提醒` 的弹窗'

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
