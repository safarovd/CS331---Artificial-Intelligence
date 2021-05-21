#Programming Assignment 3
import string

def read_data():
    #Create a file object
    f = open("./data/trainingSet.txt", 'r')
    #Read in all lines as an array
    lines = f.readlines()
    #Translate is the most efficent way to strip punctiatuon, also make it lowercase
    stripped = [line.translate(str.maketrans('', '', string.punctuation)).lower().strip("\n").strip() for line in lines]

    #Return cleansed string
    return stripped

def seperate_class_labels(cleansed_data):
    data_with_labels = [[datapoint.split('\t')[0].strip(), datapoint.split('\t')[1].lstrip()] for datapoint in cleansed_data]
    return data_with_labels


cleansed_data = read_data()
data_with_labels = seperate_class_labels(cleansed_data)

for point in data_with_labels:
    print(point)