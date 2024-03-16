# Comparative Analysis of Probabilistic and Deterministic Self-Balancing Trees

In the field of computer science, specifically with respect to organizing and managing data, the type of structures we choose to use can have a significant impact on the speed and efficiency of our operations. For example, finding a book in a library where the books are randomly placed versus a library where books are carefully organized—the difference in the time it takes you to find what you're looking for is huge. 

Treaps, Skip Lists, AVL Trees, and Red-Black trees are data structures that organize data in a form that makes it easier to perform operations such as insertion, deletion, or searching for data. The organization of data in these structures is governed by rules specific to each of them. These rules ensure that the data remains organized even when new data is added or old data is removed, thereby maintaining efficient operation.

## Probabilistic vs. Deterministic Approaches

Treaps and Skip Lists follow a probabilistic approach, meaning they use randomness in a way that balance is maintained and operations are performed quickly. Conversely, deterministic self-balancing trees such as AVL Trees and Red-Black Trees have a strict set of rules to ensure that they remain balanced and the operations on them are efficient.

## Project Objectives

The objective of this paper is to compare the performance of probabilistic structures—Treaps and Skip Lists—with deterministic self-balancing trees—AVL Trees and Red-Black Trees—when performing insertion, deletion, and searching operations. In addition to this, we will also examine how well balanced Treaps and Skip Lists are when compared to deterministic trees. This paper aims to provide a clear comparison of these data structures.  

## Code Link
You can find the implementation code in the file [algo_term_end_project_code.py](https://github.com/nidamariam/CS584Algo/blob/main/algo_term_end_project_code.py). This file contains the Python code for performing the comparative analysis of probabilistic and deterministic self-balancing trees.

---

## Usage

1. Clone the repository:

```bash
git clone https://github.com/nidamariam/CS584Algo.git