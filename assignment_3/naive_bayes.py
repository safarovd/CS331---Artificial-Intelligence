#Programming Assignment 3
import string
import csv
import time


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

###############################################
# Classification Step:
###############################################
def get_naive_bayes_parameters(vocabulary, training_data):
    num_features = len(vocabulary)
    # these two lists take on the same dimentions of vocabulary. 
    # If the current index within either of these has a value,
    # that value is a direct count of the frequency of the word
    # in it's associated sentiment (i.e. "happy" may be within index)
    # 50 in vocaulary, word_occurances_positive[50] will contain at least
    # a 1 for the word happy.
    word_occurances_positive = [0 for _ in range(num_features)]
    word_occurances_negative = [0 for _ in range(num_features)]
    
    total_words_in_positive = 0
    total_words_in_negative = 0
    num_positive_sentences = 0
    # Each slot in that feature vector will be represented by M which has the value of 0 or 1 at each index within it
    for sentence_idx, M in enumerate(training_data):
        # Count the number of positive sentences (or positive sentiment)
        
        if M[-1] == 1:
            num_positive_sentences += 1
        # iterate through the sentence vector (M) to associate each word with positive and negative sentiments
        # word_idx directly aligns with vocabulary as everything is in alphabetical order
        for word_idx, word_present in enumerate(M):
            # If positive sentiment
            if M[-1] == 1:
                # print(word_idx, M[-1])
                word_occurances_positive[word_idx] += word_present
                # NOTE: this is weird as we do not have the frequency of the positive word within the sentence...
                # we just have if the word is contained within the sentence. We might be able to just pass
                # cleaned_data to this function and in this line just count the frequency of the word
                # within the sentence at cleaned_data[sentence_idx]
                total_words_in_positive += word_present
            elif M[-1] == 0:
                word_occurances_negative[word_idx] += word_present
                total_words_in_negative += word_present
    # P(CD = 1) - reference slide 8 in NaiveBayes slide deck
    prob_positive_sentence = num_positive_sentences/len(training_data)
    # P(M = word_idx | CD = 1) list (word_idx == wi)
    prob_wi_given_positive = []
    # P(M = word_idx | CD = 0) list
    prob_wi_given_negative = []
    # calculating the probability of P(M = m | CD = v)  - reference slide 9 and 21 in NaiveBayes slide deck
    for wi in range(num_features):
        # P(word_idx = 1 | CD = 1) 
        # ((# of records with M = true AND CD = true) + 1) / (# of records with CD = true) + N
        # NOTE: Not sure if we divid by the total record of positive words or sentences
        p_wi_positive = ((word_occurances_positive[wi]*prob_positive_sentence) + 1) / (total_words_in_positive + 2)
        prob_wi_given_positive.append(p_wi_positive)
        # P(word_idx = 0 | CD = 0)
        # notice how I do 1 - prob_positive_sentence. I believe this should get us the prob of a neg sentence
        p_wi_negative = ((word_occurances_negative[wi]*(1-prob_positive_sentence)) + 1) / (total_words_in_negative + 2)
        prob_wi_given_negative.append(p_wi_negative)

    return prob_positive_sentence, prob_wi_given_positive, prob_wi_given_negative

if __name__ == "__main__": 
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

    #Obtain the Naive Bayes parameters: number of positive sentences, probability of a feature given CD is 1 and probability of a features give CD = 0
    prob_positive_sentence, prob_wi_given_positive, prob_wi_given_negative = get_naive_bayes_parameters(vocabulary, vectorized_data)
    print("Probability of positive word: ", prob_positive_sentence)
    print(prob_wi_given_negative)
    