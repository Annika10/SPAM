import numpy as np


def bitmap_representation(dataset, list_of_words, min_sup=2):
    """
    create a bitmap representation (as numpy array) from dataset
    :param dataset: dataset in format cid, tid, elements
    :param list_of_words: list of possible words which can occur
    :return: bitmap representation of data set
    """

    ### bitmap representation is always 2^x
    # need to find out which is the highest number of transactions for a customer
    # next 2^x is format for bitmap representation

    # start with 0 transactions for customers
    highest_number_sequences = 0
    # first customer
    customer = dataset[0][0]
    # counter for transactions for each customer
    current_number_sequences = 0
    # determine number of customers for number of parts/subarrays in bitmap representation
    countercustomer = 1

    for item in dataset:
        # if it is the same customer as before
        if item[0] == customer:
            # add new transaction
            current_number_sequences += 1
            # update highest number of transactions if current number of transactions is higher
            if current_number_sequences > highest_number_sequences:
                highest_number_sequences = current_number_sequences
        # new customer
        else:
            customer = item[0]
            # set number of transactions for new customer to zero
            current_number_sequences = 0
            countercustomer += 1

    # get next 2 power of highest number of transactions for bitmap representation
    # 2^100 should be enough bits
    bits = 1
    for number in range(100):
        if highest_number_sequences <= 2 ** number and highest_number_sequences > 2 ** (number - 1):
            bits = 2 ** number
            break

    current_customer = 1
    current_transaction = -1
    dict_bitmap = dict()
    for element in list_of_words:
        bitmap = np.zeros((countercustomer, bits))
        for item in dataset:
            if item[0] == current_customer:
                current_transaction += 1
            else:
                current_customer = item[0]
                current_transaction = 0
            if element in item[2]:
                bitmap[current_customer - 1][current_transaction] = 1

        # only include frequent sequences
        if check_support(bitmap) > min_sup:
            print(element, "has bitmap:", bitmap)
            dict_bitmap["[" + element + ']'] = bitmap
    return dict_bitmap


def s_step_two_elements(first_array, second_array):
    """
    makes a s-step extension where the first array is extended by the second array
    :return: array of the whole sequence
    """
    # first transform first array like described in paper
    # create a transformed array of same shape as original first array
    shape_of_first_array = np.shape(first_array)
    transformed_first_array = np.zeros(shape_of_first_array)

    ### search for value k

    # k is index of first 1 in each part(subarray) of array
    for index_subarray in range(len(first_array)):
        sub_array = first_array[index_subarray]
        # indexes where array is 1
        index_array = np.where(sub_array == 1)
        # get first index, if one exist
        if not np.size(index_array):
            # if no first index --> all 0
            k = len(sub_array)
        else:
            k = index_array[0][0]
        # create transformed array
        # all indexes higher k have value 1
        for index in range(k + 1, len(sub_array)):
            transformed_first_array[index_subarray][index] = 1
    # TODO: fix like in paper, but why like this in paper?!
    # print("inversed_first_array", transformed_first_array)

    ### bitwise and of first and second array

    # convert arrays to int for bitwise and
    transformed_first_array = transformed_first_array.astype(int)
    second_array = second_array.astype(int)

    # bitwise and
    new_sequence_array = transformed_first_array & second_array

    return new_sequence_array


def i_step_two_elements(first_array, second_array):
    """
    makes a i-step extension of the first array with the second array
    :return: array of whole sequence
    """

    # convert to int for bitwise and
    first_array = first_array.astype(int)
    second_array = second_array.astype(int)

    # bitwise and
    new_item_array = first_array & second_array

    return new_item_array


def check_support(array):
    support = 0
    for sub_array in array:
        array_ones = np.where(sub_array == 1)
        # sequence occurs at least one time for current customer
        if np.size(array_ones):
            support += 1
    return support


def get_frequent_sequences(dict_bitmap):
    return list(dict_bitmap.keys())


