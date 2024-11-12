# C/C++ Project Model

Forms project model based on C/C++ files within repository as well as provide base statistics.
Provides API for traversing the model as well as export in common format (TBP).

The model for C/C++ looks like below:
```
folder
 |- .h/.cpp file (LoC)
   |- include
   |- namespace
   |- struct
   |- function
   |- classA
     |- method (LoC, cyclomatic complexity)
       |- parameter
       |- variable
     |- field
     |- ...
   |- classB
     |- ... 
   |- ...
 |- .h/.cpp file
 |- ... 
```

Base statistics include:
- number of .h/.cpp files
- number of classes
- avg/max number of methods per class
- avg/max method size (LoC)
