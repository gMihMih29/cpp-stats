import pytest
from pathlib import Path

import cpp_stats.file_sieve

def rename_git_ignore_and_modules(repo_path: Path, to_test: bool = True):
    '''
    Renames `test.gitignore` to `.gitignore` and 
    `test.gitmodules` to `.gitmodules` if `to_test == False` or
    renames `.gitignore` to `test.gitignore` and 
    `.gitmodules` to `test.gitmodules` if `to_test == True`
    '''
    if to_test:
        for entry in repo_path.rglob('.gitignore'):
            entry.rename(entry.parent.joinpath('test.gitignore'))
        for entry in repo_path.rglob('.gitmodules'):
            entry.rename(entry.parent.joinpath('test.gitmodules'))
    else:
        for entry in repo_path.rglob('test.gitignore'):
            entry.rename(entry.parent.joinpath('.gitignore'))
        for entry in repo_path.rglob('test.gitmodules'):
            entry.rename(entry.parent.joinpath('.gitmodules'))

@pytest.fixture
def repo():
    '''
    Returns path to test repository located at `/tests/data/repo`
    '''
    repo_path = Path('./tests/data/repo')
    rename_git_ignore_and_modules(repo_path, False)
    yield repo_path
    rename_git_ignore_and_modules(repo_path, True)

@pytest.fixture
def repo_with_gitignore():
    '''
    Returns path to test repository located at `/tests/data/repo_with_gitignore`
    '''
    repo_path = Path('./tests/data/repo_with_gitignore')
    rename_git_ignore_and_modules(repo_path, False)
    yield repo_path
    rename_git_ignore_and_modules(repo_path, True)

@pytest.fixture
def repo_with_2gitignore():
    '''
    Returns path to test repository located at `/tests/data/repo_with_2gitignore`
    '''
    repo_path = Path('./tests/data/repo_with_2gitignore')
    rename_git_ignore_and_modules(repo_path, False)
    yield repo_path
    rename_git_ignore_and_modules(repo_path, True)

@pytest.fixture
def repo_with_ignr_modules():
    '''
    Returns path to test repository located at `/tests/data/repo_with_ignr_modules`
    '''
    repo_path = Path('./tests/data/repo_with_ignr_modules')
    rename_git_ignore_and_modules(repo_path, False)
    yield repo_path
    rename_git_ignore_and_modules(repo_path, True)

def test_find_gitignore_1(repo: Path):
    '''
    Tests that in repository without .gitignore 
    function src.cpp_stats.file_sieve._locate_file does not locate one
    '''
    file_to_locate = '.gitignore'
    correct = []

    result = cpp_stats.file_sieve._locate_file(repo, file_to_locate, [])

    assert correct == result

def test_find_gitignore_2(repo_with_gitignore: Path):
    '''
    Tests that in repository with .gitignore 
    function src.cpp_stats.file_sieve._locate_file finds exactly one
    '''
    file_to_locate = '.gitignore'
    correct = [
        Path('./tests/data/repo_with_gitignore/.gitignore')
    ]

    result = cpp_stats.file_sieve._locate_file(repo_with_gitignore, file_to_locate, [])

    assert correct == result

def test_find_gitignore_3(repo_with_2gitignore: Path):
    '''
    Tests that in repository with .gitignore 
    function src.cpp_stats.file_sieve._locate_file finds exactly one
    '''
    file_to_locate = '.gitignore'
    correct = [
        Path('./tests/data/repo_with_2gitignore/.gitignore'),
        Path('./tests/data/repo_with_2gitignore/folder/.gitignore'),
    ]

    result = cpp_stats.file_sieve._locate_file(repo_with_2gitignore, file_to_locate, [])

    assert correct == result

def test_find_gitignore_with_banned_dir_1(repo_with_2gitignore: Path):
    '''
    Tests that in repository with .gitignore 
    function src.cpp_stats.file_sieve._locate_file finds exactly one
    '''
    file_to_locate = '.gitignore'
    banned_dirs = [
        Path('./tests/data/repo_with_2gitignore/folder/')
    ]
    correct = [
        Path('./tests/data/repo_with_2gitignore/.gitignore'),
    ]

    result = cpp_stats.file_sieve._locate_file(repo_with_2gitignore, file_to_locate, banned_dirs)

    assert correct == result

def test_list_gitignore_dirs_1(repo_with_gitignore: Path):
    gitignore_path = repo_with_gitignore.joinpath('.gitignore')
    correct = [
        repo_with_gitignore.joinpath('ignored_dir/')
    ]

    result = cpp_stats.file_sieve._get_git_ignore_dirs(gitignore_path)

    assert correct == result

def test_list_gitignore_dirs_2(repo_with_2gitignore: Path):
    gitignore_path = repo_with_2gitignore.joinpath('.gitignore')
    correct = [
        repo_with_2gitignore.joinpath('ignored_dir')
    ]

    result = cpp_stats.file_sieve._get_git_ignore_dirs(gitignore_path)

    assert correct == result

def test_list_gitignore_dirs_3(repo_with_2gitignore: Path):
    gitignore_path = repo_with_2gitignore.joinpath('folder').joinpath('.gitignore')
    correct = [
        repo_with_2gitignore.joinpath('folder').joinpath('ignored_dir')
    ]

    result = cpp_stats.file_sieve._get_git_ignore_dirs(gitignore_path)

    assert correct == result

def test_list_git_modules_dirs_1(repo_with_ignr_modules: Path):
    gitmodules_path = repo_with_ignr_modules.joinpath('.gitmodules')
    correct = [
        repo_with_ignr_modules.joinpath('submodule1'),
        repo_with_ignr_modules.joinpath('submodule2')
    ]

    result = cpp_stats.file_sieve._get_git_modules_dirs(gitmodules_path)

    assert correct == result
