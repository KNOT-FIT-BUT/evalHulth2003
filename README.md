# evalHulth2003
Evaluation script for Hulth2003 (inspec) dataset for keywords extraction/generation task.
The dataset was introduced in:

* Improved automatic keyword extraction given more linguistic knowledge Anette Hulth. In Proceedings of EMNLP 2003. p. 216-223.

## Installation
The recommended approach is just to install the requirements:

    pip install -r requirements.txt
    
and use the:

    run.py
    
Alternatively, you can install the evaluation script as the python console application:

    python setup.py install

## Dataset
Hulth2003 (inspec) dataset is a dataset of titles and abstracts from which you should extract/generate relevant keyphrases.

It's split into three parts:

* Train
* Validation 
* Test

Each part consists of two types of files:
    
* content files
    * Files containing titles and abstracts.
* keyphrases files
    * All target keyphrases for the title-abstract pair in the corresponding document.

## Tasks
In this section is presented how to run the script to get the evaluation of your results for the given task.

The evaluation metrics are precision, recall, and F1. The result/target keyphrases are handled in a set fashion, so if you extract/generate the same keyphrase multiple times, it's considered only once. Two keyphrases are considered the same if they match according to the given scheme (matching schemes are described below).

### Matching schemes
As the very first step is performed tokenization with English spacy tokenizer and then we are investigating matches according to multiple schemes.

As valid extracted/generate keyphrase is keyphrase considered when:

* Exact match
    * All tokens of keyphrase haves an exact string match with at least one ground truth keyphrase of the given document.
* Part of match
    * All tokens of keyphrase haves an exact string match with at least one ground truth keyphrase or sub-keyphrase of the given document.
        * Examples of sub-keyphrases for: programing language
            * programing language
            * programing
            * language
* Exact match on lower case form
    * case insensitive variant of Exact match
* Part of match on lower case form
    * case insensitive variant of Part of match
    * What is sub-keyphrase is explained bellow the Part of match.
* Exact match on lower case lemma form
    * All tokens are transformed into their lower case lemma form (with spacy), and than we are finding a match with at least one target keyphrase that is transformed in the very same way.
* Part of match on lower case lemma form:
    * All tokens are transformed into their lower case lemma form (with spacy), and than we are finding a match with at least one target sub-keyphrase that is transformed in the very same way. What is sub-keyphrase is explained bellow the Part of match.
* Exact match on lower case stem form
    * All tokens are transformed into their lower case stem form with PorterStemmer (nltk), and than we are finding a match with at least one target keyphrase that is transformed in the very same way.
* Part of match on lower case stem form
    * All tokens are transformed into their lower case stem form with PorterStemmer (nltk), and than we are finding a match with at least one target sub-keyphrase that is transformed in the very same way. What is sub-keyphrase is explained bellow the Part of match.

### Keyphrase extraction
To run the evaluation script for keyphrase extraction task evaluation use following command:

    ./run.py eval -g examples/ -p examples/
    
Where the parameters are:
* g - path to the folder containing *.uncontr_in files
* p - path to the folder containing *.res files

### Keyphrase generation
To run the evaluation script for keyphrase generation task evaluation use following command:

    ./run.py evalGen -g examples/ -p examples/
    
Where the parameters are:
* g - path to the folder containing *.uncontr files
* p - path to the folder containing *.res files

## File formats
This script is working with four types of text files. Files with contents (.abstr), files with annotated keyphrases for extraction task (.uncontr_in) and files with annotated keyphrases for generation task (.uncontr).

Examples of all types of files are in:

    examples/

### .uncontr_in and .uncontr
The .uncontr_in and .uncontr files are very similar .

The .uncontr file contains keyphrases for a given document, but these keyphrases may or may not be actually in the text. Files with .uncontr_in extension contain the very same keyphrases, but only those that appear in the text. The selection of .uncontr_in keyphrases was made on the lower lemma basis. So the text and keyphrases were transformed into lower case lemma form (with spacy), and than we search the transformed keyphrase in the converted text.

Each keyphrase is separated with: ;

### .res
File with extracted/generated keyphrases. Always one keyphrase on a line.

### .abstr
Text file with title and abstract.

The script doesn't discriminate between title and abstract. In fact, the script does not use this type of file for evaluation at all. It's only used for the creation of .uncontr_in files with the keywords argument.