import numpy as np


def bitmap_representation(dataset, list_of_words):
    # get highest number of customers sequences
    highest_number_sequences = 0
    customer = dataset[0][0]
    current_number_sequences = 0
    countercustomer = 1
    for item in dataset:
        if item[0] == customer:
            current_number_sequences += 1
            if current_number_sequences > highest_number_sequences:
                highest_number_sequences = current_number_sequences
        else:
            customer = item[0]
            current_number_sequences = 0
            countercustomer += 1

    # get next 2 power for bitmap representation
    # 2^100 should be enough bits
    bits = 1
    for number in range(100):
        if highest_number_sequences <= 2**number and highest_number_sequences > 2**(number-1):
            bits = 2**number
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
                bitmap[current_customer-1][current_transaction] = 1
        print(element, "has bitmap:", bitmap)
        dict_bitmap["{" + element + '}'] = bitmap
    return dict_bitmap


def s_step_two_elements(first_array, second_array):
    # some special kind of inversion of first_array
    # search for first 1 in bitmap
    shape_of_first_array = np.shape(first_array)
    transformed_first_array = np.zeros(shape_of_first_array)
    for index_subarray in range(len(first_array)):
        sub_array = first_array[index_subarray]
        index_array = np.where(sub_array == 1)
        k = index_array[0][0]
        for index in range(k+1, len(sub_array)):
            transformed_first_array[index_subarray][index] = 1
    # TODO: fix like in paper, but why like this in paper?!
    print("inversed_first_array", transformed_first_array)

    # bitwise and
    # convert to int for bitwise and
    transformed_first_array = transformed_first_array.astype(int)
    second_array = second_array.astype(int)
    new_sequence_array = transformed_first_array & second_array
    print(new_sequence_array)
    return new_sequence_array


def s_step(dict_bitmap):
    pass


if __name__ == "__main__":

    minSup = 2

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

    first_array = dict_bitmap['{a}']
    second_array = dict_bitmap['{b}']
    new_sequence_array = s_step_two_elements(first_array, second_array)
