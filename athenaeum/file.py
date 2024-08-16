import os
from typing import List, Tuple


class File(object):

    @classmethod
    def get_files_and_dirs(cls, path: str) -> Tuple[List[str], List[str]]:
        files = []
        dirs = []

        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file():  # noqa
                    files.append(entry.path)  # noqa
                elif entry.is_dir():  # noqa
                    dirs.append(entry.path)  # noqa
                    sub_files, sub_dirs = cls.get_files_and_dirs(entry.path)  # noqa
                    files.extend(sub_files)
                    dirs.extend(sub_dirs)

        return files, dirs
