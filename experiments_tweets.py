from SPAM_algorithm import bitmap_representation, create_tree, get_frequent_sequences, plot_frequent_sequence, create_wordcloud, dataset_transformation, spam_algorithm
from twitter import read_twitter_csv_into_dataset, sort_and_anonymize_dataset
from ISPAM_algorithm import init_bit_appering_and_first_position_sequences, I_SPAM_algorithm

import time


def run_experiment_old(sorted_dataset_Cid_Tid, word_list, minSup, max_number_sequence=2):
    """

    :param sorted_dataset_Cid_Tid:
    :param word_list:
    :param minSup:
    :param max_number_sequence:
    :return:
    """
    startTime = time.time()

    dict_bitmap, dict_support = bitmap_representation(sorted_dataset_Cid_Tid, word_list, minSup)

    updated_word_list = list(dict_bitmap.keys())
    updated_word_list = [element[1:-1] for element in updated_word_list]

    dict_bitmap, dict_support = create_tree(dict_bitmap, dict_support, updated_word_list, min_sup=minSup,
                                            limit=max_number_sequence)

    frequent_sequences = get_frequent_sequences(dict_bitmap)

    executionTime = (time.time() - startTime)
    print('Execution time in seconds for SPAM: ' + str(executionTime))
    print("spam", frequent_sequences)
    print("spam", dict_support)

    # plot_frequent_sequence(dict_support)
    # create_wordcloud(dict_support)
    return executionTime


def run_experiment(sorted_dataset_Cid_Tid, word_list, minSup):
    """

    :param sorted_dataset_Cid_Tid:
    :param word_list:
    :param minSup:
    :param max_number_sequence:
    :return:
    """
    startTime = time.time()

    dict_bitmap, dict_support = bitmap_representation(sorted_dataset_Cid_Tid, word_list, minSup)

    updated_word_list = list(dict_bitmap.keys())
    updated_word_list = [element[1:-1] for element in updated_word_list]

    dict_bitmap, dict_support = spam_algorithm(dict_bitmap, dict_support, minSup)

    frequent_sequences = get_frequent_sequences(dict_bitmap)

    executionTime = (time.time() - startTime)
    print('Execution time in seconds for SPAM: ' + str(executionTime))
    # print("spam", frequent_sequences)
    # print("spam", dict_support)
    print("spam", len(frequent_sequences))

    # plot_frequent_sequence(dict_support)
    # create_wordcloud(dict_support)
    return executionTime


def run_experiment_ispam(dataset_Cid_Tid, list_of_words, minSup):
    startTime = time.time()

    dataset_sequences = dataset_transformation(dataset_Cid_Tid)
    appear_dict, fp_dict, bit_dict = init_bit_appering_and_first_position_sequences(dataset_sequences, list_of_words)

    appear_dict, fp_dict, dict_support = I_SPAM_algorithm(appear_dict, minSup, dataset_sequences, bit_dict, fp_dict)
    frequent_sequences = get_frequent_sequences(appear_dict)

    executionTime = (time.time() - startTime)
    print('Execution time in seconds for ISPAM: ' + str(executionTime))
    # print("ispam", frequent_sequences)
    # print("ispam", dict_support)
    print("ispam", len(frequent_sequences))

    # plot_frequent_sequence(dict_support)
    # create_wordcloud(dict_support)
    return executionTime


def load_dataset(number_of_tweets):
    dataset_Cid_Tid, word_list, dict_usernames = read_twitter_csv_into_dataset(number_of_tweets=number_of_tweets)
    # sorting
    sorted_dataset_Cid_Tid = sort_and_anonymize_dataset(dataset_Cid_Tid, dict_usernames,
                                                            customer_starting_index=1)
    word_list = sorted(word_list)
    return sorted_dataset_Cid_Tid, word_list


if __name__ == "__main__":
    # nltk.download('stopwords')

    dict_runtimes = dict()

    ### experiment 2
    # try SPAM algorithm with first 100 tweets and minimum support of 5

    sorted_dataset_Cid_Tid_100, word_list_100 = load_dataset(number_of_tweets=100)
    minSup_2 = 5
    # here is 2 enough because in data set there are not more than two transactions per tweet user
    max_number_sequence_2 = 2

    # SPAM
    spam_runtime = run_experiment(sorted_dataset_Cid_Tid_100, word_list_100, minSup_2)

    # ISPAM
    ispam_runtime = run_experiment_ispam(sorted_dataset_Cid_Tid_100, word_list_100, minSup_2)

    dict_runtimes["experiment_2_spam"] = spam_runtime
    dict_runtimes["experiment_2_ispam"] = ispam_runtime

    ### experiment 3: DOESN'T WORK
    # try SPAM algorithm with all tweets and minSup of 50
    # dataset_Cid_Tid_all, word_list_all, dict_usernames_all = read_twitter_csv_into_dataset(number_of_tweets=float('inf'))
    # sorted_dataset_Cid_Tid_all = sort_and_anonymize_dataset(dataset_Cid_Tid_all, dict_usernames_all)
    # word_list_all = sorted(word_list_all)

    ### experiment 4:
    # try SPAM algorithm with first 1000 tweets and minimum support of 50
    dataset_Cid_Tid_1000, word_list_1000, dict_usernames_1000 = read_twitter_csv_into_dataset(number_of_tweets=1000)
    sorted_dataset_Cid_Tid_1000 = sort_and_anonymize_dataset(dataset_Cid_Tid_1000, dict_usernames_1000)
    word_list_1000 = sorted(word_list_1000)

    minSup_4 = 50
    # one person with 27 tweets, next most tweets from one person are 9
    max_number_sequence_4 = 9
    # SPAM
    spam_runtime = run_experiment(sorted_dataset_Cid_Tid_1000, word_list_1000, minSup_4)
    # ISPAM
    ispam_runtime = run_experiment_ispam(sorted_dataset_Cid_Tid_1000, word_list_1000, minSup_4)

    dict_runtimes["experiment_4_spam"] = spam_runtime
    dict_runtimes["experiment_4_ispam"] = ispam_runtime

    ### experiment 5:
    # try SPAM algorithm with first 1000 tweets and minimum support of 30

    minSup_5 = 30
    # SPAM
    run_experiment(sorted_dataset_Cid_Tid_1000, word_list_1000, minSup_5)
    # ISPAM
    run_experiment_ispam(sorted_dataset_Cid_Tid_1000, word_list_1000, minSup_5)

    spam_runtime = dict_runtimes["experiment_5_spam"] = spam_runtime
    ispam_runtime = dict_runtimes["experiment_5_ispam"] = ispam_runtime

    print(dict_runtimes)
