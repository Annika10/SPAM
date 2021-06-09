from experiments_tweets import load_dataset, run_experiment, run_experiment_ispam
from comparison_analysis_minsup import plot_analysis
import csv


def analyse_dataset(dataset_Cid_Tid):
    dict_number_of_tweets_with_len = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
        16: 0,
        17: 0,
        18: 0,
        19: 0,
        20: 0,
        21: 0   # tweets with more than 20 words
    }
    for tweet_data in dataset_Cid_Tid:
        average_items_of_transactions = len(tweet_data[2])
        if average_items_of_transactions in dict_number_of_tweets_with_len.keys():
            new_value = dict_number_of_tweets_with_len[average_items_of_transactions] + 1
            dict_number_of_tweets_with_len[average_items_of_transactions] = new_value
        else:
            new_value = dict_number_of_tweets_with_len[21] + 1
            dict_number_of_tweets_with_len[21] = new_value

    print(dict_number_of_tweets_with_len)


def get_tweets_with_specific_len(dataset_Cid_Tid, length, number_of_tweets):
    new_dataset = list()
    new_wordlist = list()
    counter = 0
    current_user = 1
    for tweet_data in dataset_Cid_Tid:
        if counter == number_of_tweets:
            break
        items_of_transactions_lenghts = len(tweet_data[2])
        if items_of_transactions_lenghts == length:
            new_dataset.append([current_user, 1, tweet_data[2]])

            # get new word list
            for word in tweet_data[2]:
                if word not in new_wordlist:
                    new_wordlist.append(word)
                # remove duplicates
            new_wordlist = list(dict.fromkeys(new_wordlist))

            counter += 1
            current_user += 1

    if counter < number_of_tweets:
        print("not enough data provided")
    return new_dataset, new_wordlist


def analysis_to_csv_for_saving(dict_len, dataset_name, minSup):
    dict_sup_runtime_spam = dict()
    dict_sup_runtime_ispam = dict()
    for length in dict_len.keys():
        # SPAM
        spam_runtime = run_experiment(dict_len[length][0], dict_len[length][1], minSup)
        dict_sup_runtime_spam[length] = spam_runtime
        # ISPAM
        ispam_runtime = run_experiment_ispam(dict_len[length][0], dict_len[length][1], minSup)
        dict_sup_runtime_ispam[length] = ispam_runtime

    with open('spam_' + dataset_name + '.csv', 'w', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        for key, value in dict_sup_runtime_spam.items():
            # write a row to the csv file
            data_list = [key, value]
            writer.writerow(data_list)

    with open('ispam_' + dataset_name + '.csv', 'w', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        for key, value in dict_sup_runtime_ispam.items():
            # write a row to the csv file
            data_list = [key, value]
            writer.writerow(data_list)


if __name__ == "__main__":
    sorted_dataset_Cid_Tid_10000, word_list_10000 = load_dataset(number_of_tweets=10000)

    # analyse_dataset(sorted_dataset_Cid_Tid_10000)
    # result:
    # {0: 0, 1: 2, 2: 14, 3: 52, 4: 120, 5: 155, 6: 239, 7: 317, 8: 644, 9: 1115, 10: 1651, 11: 1926, 12: 1766, 13: 1144, 14: 538, 15: 231, 16: 59, 17: 15, 18: 7, 19: 3, 20: 1, 21: 1}

    dataset_Cid_Tid_9, word_list_9 = get_tweets_with_specific_len(sorted_dataset_Cid_Tid_10000, length=9, number_of_tweets=1100)
    dataset_Cid_Tid_10, word_list_10 = get_tweets_with_specific_len(sorted_dataset_Cid_Tid_10000, length=10, number_of_tweets=1100)
    dataset_Cid_Tid_11, word_list_11 = get_tweets_with_specific_len(sorted_dataset_Cid_Tid_10000, length=11, number_of_tweets=1100)
    dataset_Cid_Tid_12, word_list_12 = get_tweets_with_specific_len(sorted_dataset_Cid_Tid_10000, length=12, number_of_tweets=1100)
    dataset_Cid_Tid_13, word_list_13 = get_tweets_with_specific_len(sorted_dataset_Cid_Tid_10000, length=13, number_of_tweets=1100)

    dict_len = {
        9: [dataset_Cid_Tid_9, word_list_9],
        10: [dataset_Cid_Tid_10, word_list_10],
        11: [dataset_Cid_Tid_11, word_list_11],
        12: [dataset_Cid_Tid_12, word_list_12],
        13: [dataset_Cid_Tid_13, word_list_13]
    }

    analysis_to_csv_for_saving(dict_len, "lenT", minSup=75)

    plot_analysis([9, 10, 11, 12, 13], "lenT", "length of tweet")
