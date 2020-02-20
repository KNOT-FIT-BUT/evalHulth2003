# evalHulth2003
Evaluation script for Hulth2003 (inspec) dataset for keywords extraction/generation task.
The dataset was introduced in:

* Improved automatic keyword extraction given more linguistic knowledge Anette Hulth. In Proceedings of EMNLP 2003. p. 216-223.

## Instalation

## Dataset
Hulth2003 (inspec) dataset is dataset of titles and abastracts from which you should extract/generate relevant keyphrases.

It's split into three parts:

* Train
* Validation 
* Test

Each part consists of two types of files.
    
* content files
    * Files containing titles and abstracts.
* keyphrases files
    * All target keyphrases for the title-abstract pair in corresponding document.

## Tasks
In this section is presented how to run script to get evaluation of your results for given task.

The evaluation metrics are precision, recall and F1. The result/target keyphrases are handled in set fashion, so if you extract/generate same keyphrase multiple times it's considered only once. Two keyphrases are considered the same if they match according to given scheme (matching schemes are discribed bellow).

### Matching schemes
As the very first step is performed tokenization with english spacy tokenizer and than we are investigating
matches according to multiple schemes.

As valid extracted/generate keyphrase is keyphrase considered when:

* Plain token match
    * All tokens of keyphrase haves exact string match with at least one ground truth keyphrase of given document.



### Keyphrase extraction

### Keyphrase generation

## File formats