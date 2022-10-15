import string
import nltk
import re
from os import path


def remove_nulls(dataset):
    print("Dropping nulls...")
    print("Dataset size before - "+ str(len(dataset)))
    dataset = dataset.dropna()
    print("Dataset size after - "+ str(len(dataset)))
    return dataset

def transform_lowecase(text):
    return text.lower()

def remove_spaces(text):
    text = ' '.join(text.split())
    return re.sub(r'\s{2,}'," ",text)

def remove_punctuations(text):
    # return every character in the text if it is not punctuation
    # To rebuild the sentece, we will join the characters in the list without any seperator
    text = "".join([char for char in text if char not in string.punctuation])
    return re.sub(r'\s{2,}'," ",text)

def tokenize_text(text):
    tokenized = text.split(' ')
    return [word for word in tokenized if word != ""]

def remove_stopwords(tokenized_text):
    stopwords = nltk.corpus.stopwords.words('english')
    return [word for word in tokenized_text if word not in stopwords]

def lemmatize_text(tokenized_text):
    wn = nltk.WordNetLemmatizer()
    return [wn.lemmatize(word) for word in tokenized_text]

def reset_tokens(tokenize_text):
    return " ".join(tokenize_text)

def save_processed_data(filename,before,data_columns,after):
    BASE_DATASET_PATH = "..\\datasets"
    before[data_columns] = after
    before = before.reset_index(drop=True)
    before.to_csv(path.join(BASE_DATASET_PATH,filename),index=False)

def dataset_pipeline(dataset,data_columns,filename):
    dataset = remove_nulls(dataset)
    xs = dataset[data_columns]
    print("Transforming to lowercase...")
    xs = xs.applymap(lambda x: transform_lowecase(x))
    print("Removing spaces...")
    xs = xs.applymap(lambda x: remove_spaces(x))
    print("Removing punctuations...")
    xs = xs.applymap(lambda x: remove_punctuations(x))
    print("Tokenizing text...")
    xs = xs.applymap(lambda x: tokenize_text(x))
    print("Removing stopwords...")
    xs = xs.applymap(lambda x: remove_stopwords(x))
    print("Lemmatizing text...")
    xs = xs.applymap(lambda x: lemmatize_text(x))
    print("Resetting tokens...")
    xs = xs.applymap(lambda x: reset_tokens(x))
    print("Saving to new file "+filename)
    save_processed_data(filename,dataset,data_columns,xs)
    return dataset

def text_pipeline(text):
    text = transform_lowecase(text)
    text = remove_spaces(text)
    text = remove_punctuations(text)
    text = tokenize_text(text)
    text = remove_stopwords(text)
    text = lemmatize_text(text)
    text = reset_tokens(text)
    return text