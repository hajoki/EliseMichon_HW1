## 1 - Automatic training and test sets

# !/usr/bin/python

import sys
import os, random, shutil

# This script takes as an argument the directory path to the dataset
# We assumed it is a path that leads to the directory "69yazar" with a subdirectory "raw_texts"

#input_dir = sys.argv[1]
input_dir = os.getcwd()
raw_dir_path = os.path.join(input_dir,"69yazar","raw_texts")


# Creation of two folders training and test
training_dir_path = os.path.join(input_dir,"69yazar","training")
if not os.path.exists(training_dir_path):
    os.makedirs(training_dir_path)
test_dir_path = os.path.join(input_dir,"69yazar","test")
if not os.path.exists(test_dir_path):
    os.makedirs(test_dir_path)

authors = [d for d in os.listdir(raw_dir_path) if os.path.isdir(os.path.join(raw_dir_path, d))]
for author in authors:
    print(author)
    # Creation of a folder for each author in the training and test folders
    if not os.path.exists(os.path.join(training_dir_path,author)):
        os.makedirs(os.path.join(training_dir_path,author))
    if not os.path.exists(os.path.join(test_dir_path,author)):
        os.makedirs(os.path.join(test_dir_path,author))
            
    # Random selection of 60% of articles of an author for training
    list_files = os.listdir(os.path.join(raw_dir_path,author))
    number_files = len(list_files)
    random.shuffle(list_files)
    training_files = list_files[:round(number_files*0.6)]
    print("Total: %d, training: %d, test: %d" %(len(list_files),len(training_files),(len(list_files)-len(training_files))))
        
    # Copy of the articles files in the appropriate folders
    for file_name in list_files:
        full_file_name = os.path.join(raw_dir_path,author,file_name)
        if (os.path.isfile(full_file_name)):
            if file_name in training_files:
                full_new_name = os.path.join(training_dir_path,author,file_name)
                shutil.copy(full_file_name, full_new_name)
            else:
                full_new_name = os.path.join(test_dir_path,author,file_name)
                shutil.copy(full_file_name, full_new_name)