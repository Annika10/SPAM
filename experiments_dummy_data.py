from experiments_tweets import run_experiment


if __name__ == "__main__":
    ### experiment 1
    # test SPAM algorithm with dummy data set

    minSup = 2
    # here is 2 enough because in dummy data set only one customer has more than 2 transactions but minsup is higher than 1
    max_number_sequence = 2

    # example dataset from paper
    dataset_sequences = {
        1: [['a', 'b', 'd'], ['b', 'c', 'd'], ['b', 'c', 'd']],
        2: [['b'], ['a', 'b', 'c']],
        3: [['a', 'b'], ['b', 'c', 'd']]
    }
    dataset_Cid_Tid = [
        [1, 1, ['a', 'b', 'd']],
        [1, 3, ['b', 'c', 'd']],
        [1, 6, ['b', 'c', 'd']],
        [2, 2, ['b']],
        [2, 4, ['a', 'b', 'c']],
        [3, 5, ['a', 'b']],
        [3, 7, ['b', 'c', 'd']],
    ]
    ordered_list_of_words = ['a', 'b', 'c', 'd']

    run_experiment(dataset_Cid_Tid, ordered_list_of_words, minSup, max_number_sequence)