def create_tree(dict_bitmap, ordered_list_of_words, min_sup=2, limit=3):
    """
    creates the tree with frequent sequences as a dictionariy
    :param dict_bitmap: a dictionary where the key are the lexicographic representation (e.g. [a]) and the values is the bitmap representation
    :param ordered_list_of_words: list of possible words
    :param limit: number of possible sequences in tree
    :param min_sup: number of minimum support
    :return: extended dictionary with bitmap representation
    """
    # dummy bitmap for checking if more extensions are possible
    old_dict_bitmap = dict()

    # mark which indexes are already passed by
    already_passed_indexes = 0

    # while not all nodes are extended
    while not old_dict_bitmap.keys() == dict_bitmap.keys():

        # current keys of bitmap
        keys = list(dict_bitmap.keys())
        print("keys", keys)

        # create new dictionary where new added extensions are stored
        new_dict_bitmap = dict_bitmap.copy()

        # pruning is done by only consider frequent sequences as first element
        for current_index in range(already_passed_indexes, len(keys)):

            # get bitmap/array of current considered element in the dictionary
            first_dict_index = keys[current_index]
            print("current_index", first_dict_index)
            first_array = dict_bitmap[first_dict_index]

            # check all extensions with right side of tree
            for word in ordered_list_of_words:

                # second considered element
                current_word = '[' + word + ']'

                # break for more than 3 sequences
                if (first_dict_index.count('[') + word.count('[')) > limit:
                    break

                ### s-step extension
                # name of new sequence
                new_s_step_extended_sequence = first_dict_index + current_word
                # count number of sequences
                number_sequence = new_s_step_extended_sequence.count('[')
                # if new extension doesn't exists until know and there aren't too many sequence, do extension
                if not new_s_step_extended_sequence in keys and number_sequence <= limit:
                    print("new s-step extension", new_s_step_extended_sequence)
                    # get bitmap/array of second element (extension)
                    second_array = dict_bitmap[current_word]
                    # perform s-step extension
                    new_sequence_array = s_step_two_elements(first_array, second_array)
                    if check_support(new_sequence_array) >= min_sup:
                        # add to dictionary
                        new_dict_bitmap[new_s_step_extended_sequence] = new_sequence_array


                ### i-step extension
                list_of_current_index = first_dict_index.split("[")
                get_last_sequence = list_of_current_index[-1][:-1]
                # TODO: change compare operation for real words
                if word not in get_last_sequence and word > get_last_sequence[-1]:
                    leading_part = ''
                    for i in range(len(list_of_current_index) - 1):
                        if list_of_current_index[i]:
                            leading_part = leading_part + '[' + list_of_current_index[i]

                    # name of new sequence
                    new_i_step_extended_sequence = leading_part + '[' + get_last_sequence + ',' + word + ']'
                    print("new i-step extension", new_i_step_extended_sequence)
                    # get bitmap/array of second element (extension)
                    second_array = dict_bitmap['[' + word + ']']
                    # perform i-step extension
                    new_item_array = i_step_two_elements(first_array, second_array)
                    if check_support(new_item_array) >= min_sup:
                        # add to dictionary
                        new_dict_bitmap[new_i_step_extended_sequence] = new_item_array

        # check if there are any new additions to the dictionary
        already_passed_indexes = len(dict_bitmap)
        old_dict_bitmap = dict_bitmap.copy()
        dict_bitmap = new_dict_bitmap.copy()

    print("tree", dict_bitmap)
    return dict_bitmap


if __name__ == "__main__":
    minSup = 2
    # TODO: to which number?
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

    dict_bitmap = bitmap_representation(dataset_Cid_Tid, ordered_list_of_words, minSup)
    print(dict_bitmap)

    dict_bitmap = create_tree(dict_bitmap, ordered_list_of_words, min_sup=minSup, limit=max_number_sequence)

    frequent_sequences = get_frequent_sequences(dict_bitmap)
    print(frequent_sequences)
