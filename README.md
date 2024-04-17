# Information Retrieval System with Inverted Index and TF-IDF Scoring

This project is designed to create an information retrieval system that constructs an inverted index from a collection of XML documents and implements TF-IDF (Term Frequency-Inverse Document Frequency) scoring for ranking search results. The system utilizes tokenization methods, builds an inverted index, and calculates TF-IDF scores to retrieve relevant documents based on user queries.
Project Overview

## The project involves several key components and processes:

    - Data Collection and Parsing:
        The system starts by parsing XML documents containing textual content.
        Document IDs and content are stored in ArrayLists docIds and contents.

    - Index Construction (invidx.sh):
        The invidx.sh script takes command-line arguments:
            coll-path: Path to the collection of XML files.
            indexfile: Name of the output index file.
            tokenization type: Type of tokenization (0 for simple, 1 for BPE).
            compression type: Type of compression (0 for no compression, 1 for variable byte compression).
        The script creates a maps directory and generates .properties files for distinct words in the document content.
        The resulting index files are indexfile.dict and indexfile.idx.

    - Query Processing and TF-IDF Scoring (tf_idf_search.sh):
        The tf_idf_search.sh script processes a query file (XML format) to create mappings of query IDs to frequency maps of query titles and descriptions.
        The system calculates TF-IDF scores for each term in the query and uses them to rank documents.
        The TF-IDF formula used includes term frequency (TF) and inverse document frequency (IDF) components.
        The top 100 documents are selected based on their TF-IDF scores and stored in a file named results._file.txt.

## TF-IDF Scoring Mechanism

The TF-IDF scoring mechanism used for ranking documents is as follows:

    Term Frequency (TF): The term frequency component is calculated using the formula tfij = 1 + log2(fij), where fij is the number of times term i appears in document dj.

    Inverse Document Frequency (IDF): The inverse document frequency component is calculated using the formula idfi = log2(1 + N / dfi), where dfi is the number of documents containing term i, and N is the total number of documents.

Usage

    Run invidx.sh with appropriate command-line arguments to build the inverted index and generate index files.

    bash

sh invidx.sh [coll-path] [indexfile] [tokenization type] [compression type]

Run tf_idf_search.sh with the query file to calculate TF-IDF scores and retrieve relevant documents.

bash

    sh tf_idf_search.sh [queryfile] [resultfile] [indexfile] [dictfile]

## Conclusion

This information retrieval system efficiently handles XML documents, creates an inverted index with tokenization, and implements TF-IDF scoring for accurate document ranking. The system's usage of TF-IDF scores ensures that retrieved documents are relevant to user queries, making it a valuable tool for information retrieval tasks.