import numpy as np
from numpy import ndarray
from typing import Any


def init_bit_appering_and_first_position_sequences(dataset_sequences: dict[int, list[list[str]]], list_of_words: list[str]) \
        -> tuple[dict[Any, ndarray], dict[Any, ndarray], dict[Any, dict[Any, ndarray]]]:
    """

    :param dataset_sequences:
    :param list_of_words:
    :return:
    """
    appear_dict, fp_dict, bit_dict = initialise_zero_sequences(dataset_sequences, list_of_words)

    element_i = len(dataset_sequences) - 1
    for key, value in dataset_sequences.items():
        position_j = 1
        for sequence_j in value:
            for item_k in sequence_j:
                if appear_dict[item_k][element_i] == 0:
                    appear_dict[item_k][element_i] = 1

                bit_dict[key][item_k][-position_j] = 1

                if fp_dict[item_k][element_i] == 0:
                    fp_dict[item_k][element_i] = position_j
            position_j += 1
        element_i -= 1

    return appear_dict, fp_dict, bit_dict


def initialise_zero_sequences(dataset_sequences: dict[int, list[list[str]]], list_of_words: list[str]) \
    -> tuple[dict[Any, ndarray], dict[Any, ndarray], dict[Any, dict[Any, ndarray]]]:
    """

    :param dataset_sequences:
    :param list_of_words:
    :return:
    """
    appear_dict = dict()
    fp_dict = dict()
    bit_dict = dict()
    for word in list_of_words:
        appear_dict[word] = np.zeros(len(dataset_sequences))
        fp_dict[word] = np.zeros(len(dataset_sequences))
    for key, value in dataset_sequences.items():
        dict_sid = dict()
        for sequence in value:
            for item in sequence:
                if item not in dict_sid.keys():
                    dict_sid[item] = np.zeros(len(value))
            bit_dict[key] = dict_sid

    return appear_dict, fp_dict, bit_dict


def I_SPAM_algorithm(appear_dict: dict[Any, ndarray], min_sup, dataset_sequences, bit_dict, fp_dict):

    list_l = list()
    appear_dict_copy = appear_dict.copy()
    for itemk, value_app in appear_dict.items():
        # remove from tables
        if one_count(value_app) < min_sup:
            for i in range(1, len(dataset_sequences)):
                if value_app[-i] == 1:
                    bit_dict[i].pop(itemk)
            appear_dict_copy.pop(itemk)
            fp_dict.pop(itemk)
        else:
            list_l.append(itemk)
    appear_dict = appear_dict_copy.copy()

    for item_t in list_l:
        s_temp_t = list_l
        i_temp_t = [x for x in list_l if x > item_t]
        print(s_temp_t)
        print(i_temp_t)
        # Call M_DFS(T, AppearT, FPT, S-temp<T>, I-temp<T>)
        m_dfs(item_t, appear_dict, fp_dict, s_temp_t, i_temp_t, min_sup, bit_dict)


def m_dfs(item_t, appear_dict, fp_dict, s_temp_t, i_temp_t, min_sup, bit_dict):
    print("item_t here", item_t)
    for s_extension_element in s_temp_t:
        # convert to int for bitwise and
        print("s_extension_element", s_extension_element)
        appear_t = appear_dict[item_t].astype(int)
        appear_s_extension_element = appear_dict[s_extension_element].astype(int)
        approximate_appear_t_s = appear_t & appear_s_extension_element
        print("approximate_appear_t_s", approximate_appear_t_s)

        appear_t_s = np.zeros((len(approximate_appear_t_s)))
        fp_t_s = np.zeros((len(approximate_appear_t_s)))

        if one_count(approximate_appear_t_s) >= min_sup:
            for bit_k in range(len(approximate_appear_t_s)):
                print("bit_k", bit_k)
                print("index von hinten", -(bit_k+1))
                if approximate_appear_t_s[-(bit_k+1)] != 0:
                    fp_item_t = int(fp_dict[item_t][-(bit_k+1)])
                    fp_s = int(fp_dict[s_extension_element][-(bit_k+1)])
                    print("fp_item_t", fp_item_t)
                    print("fp_s", fp_s)
                    if fp_item_t >= fp_s:
                        print("bit_dict", bit_dict[bit_k+1])
                        print("bit_k for dict", bit_k+1)
                        print("s_extension_element", s_extension_element)
                        bit_s_extension_element = bit_dict[bit_k+1][s_extension_element]
                        print("bit_s_extension_element", bit_s_extension_element)

                        for shifting_number in range(fp_item_t):
                            print("shifting_number", shifting_number+1)
                            bit_s_extension_element = np.roll(bit_s_extension_element, 1)
                            bit_s_extension_element[0] = 0
                        print("bit_s_extension_element after shifting", bit_s_extension_element)

                        if one_count(bit_s_extension_element) > 0:
                            list_of_ones = np.where(bit_s_extension_element == 1)
                            print("list_of_ones", list_of_ones)
                            h = len(bit_s_extension_element) - np.max(list_of_ones)
                            appear_t_s[-(bit_k+1)] = 1
                            fp_t_s[-(bit_k+1)] = fp_item_t + h
                        print("current appear_t_s", appear_t_s)
                        print("current fp_t_s", fp_t_s)

                    else:
                        appear_t_s[-(bit_k + 1)] = 1
                        fp_t_s[-(bit_k + 1)] = fp_s
                        print("current appear_t_s", appear_t_s)
                        print("current fp_t_s", fp_t_s)
                else:
                    print("or here")
                    appear_t_s[-(bit_k + 1)] = 0
                    fp_t_s[-(bit_k + 1)] = 0
                    print("current appear_t_s", appear_t_s)
                    print("current fp_t_s", fp_t_s)
            print("appear_t_s", appear_t_s)
            if one_count(appear_t_s) >= min_sup:
                print("never goes here")
                appear_dict[item_t + s_extension_element] = appear_t_s
                fp_dict[item_t + s_extension_element] = fp_t_s
                m_dfs(item_t + s_extension_element, appear_dict, fp_dict, s_temp_t, i_temp_t, min_sup, bit_dict)

        print("appear_dict", appear_dict)
        print("fp_dict", fp_dict)


def one_count(array):
    array_ones = np.where(array == 1)
    return np.size(array_ones)


def s_step():
    pass