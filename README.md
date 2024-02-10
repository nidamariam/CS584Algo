# CS584Algo# Comparative Analysis of Sorting Algorithms

This project aims to explore and compare the performance of various sorting algorithms. Sorting is a fundamental operation in computer science, not only for data organization but also as a critical component in numerous algorithmic strategies. Understanding the efficiency and behavior of different sorting techniques based on the nature of input data is essential for optimizing computational tasks.

## Objectives

The primary goal of this study is to conduct a comparative analysis of sorting algorithms, focusing on their time efficiency across different scenarios, including:
- The size of the input array
- The range and nature of array elements

## Methodology

### Experimental Design

The performance comparison of the sorting algorithms will be conducted under various conditions, specifically:

- **Size of Array**: The algorithms will be tested on arrays of size 100,000; 500,000; 1,000,000; 5,000,000; and 10,000,000.
- **Ranges**:
  1. Random integers within the range of 0 to n.
  2. Random integers within a fixed range (0 to 1000), irrespective of n.
  3. Random integers within an extended range (0 to n^3), to test performance under large numeric values.
  4. Random integers within a logarithmic range (0 to log(n)), to assess behavior with smaller, more constrained datasets.
  5. Random integers that are multiples of 1000 within the range of 0 to n, to test sorting with large, evenly spaced numbers.
  6. A nearly sorted array where a subset of elements (log2(n)/2) are randomly swapped, to evaluate efficiency on almost sorted data.

## Getting Started

To replicate this study or to understand the performance of sorting algorithms under the specified conditions, follow the instructions below:

### Prerequisites

Ensure you have a programming environment capable of running code written in the language of the implemented algorithms (i.e., Python).

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/nidamariam/CS584Algo.git