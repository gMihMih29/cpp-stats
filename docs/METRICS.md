# Metrics list
## Number of C/C++ files
* Description
A metric measures the number of C/C++ files.

## Number of classes
* Description
A metric measures the number of classes. 

## Mean number of methods per class
* Description
A metric measures the mean number of methods per class. 

## Maximum number of methods per class
* Description
A metric measures the maximum number of methods per class.

## Mean length of methods
* Description
A metric measures the mean length of methods in lines of code.

## Maximum length of methods
* Description
A metric measures the maximum length of methods in lines of code. 

## Cyclomatic complexity
* Description
Cyclomatic complexity is a count of decisions in the source code. The higher the count, the more complex the code.
* Formula

    For method:
    ```math
    C = E - N + 2
    ```
    where $E$ is number of edges in code graph, $N$ is number of nodes in code graph.

    For class:
    $$
    C = E - N + 2 \cdot P = \sum_{\text{m is method of A}}C(m),
    $$
    where $E$ is number of edges in code graph, $N$ is number of nodes in code graph, P is the number of connectivity components (methods).

* Source
[Egor Bugaenko](https://www.youtube.com/watch?v=Cvv0Olx4Bpw&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=2)

## Mean cyclomatic complexity of methods
* Description
A metric measures the mean cyclomatic complexity of methods.
* Source
[Egor Bugaenko](https://www.youtube.com/watch?v=Cvv0Olx4Bpw&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=2)

## Maximum cyclomatic complexity of methods
* Description
A metric measures the maximum cyclomatic complexity of methods.
* Source
[Egor Bugaenko](https://www.youtube.com/watch?v=Cvv0Olx4Bpw&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=2)

## Cognitive complexity (TODO)

## Mean cognitive complexity (TODO)
Подсчёт средней когнитивной сложности методов. [Описание](https://habr.com/ru/articles/565652/).

## Maximum cognitive complexity (TODO)
Подсчёт максимальной когнитивной сложности методов. [Описание](https://habr.com/ru/articles/565652/).

## Halstead complexity measures
* Description
Halstead complexity measures are metrics based on the computation of operands and operators in the code.  
* Formula
    Let:
    $\eta_{1}$ = the number of distinct operators
    $\eta _{2}$ = the number of distinct operands
    $N_{1}$ = the total number of operators
    $N_{2}$ = the total number of operands

    From these numbers, several measures can be calculated:

    Program vocabulary: $\eta =\eta _{1}+\eta _{2}$
    Program length: $N=N_{1}+N_{2}$
    Calculated estimated program length: $\hat {N}=\eta _{1}\log _{2}\eta _{1}+\eta _{2}\log _{2}\eta _{2}$
    Volume: $V=N\times \log _{2}\eta$
    Difficulty : $D={\eta _{1} \over 2}\times {N_{2} \over \eta _{2}}$
    Effort: $E=D\times V$

    Time required to program: $T={E \over 18}$ seconds

    Number of delivered bugs: $B={E^{2 \over 3} \over 3000}$ or, more recently, $B={V \over 3000}$ is accepted.
* Source
[Egor Bugaenko](https://www.youtube.com/watch?v=YsGzjv0hgcc&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=4)

## Maintainability Index
* Formula
    $$
    \text{MI}=171-5.2\cdot\ln(\text{Halstead Volume})-0.23\cdot(\text{Cyclomatic Complexity})-16.2\cdot \ln(\text{LoC})
    $$
* Source
[Egor Bugaenko](https://www.youtube.com/watch?v=xnSnPfVkmkM&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=5)

## Lack of Cohesion of Methods (LCOM)
* Description
* Formula
$$
    P = \{(v_i,v_j)|v_i \cap v_j = \emptyset \}
    $$
    $$
    Q = \{(v_i,v_j)|v_i \cap v_j \neq \emptyset \}
    $$
    $$
    \text{LCOM1} = \max(0, |P| - |Q|),
    $$
    where $v_i$ is set of used attributes in method $i$.
    
    A lower value means better result. 
    $$
    \text{LCOM2} = \frac{1}{n}\sum a_i,
    $$
    where $n$ is the number of attributes in class, $a_i$ is ratio of methods that not use the attribute $i$.
    
    $\text{LCOM2} \in [0;1]$. A lower value means better result.
    
    $$
    \text{LCOM3} = \frac{m - t}{m - 1},
    $$
    where $m$ is the number of methods in class, $t = 1 - \text{LCOM2}$
    
    $\text{LCOM1} \in [0;2]$. $\text{LCOM1} \in [0;1]$ means OK.
    
    $$
    \text{LCOM4} = \text{\#connectivity components in graph } G,
    $$
    Graph $G$ is formed by rules:
    * Each attribute and method is a separate node.
    * Edge exists between a method and an attribute if the method accesses that attribute.
    * Edge exists between two methods if one method calls the other.

    A lower value means better result.
* Source
[Egor Bugaenko](https://www.youtube.com/watch?v=74YigDo8_BE&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=9)

## Tight and Loose Class Cohesion (TCC and LCC)
* Description
* Formula
Let:
    $$
    N \cdot (N - 1) / 2 = \text{NP} = \text{Max possible connections}
    $$
    $$
    \text{NDC} = \# \text{directly connected methods}
    $$
    $$
    \text{NIC} = \# \text{indirectly connected methods}
    $$
    Two methods are connected directly if exists attribute which is used in both methods.\\
    Two methods are connected indirectly if exists method which is directly connected to both methods.
    
    Then:
    $$
    \text{TCC} = \text{NDC} / \text{NP}
    $$
    $$
    \text{LCC} = (\text{NDC} + \text{NIC}) / \text{NP}
    $$
* Source
[Egor Bugaenko](https://www.youtube.com/watch?v=JOKxjpAglFU&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=9)

## CAMC
Подсчёт степени пересечения списков типов параметров. [Описание](https://www.scirp.org/pdf/JSEA20100400008_80076534.pdf).

## NHD
Подсчёт согласованности списков типов параметров. [Описание](https://www.scirp.org/pdf/JSEA20100400008_80076534.pdf).

## SNHD
Подсчёт отмасштабированной метрики NHD. [Описание](https://www.scirp.org/pdf/JSEA20100400008_80076534.pdf).

## NHDM
Подсчёт модифицированной метрики NHD. [Описание](https://www.scirp.org/pdf/JSEA20100400008_80076534.pdf).
