from ISPAM_algorithm import init_bit_appering_and_first_position_sequences


if __name__ == "__main__":
    minSup = 2

    # example dataset from paper
    dataset_sequences = {
        1: [['a'], ['c', 'd'], ['a'], ['d']],
        2: [['a'], ['c'], ['a'], ['e']],
        3: [['c'], ['a'], ['d'], ['b', 'c', 'd']],
        4: [['b'], ['b'], ['c']],
        5: [['b', 'c', 'd'], ['d']]
    }

    list_of_words = ['a', 'b', 'c', 'd', 'e']

    init_bit_appering_and_first_position_sequences(dataset_sequences, list_of_words, minSup)

