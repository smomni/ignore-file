from pathlib import Path
from typing import Generator
__version__ = '0.1.0'


def iterdir(dir_path: Path, ignore_file: str='.ignore') -> Generator[Path, None, None]:
    """
    Recursively iterate files in a directory and yield paths that have no matches in the ignore file.
    The ignore file contains rows of glob-style patterns that are to be ignored.

    :param dir_path:
    :param ignore_file:
    :raises FileNotFoundError: if no ignore file is found
    :return:
    """
    ignore_file_path = dir_path / ignore_file
    if not ignore_file_path.exists():
        raise FileNotFoundError(f'Missing ignore file {ignore_file_path}')
    ignore_pattern_arr = ignore_file_path.read_text().splitlines()
    ignore_pattern_arr.append(ignore_file)
    ignore_pattern_set = set(ignore_pattern_arr)
    for path in dir_path.rglob('*'):
        if path.is_file():
            for ignore_pattern in ignore_pattern_set:
                relative_path = path.relative_to(dir_path)
                if relative_path.match(ignore_pattern):
                    break
            else:
                yield path
