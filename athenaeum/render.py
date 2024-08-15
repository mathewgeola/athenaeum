import os
import jinja2
import shutil
from typing import Optional, Dict
from athenaeum.file import File
from athenaeum.logger import logger


class Render(object):
    logger = logger

    athenaeum_dirpath = os.path.dirname(os.path.abspath(__file__))  # noqa
    templates_dirpath = os.path.join(athenaeum_dirpath, 'templates')  # noqa
    project_dirpath = os.path.join(templates_dirpath, 'project')  # noqa
    cwd_dirpath = os.getcwd()  # noqa

    @classmethod
    def render_template(cls, filepath: Optional[str] = None,
                        filename: Optional[str] = None, dirpath: Optional[str] = None,
                        data: Optional[Dict[str, str]] = None,
                        result_filepath: Optional[str] = None) -> str:
        if not ((filepath is not None) or (filename is not None and dirpath is not None)):
            raise ValueError(f'filepath：`{filepath}` 或 filename：`{filename}` 和 dirpath：`{dirpath}` 必须赋值！')
        if data is None:
            data = dict()

        if filepath is not None:
            filename = os.path.basename(filepath)
            dirpath = os.path.dirname(filepath)

        loader = jinja2.FileSystemLoader(searchpath=dirpath)
        env = jinja2.Environment(loader=loader)
        template = env.get_template(name=filename)
        result = template.render(**data)

        if result_filepath is not None:
            with open(result_filepath, 'w', encoding='utf-8') as f:
                f.write(result)

        cls.logger.success(f'渲染结果：`{result}`')
        return result

    @classmethod
    def render_project(cls, project_name: str = os.path.basename(cwd_dirpath)) -> None:
        files, dirs = File.get_files_and_dirs(cls.project_dirpath)
        for src_file in files:
            target_file = os.path.join(cls.cwd_dirpath, os.path.relpath(src_file, cls.project_dirpath))
            try:
                target_dir = os.path.dirname(target_file)
                os.makedirs(target_dir, exist_ok=True)
                target_name = os.path.basename(target_file)
                target_prefix, target_suffix = os.path.splitext(target_name)
                if target_suffix == '.jinja2':
                    target_file = os.path.join(target_dir, target_prefix)
                    target_data = {
                        'project_name': project_name
                    }
                    if not os.path.exists(target_file):
                        cls.render_template(filepath=src_file, data=target_data, result_filepath=target_file)
                if not os.path.exists(target_file):
                    shutil.copy(src_file, target_file)
                    cls.logger.success(f'渲染项目成功，target_file：`{target_file}`')
            except Exception as exception:
                cls.logger.exception(f'渲染项目异常，exception：`{exception}`！')
