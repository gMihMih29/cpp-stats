'''
Module that sieves all files that are specified in `.gitignore` 
or located inside ignored directories, which are listed in
`.gitignore` as ignored or `.gitmodules` as submodules.
'''

from pathlib import Path

def sieve_c_cxx_files(path_to_repo: str) -> list[Path] | None:
    '''
    Returns list of C/C++ files, what have matching extensions: 
    `.h`, `.hpp`, `.C`, `.cc`, `.cpp`, `.CPP`, `.c++`, `.cp`, 
    or `.cxx`.
    
    Files that located in directories specified in `.gitignore` 
    or `.gitmodules` are ignored.
    
    Parameters:
    path_to_repo (str): Path to the repository.
    '''
    if path_to_repo is None:
        return None

    submodules_paths = _locate_file(path_to_repo, '.gitmodules', [])
    submodules_dirs = []
    for p in submodules_paths:
        submodules_dirs += _get_git_modules_dirs(p)

    gitignore_paths = _locate_file(path_to_repo, '.gitignore', submodules_dirs)
    gitignore_dirs = []
    for p in gitignore_paths:
        gitignore_dirs += _get_git_ignore_dirs(p)

    banned_dirs = submodules_dirs + gitignore_dirs

    c_cxx_files = []
    for ext in _possible_extensions:
        c_cxx_files += _locate_file(path_to_repo, ext, banned_dirs)
    c_cxx_files = set(c_cxx_files)
    return list(c_cxx_files)

_possible_extensions = ['*.h', '*.hpp', '*.c', '*.C', '*.cc', '*.cpp',
                        '*.CPP', '*.c++', '*.cp', '*.cxx']

def _locate_file(path_to_search: Path, pattern: str,
                 banned_dirs: list[Path]) -> list[Path]:
    '''
    Finds all files that match `pattern` inside `path_to_search` directory
    ignoring `banned_dirs`.
    
    Parameters:
    `path_to_search` (`pathlib.Path`): path to starting directory.
    `pattern` (`str`): pattern to find.
    `banned_dirs` (`list[pathlib.Path]`): directories that will be ignored during search.
    '''
    paths = []
    for entry in path_to_search.rglob(pattern):
        is_inside_banned_dirs = False
        for b_dir in banned_dirs:
            if entry.is_relative_to(b_dir):
                is_inside_banned_dirs = True
                break
        if not is_inside_banned_dirs:
            paths.append(entry)
    return paths

def _get_git_modules_dirs(git_modules_path: Path) -> list[Path]:
    '''
    Finds all directories that listed in `.gitmodules` file located at `git_modules_path`.
    
    Parameters:
    `git_modules_path` (`pathlib.Path`): path to `.gitmodules`.
    '''
    parent_directory = git_modules_path.parent
    paths = []
    with open(git_modules_path, 'r', encoding='utf-8') as f:
        while (line := f.readline()):
            line = line.lstrip().rstrip()
            if not line.startswith('path = '):
                continue
            path_value = line[line.find('=') + 1:].lstrip()
            paths.append(parent_directory.joinpath(path_value))
    return paths

def _get_git_ignore_dirs(git_ignore_path: Path) -> list[Path]:
    '''
    Finds all directories that listed in `.gitignore` file located at `git_ignore_path`.
    
    Parameters:
    `git_ignore_path` (`pathlib.Path`): path to `.gitignore`.
    '''
    parent_directory = git_ignore_path.parent
    paths = []
    with open(git_ignore_path, 'r', encoding='utf-8') as f:
        while (line := f.readline()):
            line = line.lstrip()
            if len(line) == 0:
                continue
            if line[0] == '#':
                continue
            if line[-1] == '\n':
                line = line[:-1]
            if line[-1] == '\\' or line[-1] == '/':
                line = line[:-1]
            p = parent_directory.joinpath(line)
            if p.is_dir():
                paths.append(p)
    return paths
