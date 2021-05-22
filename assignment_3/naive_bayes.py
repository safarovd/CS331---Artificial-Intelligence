#Programming Assignment 3
import string
import csv


def read_data(filepath):
    #Create a file object
    f = open(filepath, 'r')
    #Read in all lines as an array
    lines = f.readlines()
    #Translate is the most efficent way to strip punctiatuon, also make it lowercase
    stripped = [line.translate(str.maketrans('', '', string.punctuation)).lower().strip("\n").strip() for line in lines]

    #Return cleansed string
    return stripped


def seperate_class_labels(cleansed_data):
    #Make a smaller array with the data and its label, strip and lstrip are used to remove whitespace
    data_with_labels = [[datapoint.split('\t')[0].strip(), datapoint.split('\t')[1].lstrip()] for datapoint in cleansed_data]
    return data_with_labels


def get_vocabulary(data):
    #Get a list containing only the text part of the entries
    text = [point[0] for point in data]
    #Because a set only stores unique data use a set for storing the vocabulary
    unique_words = set()
    #Get each line
    for line in text:
        #Split each line into words
        for word in line.split(" "):
            #Make sure we aren't adding the empty string
            if word != '':
                #Add the word to the set, if it's already in the set it gets ignored
                unique_words.add(word)

    #Convert the set to a list for sorting and sort it alphabetically
    return sorted(list(unique_words))


def featurize(data, vocabulary):
    #Vector set is a list of all review vectors
    vector_set = []
    #Get just the text entries to vectorize them
    just_text = [point[0] for point in data]
    for i, review in enumerate(just_text):
        #Initialize a vector of zeroes of the length of the vocabulary for each review
        review_vector = [0]*len(vocabulary)
        #Split each review into words
        for word in review.split(" "):
            #If the word is in the review then flip the number at the index of its occurence in the vocabulary
            if word in review and word != '' and word in vocabulary:
                #print(vocabulary.index(word))
                review_vector[vocabulary.index(word)] = 1
        #Add the class label as the last element of the review vector
        review_vector[-1] = int(data[i][1])
        vector_set.append(review_vector)

    return vector_set


def write_preprocessed_data(data, vocab, name):
    with open(name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(vocab)
        
        csvwriter.writerows(data) 


#Utility function for debugging, writes all vocab words with their index to a csv file
def write_vocab_as_csv(vocabulary):  
    formatted_vocab = []

    for i, word in enumerate(vocabulary):
        formatted_vocab.append([i, word])

    pred_col_names = ["id", "word"]
    output_filename = "vocab.csv"

    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        csvwriter.writerow(pred_col_names)
        
        csvwriter.writerows(formatted_vocab)


#Read in the data
cleansed_data = read_data("./data/trainingSet.txt")
cleansed_test = read_data("./data/testSet.txt")

#add labels to it
data_with_labels = seperate_class_labels(cleansed_data)
test_data_labels = seperate_class_labels(cleansed_test)
#get unique words to form the vocabulary
vocabulary = get_vocabulary(data_with_labels)
#append a dummy class label here
vocabulary.append("classlabel")
#convert the data into feature vectors
vectorized_data = featurize(data_with_labels, vocabulary)
test_vectorized = featurize(test_data_labels, vocabulary)

#Write preprocessed training data
write_preprocessed_data(vectorized_data, vocabulary, "preprocessed_train.txt")

#Write preprocessed testing data
write_preprocessed_data(test_vectorized, vocabulary, "preprocessed_test.txt")
