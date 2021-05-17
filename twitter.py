from SPAM_algorithm import bitmap_representation
import csv
from nltk.corpus import stopwords


def remove_stopwords(tweet_list):
    """

    :param tweet_list:
    :return:
    """
    new_tweet_list = list()
    for word in tweet_list:
        if word not in stopwords.words('english'):
            new_tweet_list.append(word)
    return new_tweet_list


def sort_and_anonymize_dataset(dataset_Cid_Tid, dict_of_usernames):
    new_dataset_Cid_Tid = list()
    dict_username = dict()
    current_customer = 0

    for element in dataset_Cid_Tid:
        print("element", element)
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
                        print("additional_entry", additional_entry)
                        additional_transaction = additional_entry[1]
                        additional_tweet_list = additional_entry[2]
                        new_dataset_Cid_Tid.append([current_customer, additional_transaction, additional_tweet_list])
            current_customer += 1
    return new_dataset_Cid_Tid


# [0] = username, [9] = tweet
def read_twitter_csv_into_dataset(username=0, tweet=9, number_of_tweets=100):
    dataset_Cid_Tid = list()
    dict_of_usernames = dict()
    word_list = list()

    with open('covid19_tweets.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            elif line_count > number_of_tweets:
                break
            else:
                username_string = row[username]
                tweet_list = row[tweet].lower().split(" ")
                tweet_list = remove_stopwords(tweet_list)

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

                print(username_string + ':' + row[tweet])
                line_count += 1
        print(f'Processed {line_count} lines.')
    return dataset_Cid_Tid, word_list, dict_of_usernames


if __name__ == "__main__":
    # nltk.download('stopwords')

    dataset_Cid_Tid, word_list, dict_usernames = read_twitter_csv_into_dataset()
    print(dataset_Cid_Tid)
    print(len(word_list))

    # sorting
    sorted_dataset_Cid_Tid = sort_and_anonymize_dataset(dataset_Cid_Tid, dict_usernames)

    dict_bitmap = bitmap_representation(sorted_dataset_Cid_Tid, word_list)
    #print(dict_bitmap)
