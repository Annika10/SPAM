from ISPAM_algorithm import init_bit_appering_and_first_position_sequences, I_SPAM_algorithm
from SPAM_algorithm import get_frequent_sequences, dataset_transformation
from experiments_tweets import run_experiment, run_experiment_ispam


if __name__ == "__main__":
    minSup = 2

    # example dataset from paper
    # dataset_sequences = {
    #     1: [['a'], ['c', 'd'], ['a'], ['d']],
    #     2: [['a'], ['c'], ['a'], ['e']],
    #     3: [['c'], ['a'], ['d'], ['b', 'c', 'd']],
    #     4: [['b'], ['b'], ['c']],
    #     5: [['b', 'c', 'd'], ['d']]
    # }
    dataset_Cid_Tid = [
        [1, 1, ['a']],
        [1, 2, ['c', 'd']],
        [1, 3, ['a']],
        [1, 4, ['d']],
        [2, 5, ['a']],
        [2, 6, ['c']],
        [2, 7, ['a']],
        [2, 8, ['e']],
        [3, 9, ['c']],
        [3, 10, ['a']],
        [3, 11, ['d']],
        [3, 12, ['b', 'c', 'd']],
        [4, 13, ['b']],
        [4, 14, ['b']],
        [4, 15, ['c']],
        [5, 16, ['b', 'c', 'd']],
        [5, 17, ['d']],
    ]

    list_of_words = ['a', 'b', 'c', 'd', 'e']

    run_experiment_ispam(dataset_Cid_Tid, list_of_words, minSup, plot=True)

    # compare SPAM
    # run_experiment(dataset_Cid_Tid, list_of_words, minSup, max_number_sequence)
