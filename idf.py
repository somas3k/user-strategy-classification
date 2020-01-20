from nltk.stem.porter import *
from nltk.corpus import stopwords
from collections import Counter
import math
import os
import pickle as pic
import csv


def retrieve_and_stem(tweet_list):
    translation_table = dict.fromkeys(map(ord, '\"\'\r\n`<>-()%?.!:,;'), None)
    stemmer = PorterStemmer()
    tweet_words = " ".join(tweet_list)
    tweet_words = [x.translate(translation_table) for x in tweet_words.split()]
    english_stop_words = stopwords.words('english')
    stemmed_words = [stemmer.stem(x) for x in tweet_words if len(x) > 2 and x not in english_stop_words]
    bag_of_words = Counter(stemmed_words)
    return bag_of_words, stemmed_words


def calculate_term_idf(term, bags_of_words):
    return math.log(1.0 * len(bags_of_words) / bags_of_words[term])


def calculate_idf(bags_of_words, terms):
    idf_holder = {}
    for term in terms:
        idf_holder[term] = calculate_term_idf(term, bags_of_words)
    for word in bags_of_words.keys():
        bags_of_words[word] *= 1.0 * idf_holder[word]
    return bags_of_words


def save_dictionary(dictionary, filename):
    with open("results/" + filename, 'wb') as file:
        pic.dump(dictionary, file)


def main():
    # change here to test other values
    file_amount = len(os.listdir("data/")) - 1
    nickname_tweets = dict()
    for i in range(1, file_amount):
        with open("data/filtered_" + str(i) + ".csv", encoding="utf8") as file:
            # wczytuje każdy wiersz z csv jako oddzielny słownik
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row.get('author') in nickname_tweets.keys():
                    nickname_tweets.get(row.get('author')).append(row.get('content'))
                else:
                    nickname_tweets[row.get('author')] = [row.get('content')]

    for x in nickname_tweets:
        bags_of_words, tweet_terms = retrieve_and_stem(nickname_tweets[x])
        print(bags_of_words)
        print("\n")
        print(len(bags_of_words))
        ##opcjonalny sposób liczenia IDF, ale wychodzi coś dziwnie
        # bags_of_words = calculate_idf(bags_of_words, tweet_terms)
        # print("\n")
        # print(bags_of_words)
main()
