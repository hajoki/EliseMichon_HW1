# 06/06/16 Answer to the error reported during the grading
>> The error was:

$ python 1_set_creation.py 69yazar

fehmiKoru

Traceback (most recent call last):

  File "1_set_creation.py", line 37, in <module>
  
    training_files = list_files[:round(number_files*0.6)]
    
TypeError: slice indices must be integers or None or have an __index__ method

$ ls 69yazar/

okubeni.doc  raw_texts  test  test_texts  texts_in_arff  training

>> I obtained the same error when running my code with Python 2.7, while it was written with Python 3. A way to fix it is to replace 

    training_files = list_files[:round(number_files*0.6)]
    
by 

    training_files = list_files[:int(number_files*0.6)]

>> I also tried to rewrite more clearly the instructions to run the program in this readme below

# 19/03/16 Update 
>> The algorithm worked for a duration that seems excessive (more than 10 hours) but finally completed its running. We had provided the training set as a test set, a high accuracy was then expected. The output obtained by prints in the console is reported in the file example_result.txt, which is quite hard to process. A new script 3_read_results.py was written to process it and the processed results are then stored in the file result.txt. The confusion matrix reveals that although all articles were not attributed to a unique class, they were attributed to only a few classes globally, making again the computation of precision, recall and F1 scores not possible.


# 18/03/16 First submission of EliseMichon_HW1

>> Note: We have three programs written in Python 3, with PyDev included in the IDE Eclipse on Windows

1_set_creation.py

How to execute it:
This script takes a direct argument (sys.argv[1]), the directory path to the dataset. We assumed it is the path of a folder that contains a subfolder "69yazar" with a subdirectory "raw_texts". Stated differently, we considered that the files would be in the following locations: indicated path/69yazar/raw_texts/author1/ etc.

What it will do:
- Creation of two folders training and test
- Random selection of 60% of articles of each author for training
- Copy of the articles files in the appropriate concatenated file training/test


2_author_classification.py

How to execute it: 
This script should have taken two arguments: path to the training set and path to the test set. Because it is still in development, the script does not take arguments, but instead assumes the current directory is a folder that contains the directory "69yazar" with a subdirectory "raw_texts", and deduce from that the paths of training and test sets built in the script 1_set_creation.py. 

What it will do:
- my_tokenizer(file):
  suppress all upper comas and all the numbers
  convert all words to lower case
  find all the sequences of 1 or more alphabetical characters
  return(turkish_text)
  
- output(confusion_matrix, authors):
  compute measure values from a confusion matrix
  return precision_macro, recall_macro, f1_macro, precision_micro, recall_micro, f1_micro

- learn(training_dir_path):
  extract number of docs in each class
  tokenize each document and store the words in vocabulary
  concatenate all articles of one author in one megadocument
  calculate the log of the probability of each class
  learn the log of conditional probabilities for each word given each class 
  return authors, vocabulary, prob_classes, prob_conds

- classify_simple(training_dir_path, test_dir_path):
  for each test file go over all the classes and sum the log of probabilities knowing the class
  assign an author and fill the confusion matrix
  return (confusion_matrix)

>> Note:
At the moment of writing the report, the algorithm was attributing all test files to a same class, the one which the higher class probability. At the moment of writing this readme, the algorithm seems to finally turn and attribute the test files to different classes, at a very slow pace. 

3_read_results.py

How to execute it: 
This script does not take arguments and assumes the current directory is a folder that contains both the directory "69yazar" with a subdirectory "training", and the file example_results.txt.

What it will do:
- go over the list of training files to find back their true author
- read the assigned author in the output of the classification and fill the confusion matrix
- print the confusion matrix
