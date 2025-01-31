'''
Modules that sieves all files that are specified in .gitignore 
or are located inside ignored directories, which are listed in
.gitignore or .gitmodules
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
    return []

_possible_extensions = ['*.h', '*.hpp', '*.C', '*.cc', '*.cpp',
                        '*.CPP', '*.c++', '*.cp', '*.cxx']

def _locate_file(path_to_search: Path, file_to_find: str,
                 banned_dirs: list[Path]) -> list[Path] | None:
    paths = []
    for entry in path_to_search.rglob(file_to_find):
        is_inside_banned_dirs = False
        for b_dir in banned_dirs:
            if entry.is_relative_to(b_dir):
                is_inside_banned_dirs = True
                break
        if not is_inside_banned_dirs:
            paths.append(entry)
    return paths

def _get_git_modules_dirs(git_modules_path: Path) -> list[Path]:
    parent_directory = git_modules_path.parent
    paths = []
    with open(git_modules_path, 'r') as f:
        while (line := f.readline()):
            line = line.lstrip()
            if not line.startswith('path = '):
                continue
            path_value = line[line.find('='):].lstrip()
            paths.append(parent_directory.joinpath(path_value))
    return paths

def _get_git_ignore_dirs(git_ignore_path: Path) -> list[Path]:
    parent_directory = git_ignore_path.parent
    paths = []
    with open(git_ignore_path, 'r') as f:
        while (line := f.readline()):
            line = line.lstrip()
            if len(line) == 0:
                continue
            if line[0] == '#':
                continue
            p = parent_directory.joinpath(line)
            if p.is_dir():
                paths.append(p)
    return paths
