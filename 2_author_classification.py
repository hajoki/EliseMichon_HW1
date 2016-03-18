# !/usr/bin/python

import os, fileinput, re, locale, collections, math

def my_tokenizer(file):
    locale.setlocale(locale.LC_ALL,'Turkish_Turkey.1254')
    # print (locale.getlocale(locale.LC_ALL))
    # print (sys.getdefaultencoding(), sys.stdin.encoding, sys.stdout.encoding)
    with open(file,'r+') as f:
        original_text = f.read()
        
        replacements =  {"ð": "ğ", "ý": "ı", "þ": "ş", "Þ": "Ş", "Ý": "İ"}
        turkish_text = "".join([replacements.get(c, c) for c in original_text])
        
        delete_upper_coma = re.compile( "[\’\‘\']")
        turkish_text = delete_upper_coma.sub("",turkish_text).lower()
        
        delete_numbers = re.compile( "[0-9]")
        turkish_text = delete_numbers.sub("",turkish_text).lower()

        words = re.compile("\w+")
        turkish_text = words.findall(turkish_text)
    return turkish_text

def output(confusion_matrix, authors):
    # in the confusion matrix the lines (sublists) represent the true author
    sum_by_column = [sum(x) for x in zip(*confusion_matrix)] # across the sublists
    sum_by_row = [sum(x) for x in confusion_matrix] # inside a sublist
    
    precision_macro = 0
    recall_macro = 0
    for true_author in authors:
        precision_macro += (confusion_matrix[authors.index(true_author)][authors.index(true_author)] / sum_by_column[authors.index(true_author)])
        recall_macro += (confusion_matrix[authors.index(true_author)][authors.index(true_author)] / sum_by_row[authors.index(true_author)])
    precision_macro /= len(authors)
    recall_macro /= len(authors)
    f1_macro = 2*precision_macro*recall_macro/(precision_macro+recall_macro)
    
    precision_micro = 0
    recall_micro = 0
    for true_author in authors:
        precision_micro += confusion_matrix[authors.index(true_author)][authors.index(true_author)]
        recall_micro += confusion_matrix[authors.index(true_author)][authors.index(true_author)]
    precision_micro /= sum(sum_by_column)
    recall_micro /= sum(sum_by_row)
    f1_micro = 2*precision_micro*recall_micro/(precision_micro+recall_micro)
    
    return precision_macro, recall_macro, f1_macro, precision_micro, recall_micro, f1_micro

def learn(training_dir_path):
    # extract number of docs in each class, global vocabulary, and megadocuments by author
    authors = [d for d in os.listdir(training_dir_path) if os.path.isdir(os.path.join(training_dir_path, d))]
    vocabulary = []
    prob_classes = []
    
    for author in authors:
        # store the number of documents in each class
        prob_classes.append(len(os.listdir(os.path.join(training_dir_path,author))))
        
        os.chdir(os.path.join(training_dir_path,author))
        files = os.listdir(os.path.join(training_dir_path,author))
        for file in files:
            # tokenize each document
            list_words = my_tokenizer(file)
            # store the words in vocabulary
            vocabulary = list(set(vocabulary + list_words))
            
        # concatenate all articles of one author in one megadocument
        with open(os.path.join(training_dir_path,"%s.txt" %author), 'w') as fout, fileinput.input(files) as fin:
            for line in fin: 
                fout.write(line)
                 
    # calculate the log of the probability of each class
    total_number_docs = sum(prob_classes)
    prob_classes[:] = [(x/total_number_docs) for x in prob_classes]
    prob_classes[:] = [math.log(x) for x in prob_classes]
    
    # learn the log of conditional probabilities for each word given each class 
    prob_conds = []
    alpha = 1
    for author in authors:
        os.chdir(os.path.join(training_dir_path,author))
        files = os.listdir(os.path.join(training_dir_path,author))
        for file in files:
            prob_cond_author = []
            file = os.path.join(training_dir_path,"%s.txt" %author)
            list_words = my_tokenizer(file)
            counts = collections.Counter(list_words)
            for word in vocabulary:
                prob_cond_author.append( math.log( (counts[word]+alpha) / (len(list_words)+alpha*len(vocabulary)) ))
            prob_conds.append(prob_cond_author)           

    return authors, vocabulary, prob_classes, prob_conds

