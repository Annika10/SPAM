from SPAM_algorithm import bitmap_representation, create_tree, get_frequent_sequences, plot_frequent_sequence, create_wordcloud
from twitter import read_twitter_csv_into_dataset, sort_and_anonymize_dataset


def run_experiment(sorted_dataset_Cid_Tid, word_list, minSup, max_number_sequence=2):
    """

    :param sorted_dataset_Cid_Tid:
    :param word_list:
    :param minSup:
    :param max_number_sequence:
    :return:
    """
    dict_bitmap, dict_support = bitmap_representation(sorted_dataset_Cid_Tid, word_list, minSup)
    # print(dict_bitmap.keys())
    print("lengths of initial number of frequent items", len(dict_bitmap.keys()))

    updated_word_list = list(dict_bitmap.keys())
    updated_word_list = [element[1:-1] for element in updated_word_list]

    dict_bitmap, dict_support = create_tree(dict_bitmap, dict_support, updated_word_list, min_sup=minSup,
                                            limit=max_number_sequence)

    frequent_sequences = get_frequent_sequences(dict_bitmap)
    print(frequent_sequences)
    print(dict_support)

    plot_frequent_sequence(dict_support)
    create_wordcloud(dict_support)


if __name__ == "__main__":
    # nltk.download('stopwords')

    # ### experiment 2
    # # try SPAM algorithm with first 100 tweets and minimum support of 5
    # dataset_Cid_Tid_100, word_list_100, dict_usernames_100 = read_twitter_csv_into_dataset(number_of_tweets=100)
    # # sorting
    # sorted_dataset_Cid_Tid_100 = sort_and_anonymize_dataset(dataset_Cid_Tid_100, dict_usernames_100)
    # word_list_100 = sorted(word_list_100)
    #
    # minSup_2 = 5
    # # here is 2 enough because in data set there are not more than two transactions per tweet user
    # max_number_sequence_2 = 2
    # run_experiment(sorted_dataset_Cid_Tid_100, word_list_100, minSup_2, max_number_sequence_2)

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
    # run_experiment(sorted_dataset_Cid_Tid_1000, word_list_1000, minSup_4, max_number_sequence_4)

    ### experiment 5:
    # try SPAM algorithm with first 1000 tweets and minimum support of 30

    minSup_5 = 30
    run_experiment(sorted_dataset_Cid_Tid_1000, word_list_1000, minSup_5, max_number_sequence_4)