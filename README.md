# VMARK
Text Based Information Retrieval System using the Vector Space Model, developed in partial fulfilment for the Information Retrieval Course offered at my University. 


### Instructions:

#### To download the corpus:
We have selected the **Amazon Food Reviews Corpus** for this project. You can download the corpus from this [drive link] (https://drive.google.com/file/d/0BzNf9u6dqAlhTmVzSFdKQVA1V0U/view?usp=sharing). After downloading the file, please extract it to the folder named **Code Files**.

Now go to the folder **Code Files**, and proceed as mentioned in the following instructions.

### Executing VMARK Version 1.0.0 - Syntactic VSM Based Search Engine

#### To index the corpus:
1. Execute the python file indexer_syntactic.py
2. Execute the python file norm_syntactic.py

**CAUTION:** Create an empty file called invindex_semantic.txt before running indexer_syntactic.py file

#### To query the system:
1. Execute the python file vectors_syntactic.py
2. Enter your query on the CLI (preferably about food since the corpus contains food reviews)
3. Enter 'n', the number of documents you want to retrieve.

The Search Engine will then retrieve the top 'n' ranked files.

### Executing VMARK Version 1.0.1 - Semantic VSM Based Search Engine

#### To index the corpus:
1. Execute the python file indexer_syntactic.py
2. Execute the python file norm_syntactic.py

**CAUTION:** Create an empty file called invindex_semantic.txt before running indexer_syntactic.py file

#### To query the system:
1. Execute the python file vectors_syntactic.py
1. Enter your query on the CLI (preferably about food since the corpus contains food reviews)
2. Enter 'n', the number of documents you want to retrieve.

The Search Engine will then retrieve the top 'n' ranked files.

### Please read the file [DesignDocument_VMARK.pdf](https://drive.google.com/open?id=0BzNf9u6dqAlheTVzbS1kZDhvMzg) for complete understanding of the project.  
