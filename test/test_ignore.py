import types
import pytest
import timeit
from typing import List, Union, Generator
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


def test_iterdir_ignore_files_in_root_but_include_files_in_subdirectories(shared_datadir):
    write_ignore_file(shared_datadir, ['*/'])
    path_arr = list(iterdir(shared_datadir))
    for path in path_arr:
        print(path)
    assert 8 == len(path_arr)


def pathspec_iterdir(
        dir_path: Path, ignore_file_name_or_path: Union[str, Path]='.ignore'
) -> Generator[Path, None, None]:
    import pathspec
    if isinstance(ignore_file_name_or_path, str):
        ignore_file_path = dir_path / ignore_file_name_or_path
    else:
        ignore_file_path = ignore_file_name_or_path
    if not ignore_file_path.exists():
        raise FileNotFoundError(f'Missing ignore file {ignore_file_path}')
    spec_str = ignore_file_path.read_text()
    spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, spec_str.splitlines())
    for node in spec.match_tree(dir_path):
        yield Path(node)


@pytest.mark.pathspec
def test_pathspec_ignore_csv_files(shared_datadir):
    import pathspec
    write_ignore_file(shared_datadir, ['*', '!.ignore', '!*.csv'])
    pathspec_path_arr = list(pathspec_iterdir(shared_datadir))
    write_ignore_file(shared_datadir, ['*.csv'])
    ignore_path_arr = list(iterdir(shared_datadir))
    assert len(pathspec_path_arr) == len(ignore_path_arr)


@pytest.mark.pathspec
@pytest.mark.parametrize('n', (100, 1000))
def test_ignore_file_vs_pathspec(n, shared_datadir):
    pathspec_str = "spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, spec_str.splitlines()); " \
                   "path_arr = list(map(Path, spec.match_tree(str(shared_datadir))))"
    spec_str = """
    *
    !*.csv
    """
    pathspec_time = timeit.timeit(
        pathspec_str,
        number=n,
        setup="from pathlib import Path; import pathspec",
        globals=locals()
    )
    write_ignore_file(shared_datadir, ['*.csv'])
    ignore_str = "list(iterdir(shared_datadir))"
    ignore_time = timeit.timeit(ignore_str, number=n, setup="from ignore import iterdir", globals=locals())
    print(f'pathspec {pathspec_time}s vs {ignore_time}s ignore_file (n={n}): '
          f'{ignore_time / pathspec_time} times faster than ignore_file')