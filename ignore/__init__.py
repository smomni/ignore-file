import fnmatch
from pathlib import Path
from typing import Generator, Union
__version__ = '0.1.1'


def match(relative_path: Path, pattern: str) -> bool:
    """
    Match a relative pattern against a glob-style pattern using stdlib fnmatch.

    :param relative_path:
    :param pattern:
    :return:
    """
    return fnmatch.fnmatch(relative_path, pattern)


def iterdir(dir_path: Path, ignore_file_name_or_path: Union[str, Path]='.ignore') -> Generator[Path, None, None]:
    """
    Recursively iterate files in a directory and yield paths that have no matches in the ignore file.
    The ignore file contains rows of glob-style patterns that are to be ignored.

    :param dir_path:
    :param ignore_file_name_or_path:
    :raises FileNotFoundError: if no ignore file is found
    :return:
    """
    if isinstance(ignore_file_name_or_path, str):
        ignore_file_path = dir_path / ignore_file_name_or_path
    else:
        ignore_file_path = ignore_file_name_or_path
    if not ignore_file_path.exists():
        raise FileNotFoundError(f'Missing ignore file {ignore_file_path}')
    ignore_pattern_arr = ignore_file_path.read_text().splitlines()
    ignore_pattern_set = set(ignore_pattern_arr)
    for path in dir_path.rglob('*'):
        if path.is_file() and path != ignore_file_path:
            for ignore_pattern in ignore_pattern_set:
                relative_path = path.relative_to(dir_path)
                if match(relative_path, ignore_pattern):
                    break
            else:
                yield path
