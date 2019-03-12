import types
import pytest
from typing import List
from pathlib import Path
from ignore import iterdir


def write_ignore_file(dir_path: Path, ignore_pattern_arr: List[str]=()):
    ignore_path = dir_path / '.ignore'
    ignore_path.write_text('\n'.join(ignore_pattern_arr))
    return ignore_path


def test_iterdir_raises_file_not_found_error_if_no_ignore_file_is_found(shared_datadir):
    with pytest.raises(FileNotFoundError):
        list(iterdir(shared_datadir))


def test_iterdir_returns_generator_for_paths(shared_datadir):
    write_ignore_file(shared_datadir)
    gen = iterdir(shared_datadir)
    assert isinstance(gen, types.GeneratorType)
    for path in gen:
        assert isinstance(path, Path)


def test_iterdir_ignore_none(shared_datadir):
    write_ignore_file(shared_datadir)
    path_arr = list(iterdir(shared_datadir))
    assert 9 == len(path_arr)


def test_iterdir_ignore_bar_directory(shared_datadir):
    write_ignore_file(shared_datadir, ['bar/*'])
    path_arr = list(iterdir(shared_datadir))
    assert 4 == len(path_arr)


def test_iterdir_ignore_baz_directory(shared_datadir):
    write_ignore_file(shared_datadir, ['baz/*'])
    path_arr = list(iterdir(shared_datadir))
    assert 6 == len(path_arr)


def test_iterdir_ignore_foo_files(shared_datadir):
    write_ignore_file(shared_datadir, ['foo', '*/foo'])
    path_arr = list(iterdir(shared_datadir))
    assert 5 == len(path_arr)


def test_iterdir_ignore_csv_files(shared_datadir):
    write_ignore_file(shared_datadir, ['*.csv'])
    path_arr = list(iterdir(shared_datadir))
    assert 6 == len(path_arr)
    for path in path_arr:
        assert path.suffix != '.csv'


def test_iterdir_ignore_file_location_can_be_specified(datadir, shared_datadir):
    ignore_file_path = write_ignore_file(datadir, ['*.csv'])
    path_arr = list(iterdir(shared_datadir, ignore_file_name_or_path=ignore_file_path))
    assert 6 == len(path_arr)
    for path in path_arr:
        assert path.suffix != '.csv'