def classify_simple(training_dir_path, test_dir_path):
    authors, vocabulary, prob_classes, prob_conds = learn(training_dir_path) # the learn part is slow but seems ok, problem in the classification
    print(authors)
    print(len(vocabulary))
    print(prob_classes)
    print(len(prob_conds[0]))
    
    confusion_matrix = []
    for true_author in authors:
        confusion_matrix.append([])
        for assigned_author in authors:
            confusion_matrix[authors.index(true_author)].append(0)
        
    for author in authors: # to go over over all the files of the test set (authors)
        true_author = author
        os.chdir(os.path.join(test_dir_path,author))
        files = os.listdir(os.path.join(test_dir_path,author))
            
        for file_to_test in files: # to go over all the files of the test set (files for each author)
            print(file_to_test)
            list_words = my_tokenizer(file_to_test)
            sum_logs = []
            for author in authors: # to go over all the classes and sum the log of probabilities knowing the class
                sum_class = prob_classes[authors.index(author)]
                for word in list_words:
                    if(word in vocabulary):
                        sum_class += prob_conds[authors.index(author)][vocabulary.index(word)]
                sum_logs.append(sum_class)
            assigned_author = authors[sum_logs.index(max(sum_logs))]
            print(assigned_author)
            confusion_matrix[authors.index(true_author)][authors.index(assigned_author)]+=1
    
    return(confusion_matrix)
'''
def learn_extra(training_dir_path):
    # extract number of docs in each class, global vocabulary, and megadocuments by author
    authors = [d for d in os.listdir(training_dir_path) if os.path.isdir(os.path.join(training_dir_path, d))]
    vocabulary = []
    number_words = []
    prob_classes = []
    
    for author in authors:
        # store the number of documents in each class
        number_files_author = len(os.listdir(os.path.join(training_dir_path,author)))
        prob_classes.append(number_files_author)
        
        os.chdir(os.path.join(training_dir_path,author))
        files = os.listdir(os.path.join(training_dir_path,author))
        for file in files:
            # tokenize each document
            list_words = my_tokenizer(file)
            # store the words in vocabulary
            vocabulary = list(set(vocabulary + list_words))
            # store the number of words of the article in the possible number of words
            number_words = list(set(number_words + [len(list_words)]))
                 
    # calculate the log of the probability of each class
    total_number_docs = sum(prob_classes)
    print(prob_classes)
    prob_classes[:] = [(x/total_number_docs) for x in prob_classes]
    print(prob_classes)
    prob_classes[:] = [math.log(x) for x in prob_classes]
    
    # learn the log of conditional probabilities for each word given each class and for each number of words given each class
    prob_conds = []
    prob_number_words = []
    alpha = 1
    for author in authors:
        prob_cond_author = []
        prob_number_word_author = []
            
        os.chdir(os.path.join(training_dir_path,author))
        files = os.listdir(os.path.join(training_dir_path,author))
        for file in files:
            list_words = my_tokenizer(file)
            counts = collections.Counter(list_words)
            for word in vocabulary:
                prob_cond_author.append( math.log( (counts[word]+alpha) / (len(list_words)+alpha*len(vocabulary)) ))
            prob_conds.append(prob_cond_author)
            
    return authors, vocabulary, prob_classes, prob_conds, number_words

def classify_extra(training_dir_path, test_dir_path):
    authors, vocabulary, prob_classes, prob_conds, number_words = learn(training_dir_path)
    confusion_matrix = []
    for true_author in authors:
        confusion_matrix.append([])
        for assigned_author in authors:
            confusion_matrix[authors.index(true_author)].append(0)
        
    for author in authors: # to go over over all the files of the test set (authors)
        true_author = author
        os.chdir(os.path.join(test_dir_path,author))
        files = os.listdir(os.path.join(test_dir_path,author))
            
        for file_to_test in files: # to go over all the files of the test set (files for each author)
            print(file_to_test)
            list_words = my_tokenizer(file_to_test)
            number_words_test = len(list_words)
            
            sum_logs = []
            for author in authors: # to go over all the classes and sum the log of probabilities knowing the class
                sum_class = prob_classes[authors.index(author)] 
                for word in list_words:
                    if(word in vocabulary):
                        sum_class += prob_conds[authors.index(author)][vocabulary.index(word)]
                sum_logs.append(sum_class)
            #print(sum_logs)
            
            # 
            
            
            
            assigned_author = authors[sum_logs.index(max(sum_logs))]
            print(assigned_author)
            confusion_matrix[authors.index(true_author)][authors.index(assigned_author)]+=1
    
    return(confusion_matrix)
'''

input_dir = os.getcwd()
training_dir_path = os.path.join(input_dir,"69yazar","training")
test_dir_path = os.path.join(input_dir,"69yazar","test")
confusion_matrix = classify_simple(test_dir_path, training_dir_path)
# output(confusion_matrix)
# gives an error because all test files are wrongly attributed to a same class by the classification, so some quantities are divided by 
# but the function works well
confusion_matrix = [[1,2,3], [4,5,6], [7,8,9]]
authors = ["abbasGuclu","zekiCol","elifSafak"]
precision_macro, recall_macro, f1_macro, precision_micro, recall_micro, f1_micro = output(confusion_matrix, authors)
print("Macroaverage: Precision %d, Recall %d, F1 %d" %(precision_macro, recall_macro, f1_macro))
print("Microaverage: Precision %d, Recall %d, F1 %d" %(precision_micro, recall_micro, f1_micro))