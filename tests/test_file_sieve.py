from pathlib import Path
import src.cpp_stats.file_sieve

import pytest

def rename_gitignore(repo_path: Path, to_test: bool = True):
    '''
    Renames `test.gitignore` to `.gitignore` if `to_test == False` or
    
    renames `.gitignore` to `test.gitignore` if `to_test == True`
    '''
    if to_test:
        for entry in repo_path.iterdir():
            if entry.name == '.gitignore':
                entry.rename(repo_path.joinpath('test.gitignore'))
    else:
        for entry in repo_path.iterdir():
            if entry.name == 'test.gitignore':
                entry.rename(repo_path.joinpath('.gitignore'))

@pytest.fixture
def repo():
    '''
    Returns path to test repository located at `/tests/data/repo`
    '''
    repo_path = Path('./tests/data/repo')
    rename_gitignore(repo_path, False)
    yield repo_path
    rename_gitignore(repo_path, True)

@pytest.fixture
def repo_with_gitignore():
    '''
    Returns path to test repository located at `/tests/data/repo_with_gitignore`
    '''
    repo_path = Path('./tests/data/repo_with_gitignore')
    rename_gitignore(repo_path, False)
    yield repo_path
    rename_gitignore(repo_path, True)

def test_find_gitignore_1(repo: Path):
    '''
    Tests that in repository without .gitignore 
    function src.cpp_stats.file_sieve._locate_file does not locate one
    '''
    file_to_locate = '.gitignore'
    correct = []

    result = src.cpp_stats.file_sieve._locate_file(repo, file_to_locate, [])

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

    result = src.cpp_stats.file_sieve._locate_file(repo_with_gitignore, file_to_locate, [])

    assert correct == result
