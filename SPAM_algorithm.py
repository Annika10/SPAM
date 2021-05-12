import numpy as np
from collections import Counter


def bitmap_representation(dataset, list_of_words):
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
        if not np.any(index_array):
            k = 0
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


def create_tree(dict_bitmap, limit=3):
    """

    :param dict_bitmap: a dictionary where the key are the lexicographic representation (e.g. [a]) and the values is the bitmap representation
    :param limit: number of possible sequences in tree
    :return: extended dictionary with bitmap representation
    """
    # dummy bitmap for checking if more extensions are possible
    old_dict_bitmap = dict()

    while old_dict_bitmap != dict_bitmap:

        # current keys of bitmap
        keys = list(dict_bitmap.keys())
        print("keys", keys)

        # create new dictionary where new added extensions are stored
        new_dict_bitmap = dict_bitmap.copy()

        for current_index in range(len(keys)):

            # get bitmap/array of current considered element in the dictionary
            first_dict_index = keys[current_index]
            first_array = dict_bitmap[first_dict_index]

            # check all extensions with right side of tree
            for index in range(current_index, len(dict_bitmap)):

                # second considered element
                current_dict_index = keys[index]

                ### s-step extension
                # name of new sequence
                new_index_sequence = first_dict_index + current_dict_index
                # count number of sequences
                number_sequence = new_index_sequence.count('[')
                # if new extension doesn't exists until know and there aren't too many sequence, do extension
                if not new_index_sequence in keys and number_sequence <= limit:
                    # get bitmap/array of second element (extension)
                    second_array = dict_bitmap[current_dict_index]
                    # perform s-step extension
                    new_sequence_array = s_step_two_elements(first_array, second_array)
                    # add to dictionary
                    new_dict_bitmap[new_index_sequence] = new_sequence_array

                ### i-step extension
                # name of new sequence
                new_index_item = first_dict_index[:-1] + ',' + current_dict_index[1:]

                # check if new item is already in sequence
                # split into sequences
                list_of_new_index_item = new_index_item.split("]")
                not_in_sequence = True
                # check for each sequence if there are multiple occurrences of one element
                for element in list_of_new_index_item:
                    element = element.replace("[", "")
                    # list of words/characters
                    sub_list_of_element = element.split(",")
                    if len(sub_list_of_element) > 1:
                        # count occurrence of words
                        counter = Counter(sub_list_of_element)
                        for i, j in counter.items():
                            # if word occurs more than one time in one sequence --> not possible
                            if j > 1:
                                not_in_sequence = False
                # when there are no duplicates of words in one sequence and the new whole sequence doesn't exist until now and the limit isn't reached --> do extension
                # if not_in_sequence and not new_index_item in keys and number_sequence <= limit:
                #     # get bitmap/array of second element (extension)
                #     second_array = dict_bitmap[current_dict_index]
                #     # perform i-step extension
                #     new_item_array = i_step_two_elements(first_array, second_array)
                #     # add to dictionary
                #     new_dict_bitmap[new_index_item] = new_item_array

        # check if there are any new additions to the dictionary
        old_dict_bitmap = dict_bitmap.copy()
        dict_bitmap = new_dict_bitmap.copy()

    print("tree", dict_bitmap)
    return dict_bitmap


if __name__ == "__main__":
    minSup = 2
    # TODO: to which number?
    max_size_sequence = 3

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

    dict_bitmap = bitmap_representation(dataset_Cid_Tid, ordered_list_of_words)
    print(dict_bitmap)

    dict_bitmap = create_tree(dict_bitmap, limit=3)
