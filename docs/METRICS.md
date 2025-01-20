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

For class $A$:

```math
C = E - N + 2 \cdot P = \sum_{\text{m is method of A}}C(m),
```
where $E$ is number of edges in code graph, $N$ is number of nodes in code graph, $P$ is the number of connectivity components (methods).

* Source: [Egor Bugaenko](https://www.youtube.com/watch?v=Cvv0Olx4Bpw&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=2)

## Mean cyclomatic complexity of methods
* Description

A metric measures the mean cyclomatic complexity of methods.

* Source: [Egor Bugaenko](https://www.youtube.com/watch?v=Cvv0Olx4Bpw&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=2)

## Maximum cyclomatic complexity of methods
* Description

A metric measures the maximum cyclomatic complexity of methods.

* Source: [Egor Bugaenko](https://www.youtube.com/watch?v=Cvv0Olx4Bpw&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=2)

## Cognitive complexity
* Description

A metric measures readability complexity of code.

Metric increases by one for each cyclic constructions (`for`, `while`, `do while`, ...) and conditional constructions (`if`, `#if`, `#ifdef`, ternary operators).

Metric increases by one for each nested contructions.

* Source: [Egor Bugaenko](https://www.youtube.com/watch?v=oRUux3w4rsc&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=3)

## Mean cognitive complexity
* Description

A metric measures the mean cognitive complexity of methods.

* Source: [Egor Bugaenko](https://www.youtube.com/watch?v=oRUux3w4rsc&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=3)

## Maximum cognitive complexity
* Description

A metric measures the maximum cognitive complexity of methods.

* Source: [Egor Bugaenko](https://www.youtube.com/watch?v=oRUux3w4rsc&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=3)

## Halstead complexity measures
* Description

Halstead complexity measures are metrics based on the computation of operands and operators in the code.

* Formula

Let:

$\eta_{1}$ = the number of distinct operators

$\eta_{2}$ = the number of distinct operands

$N_{1}$ = the total number of operators

$N_{2}$ = the total number of operands

From these numbers, several measures can be calculated:

Program vocabulary: $\eta =\eta_{1}+\eta_{2}$

Program length: $N=N_{1}+N_{2}$

Calculated estimated program length: $\hat{N}=\eta_{1}\log_{2}\eta_{1}+\eta_{2}\log_{2}\eta_{2}$

Volume: $V=N\times \log_{2}\eta$

Difficulty : $D={\eta_{1} \over 2}\times {N_{2} \over \eta_{2}}$

Effort: $E=D\times V$

Time required to program: $T={E \over 18}$ seconds

Number of delivered bugs: $B={E^{2 \over 3} \over 3000}$ or, more recently, $B={V \over 3000}$ is accepted.

* Source: [Egor Bugaenko](https://www.youtube.com/watch?v=YsGzjv0hgcc&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=4)

## Maintainability Index
* Formula

$$
\text{MI}=\max(0, 171-5.2\cdot\ln(\text{Halstead Volume})-0.23\cdot(\text{Cyclomatic Complexity})-16.2\cdot \ln(\text{LoC}))
$$


$\text{MI}$ $\in [0;100]$. Higher value means higher maintainablility.

* Source: [Egor Bugaenko](https://www.youtube.com/watch?v=xnSnPfVkmkM&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=5)

## Lack of Cohesion of Methods (LCOM)
* Description

LCOM measures cohesion between methods and attributes in class.

* Formula

```math
P = \{(v_i,v_j)|v_i \cap v_j = \emptyset\}
```

```math
Q = \{(v_i,v_j)|v_i \cap v_j \neq \emptyset\}
```

$$
\text{LCOM1} = \max(0, \text{|}P\text{|}-\text{|}Q\text{|}),
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

$\text{LCOM3} \in [0;2]$. $\text{LCOM3} \in [0;1]$ means OK.

$$
\text{LCOM4} = \text{Number of connectivity components in graph } G,
$$


Graph $G$ is formed by rules:
* Each attribute and method is a separate node.
* Edge exists between a method and an attribute if the method accesses that attribute.
* Edge exists between two methods if one method calls the other.

A lower value means better result.

* Source: [Egor Bugaenko](https://www.youtube.com/watch?v=74YigDo8_BE&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=9)

## Tight and Loose Class Cohesion (TCC and LCC)
* Description

The metrics TCC and LCC provide another way to measure the cohesion of a class. The higher TCC and LCC, the more cohesive and thus better the class.

* Formula

Let:

$$
N \cdot (N - 1) / 2 = \text{NP} = \text{Max possible connections}
$$

$$
\text{NDC} = \text{Number of directly connected methods}
$$

$$
\text{NIC} = \text{Number of indirectly connected methods}
$$


Two methods are connected directly if exists attribute which is used in both methods.

Two methods are connected indirectly if exists method which is directly connected to both methods.

Then:

$$
\text{TCC} = \text{NDC} / \text{NP}
$$

$$
\text{LCC} = (\text{NDC} + \text{NIC}) / \text{NP}
$$

* Source: [Egor Bugaenko](https://www.youtube.com/watch?v=JOKxjpAglFU&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=9)

## Cohesion among Methods of a Class (CAMC)
* Description

The CAMC metric measures the extent of intersection of individual method parameter type lists with the parameter type list of all methods in the class 

* Formula

$$
\text{CAMC} = \frac{\sigma}{kl} \text{  where  } \sigma = \sum_{1}^{k}\sum_{1}^{l}PO[i][j]
$$


$PO$ is a parameter-occurrence matrix that has a row for each method and a column for each data type that appears at least once as the type of a parameter in at least one method in the class. The value in row $i$ and column $j$ in the matrix is 1 when the $i$-th method has a parameter of the $j$-th data type and is 0 otherwise

* Source

1. [Egor Bugaenko](https://www.youtube.com/watch?v=oCxJ_YSSAGo&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=12)
2. ["Exploring Design Level Class Cohesion Metrics", Kuljit Kaur, Hardeep Singh](https://www.scirp.org/pdf/JSEA20100400008_80076534.pdf)

## Normalized Hamming Distance (NHD)
* Description

NHD measures agreement between rows in the $PO$ matrix from CAMC.

* Formula

$$
\text{NHD} = \frac{2}{lk(k-1)}\sum_{1}^{k-1}\sum_{j+1}^{k}a(i,j)
$$

where $a(i,j)$ is value of the cell at $(i,j)$-th location in the parameter agreement matrix.

* Source

1. [Egor Bugaenko](https://www.youtube.com/watch?v=oCxJ_YSSAGo&list=PLaIsQH4uc08xyXRhhYPHh-Yam2kEwNaLl&index=12)
2. ["Exploring Design Level Class Cohesion Metrics", Kuljit Kaur, Hardeep Singh](https://www.scirp.org/pdf/JSEA20100400008_80076534.pdf)

<!-- ## Scaled NHD (SNHD)
* Description
* Formula
* Source
["Exploring Design Level Class Cohesion Metrics", Kuljit Kaur, Hardeep Singh](https://www.scirp.org/pdf/JSEA20100400008_80076534.pdf) -->

<!-- ## Normalized Hamming Distance Modified (NHDM)
* Description
* Formula

* Source
["Exploring Design Level Class Cohesion Metrics", Kuljit Kaur, Hardeep Singh](https://www.scirp.org/pdf/JSEA20100400008_80076534.pdf) -->