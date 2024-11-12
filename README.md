# Code Repository C/C++ Stats

Taking source code repository as an input calculate base statistics for C/C++ source files.  

Base statistics include:
- number of C/C++ files
- number of classes
- avg/max number of methods per class
- avg/max method size (in LoC)
- avg/max cyclomatic complexity of method
- _(to be extended)_ 

The stats are exposed as an API as well as exported report (in XML format)

## API Usage

```python
import ca-cpp-stats as st

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
\> python3 ca-python-stats --report path_to_xml.xml path_to_repo
```
