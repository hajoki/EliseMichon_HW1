import os

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


lines = [line.rstrip('\n') for line in open("example_result.txt")]
i = 0
input_dir = os.getcwd()
training_dir_path = os.path.join(input_dir,"69yazar","training")
authors = [d for d in os.listdir(training_dir_path) if os.path.isdir(os.path.join(training_dir_path, d))]

confusion_matrix = []
for true_author in authors:
    confusion_matrix.append([])
    for assigned_author in authors:
        confusion_matrix[authors.index(true_author)].append(0)
        
for author in authors: # to go over over all the files of the test set (authors)
    true_author = author
    print("For author: %s" %true_author)
    os.chdir(os.path.join(training_dir_path,author))
    files = os.listdir(os.path.join(training_dir_path,author))
    print("We have the files: %s" %files)
    for file_to_test in files: # to go over all the files of the test set (files for each author)
        print ("File: %s" %file_to_test)
        if(file_to_test == lines[i]):
            i+=1
            assigned_author = lines[i]
            print("assigned to %s" %assigned_author)
            i+=1
            confusion_matrix[authors.index(true_author)][authors.index(assigned_author)]+=1

print(confusion_matrix)

print(output(confusion_matrix, authors))
            