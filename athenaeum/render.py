import os
import jinja2
import shutil
from typing import Dict
from athenaeum.file import File
from athenaeum.logger import logger


class Render(object):
    logger = logger

    athenaeum_dirpath = os.path.dirname(os.path.abspath(__file__))  # noqa
    templates_dirpath = os.path.join(athenaeum_dirpath, 'templates')  # noqa
    project_dirpath = os.path.join(templates_dirpath, 'project')  # noqa
    cwd_dirpath = os.getcwd()  # noqa

    @classmethod
    def render_template(cls, template_name: str, template_data: Dict[str, str]) -> str:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(cls.templates_dirpath))
        template = env.get_template(template_name)
        result = template.render(**template_data)
        cls.logger.success(f'渲染结果：{result}')
        return result

    @classmethod
    def render_project(cls) -> None:
        files, _dirs = File.get_files_and_dirs(cls.project_dirpath)
        for src_file in files:
            target_file = os.path.join(cls.cwd_dirpath, os.path.relpath(src_file, cls.project_dirpath))
            try:
                target_dir = os.path.dirname(target_file)
                os.makedirs(target_dir, exist_ok=True)
                if not os.path.exists(target_file):
                    shutil.copy(src_file, target_file)
                    cls.logger.success(f'渲染项目成功，target_file：{target_file}')
            except Exception as exception:
                cls.logger.exception(f'渲染项目异常，exception：{exception}！')
