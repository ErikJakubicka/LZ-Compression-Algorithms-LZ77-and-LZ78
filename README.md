# LZ-Compression-Algorithms-LZ77-and-LZ78

Welcome to the GitHub repository for our implementation and analysis of the LZ77 and LZ78 data compression algorithms. This project explores the efficiency, complexity, and practical application of these algorithms in compressing various types of data.

# Table of Contents
* Introduction
* Features
* Installation
* Usage
* Examples
* Results
* License
* References

# Introduction
This repository contains code implementations of the LZ77 and LZ78 compression algorithms, as well as the experimental results derived from their application on different datasets. The goal of this project is to investigate the trade-offs between compression efficiency and processing time for both algorithms and to provide insights into potential areas for further optimization.

# Features
* Implementation of LZ77 and LZ78 algorithms.
* Customizable buffer sizes for LZ77.
* Compression and decompression functionality.
* Performance metrics and analysis.
* Sample datasets for testing.
* Documentation and comments within the code for clarity.

# Installation
To install and run the project, follow these steps:

First you need to have Python installed:

    pip install python3

Second is the need to have all the necessary Packages: 

    pip install pillow
    pip install numpy
    pip install collection
    pip install PyQt5
    pip install PyQt5-Qt5
    pip install PyQt5-sip

# Using compression codes
To use the compression algorithms, you can run the provided scripts from the terminal. Below are some example commands:

# Compress a file using LZ77
The following command in the terminal starts the LZ77 Algorithm, where parameter -s stands for Search Buffer and parameter -l stands for Look-ahead Buffer, in case the user doesn't know what values to enter into each parameter there is an option to type into the terminal the given "parameter" --help

    python3 lz77_compress.py -s -l input_file compressed_output_file

# Decompress a file using LZ77
The following command in the terminal starts the LZ77 Decompression Algorithm

    python3 lz77_decompress.py compressed_output_file decompressed_output_file

# Compress a file using LZ78
The following command in the terminal starts the LZ78 Algorithm

    python3 lz78_compress.py input_file compressed_output_file

# Decompress a file using LZ78
The following command in the terminal starts the LZ78 Decompression Algorithm

    python3 lz78_decompress.py compressed_output_file decompressed_output_file

# Using GUI code
If you want to use GUI code, you will need to download PyCharm or other integrated development environment for Python.

# Examples
Example usage of the compression and decompression scripts is provided in the examples directory. You can run these examples to see how the algorithms perform with different datasets.

# Results
Our experiments showed that for larger files, increasing the search buffer and look-ahead buffer sizes in LZ77 improved compression ratios but also increased compression time. The LZ78 algorithm did not require such adjustments, offering consistent performance across different file sizes. Detailed results and analysis can be found in the results directory.

# License
This project is licensed. See the LICENSE file for more details.

# References
* Go Compression GitHub. "The Hitchhiker's Guide to Compression."
* Compression According to Lempel, Ziv and Welch
    

