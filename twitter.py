import csv
from nltk.corpus import stopwords
import re
import os
import sys
from pathlib import Path


def remove_stopwords(tweet_list):
    """
    removes stopwords from tweets
    :param tweet_list: list with each word of tweet
    :return: cleaned up list with words of tweet
    """
    special_characters = ["\"", "?", ":", "…", "…", "…", "(", ")", "“", "”", "-", "|", "&amp;"]
    new_tweet_list = list()
    for word in tweet_list:
        if word not in stopwords.words('english'):
            for char in special_characters:
                word = word.replace(char, "")
            # by replacing possibly no characters left
            if word and not word.isnumeric():
                new_tweet_list.append(word)
    return new_tweet_list


def sort_and_anonymize_dataset(dataset_Cid_Tid, dict_of_usernames, customer_starting_index=1):
    """
    sort dataset that each user's tweets follow up after each other
    :param dataset_Cid_Tid: unsorted dataset
    :param dict_of_usernames: dictionary where number of tweets for each user is stored
    :return: sorted dataset
    """
    new_dataset_Cid_Tid = list()
    dict_username = dict()
    current_customer = customer_starting_index

    for element in dataset_Cid_Tid:
        # print("element", element)
        username = element[0]
        if username not in dict_username.keys():
            dict_username[username] = current_customer
            transaction = element[1]
            tweet_list = element[2]
            new_dataset_Cid_Tid.append([current_customer, transaction, tweet_list])
            if not dict_of_usernames[username] == 1:
                # search for other entries
                for additional_entry in dataset_Cid_Tid:
                    additional_username = additional_entry[0]
                    if username == additional_username and not element == additional_entry:
                        # print("additional_entry", additional_entry)
                        additional_transaction = additional_entry[1]
                        additional_tweet_list = additional_entry[2]
                        new_dataset_Cid_Tid.append([current_customer, additional_transaction, additional_tweet_list])
            current_customer += 1
    return new_dataset_Cid_Tid


# [0] = username, [9] = tweet
def read_twitter_csv_into_dataset(username=7, tweet=10, number_of_tweets=float('inf')):
    """
    reads the data out of the csv into a dataset (list)
    in addition all words are collected and a dictionary of usernames is created with the number of tweets for each user
    :param username: column in csv where username is stored
    :param tweet: column in csv where tweet text is stored
    :param number_of_tweets: number of collected tweets
    :return: dataset, list of words, dictionary of usernames
    """
    dataset_Cid_Tid = list()
    dict_of_usernames = dict()
    word_list = list()

    parent_path = Path(sys.path[0]).parent
    with open(os.path.join(parent_path, 'data/covid.csv'), encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            elif line_count > number_of_tweets:
                break
            else:
                username_string = row[username]
                # remove links
                tweet_str = re.sub("http(\S)*", "", row[tweet].lower())
                tweet_list = re.split('\s|,|\.', tweet_str)
                tweet_list = remove_stopwords(tweet_list)
                tweet_list = sorted(tweet_list)

                if username_string not in dict_of_usernames.keys():
                    # add to username dict
                    dict_of_usernames[username_string] = 1
                    new_row = [username_string, 1, tweet_list]
                else:
                    # update username dict
                    new_value = dict_of_usernames[username_string] + 1
                    dict_of_usernames[username_string] = new_value
                    new_row = [username_string, new_value, tweet_list]
                dataset_Cid_Tid.append(new_row)

                for word in tweet_list:
                    if word not in word_list:
                        word_list.append(word)
                # remove duplicates
                word_list = list(dict.fromkeys(word_list))

                # print(username_string + ':' + row[tweet])
                line_count += 1
        print(f'Processed {line_count} lines.')
    return dataset_Cid_Tid, word_list, dict_of_usernames