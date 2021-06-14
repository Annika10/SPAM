import numpy as np
from matplotlib import pyplot as plt
from wordcloud import WordCloud


def bitmap_representation(dataset, list_of_words, min_sup=2):
    """
    create a bitmap representation (as numpy array) from dataset
    :param dataset: dataset in format cid, tid, elements
    :param list_of_words: list of possible words which can occur
    :param min_sup: minimum support
    :return: bitmap representation of data set, dictionary with support of each frequent sequence
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
            current_number_sequences = 1
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
    dict_support = dict()
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
        current_support = check_support(bitmap)
        if current_support >= min_sup:
            # (element, "has bitmap:", bitmap)
            dict_bitmap["[" + element + ']'] = bitmap
            dict_support["[" + element + ']'] = current_support
    return dict_bitmap, dict_support


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
    """
    returns support of an element in the bitmap
    :param array: bitmap representation of an element
    :return: support of element
    """
    support = 0
    for sub_array in array:
        array_ones = np.where(sub_array == 1)
        # sequence occurs at least one time for current customer
        if np.size(array_ones):
            support += 1
    return support


def get_frequent_sequences(dict_bitmap):
    """
    returns frequent sequences from bitmap
    :param dict_bitmap: bitmap dictionary
    :return: keys of bitmap dictionary, which are the frequent word patterns
    """
    return list(dict_bitmap.keys())


def plot_frequent_sequence(dict_support):
    """
    plot a barplot of frequent sequences
    :param dict_support: dictionary with frequent sequences and their support
    """

    if len(dict_support) <= 30:
        # Create horizontal bars
        plt.barh(range(len(dict_support)), list(dict_support.values()))

        # Create names on the x-axis
        plt.yticks(range(len(dict_support)), list(dict_support.keys()))

        # Add title and axis names
        plt.title('frequent word sequences')
        plt.xlabel('support')
        plt.ylabel('word sequences')

        plt.show()
    else:
        print("no pretty bar plotting possible with such a high amount of values", len(dict_support))


def create_wordcloud(dict_support):
    """
    plots wordcloud of frequent sequences
    :param dict_support: dictionary with frequent sequences and their support
    """
    wordcloud = WordCloud(background_color="white", width=1920, height=1080).generate_from_frequencies(dict_support)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def spam_algorithm(dict_bitmap, dict_support, min_sup=2):
    """
    run spam algorith
    :param dict_bitmap: bitmap representation
    :param dict_support: dict stores support of all frequent sequences
    :param min_sup: minimum support
    :return: bitmap representation, dict with support
    """
    list_l = dict_bitmap.keys()
    global dict_bitmap_global
    dict_bitmap_global = dict_bitmap.copy()
    for node_n in list_l:
        s_n = list_l
        i_n = [x for x in list_l if x > node_n]
        dict_support = dfs_pruning(node_n, s_n, i_n, dict_support, min_sup)
    return dict_bitmap_global, dict_support


def dfs_pruning(node_n, s_n, i_n, dict_support, min_sup):
    """
    depth first search
    :param node_n: current sequence
    :param s_n: possible sequence extensions
    :param i_n: possible item extensions
    :param dict_support: dict which stores support of all frequent sequences
    :param min_sup: minimum support
    :return: dict which stores support of all frequent sequences
    """
    s_temp, i_temp = list(), list()

    # s-step
    for i in s_n:
        new_sequence_array = s_step_two_elements(dict_bitmap_global[node_n], dict_bitmap_global[i])
        if check_support(new_sequence_array) >= min_sup:
            s_temp.append(i)
            dict_bitmap_global[node_n + i] = new_sequence_array
            dict_support[node_n + i] = check_support(new_sequence_array)
    for i in s_temp:
        new_i_temp = [x for x in s_temp if x > i]
        dfs_pruning(node_n + i, s_temp, new_i_temp, dict_support, min_sup)

    # i-step
    for i in i_n:
        str_index = node_n[:-1] + ',' + i[1:]
        new_item_array = i_step_two_elements(dict_bitmap_global[node_n], dict_bitmap_global[i])
        if check_support(new_item_array) >= min_sup:
            i_temp.append(i)
            dict_bitmap_global[str_index] = new_item_array
            dict_support[str_index] = check_support(new_item_array)
    for i in i_temp:
        new_i_temp = [x for x in i_temp if x > i]
        dfs_pruning(node_n[:-1] + ',' + i[1:], s_temp, new_i_temp, dict_support, min_sup)

    return dict_support


def dataset_transformation(dataset_Cid_Tid):
    """
    transform a dataset into a sequence dataset (needed for ISPAM)
    :param dataset_Cid_Tid: input dataset
    :return: transformed dataset
    """
    dataset = dict()
    current_customer = 1
    dataset[current_customer] = list()
    for line in dataset_Cid_Tid:
        if line[0] == current_customer:
            # append with current element
            # append with current element
            dataset.get(current_customer).append(line[2])
            dataset[current_customer] = dataset.get(current_customer)
        else:
            current_customer = line[0]
            dataset[current_customer] = [line[2]]
    return dataset