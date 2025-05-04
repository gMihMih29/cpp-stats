# Code Repository C/C++ Stats

Taking source code repository as an input calculate base statistics for C/C++ source files.  

Base statistics include:
- number of C/C++ files
- lines of code
- number of classes
- avg/max number of methods per class
- avg/max method size (in LoC)
- avg/max cyclomatic complexity of method
- avg/max cognitive complexity of method
- avg/max halstead program vocabulary
- avg/max halstead program length
- avg/max halstead estimated program length
- avg/max halstead volume
- avg/max halstead difficulty
- avg/max halstead effort
- avg/max halstead time required to program
- avg/max halstead number of delivered bugs
- avg/min maintainability index
- avg/min/max cohesion among methods of class
- avg/min/max normalized hamming distance between methods of class
- avg/max lack of cohesion of methods 1
- avg/max lack of cohesion of methods 2
- avg/max lack of cohesion of methods 3
- avg/max lack of cohesion of methods 4
- avg/min tight class cohesion
- avg/min loose class cohesion

The stats are exposed as an API as well as exported report (in XML format)

## API Usage

```python
from cpp_stats import CppStats

stats = CppStats("path/to/repo")

# Print available metrics
print(stats.list())

# Print number of classes
print(stats.metric("NUMBER_OF_CLASSES"))

# Print XML report
print(stats.as_xml())
```

## CLI Usage

```shell
\> cpp-stats --report path_to_xml.xml path_to_repo
```

## Installation guide

### Cpp-stats
```shell
git clone https://github.com/SctCodeAnalysis/cpp-stats
cd cpp-stats
pip install .
```

### LibClang
On Linux:
```bash
sudo apt install clang libclang-17-dev
export LIBCLANG_LIBRARY_PATH="path/to/libclang-17.so"
```

On Windows:

You need to install Clang compiler (ex. mingw64). Then:
```shell
setx LIBCLANG_LIBRARY_PATH "path\\to\\libclang.dll"
```
